# Speaker Script v2 -- 5-Minute Loom Recording

**Thesis**: Visibility IS governance. Visibility IS enablement. Visibility is the common ground.
**Target**: 5:00 total (slides ~2:00, demo ~3:00)
**Demo repo**: RetailPOS — open-source Java retail peripheral platform
**Recording strategy**: 2-3 full takes at ~5-6 min. Pick the best. Don't chase perfection -- chase clarity.

---

## [0:00-0:12] Opening — Hook First

> "I'm [Presenter Name]. The last AI coding tool rollout at this company was killed in weeks. Source code reached third-party servers, there was no audit trail, compliance flagged SOX risk, and the project was shut down. This session is about making sure that doesn't happen again."

[BEAT — let the title slide breathe]

---

## [0:12-0:30] Slide 2: Four Problems. One Root Cause.

[ADVANCE SLIDE]

> "Here's what discovery told us. Engineering: 15-year-old checkout codebase, 3-month onboarding, test coverage gaps, tribal knowledge locked in senior heads. IT: that prior rollout -- no governance, no visibility, no way to know what was happening.

> Four problems, one root cause: invisibility. The codebase is invisible to new developers. Usage is invisible to leadership. Risk is invisible to compliance."

---

## [0:30-0:50] Slide 3: Agentic. Sandboxed. Every Action Audited.

[ADVANCE SLIDE]

> "Codex is not autocomplete — it's an agentic system. It reads your entire codebase, plans an approach, executes in a kernel-level sandbox, and verifies the result. Source code stays on the developer's machine. Only relevant context reaches the API.

> But here's what matters for this deployment: every interaction generates structured metadata. What was asked, what was read, what changed, who approved it. That metadata is the raw material for governance AND enablement. The tool doesn't just write code — it generates the data that makes engineering visible."

---

## [0:50-1:10] Slide 4: Your Standards Become the AI's Operating Rules

[ADVANCE SLIDE]

> "The harness is how you make visibility operational. Three components.

> AGENTS.md — per-repo rules, version-controlled, team-owned. requirements.toml — enterprise policies, IT-managed, centrally enforced. Approval modes — graduated trust from 'ask every time' to autonomous with test gates.

> OpenAI built a million lines of production code using this exact system. Every action governed, logged, attributable."

---

## [1:10-1:40] Slide 5: Start Read-Only. Scale on Evidence.

[ADVANCE SLIDE]

> "Three workflows, phased. Start with Code Understanding — read-only, zero generation risk, directly addresses the biggest pain. At Cisco, Codex saved 1,500 engineering hours per month. DX Research shows AI-assisted onboarding cuts time-to-productivity by 46% — from 91 days to 49.

> [PAUSE — let the numbers land]

> We highlight Code Understanding because it's the visibility thesis in action. A developer asks Codex to explain a module — that query becomes a visible artifact. For the first time, leadership can see which parts of the codebase developers struggle with, how long onboarding really takes, where the knowledge gaps live. Read-only for developers. High-signal for leadership."

---

## [1:40-2:00] Slide 6: Same Data. Two Audiences.

[ADVANCE SLIDE]

> "The visibility layer turns Codex metadata into two views. Engineering sees which modules developers explore, where they're getting stuck. Leadership sees usage by team, risk distribution, compliance status.

> Same data, two audiences, one system. Not 'trust us, developers are being careful.' Observable evidence that governance is working."

---

## [2:00-3:00] Demo Move 1: Code Understanding on RetailPOS

[SWITCH TO CODEX SCREEN]

> "Let me show you what this looks like. I've loaded RetailPOS -- an open-source Java retail peripheral platform. Think of this as a stand-in for your checkout infrastructure."

[SUBMIT PROMPT: "Explain the device management architecture in this codebase. What are the main components, how do they interact, and what would a new developer need to understand first?"]

> "I'm asking Codex to explain the architecture to a new developer. This is the Code Understanding workflow -- entirely read-only."

[WAIT FOR RESPONSE -- narrate while waiting if needed: "Codex is reading the Java source, tracing the call graph, building a dependency map..."]

> "Look at what we get. A clear explanation of what this module does, its upstream and downstream dependencies, the data flow. A developer who's never seen this codebase has a working mental model in 30 seconds. That's work that would take 2 to 3 hours of code archaeology.

> And notice -- nothing was changed. Read-only. But the metadata from this interaction is now visible: which module was queried, how many files were read, the dependency map itself. That's the visibility thesis. The act of understanding the codebase generates governance data."

---

## [3:00-4:00] Demo Move 2: Codex Self-Awareness -- Limitations

[SUBMIT PROMPT: "What are you likely to get wrong about this codebase? What should I verify before trusting your analysis?"]

[PAUSE -- let this land]

> "This is a question most people don't think to ask an AI coding tool. Watch what Codex says."

[WAIT FOR RESPONSE]

> "Codex identifies its own blind spots -- runtime behavior it can't see from static analysis, configuration files that change behavior, integration patterns that depend on external systems, implicit conventions that aren't in the code.

> This is what responsible enablement looks like. We're not telling developers 'Codex is always right.' We're teaching them to ask: 'Where should I not trust this?' That question -- and the answer -- is itself a governance artifact. It's visible, it's logged, it's part of the operating model."

---

## [4:00-4:45] Demo Move 3: Dashboard Reveal

[SWITCH TO STREAMLIT DASHBOARD]

> "Now let me show you where all of this goes."

[SHOW BUBBLE CHART — workflow distribution by team]

> "This is a visibility dashboard we built in 48 hours — using Codex. Every Codex interaction from a two-week pilot, visualized. Teams, workflows, risk levels — at a glance."

[RUN PRE-SCRIPTED CHAT QUERY: "Show me security-related queries this week"]

> "Natural language queries against the usage data. The VP asks 'show me security queries this week' — instant answer. The Director asks 'which team has highest adoption' — same data, different question, both answered."

> "We built this in 48 hours. The tool built its own visibility layer."

---

## [4:45-5:00] Closing

> "Start visible. Stay visible. Scale on evidence. Next step: select the pilot team. We can have them running in two weeks. Thank you."

---

## Timing Notes

| Segment | Target | Hard Limit |
|---|---|---|
| Opening (hook first) | 0:12 | 0:15 |
| Slide 2: Four problems, one root cause | 0:18 | 0:22 |
| Slide 3: Agentic, sandboxed, audited | 0:20 | 0:25 |
| Slide 4: Your standards = AI's rules | 0:20 | 0:25 |
| Slide 5: Start read-only, scale on evidence | 0:30 | 0:35 |
| Slide 6: Same data, two audiences | 0:20 | 0:25 |
| Demo Move 1: Code understanding | 1:00 | 1:10 |
| Demo Move 2: Limitations | 1:00 | 1:10 |
| Demo Move 3: Dashboard | 0:45 | 0:55 |
| Closing (with next step) | 0:15 | 0:18 |
| **TOTAL** | **5:00** | **5:30** |

## Contingency Instructions

- **If running long at 2:00**: compress Slide 6 to one sentence: "Same data, two audiences — I'll show you the live version in a moment."
- **If Codex response is slow (>20s)**: narrate while waiting. "Response times vary with codebase size. The structured metadata is generated regardless."
- **If Codex gives a weak response on Move 2 (limitations)**: pivot to the point. "Even a partial answer demonstrates the principle — we're teaching developers to interrogate the tool, not just consume its output."
- **If dashboard doesn't load**: describe it verbally. "The dashboard visualizes every Codex interaction by team, workflow, risk level, and module. It turns usage data into governance evidence."
- **If running long at 4:00**: compress Move 3 to 20 seconds — show the bubble chart, skip the chat query, close.
- **If running short**: expand Move 1 narration. Point to specific modules and explain what the VP would see vs. what the developer would see. Or add: "Phase two adds Test Generation — measurable coverage lift. Phase three, Docs and Refactoring — by then teams have trust and muscle memory."

## Key Lines — Must Hit

These six lines carry the thesis. If you forget everything else, land these:

1. "The last AI coding tool rollout was killed in weeks." (hook — first 5 seconds)
2. "Four problems, one root cause: invisibility." (thesis — slide 2)
3. "Cisco: 1,500 engineering hours per month. Onboarding: 91 days to 49." (credibility — slide 5)
4. "This is what responsible usage looks like." (Move 2 — the differentiator)
5. "We built this in 48 hours. The tool built its own visibility layer." (Move 3 — payoff)
6. "Start visible. Stay visible. Scale on evidence." (close — last line)

## Energy Notes

- Opening: confident, direct. No warmup patter. The hook is the first thing they hear.
- Discovery: compressed energy — you're playing back facts, not performing
- "Four problems, one root cause" — slow down, this is the thesis moment
- Numbers (Cisco, onboarding) — steady, factual. Let the data speak. Don't oversell.
- Demo: teaching energy — you're showing, not selling
- Limitations question: let it breathe. The pause after submitting is powerful.
- Dashboard: pace picks up slightly — this is the payoff
- Closing: downward pressure. Calm authority. "Next step" = forward momentum. End clean.
