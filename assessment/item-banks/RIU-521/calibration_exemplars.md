# Calibration Exemplars — RIU-521: LLM Model Version Management

> **Reference exemplar set.** Each snippet is written from the developer's perspective, as submitted portfolio work. Levels differ in operational maturity and multi-provider awareness — not in word count.
>
> Based on Exercise RIU-521-EX-01: LLM provider silently updates model. System behavior changes subtly. Nobody notices for 2 weeks because model version is not tracked per request.

---

## Dimension 1: Version Tracking

### Insufficient

We should log which model we're using. We can add the model name to our configuration file and check it when something goes wrong.

> **Why this is insufficient**: A config file records what you intended to use, not what you actually used. If the provider silently updates the model behind the same API endpoint, your config still says "gpt-4" while the actual model changed. No per-request tracking means you can't correlate behavior changes with version changes.

### Basic

We log the model name and version from the API response headers for every request. We store this in our request logs alongside the input, output, and timestamp. If behavior changes, we can check whether the model version changed at the same time.

> **Why this is basic**: Per-request logging from response headers is the right approach — it captures what actually ran, not what was configured. But the analysis is reactive ("if behavior changes, we can check"). There's no automated detection of version changes and no alerting. The 2-week detection gap in the scenario would still happen.

### Competent

**Version tracking system**:
- Per-request: log model identifier from API response (not from config) with every request. Store: `{request_id, timestamp, model_id, model_version, input_hash, output_hash, latency_ms}`.
- Version change detection: automated alert when the model version in responses differs from the expected version. Alert fires on the first divergent response, not after a pattern emerges.
- Version pinning: where the API supports it, pin to a specific model version (e.g., `gpt-4-0613` not `gpt-4`). Where pinning isn't supported, the version change alert is the safety net.
- Dashboard: current model version per endpoint, last version change date, days since last change. Visual indicator when a version is approaching its deprecation date.

> **Why this is competent**: Automated detection eliminates the 2-week gap. Version pinning prevents silent updates where possible. The dashboard provides ongoing visibility. Per-request logging with input/output hashes enables before/after comparison when a version change is detected.

### Expert

Version tracking is necessary but not sufficient. The real question isn't "did the version change?" — it's "did the behavior change?" A version change with identical behavior is a non-event. A behavior change without a version change (provider-side A/B testing, infrastructure changes, rate limit changes) is invisible to version tracking alone.

**Behavioral fingerprinting**:
- Maintain a golden set of 20-50 representative inputs with expected outputs. Run this set against the model daily (or on every detected version change). Compare outputs against the golden set using semantic similarity, not exact match.
- Behavioral drift metric: percentage of golden set outputs that changed beyond a threshold. Alert when drift exceeds 5%.
- This catches both version changes (provider updated the model) and non-version changes (provider changed inference infrastructure, adjusted safety filters, modified system prompts).

**Version tracking as audit trail**: Every production request should be reproducible — given the same input and the same model version, you should get the same output (within stochastic bounds). If you can't reproduce a result, you can't debug it, explain it, or defend it. Version tracking is the foundation of reproducibility.

> **Why this is expert**: Separates version changes from behavior changes — the thing you actually care about. The golden set approach detects behavioral drift regardless of cause. The reproducibility framing connects version tracking to auditability and explainability, which matter for compliance and debugging. This is version management as an observability practice, not just a logging practice.

---

## Dimension 2: Testing Rigor

### Insufficient

We should test new model versions before deploying them. We can run our test suite and check if the results look good.

> **Why this is insufficient**: "Look good" is subjective. "Test suite" is unspecified. No comparison methodology, no acceptance criteria, no definition of what "passing" means for a stochastic system.

### Basic

When a new model version is available, we run our eval suite (50 test cases with expected outputs) against both the current and new version. We compare accuracy: if the new version scores within 5% of the current version, we approve the upgrade. If it scores lower, we investigate.

> **Why this is basic**: Structured comparison with a defined threshold is good. But 50 test cases may not cover the distribution of production traffic. The 5% threshold is applied globally — the new version could be 20% worse on critical cases while being 10% better on easy cases, and still pass. No regression testing on specific failure modes.

### Competent

**Version validation protocol**:
1. Golden set test: 50 curated cases covering normal, edge, and adversarial inputs. Must pass with >90% agreement with expected outputs.
2. Production shadow test: run the new version on a sample of live production traffic (shadow mode — results logged but not served). Compare against the current version's outputs on the same inputs.
3. Stratified comparison: break results down by input category, difficulty, and criticality. The new version must not regress on any critical category, even if aggregate performance improves.
4. Regression gate: maintain a list of previously-fixed failure cases. If the new version reintroduces any of these failures, it's automatically rejected.

**Acceptance criteria**: Pass golden set AND no critical-category regression AND no reintroduced failures. Aggregate improvement is nice but not required — stability matters more than marginal gains.

> **Why this is competent**: Multi-layer testing (golden set + production shadow + stratified + regression) catches different failure modes. The stratified comparison prevents the "better on average, worse where it matters" problem. The regression gate prevents known-fixed issues from recurring. Acceptance criteria are explicit and automatable.

### Expert

The fundamental challenge with LLM version testing is that the output space is enormous and stochastic. You can't test every possible input, and the same input may produce different outputs on different runs. Testing rigor for LLMs requires a different mental model than testing deterministic software.

**Testing as statistical inference**:
- The golden set isn't a pass/fail test — it's a sample from which you estimate the population behavior. 50 cases give you a confidence interval, not a certainty. Report results as "92% ± 4% agreement" not "92% agreement."
- Production shadow testing should run for long enough to capture the full distribution of input types. One hour of shadow traffic during business hours is different from one hour at 3am. Run for at least one full business cycle (24 hours minimum).
- Behavioral comparison should use semantic similarity metrics, not exact match. Two different phrasings of the same correct answer should both count as passes. This requires a comparison model or embedding-based similarity — which itself needs to be versioned and validated.

**The meta-testing problem**: Your test harness uses an LLM to evaluate LLM outputs. If the evaluation model also changes, your test results are unreliable. Pin the evaluation model independently of the production model. Version-track both.

**Canary deployment**: Even after testing, deploy the new version to 1% of traffic first. Monitor for 24-48 hours. Compare error rates, latency, user feedback, and downstream metrics against the 99% still on the old version. Promote to 100% only after the canary period passes.

> **Why this is expert**: Treats LLM testing as statistical inference rather than deterministic pass/fail. The confidence interval approach is honest about what testing can and can't tell you. The meta-testing insight (your evaluator is also an LLM that can change) is a subtle but critical point most teams miss. Canary deployment adds a production-level safety net beyond pre-deployment testing.

---

## Dimension 3: Deprecation Management

### Insufficient

When the provider deprecates a model, we should switch to the new version.

> **Why this is insufficient**: "Switch to the new version" treats deprecation as a simple swap. In reality, deprecation means your prompts, evaluation criteria, and downstream integrations may all need updating. No timeline, no migration plan, no risk assessment.

### Basic

We maintain a deprecation calendar that tracks when each model version reaches end-of-life. When a deprecation is announced, we start evaluation of the replacement version immediately. We aim to complete migration at least 1 week before the deprecation date.

> **Why this is basic**: Proactive tracking and early evaluation are good. But 1 week of buffer assumes evaluation and migration go smoothly. The scenario shows evaluation takes 3 weeks — leaving only 1 week for migration. No contingency for when evaluation reveals the replacement is worse.

### Competent

**Deprecation management protocol**:
- Monitoring: subscribe to provider deprecation announcements (API, email, changelog). Alert the team within 24 hours of any announcement.
- Timeline: deprecation notice → evaluation start (within 48 hours) → evaluation complete (2 weeks) → migration (1 week) → buffer (remaining time). If the timeline doesn't allow for this sequence, escalate immediately.
- Pre-evaluation: before any deprecation is announced, maintain a running evaluation of the next likely replacement version. This means when deprecation hits, you already have preliminary results.
- Contingency: if the replacement version fails evaluation, options are: (a) negotiate extended support with provider, (b) switch to alternative provider, (c) accept degraded performance with documented risk. Decision is a ONE-WAY DOOR if it affects production quality.

**Migration playbook**: step-by-step runbook for version migration including: prompt compatibility check, evaluation suite run, canary deployment, rollback procedure, downstream notification.

> **Why this is competent**: Pre-evaluation of likely replacements eliminates the "evaluation takes 3 weeks" bottleneck. The timeline template makes the schedule explicit and reveals when buffer is insufficient. The contingency options are realistic and include the escalation path. The migration playbook makes the process repeatable.

### Expert

Deprecation management is a supply chain problem. You depend on an external provider for a critical component, and they control the lifecycle. The strategic response isn't better migration processes — it's reducing your exposure to any single provider's lifecycle decisions.

**Strategic deprecation management**:
- Provider abstraction layer: your application talks to an internal API that routes to providers. Switching providers means changing the routing, not the application code. This turns a provider deprecation from a code change into a config change.
- Multi-provider readiness: maintain evaluated alternatives for every model you use in production. When Provider A deprecates, you can route to Provider B within hours, not weeks. The evaluation is already done.
- Prompt portability: prompts should be tested against multiple models during development, not just the target model. A prompt that only works with one specific model version is a liability.

**Deprecation as a forcing function**: Every deprecation is an opportunity to re-evaluate whether you're using the right model for the task. The replacement version might be better — or a completely different model (smaller, cheaper, faster) might have caught up. Deprecation forces the comparison you should have been doing continuously.

**Metric**: time-to-migrate. How long from deprecation announcement to production migration complete? Target: <1 week for routine deprecations (same provider, similar model). <2 weeks for provider switches. If it takes longer, your abstraction layer is leaking provider-specific details.

> **Why this is expert**: Reframes deprecation from an operational problem (migrate before the deadline) to a strategic problem (reduce dependency on any single provider's decisions). The provider abstraction layer and multi-provider readiness turn deprecation from a crisis into a routine operation. The prompt portability insight prevents the most common migration blocker — prompts that are accidentally coupled to a specific model's behavior. The time-to-migrate metric makes migration readiness measurable.

---

## Dimension 4: Multi-Provider Management

### Insufficient

We use OpenAI for everything. If we need to switch, we'll evaluate alternatives at that time.

> **Why this is insufficient**: Single-provider dependency with no contingency plan. "Evaluate at that time" means evaluation happens under deadline pressure, which leads to poor decisions. No awareness of the multi-provider landscape.

### Basic

We use two providers: OpenAI for generation and Anthropic for classification. Each has its own API integration. If one provider has issues, we can manually switch tasks to the other provider, though the prompts may need adjustment.

> **Why this is basic**: Using multiple providers is better than single-provider dependency. But the integrations are provider-specific ("each has its own API integration"), which means switching requires code changes. "Prompts may need adjustment" understates the problem — prompts tuned for one model often perform poorly on another.

### Competent

**Multi-provider architecture**:
- Unified API layer: all providers accessed through a common interface. Provider-specific details (auth, rate limits, response format) are handled in adapters.
- Per-task provider assignment: each task (generation, classification, summarization) has a primary and fallback provider. Failover is automatic — if the primary returns errors or exceeds latency SLA, traffic routes to the fallback.
- Normalized version tracking: each provider has different versioning schemes (OpenAI uses dates, Anthropic uses names, open-source uses commit hashes). Normalize to a common format: `{provider, model_family, version, capabilities, last_evaluated}`.
- Cross-provider evaluation: when evaluating a new version from any provider, also run the eval against the current best from other providers. This prevents lock-in and surfaces when a competitor has caught up or surpassed your current choice.

> **Why this is competent**: The unified API layer makes provider switching a routing change. Automatic failover provides resilience. Normalized version tracking enables cross-provider comparison. Cross-provider evaluation during version changes prevents gradual lock-in.

### Expert

Multi-provider management isn't about having backup providers — it's about maintaining optionality in a market that changes quarterly. The provider that's best today may not be best in 6 months. Your architecture should make switching cheap enough that you actually do it when the market shifts.

**Optionality architecture**:
- Provider-agnostic prompts: write prompts that work across providers, then add provider-specific optimizations as a separate layer. The base prompt is portable; the optimization layer is disposable.
- Continuous benchmarking: run your golden set against all viable providers monthly. Maintain a leaderboard: `{provider, model, task, score, cost_per_1k, latency_p95}`. When a provider's score/cost ratio changes significantly, trigger a migration evaluation.
- Cost-aware routing: for non-critical tasks, route to the cheapest provider that meets the quality threshold. For critical tasks, route to the highest-quality provider regardless of cost. This naturally distributes traffic across providers, keeping all integrations warm.

**The prompt-model compatibility matrix**: For each prompt in production, track which models it's been validated against and when. A prompt validated only against `gpt-4-0613` is a single point of failure. A prompt validated against 3 providers and 5 model versions is resilient. The matrix tells you exactly where your exposure is.

**Metric**: provider concentration risk. What percentage of your production traffic goes to a single provider? If it's >80%, you have concentration risk regardless of how many fallback providers you've configured. The fallback providers' integrations may have rotted because they never carry real traffic.

> **Why this is expert**: Frames multi-provider management as optionality maintenance, not just redundancy. The continuous benchmarking leaderboard makes provider comparison a routine operation rather than a crisis response. Cost-aware routing keeps all integrations warm with real traffic, preventing the "fallback that doesn't actually work" problem. The prompt-model compatibility matrix makes dependency exposure visible and actionable. The concentration risk metric prevents false confidence from having "backup providers" that never carry traffic.
