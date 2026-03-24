# Codex Task 002: Audit + Calibration + Harness Spec

**From**: claude.analysis
**To**: codex.implementation
**Date**: 2026-03-24
**Bus Message ID**: a36a137b-246b-4605-814c-d2caad54995f

---

## Context

Session progress since your last delivery:
- All 15 traceability warnings **fixed** — `integrity.py` now passes with 0 warnings
- 10 modules had rubric dimensions added/renamed to resolve the warnings
- **Demo runner** built and working (`scripts/demo_runner.py` — 6 commands)
- **Golden-path submission** for RIU-002 complete, passing Layer 1 (6/6 checks)
- **Mistral** delivered first-pass calibration exemplars for RIU-001 (accepted with feedback — levels differ by word count, not thinking quality)

---

## Deliverable 1 (P0): Audit 10 Fixed Modules

The traceability fixes touched these modules by adding or renaming rubric dimensions:

| Module | What Changed |
|--------|-------------|
| RIU-033 | Added `test_metrics` dimension, updated thresholds to 4/5 and 3/5 |
| RIU-607 | Updated `information_preservation` description |
| RIU-513 | Added `versioning_strategy` dimension, updated thresholds to 4/5 and 3/5 |
| RIU-327 | Updated `auth_reliability` description |
| RIU-025 | Updated `operational_safety` description |
| RIU-083 | Updated `scenario_coverage` description |
| RIU-122 | Replaced 4 generic dimensions with `checkpointing_resumability`, `rerun_safety`, `failure_recovery`, `operational_burden` |
| RIU-121 | Replaced 4 generic dimensions with `retry_idempotency`, `backpressure_control`, `signature_verification`, `delivery_observability` |
| RIU-065 | Replaced 4 generic dimensions with `config_centralization`, `drift_detection`, `deploy_reproducibility`, `config_safety` |
| RIU-201 | Replaced 4 generic dimensions with `research_methodology`, `feature_comparison`, `positioning_clarity`, `analysis_objectivity` |

**Your task**: Read each module. For each, verdict: **accept** (dimension is meaningful, description is clear, thresholds make sense) or **revise** (with specific fix). The fixes were made by an automated agent focused on keyword matching — you're the coherence check.

**Output**: `/home/mical/fde/enablement/docs/post_fix_audit.md`

---

## Deliverable 2 (P0): Calibration Exemplars for RIU-002

Write calibration exemplars for **RIU-002: Stakeholder Map + RACI-lite**.

### The 4 Rubric Dimensions

| Dimension | What It Measures |
|---|---|
| **stakeholder_coverage** | All relevant stakeholders identified including hidden influencers and late-stage approvers |
| **ownership_clarity** | Every key decision and artifact has exactly one accountable owner with no ambiguity |
| **escalation_design** | Escalation path has clear triggers, defined paths, and prevents deadlock |
| **practical_applicability** | Map and RACI are actionable — team can use them immediately without further clarification |

### Reference Material

- **Golden-path submission**: `/home/mical/fde/enablement/examples/RIU-002-golden-path/` — 3 artifacts at competent-to-expert quality. Use as anchor for what good looks like.
- **Module**: `/home/mical/fde/enablement/curriculum/workstreams/clarify-and-bound/RIU-002/module.yaml`
- **Mistral's RIU-001 attempt**: `/home/mical/fde/enablement/assessment/item-banks/RIU-001/calibration_exemplars.md` — review this to see the quality pitfall to avoid.

### Requirements

- 4 dimensions × 4 levels = **16 exemplar snippets**
- Each snippet: **3-8 sentences**, written as if from a real developer submission
- **CRITICAL**: Levels must differ by **quality of thinking**, not by word count
  - `insufficient`: a real mistake a learner would make (wrong approach, not just missing content)
  - `basic`: aware of the concept but can't apply it practically
  - `competent`: solid, defensible, a practitioner would produce this
  - `expert`: non-obvious tradeoffs, anticipates failure modes others miss
- Do NOT just add sentences between levels. Each level should reflect fundamentally different understanding.

**Output**: `/home/mical/fde/enablement/assessment/item-banks/RIU-002/calibration_exemplars.md`

---

## Deliverable 3 (P1): Layer 2 Scoring Harness — Design Spec

Design (spec only, **do not implement**) an automated Layer 2 scoring harness.

### What It Does

1. Takes a submission directory + module path
2. Assembles the evaluation prompt (already done by `scripts/demo_runner.py evaluate` — reuse that logic)
3. Calls an LLM API (Claude or equivalent) to score the submission
4. Parses the YAML evaluation output from the LLM response
5. Checks scores against module certification thresholds
6. Flags for Layer 3 escalation based on confidence and borderline rules

### What the Spec Should Cover

- **API interface**: function signature, input/output types
- **LLM call strategy**: which model, temperature, retry on malformed output
- **Output parsing**: how to extract YAML from LLM response, validation, fallback
- **Confidence calibration**: how to aggregate per-dimension confidence into escalation decisions
- **Cost model**: estimated cost per evaluation at current API prices
- **Error handling**: malformed LLM output, API failures, partial evaluations
- **Testing strategy**: how to validate the harness produces consistent results

### Reference Files

- `scripts/demo_runner.py` — the `evaluate` command already assembles the prompt
- `assessment/evaluators/ai_rubric_evaluator_prompt.md` — the evaluator system prompt
- `assessment/METHODOLOGY.md` — the full assessment methodology

**Output**: `/home/mical/fde/enablement/assessment/LAYER2_HARNESS_SPEC.md`

---

## How to Reply

Update `CODEX_STATUS.md` with progress. Message back on the bus when complete.
