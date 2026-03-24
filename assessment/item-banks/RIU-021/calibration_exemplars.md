# Calibration Exemplars — RIU-021: Golden Set + Offline Evaluation Harness

> Reference set. Levels differ by evaluation judgment, ambiguity handling, and operational usefulness, not by length.

## Dimension 1: Golden Set Quality

### Insufficient
"We created 25 examples from recent successful queries so we can test the system before launch."

Why:
- Happy-path only.
- No difficulty spread, failure-mode intent, or coverage logic.

### Basic
"We created examples across easy, medium, and hard questions, including a few edge cases from support tickets."

Why:
- Some variety exists.
- Coverage is still anecdotal rather than systematic.

### Competent
"The golden set is stratified by document type, task type, and failure mode. It includes routine cases, edge cases, and deliberately ambiguous cases, and it explicitly records which source families are still underrepresented so coverage can expand in a planned way."

Why:
- Coverage is intentional, not accidental.
- The set can actually support improvement work.

### Expert
"The golden set is designed to answer two different questions: 'Does the system work on common traffic?' and 'Where does it break in ways that matter?' It therefore mixes representative production cases, adversarial edge cases, and borderline cases that reveal metric blind spots. Coverage gaps are not just noted; they are tied to a backlog for the next expansion pass."

Why:
- Distinguishes representativeness from diagnostic value.
- Treats the golden set as a measurement instrument rather than a test collection.

## Dimension 2: Harness Functionality

### Insufficient
"The harness runs the cases and prints pass or fail."

Why:
- Bare execution, no reproducibility or gating value.

### Basic
"The harness runs the cases, computes scores, and fails if the score drops below a threshold."

Why:
- Functional but shallow.
- Assumes the threshold means something without showing why.

### Competent
"The harness runs deterministically, records reproducible outputs, and applies explicit pass/fail gates tied to the module's success criteria. When a case fails, the report shows which metric failed and which artifact or system behavior needs investigation."

Why:
- Operationally useful.
- Connects harness output to remediation.

### Expert
"The harness is not just a score calculator; it is a release gate. It distinguishes configuration failures, model-quality failures, and ground-truth ambiguity, so the team knows whether to fix code, revise evaluation, or escalate to human review. The result is actionable under delivery pressure, not just informative."

Why:
- Differentiates classes of failure.
- Demonstrates release-governance thinking.

## Dimension 3: Metric Selection

### Insufficient
"We use accuracy for all outputs because it is simple to understand."

Why:
- One metric for incompatible output types.
- Ignores construct mismatch.

### Basic
"We use precision/recall for extraction and an LLM judge for summaries."

Why:
- Better than one metric.
- Still incomplete because the reasoning behind each choice is weak.

### Competent
"Metrics are selected by output type and business consequence: extraction uses precision/recall or exactness checks, classification uses per-class performance, and generative outputs use rubric-based review tied to the actual success criteria. The team can explain why each metric answers a different quality question."

Why:
- Metrics fit the work being measured.
- Shows construct validity rather than metric shopping.

### Expert
"Metric selection is driven by failure cost, not habit. A metric is only used if it would detect the kind of regression the business actually cares about. That means exact-match style checks for deterministic outputs, calibrated rubric judgment for subjective outputs, and composite scoring only where a single metric would conceal an important failure mode."

Why:
- Shows second-order evaluation judgment.
- Avoids false confidence from easy-but-wrong metrics.

## Dimension 4: Calibration and Adjudication

### Insufficient
"If reviewers disagree, we will discuss it later."

Why:
- No adjudication protocol.
- Assumes disagreement is exceptional rather than expected.

### Basic
"Ambiguous cases are tagged and a human will review them if needed."

Why:
- Acknowledges ambiguity.
- Still lacks calibration mechanics and clear escalation triggers.

### Competent
"Ambiguous cases are tagged explicitly, calibration exemplars anchor what different score levels mean, and disagreements above a defined threshold route to human review. The harness distinguishes contested ground truth from model failure so the team does not 'fix' the wrong thing."

Why:
- Makes adjudication operational.
- Prevents ambiguity from being mislabeled as system error.

### Expert
"Calibration is designed as an ongoing control, not a one-time setup. The process names which cases are inherently contestable, which cases define anchor standards, and which signals trigger escalation when the automated judgment is likely unreliable. The result is a scoring system that remains honest about uncertainty instead of hiding it behind a numeric score."

Why:
- Treats disagreement as a system property.
- Aligns strongly with Layer 2 / Layer 3 boundary design.

## Dimension 5: Failure Analysis

### Insufficient
"Some examples failed and the team should improve the model."

Why:
- No pattern analysis.
- No actionable diagnosis.

### Basic
"The report shows that failures happen most often on longer documents and some ambiguous prompts."

Why:
- Observes a pattern.
- Still too shallow to guide next action.

### Competent
"The report groups failures by root cause such as retrieval miss, metric mismatch, ambiguous gold answer, or prompt brittleness. For each group it proposes a next action, so the team can decide whether to fix the system, expand the golden set, or revise the scoring method."

Why:
- Turns results into a decision tool.

### Expert
"Failure analysis does not just describe what broke; it separates learner/system defects from evaluation defects. The report makes clear when the system is weak, when the item bank is weak, and when the rubric is weak. That distinction prevents the team from overfitting the product to a broken evaluation harness."

Why:
- Shows mature evaluation governance.
- Prevents the harness from becoming a source of false optimization.
