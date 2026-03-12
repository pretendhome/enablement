# Speaker Script v2 -- 5-Minute Loom Recording

**Thesis**: Visibility IS governance. Visibility IS enablement. Visibility is the common ground.
**Target**: 5:00 total (slides ~2:00, demo ~3:00)
**Demo repo**: RetailPOS — open-source Java retail peripheral platform
**Recording strategy**: 2-3 full takes at ~5-6 min. Pick the best. Don't chase perfection -- chase clarity.

---

## [0:00-0:10] Opening

> "Hi, I'm [Presenter Name], and I'll be walking you through our Codex enablement plan."

[PAUSE -- let the title slide breathe for one beat]

---

## [0:10-0:30] Slide 2: Discovery Findings --> Visibility Insight

[ADVANCE SLIDE]

> "Here's what came out of discovery at a Fortune 500 retailer with several hundred developers.

> Engineering side: a 15-year-old checkout codebase, 3-month developer onboarding, test coverage gaps, tribal knowledge. IT side: a prior AI tool rollout that ended in a security incident -- source code sent to third-party servers, no audit trail, no usage data, compliance flagged SOX risk, project killed.

> All four problems share one root cause: invisibility. The codebase is invisible to new developers. Usage is invisible to leadership. Risk is invisible to compliance. And the prior tool made all of it worse because it was itself invisible -- no governance data, no audit trail, no way to know what was happening."

---

## [0:30-0:50] Slide 3: How Codex Works, Why It's Different

[ADVANCE SLIDE]

> "Codex is different because of how it works. It's an agentic system -- not autocomplete. It reads your codebase, plans an approach, executes in a kernel-level sandbox, and verifies the result. Seatbelt on macOS, Landlock plus seccomp on Linux. Stronger than Docker. Source code stays on the developer's machine. Only relevant context reaches the API.

> But here's what matters for this company: Codex doesn't just write code -- it generates the data that makes engineering visible. Every interaction produces structured metadata: what was asked, what was read, what was changed, who approved it, when. That metadata is the raw material for governance AND enablement."

---

## [0:50-1:10] Slide 4: The Harness (Governance Architecture)

[ADVANCE SLIDE]

> "The harness makes visibility operational. Three components.

> AGENTS.md -- per-repo config, version-controlled, teams own their policies. requirements.toml -- cloud-managed enterprise policies set by IT, overrides local configs when stricter. Approval modes -- graduated trust from on-request to autonomous.

> Together, these three components create a system where every Codex action is governed, logged, and attributable. Governance isn't a layer on top -- it's the operating architecture."

---

## [1:10-1:40] Slide 5: Three Workflows, Phased Rollout

[ADVANCE SLIDE]

> "Three workflows, phased. We start with Code Understanding -- read-only, zero generation risk, and it directly addresses the biggest pain: nobody fully understands the legacy codebase.

> Phase two adds Test Generation -- measurable coverage lift. Phase three, Docs and Refactoring -- highest impact, highest review need, but by then teams have trust and muscle memory.

> We highlight Code Understanding because it's the visibility thesis in action. A developer asks Codex to explain a module -- and that question, that answer, those dependency maps become visible artifacts. For the first time, the organization can see which parts of the codebase developers are struggling with, how long onboarding really takes, where the knowledge gaps live. Read-only for developers. High-signal for leadership."

---

## [1:40-2:00] Slide 6: The Visibility Layer (Dashboard Concept)

[ADVANCE SLIDE]

> "This is the visibility layer -- a dashboard that turns Codex metadata into two views.

> The engineering view: which modules are being explored, what questions developers are asking, where they're getting stuck. The executive view: usage by team, risk distribution, compliance status, harness policy adherence.

> Same data, two audiences, one system. This is what responsible usage looks like. Not 'trust us, developers are being careful.' Observable evidence that governance is working."

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

## [4:00-4:50] Demo Move 3: Dashboard Reveal

[SWITCH TO STREAMLIT DASHBOARD]

> "Now let me show you where all of this goes."

[SHOW BUBBLE CHART -- workflow distribution by team]

> "This is a visibility dashboard we built in 48 hours using Codex. Every dot is a Codex interaction from a simulated two-week pilot. Bubble size is session duration. Color is workflow type. You can see at a glance: which teams are using it, what they're asking, where the activity clusters.

[RUN PRE-SCRIPTED CHAT QUERY: "Show me security-related queries this week"]

> "Natural language queries against the usage data. The VP of IT can ask 'show me security queries this week' and see the answer instantly. The Director of Engineering can ask 'which team is using Codex most?' Same data, different questions, both answered."

[BRIEFLY SHOW: Codex generating a visualization component -- ~10 seconds]

> "And this dashboard itself was built with Codex -- that's the tool building its own visibility layer."

---

## [4:50-5:00] Closing

> "Start visible, stay visible, scale on evidence. Codex is the tool. Visibility is the operating model. Thank you."

---

## Timing Notes

| Segment | Target | Hard Limit |
|---|---|---|
| Opening | 0:10 | 0:12 |
| Slide 2: Discovery + visibility insight | 0:20 | 0:25 |
| Slide 3: How Codex works | 0:20 | 0:25 |
| Slide 4: The harness | 0:20 | 0:25 |
| Slide 5: Workflows + highlighted | 0:30 | 0:35 |
| Slide 6: Visibility layer | 0:20 | 0:25 |
| Demo Move 1: Code understanding | 1:00 | 1:10 |
| Demo Move 2: Limitations | 1:00 | 1:10 |
| Demo Move 3: Dashboard | 0:50 | 1:00 |
| Closing | 0:10 | 0:12 |
| **TOTAL** | **5:00** | **5:30** |

## Contingency Instructions

- **If running long at 2:00**: compress Slide 6 (visibility layer) to one sentence. The dashboard demo will show it live.
- **If Codex response is slow (>20s)**: narrate while waiting. "In production, response times are typically 5-15 seconds depending on codebase size. The structured metadata is generated regardless of response time."
- **If Codex gives a weak response on Move 2 (limitations)**: pivot to the point. "Even a partial answer here demonstrates the principle -- we're teaching developers to interrogate the tool, not just consume its output."
- **If dashboard doesn't load**: describe it verbally. "The dashboard we built visualizes every Codex interaction by team, workflow, risk level, and module. It turns usage data into governance evidence."
- **If running long at 4:00**: cut the Codex-building-dashboard component (last 10s of Move 3). Go straight to closing.
- **If running short**: expand the dependency map narration in Move 1. Point to specific modules and explain what the VP would see vs. what the developer would see.

## Key Lines -- Must Hit

These five lines carry the thesis. If you forget everything else, land these:

1. "All four problems share one root cause: invisibility."
2. "Codex doesn't just write code -- it generates the data that makes engineering visible."
3. "This is what responsible usage looks like."
4. "We built this dashboard in 48 hours using Codex."
5. "Start visible, stay visible, scale on evidence."

## Energy Notes

- Opening: calm, professional, no warmup patter
- Discovery: slightly compressed energy -- you're playing back facts, not performing
- "All four problems share one root cause" -- slow down, this is the thesis moment
- Demo: teaching energy -- you're showing, not selling
- Limitations question: let it breathe. The pause after submitting is powerful.
- Dashboard: pace picks up slightly -- this is the payoff
- Closing: downward pressure. Calm authority. End clean.
