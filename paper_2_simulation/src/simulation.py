"""
Novelty-as-Community-Arbitration: MiroFish ABM Simulation
CAISc 2026 — Paper 2

Experiment: Do isolated agents with local semantic memory reliably
identify globally novel hypotheses? How does knowledge-sharing
topology affect community novelty consensus?

Search space S: latent concept graph (networkx)
Agents: ReviewerAgent (local M_s, semantic classifier, trust weights)
Ground truth: global novelty = latent class never published before
"""

import random
import numpy as np
import networkx as nx
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Hypothesis Space
# ---------------------------------------------------------------------------

def build_hypothesis_space(
    n_hypotheses: int = 200,
    n_latent_classes: int = 40,
    surface_noise: float = 0.2,
    seed: int = 42,
) -> tuple[nx.Graph, dict]:
    """
    Returns:
        graph: nodes = hypotheses, edges = conceptual similarity
        ground_truth: {hyp_id: {'latent_class': int, 'true_novel': bool}}
    """
    rng = random.Random(seed)
    np.random.seed(seed)

    G = nx.barabasi_albert_graph(n_hypotheses, m=3, seed=seed)

    latent_classes = {i: rng.randint(0, n_latent_classes - 1) for i in range(n_hypotheses)}
    published_classes: set[int] = set()
    ground_truth = {}

    for hyp_id in range(n_hypotheses):
        lc = latent_classes[hyp_id]
        is_novel = lc not in published_classes
        ground_truth[hyp_id] = {
            "latent_class": lc,
            "true_novel": is_novel,
            "surface_features": _surface_features(lc, n_latent_classes, surface_noise, rng),
        }
        published_classes.add(lc)

    return G, ground_truth


def _surface_features(latent_class: int, n_classes: int, noise: float, rng: random.Random) -> np.ndarray:
    vec = np.zeros(n_classes)
    vec[latent_class] = 1.0
    noise_vec = np.array([rng.gauss(0, noise) for _ in range(n_classes)])
    return np.clip(vec + noise_vec, 0, 1)


# ---------------------------------------------------------------------------
# Agents
# ---------------------------------------------------------------------------

@dataclass
class ReviewerAgent:
    agent_id: int
    local_memory: dict = field(default_factory=dict)   # {latent_class: count}
    classifier_accuracy: float = 0.8                   # semantic equiv. accuracy
    trust_neighbors: list[int] = field(default_factory=list)

    def estimate_novelty(self, hypothesis: dict, shared_memory: Optional[dict] = None) -> bool:
        """Returns True if agent believes hypothesis is novel."""
        memory = shared_memory if shared_memory is not None else self.local_memory
        lc = hypothesis["latent_class"]

        # Imperfect classifier: sometimes misidentifies latent class
        if random.random() > self.classifier_accuracy:
            lc = random.randint(0, len(hypothesis["surface_features"]) - 1)

        return lc not in memory

    def update_memory(self, latent_class: int) -> None:
        self.local_memory[latent_class] = self.local_memory.get(latent_class, 0) + 1


# ---------------------------------------------------------------------------
# Community Topologies
# ---------------------------------------------------------------------------

def build_reviewer_network(
    n_reviewers: int,
    topology: str = "small_world",
    classifier_accuracy: float = 0.8,
    seed: int = 42,
) -> tuple[list[ReviewerAgent], nx.Graph]:
    """
    topology: 'isolated' | 'lattice' | 'small_world' | 'shared' (fully connected)
    """
    agents = [
        ReviewerAgent(
            agent_id=i,
            classifier_accuracy=classifier_accuracy + random.gauss(0, 0.05),
        )
        for i in range(n_reviewers)
    ]

    if topology == "isolated":
        net = nx.empty_graph(n_reviewers)
    elif topology == "lattice":
        net = nx.cycle_graph(n_reviewers)
    elif topology == "small_world":
        net = nx.watts_strogatz_graph(n_reviewers, k=4, p=0.3, seed=seed)
    elif topology == "shared":
        net = nx.complete_graph(n_reviewers)
    else:
        raise ValueError(f"Unknown topology: {topology}")

    for agent in agents:
        agent.trust_neighbors = list(net.neighbors(agent.agent_id))

    return agents, net


# ---------------------------------------------------------------------------
# Simulation Runner
# ---------------------------------------------------------------------------

def run_simulation(
    topology: str = "small_world",
    n_reviewers: int = 20,
    n_hypotheses: int = 200,
    classifier_accuracy: float = 0.8,
    human_oracle: str = "none",   # 'none' | 'random' | 'high_impact'
    human_audit_rate: float = 0.1,
    seed: int = 42,
) -> dict:
    """
    Returns metrics dict: false_novelty_rate, true_novelty_recall,
    consensus_accuracy, mean_agreement.
    """
    random.seed(seed)
    np.random.seed(seed)

    _, ground_truth = build_hypothesis_space(seed=seed)
    agents, _ = build_reviewer_network(n_reviewers, topology, classifier_accuracy, seed)

    results = {
        "topology": topology,
        "classifier_accuracy": classifier_accuracy,
        "tp": 0, "fp": 0, "tn": 0, "fn": 0,
        "agreement_scores": [],
    }

    # Seed agents with sparse prior knowledge (each agent knows ~5% of hypotheses)
    for agent in agents:
        known = random.sample(list(ground_truth.keys()), k=max(1, n_hypotheses // 20))
        for hyp_id in known:
            lc = ground_truth[hyp_id]["latent_class"]
            agent.update_memory(lc)

    # Evaluate each hypothesis
    for hyp_id, hyp in ground_truth.items():
        votes = []
        for agent in agents:
            # Share memory based on topology:
            # isolated: no sharing; lattice/small_world: neighbors only; shared: all
            if topology == "isolated":
                shared_mem = None
            else:
                shared_mem = _merge_memories(agent, agents)
            vote = agent.estimate_novelty(hyp, shared_mem)
            votes.append(vote)

        # Human oracle override
        if human_oracle == "random" and random.random() < human_audit_rate:
            community_vote = hyp["true_novel"]
        elif human_oracle == "high_impact" and hyp["true_novel"] and random.random() < human_audit_rate:
            community_vote = True
        else:
            community_vote = sum(votes) > len(votes) / 2  # majority vote

        true_novel = hyp["true_novel"]
        if community_vote and true_novel:
            results["tp"] += 1
        elif community_vote and not true_novel:
            results["fp"] += 1
        elif not community_vote and not true_novel:
            results["tn"] += 1
        else:
            results["fn"] += 1

        # Inter-agent agreement
        results["agreement_scores"].append(
            max(sum(votes), len(votes) - sum(votes)) / len(votes)
        )

    # Compute summary metrics
    tp, fp, tn, fn = results["tp"], results["fp"], results["tn"], results["fn"]
    results["false_novelty_rate"] = fp / (fp + tn) if (fp + tn) > 0 else 0
    results["true_novelty_recall"] = tp / (tp + fn) if (tp + fn) > 0 else 0
    results["consensus_accuracy"] = (tp + tn) / (tp + fp + tn + fn)
    results["mean_agreement"] = np.mean(results["agreement_scores"])

    return results


def _merge_memories(agent: ReviewerAgent, all_agents: list[ReviewerAgent]) -> dict:
    merged: dict[int, int] = {}
    for neighbor_id in agent.trust_neighbors:
        for lc, cnt in all_agents[neighbor_id].local_memory.items():
            merged[lc] = merged.get(lc, 0) + cnt
    merged.update(agent.local_memory)
    return merged


# ---------------------------------------------------------------------------
# Parameter Sweep
# ---------------------------------------------------------------------------

def sweep(
    topologies: Optional[list[str]] = None,
    classifier_accuracies: Optional[list[float]] = None,
    n_seeds: int = 10,
) -> list[dict]:
    if topologies is None:
        topologies = ["isolated", "lattice", "small_world", "shared"]
    if classifier_accuracies is None:
        classifier_accuracies = [0.6, 0.75, 0.9]

    all_results = []
    for topology in topologies:
        for acc in classifier_accuracies:
            for seed in range(n_seeds):
                r = run_simulation(topology=topology, classifier_accuracy=acc, seed=seed)
                all_results.append(r)
                print(
                    f"[{topology:12s}] acc={acc:.2f} seed={seed} "
                    f"FNR={r['false_novelty_rate']:.3f} "
                    f"recall={r['true_novelty_recall']:.3f} "
                    f"agree={r['mean_agreement']:.3f}"
                )
    return all_results


if __name__ == "__main__":
    print("=== Single run (small_world, acc=0.8) ===")
    r = run_simulation(topology="small_world", classifier_accuracy=0.8)
    print(f"False Novelty Rate : {r['false_novelty_rate']:.3f}")
    print(f"True Novelty Recall: {r['true_novelty_recall']:.3f}")
    print(f"Consensus Accuracy : {r['consensus_accuracy']:.3f}")
    print(f"Mean Agreement     : {r['mean_agreement']:.3f}")
    print()
    print("=== Parameter sweep ===")
    sweep(n_seeds=3)
