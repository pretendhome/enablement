# Coherence Audit — Example Modules

Date: 2026-03-24
Scope: RIU-001, RIU-021, RIU-510, RIU-082, RIU-603

## Audit Standard

Each example module was checked for five forms of coherence:

1. Learning objectives map cleanly to rubric dimensions and required artifacts.
2. Exercises cover the RIU failure-mode shape: silent, loud, and clustered.
3. Assessment type matches the competency being demonstrated.
4. Prerequisites support the target difficulty without circularity or major hidden dependencies.
5. Certification thresholds are calibrated consistently with difficulty, evidence burden, and assessment type.

## Executive Read

The overall pattern is strong enough to scaffold from, but three template-level issues should be corrected before large-scale generation:

1. Several modules include objectives that are not directly measured as rubric dimensions.
2. Threshold calibration is inconsistent around high-risk service and governance work.
3. A few prerequisites are too light for the stated difficulty, which will create avoidable learner failure later in the graph.

## Cross-Module Findings

### Finding 1: Objective-to-rubric traceability is incomplete in 4 of 5 modules

What is wrong:
Multiple modules include objectives that are only indirectly measured. Examples:
- RIU-021 teaches calibration for LLM-as-judge, but no rubric dimension explicitly scores calibration design quality.
- RIU-082 teaches evidence requirements, but the rubric does not explicitly assess evidence-policy design.
- RIU-603 teaches phased rollout design, but rollout sequencing is only implied inside behavior-change and champions dimensions.
- RIU-001 requires tracing asks back to the brief, but no rubric dimension explicitly measures change-control or traceability mechanics.

Why it matters:
If objectives are not directly measured, generated modules will drift toward attractive prose instead of observable competency. That weakens both learner clarity and AI-assisted evaluation.

Specific fix:
Adopt a generation rule that every learning objective must map to either:
- a dedicated rubric dimension, or
- a named artifact acceptance criterion inside an existing dimension description.

For the current examples:
- RIU-021: add `calibration_design`
- RIU-082: rename `policy_completeness` to `policy_and_evidence_design`
- RIU-603: add `rollout_adaptivity` or expand `behavior_change_focus`
- RIU-001: expand `scope_discipline` to mention change-control traceability explicitly

### Finding 2: Thresholds are mostly coherent, but service-integration and safety modules are under-gated

What is wrong:
RIU-082 is `critical`, one-way-door adjacent work, and includes tool-use boundaries, but WORKING is only `competent on 3/4 dimensions`. A learner could miss either implementation quality or adversarial robustness and still pass.

Why it matters:
For safety-sensitive modules, partial competence is not enough. A guardrail design that is good on policy but weak in adversarial robustness creates false confidence and real deployment risk.

Specific fix:
Raise RIU-082 WORKING to `competent on all 4 dimensions` or `competent on 4/4 with no dimension below basic and mandatory competence in adversarial_robustness + implementation_quality`.

### Finding 3: Critical/high modules need stronger prerequisite signaling

What is wrong:
RIU-021, RIU-082, and RIU-603 all have recommended prerequisites that function like practical prerequisites for success.

Why it matters:
When Kiro scales this pattern, weak prerequisite signaling will produce modules that are formally traversable but pedagogically brittle.

Specific fix:
Use this rule:
- `required` when the learner cannot realistically produce the artifacts without prior mastery
- `recommended` only when the dependency improves quality but is not needed to complete the work

Immediate corrections:
- RIU-021: make RIU-001 required, not recommended
- RIU-082: make RIU-021 required for the testing/evaluation portion, or split testing into a separate dependency note if the module is intentionally dual-entry
- RIU-603: consider RIU-082 required when the adoption program includes broad employee AI access

## Module-by-Module Audit

### RIU-001 — Convergence Brief (Semantic Blueprint)

Assessment:
- Assessment type is appropriate. Portfolio evidence matches a scoping competency.
- Silent/loud/clustered exercises reflect the RIU failure modes well.
- Thresholds are reasonable for a high-difficulty foundation module.

Finding:
The objective `Detect and resolve scope creep by tracing asks back to the Convergence Brief` is only partially measured.

Why it matters:
The current rubric rewards explicit non-goals and boundary discipline, but not the operational behavior of using the brief as an active change-control instrument.

Specific fix:
Update `scope_discipline` to: `Non-goals are explicit, boundary conditions are clear, and new asks are explicitly traced back to the brief with accept/defer/escalate handling.`

Additional fix:
Add a required artifact or appendix section inside `convergence_brief.md` for `change_requests` or a traceability table.

### RIU-021 — Golden Set + Offline Evaluation Harness

Assessment:
- Assessment type is appropriate. Portfolio artifacts are the right evidence for evaluation-system design.
- Exercises cover failure modes strongly and are among the best examples in the set.

Finding:
Objective coverage is incomplete for calibration and disagreement handling.

Why it matters:
The exercises correctly surface ambiguity and LLM-as-judge calibration, but the rubric can still award high scores to a technically functional harness that lacks a credible adjudication protocol.

Specific fix:
Add rubric dimension `calibration_and_adjudication` with language such as:
`Handles ambiguous ground truth, uses calibration exemplars or agreement checks, and defines when human review is required.`

Additional fix:
Move RIU-001 from recommended to required. This module assumes stable success criteria before metric selection.

Threshold note:
`WORKING: competent on 3/4` is acceptable if the fifth calibration dimension is added and metric selection is treated as non-optional inside the pass rule.

### RIU-510 — Multi-Agent Workflow Design

Assessment:
- Assessment type is appropriate. Architecture defense is the correct mode for adversarial tradeoff reasoning.
- Exercises cover all three failure modes with the right system-level shape.
- Thresholds are coherent for a critical orchestration module.

Finding:
The prerequisites are directionally correct but slightly under-declared.

Why it matters:
The module assumes explicit interface contracts and safety boundaries. Listing RIU-022 and RIU-082 as recommended works for experienced learners, but not for a certification pathway where artifacts will be AI-evaluated against explicit contracts.

Specific fix:
If RIU-510 is part of a formal Agent Architect journey, treat RIU-022 as required in that journey even if the module file keeps it recommended. This preserves graph flexibility while preventing a brittle track.

Secondary fix:
Expand `handoff_protocol` rubric language to mention schema validation and versioning so it measures the contract discipline implied by the objective.

### RIU-082 — LLM Safety Guardrails (Content + Tool Use)

Assessment:
- Assessment type is appropriate because service evaluation is part of the competency, but the module also contains architecture and policy design work.
- Exercises are strong and cover the real failure shape well.

Finding:
Evidence requirements are taught but not explicitly assessed, and the threshold is too permissive for a critical safety module.

Why it matters:
This module is likely to be reused as a pattern for many guardrail/safety modules. If the template allows passing without strong evidence-policy design and adversarial robustness, downstream certification trust will degrade.

Specific fix:
Change `policy_completeness` to `policy_and_evidence_design` and mention evidence thresholds, refusal conditions, and user-tier differentiation.

Specific fix:
Raise WORKING threshold to require competence on all dimensions, with adversarial robustness mandatory.

Specific fix:
Add either:
- required prerequisite RIU-021, or
- explicit note that the instructor must provide a prebuilt test harness when RIU-021 is not completed.

### RIU-603 — Employee AI Adoption Program

Assessment:
- Assessment type is appropriate. Portfolio evidence is the right modality for change-program design.
- Failure-mode coverage is strong and realistic.

Finding:
The module teaches adaptive rollout and organizational sequencing, but the rubric does not directly score it.

Why it matters:
A learner could produce good personas and recipes but still design a rollout that fails in heterogeneous organizations, which is exactly the clustered failure mode this module is meant to address.

Specific fix:
Add rubric dimension `rollout_adaptivity`:
`Rollout sequencing, segmentation, and support model are adapted to persona and maturity differences rather than imposed uniformly.`

Additional fix:
Because the module includes union concerns and safe-use behavior change, add RIU-082 as a required prerequisite for governance-sensitive deployments or explicitly scope the module to internal low-risk adoption if that dependency is intentionally optional.

Threshold note:
`competent on 4/5` is reasonable today; if `rollout_adaptivity` is added, WORKING should become `competent on 5/6 with no gap in behavior_change_focus or rollout_adaptivity`.

## Recommended Template Corrections Before Mass Generation

1. Add an `objective_to_rubric_traceability` validation check in generation QA.
2. Add a threshold policy by risk class:
   - foundation/high portfolio modules can pass with one weak dimension
   - critical safety/service/governance modules cannot pass with a weak core-control dimension
3. Tighten prerequisite rules so critical modules do not rely on informal recommended dependencies.
4. Require every module with a testing, evaluation, or guardrail objective to include a rubric dimension for calibration/evidence/adjudication when relevant.
5. For clustered failure modes, require one rubric dimension that explicitly measures adaptation across multiple actors, environments, or populations.

## Priority Fix Order

1. Fix RIU-082 threshold + evidence-dimension gap.
2. Fix RIU-021 calibration/adjudication rubric coverage.
3. Fix RIU-603 rollout-adaptivity rubric gap.
4. Expand RIU-001 scope-traceability measurement.
5. Enforce journey-level prerequisite hardening for RIU-510 and similar critical modules.
