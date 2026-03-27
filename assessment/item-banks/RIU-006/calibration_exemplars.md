# Calibration Exemplars — RIU-006: Success Metrics Charter

> **Reference exemplar set.** Each snippet is written from the developer's perspective, as submitted portfolio work. Levels differ in analytical depth and systems thinking — not in word count.
>
> Based on Exercise RIU-006-EX-01: The team reports 95% accuracy on their AI classification system. Everyone is happy. But the metric is gamed: the test set only includes easy cases, and the 5% errors are all in the highest-value category (fraud detection). The system is actually failing on the cases that matter most. Design a metrics charter that would have caught this.

---

## Dimension 1: Metric Quality

### Insufficient

We should track accuracy, precision, and recall. The current 95% accuracy is good but we should also look at F1 score. We should set a target of 98% accuracy and review monthly.

> **Why this is insufficient**: Lists standard ML metrics without connecting them to the business problem. Doesn't address the core issue — that 95% accuracy hides catastrophic failure on high-value cases. "Review monthly" is a schedule, not a measurement strategy. The student knows metric names but not what they're for.

### Basic

The 95% accuracy is misleading because it's averaged across all categories. We need per-category accuracy, especially for fraud detection. The metrics charter should include: overall accuracy (target 95%), fraud detection precision (target 90%), fraud detection recall (target 85%), and false positive rate (target <5%).

> **Why this is basic**: Correctly identifies that aggregate accuracy hides category-level failure and proposes stratified metrics. But the targets are arbitrary (why 90% precision? why 85% recall?) and there's no connection to business impact. The student sees the problem but doesn't connect metrics to outcomes.

### Competent

**Root cause**: The test set doesn't represent production traffic. Easy cases dominate, so aggregate accuracy is high while the system fails on the cases that matter most.

**Metrics charter**:
- Outcome metric: cost of undetected fraud per month (business impact, not model accuracy)
- Stratified accuracy: per-category, per-difficulty tier (easy/medium/hard based on historical human disagreement rates)
- Leading indicator: test set distribution vs production distribution — if these diverge by more than 10%, the eval is invalid
- Acceptance check: accuracy on the hardest 10% of cases must exceed 80% (this is where fraud hides)
- Gaming resistance: precision/recall on high-value categories reported separately, not averaged into aggregate

> **Why this is competent**: Connects metrics to business outcomes (cost of undetected fraud), identifies the distribution mismatch as the root cause, and builds in gaming resistance through stratified reporting. A team could implement this charter immediately and it would have caught the original failure.

### Expert

The interesting failure here isn't bad metrics — it's that the metrics were designed to confirm success rather than detect failure. A 95% accuracy number is a vanity metric when the cost distribution is skewed: one missed fraud case costs more than 1,000 correct easy classifications.

**Charter design principle**: Metrics should be weighted by consequence, not by frequency.

**Metrics**:
- North Star: expected loss per 1,000 classifications (combines error rate × cost per error type)
- Diagnostic: per-category precision/recall, but reported as a confusion matrix so you can see where errors cluster
- Leading indicator: test set representativeness score — KL divergence between test distribution and production distribution, with a hard gate: if divergence exceeds threshold, the eval is rejected before anyone sees an accuracy number
- Acceptance gate: the system must outperform the baseline on the hardest 20% of cases specifically — not on average

The deeper fix is structural: separate the "is the model good?" question from the "is the eval honest?" question. The first is about model performance. The second is about whether the test set is lying to you. Most teams only ask the first question.

> **Why this is expert**: Reframes the problem from "wrong metrics" to "metrics designed to confirm rather than challenge." The expected-loss metric weights errors by consequence, which is the actual business question. The KL divergence gate catches the root cause (dishonest test sets) before it can produce misleading accuracy numbers. The structural insight — separating model quality from eval honesty — generalizes beyond this scenario.

---

## Dimension 2: Stakeholder Alignment

### Insufficient

All stakeholders should agree on the metrics. We should have a meeting to discuss what metrics to track and get everyone's buy-in.

> **Why this is insufficient**: "Have a meeting" is a process suggestion, not a metrics alignment strategy. No identification of who the stakeholders are, what they care about, or how their definitions of success differ.

### Basic

The data team cares about model accuracy. The business team cares about fraud losses. The compliance team cares about false positive rates (wrongly flagging legitimate transactions). We should track all three: accuracy for the data team, fraud loss reduction for business, and false positive rate for compliance.

> **Why this is basic**: Correctly identifies three stakeholder perspectives and maps a metric to each. But the metrics exist in parallel — there's no mechanism for resolving conflicts (what if improving recall increases false positives?) and no shared definition of success.

### Competent

**Stakeholder-metric mapping**:
- Business (CFO): fraud loss reduction — the metric they report to the board
- Data team (ML lead): per-category precision/recall — the metric they optimize against
- Compliance (risk officer): false positive rate — the metric that triggers customer complaints and regulatory scrutiny
- Operations (fraud analysts): alert volume and quality — the metric that determines their workload

**Alignment mechanism**: The North Star metric (expected loss per 1,000 classifications) satisfies business directly and constrains the other three. The data team can't optimize accuracy at the expense of false positives because expected loss includes the cost of false positives. Compliance can't demand zero false positives because expected loss balances fraud detection against customer friction.

> **Why this is competent**: Maps stakeholders to specific metrics with clear rationale, and uses a North Star metric to create alignment without pretending the goals are identical. The constraint mechanism (expected loss includes all costs) prevents one stakeholder from optimizing at another's expense.

### Expert

The alignment problem isn't that stakeholders want different metrics — it's that they have different loss functions. The CFO's loss function is asymmetric: missing a $100K fraud case is catastrophic, while a false positive costs $50 in analyst time. The compliance officer's loss function is also asymmetric but in a different direction: one wrongly frozen account generates a regulatory complaint that costs $10K in remediation.

The charter resolves this by making the loss functions explicit and composable. Each stakeholder defines their cost-per-error-type. The North Star metric is the weighted sum. When stakeholders disagree, the disagreement is about weights, not about metrics — and weight disagreements can be resolved by the person who owns the budget.

The acceptance criteria become: "The system's expected loss must be lower than the baseline's expected loss, using the agreed weight vector." If the weight vector changes (new regulation, new fraud pattern), the acceptance criteria automatically adapt without rewriting the charter.

> **Why this is expert**: Identifies that stakeholder misalignment is fundamentally about different loss functions, not different metrics. Making loss functions explicit and composable turns a political negotiation ("whose metric matters more?") into a quantitative one ("what are the costs?"). The weight-vector approach makes the charter adaptive — it survives changing priorities without structural changes.

---

## Dimension 3: Gaming Resistance

### Insufficient

We should make sure nobody games the metrics. Regular audits should catch any problems.

> **Why this is insufficient**: "Regular audits" is a hope, not a mechanism. No identification of how gaming happens or what structural features would prevent it.

### Basic

To prevent gaming, we should: (1) use a held-out test set that the model team can't see, (2) rotate the test set quarterly, (3) require that test cases include hard examples, not just easy ones.

> **Why this is basic**: Identifies the test set as the gaming vector and proposes reasonable countermeasures. But "include hard examples" is vague — how many? defined how? And held-out test sets can still be gamed if the team knows the distribution.

### Competent

**Gaming vectors identified**:
1. Test set cherry-picking (only easy cases) — the exact failure in this scenario
2. Threshold manipulation (lowering the bar until the metric passes)
3. Category redefinition (reclassifying hard cases into easier categories)

**Countermeasures**:
- Test set representativeness gate: automated comparison of test distribution vs production distribution, with a hard reject if divergence exceeds threshold
- Stratified reporting: accuracy reported per-category and per-difficulty, not just aggregate
- Threshold anchoring: acceptance thresholds set by business impact analysis, not by what the current model can achieve
- Independent evaluation: test set maintained by a different team than the model team

> **Why this is competent**: Names specific gaming vectors and designs targeted countermeasures for each. The representativeness gate directly prevents the failure in this scenario. Independent evaluation adds organizational separation. A team could implement these countermeasures and they would work.

### Expert

Gaming is a systems problem, not a people problem. The original metrics were gameable because they measured what was easy to measure (aggregate accuracy) rather than what was expensive to get wrong (fraud misses). Any metric that can be improved by changing the measurement rather than changing the system is gameable.

The structural fix: every outcome metric must have a corresponding process metric that validates the measurement itself. Accuracy is an outcome metric. Test set representativeness is its process metric. If you report accuracy without representativeness, the number is unauditable.

Second structural fix: metrics should be adversarial by design. Instead of "what's our accuracy?", the charter asks "what's the worst-case accuracy across any category with >1% of production traffic?" This forces the team to find and fix their weakest category rather than hiding it in an average.

The deepest gaming resistance isn't a countermeasure — it's incentive alignment. If the team is rewarded for high accuracy numbers, they'll optimize for high accuracy numbers. If they're rewarded for low fraud losses, they'll optimize for low fraud losses. The charter should specify which outcome the team is accountable for, and it should be the business outcome, not the model metric.

> **Why this is expert**: Reframes gaming as a systems/incentive problem rather than a compliance problem. The process-metric-per-outcome-metric pattern is generalizable — it works for any domain where measurement can be manipulated. The adversarial metric design (worst-case across categories) structurally prevents the averaging trick. The incentive alignment insight connects metrics design to organizational behavior.

---

## Dimension 4: Baseline Handling

### Insufficient

We don't have baseline data so we should just start tracking metrics now and compare against ourselves over time.

> **Why this is insufficient**: "Compare against ourselves over time" means the first version has no acceptance criteria. There's no way to know if the system is good enough to launch, only whether it's getting better or worse.

### Basic

Since there's no baseline, we should: (1) run the current manual process for 2 weeks and measure its accuracy, (2) use that as the baseline, (3) require the AI system to beat the baseline by at least 5% before launch.

> **Why this is basic**: Correctly identifies the need to establish a baseline before comparing. The 2-week measurement sprint is practical. But "beat by 5%" is arbitrary and doesn't account for the cost-weighted nature of errors — beating the baseline on easy cases while losing on hard cases would pass this criterion.

### Competent

**Baseline establishment plan**:
1. 2-week measurement sprint: sample 500 production cases, have human experts classify them, record accuracy per category
2. Cost-weight the baseline: for each category, multiply error rate × cost per error to get baseline expected loss
3. Set acceptance criteria against the cost-weighted baseline, not the raw accuracy baseline
4. Account for baseline uncertainty: with 500 samples, report confidence intervals. Acceptance criterion: AI system's expected loss must be lower than the baseline's upper confidence bound (conservative)

**Why cost-weighting matters here**: The manual process might be 90% accurate overall but 99% accurate on fraud cases (humans are careful with high-stakes decisions). The AI system might be 95% accurate overall but only 85% on fraud. Raw accuracy says the AI wins. Cost-weighted accuracy says the AI loses — because the 15% fraud misses cost more than the 5% improvement on easy cases.

> **Why this is competent**: Establishes a practical baseline with cost-weighting that directly addresses the scenario's failure mode. The confidence interval approach handles the small sample size honestly. The cost-weighting example makes the reasoning concrete and actionable.

### Expert

The baseline question is actually two questions: "how good is the current process?" and "how good does the new process need to be?" These have different answers and different measurement strategies.

For "how good is the current process": measure the manual process on a stratified sample that over-represents hard cases (because that's where the AI is most likely to fail and where the cost of failure is highest). Don't measure on a representative sample — measure on a diagnostic sample designed to stress-test the comparison.

For "how good does the new process need to be": this isn't a statistical question, it's a business question. The acceptance threshold should come from the cost model: "What error rate on fraud cases would make the AI system net-negative after accounting for the cost savings from automation?" That's the break-even point. The acceptance criterion is: perform better than break-even on every category, not just on average.

When no historical data exists at all (greenfield), the baseline is the null model: "what happens if we do nothing?" or "what happens if we use the simplest possible heuristic?" This gives a floor that any real system should beat. If the AI can't beat a simple heuristic on the hard cases, the problem isn't the baseline — it's the AI.

> **Why this is expert**: Separates the baseline question into two distinct problems with different measurement strategies. The diagnostic sampling approach (over-represent hard cases) is more informative than representative sampling for comparison purposes. The break-even analysis connects the acceptance threshold to business economics rather than arbitrary improvement targets. The null-model baseline for greenfield scenarios is practical and generalizable.
