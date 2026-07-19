# OpenReview 카메라레디 메타데이터 (2026-07-19 기준)

> **주의.** `HANDOFF.md` §6의 메타데이터는 **2026-05-29 작성분으로 폐기**한다.
> 제목이 다르고(“A Unified Framework…”), TL;DR이 카메라레디에서 철회한 인과 주장을
> 그대로 담고 있다. 아래 내용이 현재 `submission/main.tex`와 일치하는 유일한 버전이다.

## Title

```
Formalizing AI Scientist Systems: A Component Framework and Theoretical Analysis
```

## Authors (탈익명화)

```
Jaesol Shin — WeDataLab
```

## TL;DR

```
A six-component formal vocabulary (S, G, E, V, M, pi) for AI Scientist systems, grounded in POMDP
and Bayesian experimental design, that separates three distinctions current systems conflate and
states three open problems with falsification criteria.
```

TL;DR 작성 원칙: 본문이 명시적으로 헷지한 주장(“$V$ completeness가 가장 중요한 설계 변수”,
“gating calibration이 trustworthy closure를 야기한다”)을 **단정형으로 되살리지 않는다**.
본문 §8은 이를 “a recurring bottleneck, not a causal priority”, 초록은 “should not be read as an
empirical finding”으로 규정한다.

## Abstract (본문 초록과 일치, plain text)

```
The field of AI Scientist systems -- agents that generate hypotheses, execute experiments, and
synthesize knowledge -- lacks a shared formal vocabulary. We propose Servo (S, G, E, V, M, pi), a
six-component taxonomy comprising the Search space, hypothesis Generator, Experiment executor,
Validator, Memory, and search Policy (pi), grounded in Partially Observable Markov Decision Process
(POMDP) and Bayesian Experimental Design (BED) theory. The framework's core contribution is three
diagnostic separations that current systems conflate: the observation likelihood from the validator
as a reward channel; calibrated gating (V_gating) from mere layer presence (V_present); and episodic
from semantic memory. We formalize these as three propositions under tractable, identifying
assumptions -- the loop closes independently of the validator; a miscoupled validator can drive
convergence to a misspecified target; and a novelty component absent from every automated channel is
non-identifiable (Propositions 1-3) -- which no surveyed system satisfies, so they clarify the formal
structure of the distinctions rather than certify their empirical prevalence. We apply it to six core
systems and seven domains and identify three open problems with falsification criteria: the lack of
validated automated novelty gates, the BED-practice gap for search policies, and the experiment
fidelity gap (no principled criterion for escalating from computational proxy to physical
validation). The cross-system survey is offered as provisional structured annotation; the organizing
hypothesis that gating calibration co-occurs with trustworthy closure is direction-consistent under
some outcome-recoding assumptions but not adjudicated, and should not be read as an empirical
finding.
```

## Keywords

```
AI scientist, automated scientific discovery, POMDP, Bayesian experimental design,
validator calibration, hypothesis generation, scientific automation, formal framework
```

`HANDOFF.md`의 “multi-agent systems”는 뺐다 — 본문 §8은 “All systems analyzed are single-agent
loops”라고 명시하며, 집단·다중 에이전트는 향후 과제로만 다룬다.

## 기타 폼 필드

| 필드 | 값 |
|------|-----|
| Track | Track 2: Open-Ended Problems |
| Archival | Archival |
| Checklist | 두 체크리스트 모두 `main.tex`에 포함 |

## 업로드 산출물

| 항목 | 경로 |
|------|------|
| 카메라레디 PDF | `submission/servo_caiscfp2026.pdf` (본문 8쪽) |
| 보충자료 ZIP | `submission/caisc2026-servo-supplement.zip` |
| 공개 저장소 | https://github.com/ysys143/servo-caisc2026 |

## 업로드 후 확인

1. OpenReview가 렌더링한 PDF에서 **본문이 8쪽에서 끝나는지**(Conclusion이 p8에서 완결) 확인.
2. 폼의 TL;DR·Abstract가 위 내용과 일치하는지 확인 — 특히 예전 TL;DR이 남아 있지 않은지.
