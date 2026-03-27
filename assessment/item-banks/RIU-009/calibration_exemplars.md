# Calibration Exemplars — RIU-009: Risk Register + Mitigation Plan

> **Reference exemplar set.** Each snippet is written from the developer's perspective, as submitted portfolio work. Levels differ in risk thinking maturity and operational realism — not in word count.
>
> Based on Exercise RIU-009-EX-01: The risk register hasn't been updated in 6 weeks. The team says 'nothing has changed.' But: the primary data source added rate limiting last week, the ML engineer who built the model gave notice, and the customer's compliance team published new AI guidelines. None of these are in the register. Audit the register and add the missing risks.

---

## Dimension 1: Risk Identification

### Insufficient

The risk register should be updated more frequently. We should add: (1) API changes, (2) team changes, (3) compliance changes. Going forward, we'll update the register every week.

> **Why this is insufficient**: Restates the three problems from the scenario as one-word categories without analysis. "API changes" is not a risk — it's a category. There's no assessment of impact, probability, or what specifically could go wrong. "Update every week" is a schedule, not a detection mechanism.

### Basic

**Missing risks identified**:
1. API rate limiting — the data source added rate limits, which could reduce our throughput and cause timeouts
2. Key person departure — the ML engineer who built the model is leaving, taking institutional knowledge with them
3. New compliance requirements — the customer's compliance team published new AI guidelines that may affect our architecture

Each risk should be added to the register with severity (high/medium/low) and an owner.

> **Why this is basic**: Correctly identifies all three risks with reasonable descriptions. But the analysis stops at identification — there's no assessment of how these risks interact, no distinction between the risk and its symptoms, and no exploration of second-order effects (e.g., the departing engineer is also the only person who understands the rate-limited API).

### Competent

**Audit findings**: The register is stale because there's no detection mechanism — it relies on someone remembering to update it. The three missing risks are symptoms of a process failure, not just individual oversights.

**Risk 1: API rate limiting (operational)**
- Specific impact: throughput drops from 1,000 req/min to 100 req/min. Batch processing that currently takes 2 hours would take 20 hours. Real-time features would timeout.
- Probability: certain (already happened)
- Detection signal that was missed: API changelog, HTTP 429 responses in logs

**Risk 2: Key person dependency (organizational)**
- Specific impact: model retraining, debugging, and architecture decisions depend on one person. After departure, the team cannot safely modify the model.
- Probability: certain (notice given)
- Detection signal that was missed: bus factor analysis (who knows what?)
- Second-order risk: the departing engineer is likely the only person who understands the rate-limited API's quirks

**Risk 3: Compliance requirement change (regulatory)**
- Specific impact: unknown until guidelines are reviewed, but could require architecture changes (data residency, explainability, audit logging)
- Probability: high (guidelines published, applicability likely)
- Detection signal that was missed: customer compliance team communications, regulatory monitoring

**Process fix**: Each risk category needs an automated or scheduled detection mechanism, not just a reminder to "check the register."

> **Why this is competent**: Analyzes each risk with specific impact assessment, identifies the detection signals that were missed, and connects the three risks through second-order effects. The process fix addresses the root cause (no detection mechanism) rather than the symptom (stale register). A team could act on this immediately.

### Expert

The register wasn't stale because the team forgot to update it. It was stale because the team's mental model of "risk" was limited to things that go wrong inside the system. All three missed risks originated outside the system boundary: an upstream API change, a human resource change, and a regulatory change. The register had no sensors pointed outward.

**The real risk inventory**:

The three obvious risks are table stakes. The interesting risks are the interactions:
- The departing engineer + the rate-limited API = nobody who understands the API's behavior is available to design the caching/retry layer needed to handle rate limits
- The compliance guidelines + the departing engineer = if the guidelines require model explainability, the only person who can explain the model's design decisions is leaving
- Rate limiting + compliance = if compliance requires audit logging of every API call, the rate limit becomes even tighter because audit calls consume quota

**Detection architecture**: Instead of "update the register weekly," instrument the risk sources:
- Upstream APIs: monitor changelogs, alert on new rate limit headers or error codes
- Team composition: trigger risk review when anyone with "sole knowledge" status gives notice
- Regulatory: subscribe to customer compliance team updates, flag any mention of AI/ML

The register should be a living dashboard with automated feeds, not a document someone opens every Friday.

> **Why this is expert**: Identifies the structural blind spot (no outward-facing sensors) rather than just the missing entries. The interaction analysis reveals compound risks that are invisible when risks are assessed individually. The detection architecture transforms the register from a periodic document into a continuous monitoring system. This is risk management as systems design, not as checklist maintenance.

---

## Dimension 2: Mitigation Quality

### Insufficient

For the API rate limiting, we should add caching. For the departing engineer, we should do a knowledge transfer. For compliance, we should review the guidelines.

> **Why this is insufficient**: Each mitigation is a single vague action with no specifics. "Add caching" — what gets cached? for how long? what's the invalidation strategy? "Knowledge transfer" — of what? to whom? by when? These are intentions, not plans.

### Basic

**Mitigations**:
1. API rate limiting: implement request caching with 1-hour TTL, add retry logic with exponential backoff, request rate limit increase from provider
2. Key person departure: schedule 2-week knowledge transfer, document model architecture and training pipeline, pair the departing engineer with a backup
3. Compliance: schedule review meeting with compliance team within 1 week, identify affected components, create remediation plan

Each mitigation has an owner and a deadline.

> **Why this is basic**: Mitigations are specific and actionable with reasonable steps. But they're treated as independent — there's no prioritization, no resource conflict analysis (the departing engineer is needed for both the knowledge transfer AND the rate limit workaround), and no verification that the mitigation actually worked.

### Competent

**Prioritized mitigation plan** (resource-aware):

**Week 1 (critical — departing engineer still available)**:
- Knowledge transfer: model architecture, training pipeline, AND API integration quirks (the engineer knows both)
- Owner: ML lead. Verification: backup engineer can independently explain model decisions and API behavior
- Rate limit workaround: departing engineer designs the caching layer before leaving (they understand the API's idiosyncrasies)
- Owner: departing engineer + backup. Verification: caching layer handles 10x current load in staging

**Week 1-2 (parallel)**:
- Compliance review: read guidelines, map to current architecture, identify gaps
- Owner: tech lead + compliance liaison. Verification: gap analysis document with severity ratings

**Week 2-3 (dependent on compliance review)**:
- Compliance remediation: implement required changes based on gap analysis
- Owner: tech lead. Verification: compliance team sign-off

**Verification for each mitigation**: Not "did we do the thing?" but "did the thing work?" Knowledge transfer verified by independent demonstration. Caching verified by load test. Compliance verified by sign-off.

> **Why this is competent**: Mitigations are sequenced by resource dependency (departing engineer is the bottleneck), each has a verification step that tests effectiveness rather than completion, and the plan accounts for the interaction between risks. This is executable.

### Expert

The mitigations address the three immediate risks, but the deeper problem is that the team has no mitigation capacity — they're fully allocated to feature work, and risk mitigation is competing for the same people and time.

**Structural mitigation** (beyond the immediate fixes):

The departing engineer mitigation isn't "knowledge transfer" — it's "eliminate single points of failure." The knowledge transfer is the immediate action, but the structural fix is: no component should have fewer than two people who can modify it. This is a permanent team policy, not a one-time response to someone leaving.

The rate limit mitigation isn't "add caching" — it's "design for upstream instability." The caching layer is the immediate action, but the structural fix is: every external dependency should have a degradation mode. What happens when the API is slow? Down? Rate-limited? Changed? Each scenario needs a pre-designed response, not an ad-hoc fix.

The compliance mitigation isn't "review the guidelines" — it's "build regulatory awareness into the development process." The review is the immediate action, but the structural fix is: compliance requirements are checked at design time (before building), not at audit time (after building).

Each immediate mitigation should produce a lasting artifact: the knowledge transfer produces a runbook, the caching layer produces a dependency resilience pattern, the compliance review produces a design checklist. These artifacts prevent the same class of risk from recurring.

> **Why this is expert**: Distinguishes between immediate mitigations (fix the problem) and structural mitigations (prevent the class of problem). Each immediate action is connected to a lasting artifact that reduces future risk. The insight that mitigation capacity is itself a risk — the team can't mitigate because they're fully allocated — is a meta-risk that most registers miss entirely.

---

## Dimension 3: Escalation Timeliness

### Insufficient

We should escalate risks when they become critical. The team lead should decide when to escalate.

> **Why this is insufficient**: "When they become critical" means after the risk has materialized — that's incident response, not risk escalation. No trigger conditions, no thresholds, no defined escalation path.

### Basic

**Escalation triggers**:
- API rate limiting: escalate if throughput drops below 50% of normal for more than 1 hour
- Key person departure: escalate immediately when notice is given
- Compliance: escalate if guidelines require architecture changes

Escalation goes to the project lead, who decides on resource allocation.

> **Why this is basic**: Defines specific triggers for each risk, which is a significant improvement over "when it's critical." But the triggers are reactive (throughput already dropped, notice already given) rather than predictive. The escalation path is a single person with no backup or time constraint.

### Competent

**Escalation framework with leading indicators**:

| Risk | Leading Indicator | Yellow Trigger | Red Trigger | Escalation Path |
|------|-------------------|----------------|-------------|-----------------|
| API rate limiting | HTTP 429 count in logs | >10 per hour (new behavior) | >100 per hour OR throughput <50% | Yellow: tech lead within 4 hours. Red: project lead + API provider within 1 hour |
| Key person departure | Team composition changes | Any team member with sole-knowledge status updates resume | Notice given | Yellow: initiate knowledge audit within 1 week. Red: knowledge transfer sprint, block feature work |
| Compliance | Regulatory communications | Customer compliance team publishes any AI-related update | Guidelines require architecture changes | Yellow: compliance review within 1 week. Red: architecture review within 48 hours, potential scope change |

**Key design choice**: Yellow triggers fire before the risk materializes. Red triggers fire when it has materialized or is imminent. Yellow gives you time to prepare. Red demands immediate action.

> **Why this is competent**: Two-tier escalation with leading indicators means the team gets early warning before the risk materializes. The triggers are specific and measurable. The escalation paths have time constraints and named roles. This framework would have caught all three risks in the scenario before they became problems.

### Expert

The escalation framework is necessary but insufficient. The real question is: why did three significant external changes happen without anyone in the team noticing for 6 weeks?

The answer is that escalation was designed as a human process (someone notices → someone escalates) rather than a system process (a sensor detects → an alert fires → a human decides). Human-dependent escalation fails silently — exactly the failure mode in this scenario.

**Escalation as infrastructure**:
- API monitoring: automated alert on any new HTTP status code, any new response header (like rate limit headers), any changelog update from the provider. These are zero-cost sensors that fire before anyone needs to "notice" anything.
- Team composition: HR system integration or simple calendar reminder — when anyone's status changes, trigger a bus-factor review for their components.
- Regulatory: RSS/email subscription to customer compliance publications. Flag any document containing "AI," "machine learning," or "automated decision."

**Escalation timeliness metric**: Time from external change to team awareness. In this scenario, it was 6+ weeks for all three risks. The target should be <48 hours for any change that affects a system dependency.

The escalation framework should be auditable: for each external change that affected the system, when did the team become aware? If the answer is "when it broke," the escalation system failed.

> **Why this is expert**: Identifies that the escalation failure is structural (human-dependent detection) rather than procedural (wrong triggers). The "escalation as infrastructure" approach replaces human vigilance with automated sensors. The timeliness metric makes escalation effectiveness measurable and auditable. The audit question ("when did the team become aware?") is a powerful retrospective tool that reveals detection gaps.
