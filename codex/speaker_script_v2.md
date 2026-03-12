# Speaker Script v2 -- 5-Minute Loom Recording

**Thesis**: Codex adoption succeeds when developer value and operational control are designed together.
**Target**: 5:00 total (slides ~2:00, demo ~3:00)
**Demo repo**: JavaPOS — open-source Java retail peripheral platform
**Recording strategy**: 2-3 full takes at ~5-6 min. Pick the best. Don't chase perfection -- chase clarity.

---

## [0:00-0:12] Opening — Hook First

> "I'm [Presenter Name]. The issue here is not whether AI can help engineers. It can. The issue is whether you can roll it out in a way developers actually adopt and leadership can safely scale. This session is about how to do both."

[BEAT — let the title slide breathe]

---

## [0:12-0:30] Slide 2: Four Problems. One Root Cause.

[ADVANCE SLIDE]

> "Here's what discovery told us. Engineering: a large aging checkout codebase, slow onboarding, inconsistent tests, and tribal knowledge locked in senior heads. IT: prior tool rollouts failed because guidance was unclear, adoption was uneven, and no one could see what good or unsafe usage looked like.

> Four problems, one root cause: invisibility. The codebase is invisible to new developers. Usage is invisible to leadership. Risk is invisible to compliance."

---

## [0:30-0:50] Slide 3: Codex in the Workflow

[ADVANCE SLIDE]

> "Codex is not just autocomplete. It can work across a real codebase, reason about multiple files, and operate inside a controlled local environment. That makes it useful for understanding unfamiliar systems, planning bounded changes, and generating tests.

> For this deployment, the key point is not novelty. It's control. Teams can define local instructions, IT can set central guardrails, and leaders can review how the tool is being used over time."

---

## [0:50-1:10] Slide 4: Your Standards Become the AI's Operating Rules

[ADVANCE SLIDE]

> "The harness is how you make that control operational. Three components.

> AGENTS.md gives each repo version-controlled instructions. An org policy layer gives IT and security central guardrails. Approval modes let you phase trust from 'ask every time' to broader autonomy only when the evidence supports it.

> The important idea is that the rollout model is durable. Teams know how to use Codex. Leadership knows where it is being used. Security knows which controls are in force."

---

## [1:10-1:40] Slide 5: Start Read-Only. Scale on Evidence.

[ADVANCE SLIDE]

> "Three workflows, phased. Start with Code Understanding: read-only, low risk, and directly tied to the customer's biggest pain point, which is getting engineers productive in a large legacy codebase.

> We teach this workflow first because it builds judgment, not just speed. Developers learn how to ask Codex to explain a module, trace dependencies, and identify what they still need to verify. Leadership gets a low-risk adoption path with clear patterns to monitor before enabling higher-trust workflows.
>
> During the pilot: weekly office hours, a shared prompt library, and explicit review expectations. Enablement is not a launch event. It's an operating cadence."

---

## [1:40-2:00] Slide 6: Same Data. Two Audiences.

[ADVANCE SLIDE]

> "The same usage data serves two audiences. Engineering leaders see adoption by workflow, where teams are getting stuck, and which use cases are worth scaling. IT sees whether guardrails are being followed and whether usage patterns match the approved rollout.

> Same data, two audiences, one system. Not 'trust us, developers are being careful.' Observable evidence that governance is working."

---

## [2:00-3:05] Demo Move 1: Code Understanding on JavaPOS

[SWITCH TO CODEX SCREEN]

> "Let me show you what this looks like. I've loaded JavaPOS -- an open-source Java point-of-sale device API. Think of this as a stand-in for your checkout infrastructure."

[SUBMIT PROMPT: "Explain the device management architecture in this codebase. What are the main components, how do they interact, and what would a new developer need to understand first?"]

> "I'm asking Codex to explain the architecture to a new developer. This is the Code Understanding workflow -- entirely read-only."

[WAIT FOR RESPONSE -- narrate while waiting if needed: "Codex is reading the Java source, tracing the call graph, building a dependency map..."]

> "Look at what we get. A clear explanation of what this module does, its upstream and downstream dependencies, and where a new developer should start. That's the fastest path to value in an enterprise rollout because it reduces code archaeology without changing a line of code.

> And notice -- nothing was changed. This is where I would start the pilot: useful for developers on day one, low risk for leadership on day one."

---

## [3:05-4:15] Demo Move 2: Bounded Change Planning and Review

[SUBMIT PROMPT: "Based on that architecture, propose a small low-risk refactor to improve maintainability. Do not write code yet. Give me the files you would inspect, the tests you would run, and the risks I should review before approving any change."]

[PAUSE -- let this land]

> "Now I move from understanding to a bounded change plan. Still no code. I want Codex to scope the work, surface the files involved, and tell me what needs review before anyone approves a change."

[WAIT FOR RESPONSE]

> "This is the workflow I would teach in week two. Codex helps the developer break a change into something reviewable: what to inspect, what might break, and what tests or owners need to be involved.

> This is what responsible usage looks like. Codex accelerates planning, but the developer still owns the decision, the review, and the merge. That is the standard I would set from the first enablement session."

---

## [4:15-4:45] Demo Bridge Back to Rollout

[RETURN TO SLIDES OR STAY ON CODEX OUTPUT]

> "In a pilot, those same interactions become the evidence base for rollout. You can see which workflows teams actually use, where they need more guidance, and whether it is safe to expand from read-only understanding into test generation and refactoring."

---

## [4:45-5:00] Closing

> "Start with code understanding. Put the harness in place early. Then scale based on evidence, not enthusiasm. Next step: select the pilot team and define the success criteria before rollout. Thank you."

---

## Timing Notes

| Segment | Target | Hard Limit |
|---|---|---|
| Opening (hook first) | 0:12 | 0:15 |
| Slide 2: Four problems, one root cause | 0:18 | 0:22 |
| Slide 3: Codex in the workflow | 0:20 | 0:25 |
| Slide 4: Your standards = AI's rules | 0:20 | 0:25 |
| Slide 5: Start read-only, scale on evidence | 0:30 | 0:35 |
| Slide 6: Same data, two audiences | 0:20 | 0:25 |
| Demo Move 1: code understanding | 1:05 | 1:15 |
| Demo Move 2: bounded change planning | 1:10 | 1:20 |
| Demo bridge back to rollout | 0:30 | 0:35 |
| Closing (with next step) | 0:15 | 0:18 |
| **TOTAL** | **5:00** | **5:30** |

## Contingency Instructions

- **If running long at 2:00**: compress Slide 6 to one sentence: "The same usage data tells engineering what to teach next and IT what is safe to scale."
- **If Codex response is slow (>20s)**: narrate while waiting. "Response times vary with codebase size. What matters is that the workflow stays reviewable."
- **If Codex gives a weak response on Move 2**: pivot to the standard. "Even if the plan is imperfect, the point is the workflow: Codex scopes the work, and the developer reviews before any code is written."
- **If running long at 4:00**: cut the bridge section to one sentence and go straight to the close.
- **If running short**: expand Move 2 by naming exactly which owners or tests you would require before approving a change.

## Key Lines — Must Hit

These six lines carry the thesis. If you forget everything else, land these:

1. "The issue is not whether AI can help engineers. It can. The issue is whether you can roll it out safely and actually get adoption." (hook — first 5 seconds)
2. "Four problems, one root cause: invisibility." (thesis — slide 2)
3. "Start with Code Understanding: read-only, low risk, directly tied to the biggest pain point." (strategy — slide 5)
4. "This is what responsible usage looks like." (Move 2 — the differentiator)
5. "The same usage data serves two audiences." (governance — slide 6)
6. "Scale based on evidence, not enthusiasm." (close — last line)

## Energy Notes

- Opening: confident, direct. No warmup patter.
- Discovery: compressed energy — you're playing back facts, not performing.
- "Four problems, one root cause" — slow down. This is the thesis moment.
- Strategy section — steady, practical. You're showing judgment, not hype.
- Demo: teaching energy — you're showing, not selling.
- Bounded change plan: let it breathe. This is where they see your operating standards.
- Closing: downward pressure. Calm authority. "Next step" = forward momentum. End clean.
