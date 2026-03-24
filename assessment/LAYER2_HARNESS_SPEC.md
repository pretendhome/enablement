# Layer 2 Scoring Harness Specification

Date: 2026-03-24
Status: Design only, not implementation

## Purpose

This document specifies the automated Layer 2 scoring harness for the Palette Developer Enablement & Certification System.

The harness sits between:

- Layer 1 automated checks, which validate artifact presence and basic integrity
- Layer 3 human review, which handles calibration samples, low-confidence cases, and high-stakes escalation

Its job is to:

1. assemble a complete scoring prompt from module data, submission artifacts, and calibration exemplars
2. call an LLM API
3. parse the returned YAML evaluation
4. check certification thresholds
5. flag cases that must escalate to Layer 3

This spec assumes the current `scripts/demo_runner.py` already demonstrates prompt assembly flow and file loading patterns.

## Scope

In scope:

- prompt assembly contract
- scoring request and response format
- threshold evaluation
- escalation logic
- audit logging
- error handling
- cost estimation

Out of scope:

- UI
- reviewer workflow tooling
- model selection experimentation framework
- long-term storage implementation details

## Inputs and Outputs

### Inputs

- `module_path`
  Path to `module.yaml`
- `submission_dir`
  Directory containing the learner submission artifacts
- `submission_id`
  Stable identifier for the submission
- `evaluation_mode`
  `working` or `production`
- `model_config`
  Chosen Layer 2 model, temperature, max tokens, timeout

Optional inputs:

- `calibration_path`
  Path to calibration exemplars if available
- `prompt_override`
  Alternate evaluator prompt for testing or rollback

### Outputs

Primary output:

- YAML evaluation object matching the evaluator prompt schema

Derived outputs:

- threshold decision
- escalation flags
- normalized evaluation record for persistence
- operator-readable summary

## Functional Architecture

### 1. Loader

Responsibilities:

- read `module.yaml`
- discover and load required artifacts from `submission_dir`
- load evaluator system prompt from `assessment/evaluators/ai_rubric_evaluator_prompt.md`
- load calibration exemplars from `assessment/item-banks/<RIU-ID>/calibration_exemplars.md` when present

Failure behavior:

- if required module or artifacts are missing, return a harness error and stop
- if calibration exemplars are missing, continue with rubric-only scoring and set `calibration_available: false`

### 2. Prompt Builder

Responsibilities:

- assemble one deterministic scoring prompt from:
  - evaluator system prompt
  - module rubric dimensions
  - certification thresholds
  - submitted artifacts
  - calibration exemplars when available
- stamp metadata:
  - module id
  - submission id
  - timestamp
  - evaluation mode

Design rule:

- prompt assembly must be deterministic for a given set of inputs so scoring drift can be traced to model behavior, not prompt formatting drift

### 3. Model Client

Responsibilities:

- call the configured LLM provider
- pass timeout, retry, and response-format preferences
- capture raw request and response metadata

Preferred interface:

- model abstraction should isolate provider-specific API details from threshold and escalation logic

### 4. YAML Parser and Validator

Responsibilities:

- parse the returned YAML safely
- validate required sections:
  - `evaluation.module`
  - `evaluation.submission_id`
  - `evaluation.dimensions`
  - `evaluation.overall`
  - `evaluation.feedback`
- validate that all rubric dimensions from `module.yaml` are present in the response
- validate that levels are from the allowed set
- validate that confidence is present per dimension

Failure behavior:

- malformed YAML or incomplete structure triggers a retry with the same prompt
- if retries are exhausted, return `layer2_failed` and escalate to human review

### 5. Threshold Engine

Responsibilities:

- interpret threshold strings from `module.yaml`
- compute:
  - `certification_eligible`
  - `production_eligible`
- evaluate mandatory-dimension rules when present

Examples it must handle:

- `competent on 3/4 dimensions`
- `expert on 2/4, competent on remaining`
- `competent on all 4 dimensions, with mandatory competence in adversarial_robustness`

Implementation note:

- thresholds should be parsed into a normalized internal rule object rather than string-matched repeatedly.

### 6. Escalation Engine

Responsibilities:

- inspect model output and threshold result
- set Layer 3 escalation flags

Escalation triggers:

- any dimension has `low` confidence
- overall result is exactly at the WORKING boundary
- 2 or more dimensions are adjacent-level with medium confidence
- model parsing failed after retry
- hard-fail criterion triggered if present
- evaluation mode is `production`

Recommended additional trigger:

- large internal inconsistency between dimension evidence and assigned level

### 7. Recorder

Responsibilities:

- write normalized evaluation results to disk or storage
- persist:
  - raw prompt hash
  - model id
  - request timestamp
  - parsed YAML result
  - threshold result
  - escalation flags
  - retry count

This is necessary for appeals, audit, and calibration review.

## Proposed API Interface

### Python Entry Point

```python
def evaluate_submission(
    module_path: str,
    submission_dir: str,
    submission_id: str,
    evaluation_mode: str = "working",
    calibration_path: str | None = None,
    prompt_override: str | None = None,
    model_config: dict | None = None,
) -> dict:
    """Run Layer 2 scoring and return normalized evaluation result."""
```

### Return Shape

```yaml
status: "ok | parse_error | model_error | input_error"
submission_id: "SUB-XXXXX"
module: "RIU-XXX"
model: "provider/model-name"
calibration_available: true
prompt_hash: "sha256:..."
evaluation:
  dimensions:
    dimension_name:
      level: "competent"
      confidence: "high"
      evidence: "..."
      calibration_note: "..."
  overall:
    certification_eligible: true
    production_eligible: false
threshold_result:
  working_pass: true
  production_pass: false
  boundary_case: false
layer3_flags:
  escalate: false
  reasons: []
meta:
  retries: 0
  latency_ms: 4200
  estimated_cost_usd: 0.09
```

## Prompt Assembly Contract

The harness should assemble prompts in this order:

1. evaluator system prompt
2. evaluation request metadata
3. module rubric dimensions
4. certification thresholds
5. submitted artifacts
6. calibration exemplars

Why this order:

- rubric and thresholds define the scoring task
- artifacts provide the evidence
- exemplars calibrate boundaries after the task is already defined

Guardrails:

- truncate extremely large artifacts only with explicit section markers
- preserve file names so the model can cite evidence by artifact
- never merge artifact text so aggressively that provenance is lost

## Error Handling

### Input Errors

Examples:

- missing module file
- missing required artifacts
- unreadable calibration file

Handling:

- fail fast on missing module or required artifact
- continue without calibration file if absent

### Model Errors

Examples:

- timeout
- API failure
- rate limit

Handling:

- retry with bounded exponential backoff
- after max retries, mark as `model_error` and escalate to Layer 3

### Parse Errors

Examples:

- invalid YAML
- missing dimensions
- invalid levels

Handling:

- one retry with the same prompt plus a terse formatting correction instruction
- if still invalid, escalate to Layer 3

### Threshold Errors

Examples:

- threshold string cannot be parsed

Handling:

- fail closed and escalate
- log module id as a configuration defect

## Cost Estimate

This is a planning estimate, not a contract.

Assumptions for a typical portfolio submission:

- prompt size: 8k-20k input tokens depending on artifact volume
- response size: 800-2k output tokens
- 1 model call per submission in the common case
- 1 extra call for retry or calibration comparison in a minority of cases

Expected cost pattern:

- medium module with small artifacts:
  roughly low single-digit cents per submission on an efficient frontier model
- larger architecture-defense submission:
  can rise meaningfully if artifact payloads are long

Operational guidance:

- cache assembled prompt components where possible
- avoid resending unchanged calibration exemplar text if a future API supports cached context
- keep artifact inclusion targeted rather than dumping entire repos without filtering

## Integration With Current Demo Flow

`scripts/demo_runner.py` already proves the following pieces:

- module discovery
- journey and capstone discovery
- file loading
- evaluator prompt path conventions

The Layer 2 harness should reuse those same path conventions instead of inventing a parallel layout.

Recommended integration path:

1. extract reusable loading helpers from `demo_runner.py`
2. create a dedicated Layer 2 evaluator module under `assessment/evaluators/`
3. let the demo runner call the harness, not duplicate its logic

## Open Questions

1. Should Layer 2 use one model or a small cascade before human escalation?
2. Should confidence come from the model's self-report only, or also from multi-run consistency?
3. How much artifact truncation is acceptable before fairness or evidence quality degrades?
4. Should calibration exemplars be injected inline, or referenced by summary when they become large?

## Recommended Next Build Order

1. Implement threshold parsing as a standalone utility.
2. Implement prompt assembly and YAML validation.
3. Add a provider-agnostic model client.
4. Add escalation-flag evaluation.
5. Wire the demo runner to call the harness.
6. Add persistence and audit logging before any production-facing use.
