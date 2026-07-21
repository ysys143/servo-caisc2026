from __future__ import annotations

from .servo2_io import Servo2Error, Table, require


EVENT_COMPONENTS = {
    "runtime_validation": {"V"},
    "artifact_assessment": {"V"},
    "human_feedback": {"external"},
    "external_assessment": {"external"},
    "artifact_production": {"W_A"},
    "execution": {"E"},
    "generation": {"G"},
    "state_update": {"M"},
}

EDGE_TRANSITIONS = {
    "observation": {("E", "V")},
    "epistemic_update": {("V", "M")},
    "artifact_revision": {("V", "W_A"), ("pi", "W_A")},
    "feedback_control": {
        ("V", "G"),
        ("V", "pi"),
        ("M", "G"),
        ("M", "pi"),
        ("pi", "G"),
        ("pi", "E"),
        ("G", "E"),
        ("W_A", "E"),
        ("external", "W_A"),
    },
    "external_only": {("external", "external")},
}


def validate_component_graph_conformance(tables: dict[str, Table]) -> None:
    endpoints = {
        require(row, "endpoint_id", "endpoints"): row
        for row in tables["endpoints"].rows
    }
    for event in tables["events"].rows:
        event_class = require(event, "event_class", "events")
        actor = endpoints[require(event, "actor_endpoint_id", "events")]
        if actor["component"] not in EVENT_COMPONENTS[event_class]:
            raise Servo2Error(
                "EVENT_COMPONENT_MISMATCH", require(event, "event_id", "events")
            )
    for edge in tables["edges"].rows:
        edge_id = require(edge, "edge_id", "edges")
        mediator_id = require(edge, "mediator_endpoint_id", "edges")
        if mediator_id not in endpoints:
            raise Servo2Error("EDGE_MEDIATOR_ENDPOINT_INVALID", edge_id)
        mediator = endpoints[mediator_id]
        if mediator["case_id"] != edge["case_id"]:
            raise Servo2Error("EDGE_MEDIATOR_CASE_MISMATCH", edge_id)
        human_mediation = edge["mediation_actor"] == "human"
        external_mediator = mediator["component"] == "external"
        if human_mediation != external_mediator:
            raise Servo2Error("EDGE_MEDIATION_ACTOR_INVALID", edge_id)
        source = endpoints[require(edge, "source_endpoint_id", "edges")]["component"]
        destination = endpoints[
            require(edge, "destination_endpoint_id", "edges")
        ]["component"]
        edge_type = require(edge, "edge_type", "edges")
        if (source, destination) not in EDGE_TRANSITIONS[edge_type]:
            raise Servo2Error(
                "EDGE_COMPONENT_TRANSITION_INVALID",
                edge_id,
            )
        if source == "external" and edge_type == "feedback_control":
            if edge["mediation_actor"] != "human":
                raise Servo2Error(
                    "EXTERNAL_FEEDBACK_ACTOR_INVALID",
                    edge_id,
                )
