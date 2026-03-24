# Assessment Methodology

Date: 2026-03-24
Status: Phase 1 methodology for the Palette Developer Enablement & Certification System

## 1. Assessment Philosophy

Palette uses portfolio-based assessment because the target competencies are operational, architectural, and judgment-heavy. Multiple choice can test vocabulary recognition; it cannot credibly test whether a practitioner can:

- bound an ambiguous engagement,
- build an evaluation harness,
- defend a multi-agent architecture,
- implement safety controls with real tradeoffs, or
- operate an AI system under production constraints.

This design follows the strongest signals from professional certification research:

- CNCF CKA/CKAD is trusted because it is performance-based rather than recall-based.
- HashiCorp professional-style labs are trusted because the candidate must produce working artifacts, not select a plausible answer.

Our approach extends that logic from lab tasks to portfolio evidence. Every assessment requires artifacts that can be inspected, rerun, challenged, and defended. The question is not "does the learner know the term?" It is "can the learner produce the work a competent practitioner would be expected to produce?"

This is also the correct fit for the RIU model. Each RIU already defines:

- a problem pattern,
- concrete artifacts,
- success conditions,
- failure modes, and
- reversibility risk.

The assessment system therefore measures demonstrated capability against the RIU itself, not against a detached exam blueprint.

## 2. Tier Model

Palette uses three certification tiers:

- `UNVALIDATED`: learner has entered the system and completed placement or foundational orientation.
- `WORKING`: learner has demonstrated track-specific competence through module evidence and a capstone.
- `PRODUCTION`: learner has demonstrated expert-level judgment across multiple tracks, including architecture defense and human sign-off.

Assessment rigor rises with certification risk:

- `UNVALIDATED` can rely on lower-stakes diagnostics and placement exercises.
- `WORKING` requires artifact-based evidence for one certification journey.
- `PRODUCTION` requires stronger proof, including one-way-door decision defense, auditability, and mandatory human review.

## 3. Three-Layer Evaluation Pipeline

Palette uses a three-layer, LLM-first human-final pipeline. AI increases scale and consistency, but it does not make final high-stakes decisions without human oversight.

### Layer 1: Automated Checks

Purpose:
Reject incomplete, malformed, or obviously non-runnable submissions before rubric scoring.

Checks include:

- required artifacts present,
- schema validity,
- code runs or command entrypoints execute where applicable,
- sources or evidence are cited where required,
- basic uniqueness checks pass,
- submission metadata is complete.

What it catches:

- missing files,
- broken repos,
- empty or placeholder artifacts,
- schema violations,
- missing citations,
- obvious integrity failures.

Escalation rule:
Submissions that fail Layer 1 do not proceed to certification scoring. They are returned for remediation or routed to admin review if integrity is in question.

### Layer 2: AI Rubric Evaluation

Purpose:
Score each rubric dimension against explicit criteria and calibration exemplars.

Method:

- The evaluator scores dimensions independently using absolute rubric criteria.
- The preferred scale is small and discrete. Internally, rubrics should align to a 0-5 style boundary model, even if learner-facing levels are `insufficient`, `basic`, `competent`, `expert`.
- Each dimension includes explicit level definitions, hard-fail conditions where relevant, and exemplar comparisons when available.
- The evaluator must report both evidence and confidence for each dimension.

Bias controls:

- absolute scoring, not pairwise ranking, to reduce position bias,
- rubric language that rewards substance over verbosity,
- model-family separation where feasible to reduce self-preference bias,
- explicit uncertainty reporting rather than forced certainty.

What it catches well:

- rubric compliance,
- artifact completeness beyond syntactic checks,
- tradeoff quality,
- failure analysis quality,
- portfolio evidence consistency across artifacts.

What it does not do alone:

- make final high-stakes decisions without oversight,
- resolve ambiguous domain disagreements with no gold-set guidance,
- replace expert adjudication for borderline or one-way-door submissions.

### Layer 3: Human Calibration and Review

Purpose:
Provide legal, psychometric, and operational oversight for high-stakes outcomes.

Human review is triggered by two paths:

1. Fixed calibration sample:
   A standing sample of at least 10% of all submissions is double-scored by human reviewers to monitor ongoing AI-human agreement.

2. Confidence-based escalation:
   Any submission is escalated when the AI judge is uncertain, borderline, contradictory across dimensions, or handling a high-risk tier.

Mandatory escalation triggers:

- any dimension with low confidence,
- overall result at or near a certification boundary,
- disagreement across repeated scoring passes,
- hard-fail criteria triggered,
- one-way-door or safety-critical modules where a core control dimension is weak,
- all `PRODUCTION` submissions.

This follows the architecture update informed by "Trust or Escalate" style cascaded evaluation. The design goal is not maximum automation. The design goal is controlled trust with auditable override.

## 4. Scoring Model

Each module defines 3-5 rubric dimensions derived from RIU success conditions. Dimensions are scored independently, then checked against module thresholds.

Scoring principles:

- Every learning objective must map to a rubric dimension or explicit artifact acceptance rule.
- Every dimension must be evidence-based.
- Hard failures override average quality when safety or compliance is at risk.
- `Competent` is the expected WORKING target; `Expert` is reserved for unusually strong work.

Recommended dimension structure:

- dimension name,
- description,
- level criteria,
- optional hard-fail clause,
- optional exemplar references,
- confidence output.

Threshold structure:

- `WORKING`: demonstrates reliable practitioner competence on the required mix of dimensions.
- `PRODUCTION`: demonstrates expert performance on the designated subset, with competence on the remainder.

Threshold policy by risk class:

- foundation portfolio modules may allow one weaker dimension,
- critical safety, governance, or service-control modules should require competence on all core-control dimensions,
- one-way-door domains should use mandatory-dimension gating, not average-score compensation.

## 5. Item Bank Architecture

The item bank supports both module assessments and eventual adaptive assessment.

### 5.1 Anchor Items

Anchor items are human-calibrated exemplars. They define the standard.

Per module target:

- 3-5 anchor items in Phase 1,
- expanded over time as calibration data grows.

Each anchor item should include:

- prompt or task statement,
- expected artifact shape,
- scored rubric output,
- rationale for each dimension,
- notes on borderline distinctions,
- human reviewer agreement record.

Anchor items are used for:

- evaluator prompt calibration,
- rater training,
- drift detection,
- threshold refinement,
- appeals reference.

### 5.2 Generated Items

Generated items are produced from anchor patterns and RIU failure modes.

Per module target:

- 15-30 generated items,
- distributed across difficulty and failure-mode shape.

Generation rules:

- preserve the same competency construct as anchor items,
- vary context, domain, and artifact details,
- include silent, loud, and clustered failure cases where applicable,
- tag difficulty and intended rubric dimensions,
- route new items through validation before production use.

Generated items expand coverage, but they do not become authoritative merely by existing. They inherit trust only through performance against calibration data.

### 5.3 Retired Items

Retired items remain in the bank with rationale metadata.

Retirement reasons include:

- ambiguity,
- stale technology assumptions,
- overexposure,
- unfairness,
- weak discrimination,
- poor rater agreement.

Retired items should not be deleted silently. They are part of the audit trail.

## 6. Inter-Rater Reliability and Calibration

Target:

- Maintain >80% AI-human agreement at the dimension and outcome level, roughly comparable to acceptable human inter-rater agreement for operational certification contexts.

Calibration baseline:

- 30-50 expert-annotated examples per rubric dimension for production-quality evaluation.

Calibration process:

1. Define the rubric dimension and explicit boundary language.
2. Collect 30-50 expert-scored examples, including borderline cases.
3. Build or refresh anchor exemplars from those cases.
4. Compare AI scoring against expert judgments.
5. Identify systematic drift:
   - too lenient,
   - too strict,
   - bias toward verbosity,
   - weak handling of ambiguity,
   - false confidence at threshold boundaries.
6. Update exemplars, rubric wording, or escalation rules.
7. Re-test before deploying the evaluator update.

Operational monitoring:

- Sample at least 10% of scored submissions for human comparison.
- Review agreement quarterly at minimum, and immediately after model, rubric, or prompt changes.
- Track reliability by module, dimension, and track rather than only as a global average.

Response when agreement drops:

- Below target on one dimension:
  refresh exemplars and tighten dimension wording.
- Below target on a whole module:
  increase human review coverage and pause auto-pass on that module.
- Below target systemically:
  revert to previous evaluator configuration or raise escalation thresholds until recalibration completes.

## 7. Adaptive Difficulty

Adaptive logic will be introduced in phases.

### Phase 1

Use guided adaptivity rather than full computerized adaptive testing:

- placement tasks route learners into likely starting journeys,
- generated items can be selected by prior performance,
- remediation modules are recommended based on weak dimensions.

### Future Path to CAT

Full CAT is a later-stage capability and should not be claimed prematurely. It requires:

- 300-500 calibrated items per track,
- stable item characteristic estimates,
- enough candidate volume to maintain calibration quality,
- governance controls to avoid opaque or unfair routing decisions.

Adaptive rules should never hide standards. They should change which evidence is requested, not whether competence is required.

## 8. Integrity Measures

Because assessments are portfolio-based and AI-assisted, integrity controls must address both plagiarism and over-delegation.

### 8.1 Artifact Uniqueness and Submission Screening

Controls:

- similarity checks across prior submissions,
- metadata and provenance collection,
- evidence requirements tied to design rationale,
- rerunnable artifacts where feasible,
- spot checks on cited sources and implementation claims.

### 8.2 AI-Generated Submission Detection

Detection should be used as a flag, not as sole proof of misconduct. Style-based detectors are too unreliable to justify punitive action on their own.

Use detection as one signal among several:

- mismatch between architecture reasoning and produced artifacts,
- inability to defend decisions orally,
- copied structure across submissions,
- absent or inconsistent iteration history,
- suspiciously generic but technically shallow evidence.

### 8.3 Architecture Defense for Higher Tiers

For `PRODUCTION`, architecture defense is required because it tests real authorship and real judgment under challenge.

Candidates must be able to:

- explain tradeoffs,
- justify safety and reliability controls,
- respond to changed constraints,
- defend one-way-door decisions,
- describe what they would do when the submitted design fails in production.

### 8.4 Human Review on One-Way Doors

Any assessment involving irreversible actions, regulated controls, or safety-critical boundaries must include a human sign-off path. This is both a psychometric control and a regulatory requirement.

## 9. Compliance and Governance

Palette assumes the assessment system may be used in contexts that affect employment or professional standing. The methodology therefore adopts a conservative governance posture.

### EU AI Act Alignment

Educational assessment AI is treated as high-risk under the EU AI Act, with full enforcement beginning August 2, 2026.

Design response:

- AI is not the sole final decision-maker.
- Human reviewers can override automated outcomes.
- Candidates must be informed when AI is used in evaluation.
- Evaluation methodology, calibration, and performance metrics are documented.
- Annual bias audit is built into the operating model.

### Bias Monitoring

Track for:

- demographic performance disparities where legally appropriate,
- module-level false positive and false negative patterns,
- over-refusal or over-escalation on certain artifact styles,
- model-family bias where evaluator and candidate tooling overlap.

### Transparency and Appeals

Every scored submission should retain:

- rubric version,
- evaluator version,
- confidence indicators,
- escalation reason if reviewed,
- human override record if applicable.

Candidates should be able to request a human appeal for disputed outcomes.

## 10. Operating Procedure

### Before Launch

1. Define module rubrics with explicit thresholds and hard-fail clauses.
2. Build anchor sets for priority modules.
3. Validate evaluator prompts against expert gold sets.
4. Set escalation thresholds conservatively.
5. Document AI-use disclosure and appeal process.

### During Operation

1. Run Layer 1 checks.
2. Run AI rubric scoring.
3. Escalate based on confidence and risk triggers.
4. Human-review the fixed calibration sample plus escalated cases.
5. Record agreement, drift, overrides, and appeals.

### Quarterly

1. Refresh gold sets and exemplars.
2. Review agreement by dimension and track.
3. Retire stale or weak-discrimination items.
4. Run bias and compliance audit checks.
5. Re-baseline thresholds if item mix or evaluator models have changed.

## 11. Design Commitments

This methodology commits Palette to the following:

- no multiple-choice-only certification tiers,
- no AI-only final decisions for high-stakes outcomes,
- no hidden threshold changes without recalibration,
- no adaptive pathway claims without sufficient item-bank maturity,
- no certification trust without auditability, appeals, and human override.

The system is intentionally harder to scale than an MCQ exam. That difficulty is the point. The credential should mean the candidate can do the work, not merely recognize the right answer when shown four options.
