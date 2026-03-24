# Module Generation Rules

Date: 2026-03-24
Purpose: Prevent audit-identified coherence issues from propagating during scaffold and enrichment passes.

These rules apply to all generated or enriched `module.yaml` files.

## 1. Objective-to-Assessment Traceability

Every learning objective must map to at least one of:

- a named rubric dimension, or
- an explicit acceptance criterion embedded in a required artifact.

Generator rule:

- Do not write objectives that are only implied.
- If an objective introduces a distinct competency, create a rubric dimension for it unless it is already enforced through a specific artifact requirement.
- If the competency is assessed through an artifact instead of a dedicated dimension, the artifact text must make that acceptance criterion explicit.

Examples:

- If the objective teaches calibration or adjudication, there must be a calibration/adjudication rubric dimension or an artifact that explicitly captures calibration procedure and escalation rules.
- If the objective teaches change-control traceability, there must be a traceability artifact or a rubric dimension that names trace-back handling.

## 2. Threshold Policy by Risk Class

Thresholds are not generic. They must reflect risk, reversibility, and control sensitivity.

Use this policy:

- `low` or `medium` difficulty portfolio modules:
  `WORKING` may allow one weaker dimension if the weak dimension is not a core control.
- `high` difficulty modules:
  `WORKING` usually requires competence on most dimensions, typically `3/4`, `4/5`, or `5/6`.
- `critical` modules:
  `WORKING` must require competence on every core-control dimension.
- safety, governance, privacy, or one-way-door modules:
  name the mandatory dimensions explicitly in the threshold text.

Examples:

- acceptable: `competent on 5/6 dimensions`
- stronger for safety: `competent on all 4 dimensions, with mandatory competence in adversarial_robustness`

Do not allow a candidate to pass a safety-critical module while weak on the dimension that actually enforces safety.

## 3. Prerequisite Strength Rules for Critical Modules

The taxonomy `dependencies` field is the minimum baseline, not the full pedagogical truth.

Use this rule:

- `required` if the learner cannot realistically produce the artifacts or defend the assessment without prior mastery.
- `recommended` only if the dependency improves quality but is not necessary for successful completion.

Strengthening rules:

- If the module requires measurable evaluation, prior success-criteria or evaluation-harness skills should usually be `required`.
- If the module teaches agent orchestration, explicit contract design should usually be `required` at the journey level even if left flexible in the module file.
- If the module teaches safety or governance controls, prior evaluation or guardrail literacy should not be treated as optional when those controls must be tested.

## 4. Calibration and Evidence Dimensions Are Mandatory in Evaluation/Safety Modules

Any module centered on testing, evaluation, adjudication, guardrails, or AI-assisted review must include an explicit rubric dimension for the quality of evidence, calibration, adjudication, or review design.

Required patterns:

- testing/evaluation modules:
  include a dimension such as `calibration_and_adjudication`, `evaluation_design`, or equivalent
- guardrail/safety modules:
  include evidence requirements in a policy rubric dimension, not only in artifact text
- human-review or governance modules:
  score the review-gate design explicitly

Do not hide these competencies inside generic implementation or completeness dimensions.

## 5. Clustered Failure Modes Require an Adaptation Dimension

If a module includes a `clustered` failure mode involving multiple actors, populations, environments, or maturity levels, at least one rubric dimension must score adaptation across that diversity.

This dimension may cover:

- rollout adaptivity,
- multi-population policy variation,
- environment-specific controls,
- multi-team governance,
- cross-system coordination.

Do not rely on exercises alone to test clustered complexity. The rubric must reward successful adaptation explicitly.

## 6. Pre-Submission Checklist for Generators

Before finalizing a module:

- verify every objective is measured
- verify all three failure modes are exercised when the RIU defines them
- verify the threshold matches module risk
- verify prerequisites are strong enough for the artifacts
- verify evaluation/safety modules score evidence or calibration explicitly
- verify clustered scenarios have an adaptation rubric dimension when needed

If any of the above fail, the module is not ready for enrichment or scale-out.
