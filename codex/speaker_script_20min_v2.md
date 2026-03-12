# Speaker Script v2 -- 20-Minute Part 2 Presentation

**Context**: 30-minute live session with VP Engineering role-player. Target 18-19 min for presentation + demo, leaving 11-12 min for Q&A.
**Audience**: VP Engineering who is skeptical but open. Has been burned by prior AI tool deployments.
**Thesis**: Visibility IS governance. Visibility IS enablement. Visibility is the common ground.
**Demo repo**: RetailPOS — open-source Java retail peripheral platform
**Dashboard**: Pre-built Streamlit visibility dashboard

---

## [0:00-1:00] Opening + Framing

> "Thank you for the time. Before I get into the deck, I want to name the tension directly.

> Your engineering teams need velocity. You have an aging codebase, onboarding takes months, feature delivery is slowing. But the last AI tool rollout didn't just fail -- it created a trust deficit. Governance was invisible. Usage was invisible. Risk was invisible. And when things went wrong, nobody could see what had happened or why.

> So the question isn't 'should we use AI coding tools?' You already tried that. The question is: 'How do we deploy one so that everything it does is visible -- visible to developers who need to learn from it, visible to leadership who need to govern it, visible to compliance who need to audit it?'

> [PAUSE]

> That's the thesis for this session. Visibility IS governance. Visibility IS enablement. They're not competing priorities -- they're the same system. I'll show you exactly what I mean."

[ADVANCE SLIDE]

---

## [1:00-3:00] Slide 2: Four Problems. One Root Cause.

> "Let me play back what we heard in discovery, and then I'll reframe it.

> From the engineering side: you have checkout and inventory systems that are 15 years old. New developers take three or more months to become productive because the codebase is complex and underdocumented. Test coverage has gaps, so teams are afraid to refactor -- they can't predict what will break. Documentation exists in people's heads, not in the code. Knowledge leaves when people leave.

> From the IT side: the previous AI tool deployment -- likely an autocomplete tool -- resulted in source code being sent to third-party servers without the security team's knowledge. There was no audit trail, no usage visibility. The compliance team flagged SOX risk, and the project was shut down. The damage wasn't just the tool -- it was trust. Developers who liked the tool felt punished. IT felt validated that AI is risky. Both sides are right, and both sides are stuck.

> [PAUSE]

> Here's the reframe I want to offer. All four problems share one root cause: invisibility.

> The codebase is invisible to new developers -- that's why onboarding takes three months. Usage patterns are invisible to leadership -- that's why the prior tool had no governance. Risk is invisible to compliance -- that's why SOX was flagged. And the prior tool itself was invisible -- no structured data about what it was doing, no way for anyone to see whether it was helping or hurting.

> The solution isn't just a better tool. It's a tool that makes engineering visible.

> [PAUSE -- let the VP respond if they want to]

> Does that match what you're seeing?"

[ADVANCE SLIDE]

---

## [3:00-5:00] Slide 3: Agentic. Sandboxed. Every Action Audited.

> "Let me show you how Codex works, because the architecture itself is the first layer of visibility.

> Codex is an agentic system -- fundamentally different from autocomplete tools like Copilot. The CLI is open-source, written in Rust. It runs locally on the developer's machine. The agent loop is: read the code, plan an approach, make edits, execute them in a sandbox, verify the result. This is not line-by-line prediction. It's a reasoning system that reads your codebase, thinks about it, and acts.

> All of this happens inside a kernel-level sandbox -- Seatbelt on macOS, Landlock plus seccomp on Linux. This is stronger isolation than Docker. Network access is blocked by default. File system access is restricted to the project directory. The sandbox is kernel-enforced, not policy-based -- there's nothing the agent can do to escape it.

> When the agent needs model inference, it sends only relevant context to the OpenAI API -- not the entire codebase. Source code stays on the machine. On the cloud side, you get the enterprise control plane: SAML SSO tied to your identity provider, SCIM for auto-provisioning, role-based access control, and a Compliance API that logs every Codex action.

> For the VP: the open-source CLI is auditable. Your security team can read every line of the agent code. No training on your data by default -- that's opt-in, and enterprise customers almost always leave it off.

> [PAUSE]

> But here's what matters most for your situation. Codex doesn't just write code -- it generates the data that makes engineering visible. Every interaction produces structured metadata: what was asked, what code was read, what was changed, who approved it, when. Every file touched, every dependency traced, every approval decision -- all logged, all queryable, all auditable.

> That metadata is the raw material for both governance and enablement. Same data, two purposes. That's the architectural foundation of everything I'm about to show you."

[ADVANCE SLIDE]

---

## [5:00-7:00] Slide 4: Your Standards Become the AI's Operating Rules

> "The harness is what makes visibility operational. Three components.

> First: AGENTS.md. This is a per-repository configuration file that defines what Codex can and cannot do in that repo. It's version-controlled alongside the code. Engineering teams own their own policies. The hierarchy cascades: org-level, repo-level, folder-level. If you say 'do not modify files in /payments,' Codex obeys. If you say 'always run tests before committing,' Codex follows that instruction.

> What makes this a visibility tool, not just a policy tool: every AGENTS.md instruction generates compliance data. When Codex obeys a constraint, that's a logged event. When a developer works within bounds, that's measurable. You can see, team by team, which policies are active, which are being tested, and which need revision.

> [ADVANCE SLIDE]

> Second: requirements.toml. These are cloud-managed enterprise policies set by IT and Security. They override AGENTS.md when they're stricter. This is your central governance lever. Block direct database writes across the org. Require review for security-critical paths. Define which file patterns are off-limits for generation.

> The visibility angle: requirements.toml violations don't silently fail -- they produce audit events. If a developer asks Codex to do something that policy blocks, you have a record of the attempt, the policy that blocked it, and the outcome. That's not just governance -- it's a signal about where your developers are pushing boundaries and where your policies need to evolve.

> Third: approval modes. These create graduated trust. Start with 'on-request' -- Codex asks the developer before every action. Move to 'untrusted' -- safe operations auto-approve, risky ones still ask. The full-auto mode runs within the sandbox but with maximum autonomy.

> Every approval decision is a data point. On-request mode generates the richest metadata because every action has an explicit human decision attached. As you graduate to less restrictive modes, you're doing it based on the evidence from the previous mode. You can see exactly what changed when you loosened the controls.

> [PAUSE]

> The insight is: this harness is how OpenAI built a million lines of their own production code in five months. It's not theoretical. It's an operational system that was tested at scale -- and the reason it works at scale is that the governance data is built into every operation, not bolted on after the fact."

[ADVANCE SLIDE]

---

## [7:00-10:00] Slide 5: Start Read-Only. Scale on Evidence.

> "Now let's talk about what developers actually do with Codex. Three workflows, phased.

> Workflow one: Code Understanding. Read-only. Developers ask Codex to explain code, map dependencies, trace call chains, analyze impact.

> Workflow two: Test Generation. Measurable output — you can track coverage percentage before and after.

> Workflow three: Documentation and Refactoring. Highest impact, highest review need.

> Before I go deeper, let me ground this in data. At Cisco, Codex saved 1,500 engineering hours per month. DX Research across six multinationals shows AI-assisted onboarding cuts time-to-productivity by 46% — from 91 days to the 10th pull request down to 49. OpenAI's own engineering team reports 92% daily usage and 3.5 pull requests per engineer per day. These aren't projections. These are measured outcomes from production deployments.

> [ADVANCE SLIDE]

> We start with Code Understanding, and I want to spend time on why, because the reasoning goes deeper than 'it's the safest.'

> Reason one: it directly addresses your biggest pain point. You told me nobody fully understands the 15-year-old checkout code. Code Understanding is the tool that fixes that -- not by documenting everything once, but by giving every developer an on-demand way to understand any module they touch.

> Reason two: it's read-only. Codex reads and explains. It doesn't generate code that goes into production. For the VP, this means zero generation risk on day one. No code review debates about AI-generated code. No compliance questions about who authored what. The tool is helping developers think, not write.

> Reason three: it's the visibility thesis in action. When a developer asks 'explain this module and map its dependencies,' three things happen simultaneously. The developer gets a clear mental model. The organization gets data about which modules are being explored and where knowledge gaps cluster. And governance gets a logged, auditable record of Codex operating within its read-only boundaries. Developer value, organizational visibility, and compliance evidence -- from the same interaction.

> Reason four: it's the fastest path to the aha moment. When a developer asks 'explain this function and its dependencies' and gets a clear answer in 30 seconds instead of spending 3 hours reading code -- that's when adoption happens. Not because you mandated it, but because it's genuinely useful.

> Reason five: it's the gateway. Once developers trust Codex for understanding, the transition to test generation is natural. And once they trust it for testing, refactoring follows. The trust chain is: understand, test, refactor. You don't skip steps.
>
> And to support that chain: weekly office hours during the pilot, a shared prompt library in Slack, and a dedicated channel for questions. Enablement doesn't end at deployment — it's an ongoing cadence that evolves with the team.

> Let me walk through three interactions from the highlighted workflow.

> 'Explain this checkout function and map its dependencies.' Developer gets a dependency map. Work that previously took hours.

> 'What would break if I changed the tax calculation logic?' Impact analysis before any change. Prevents cascade failures.

> 'Summarize how the inventory sync pipeline works end-to-end.' New team member onboards in hours instead of weeks.

> [PAUSE]

> Important caveat. Codex is not a replacement for code review, and it's not infallible. It can hallucinate -- it may infer intent that isn't in the code. It can miss runtime behavior that only appears in production. Developers must verify generated explanations against the actual code. For any generated code -- tests, refactoring -- standard code review applies. Security-critical paths get mandatory human review, no exceptions.

> But here's the visibility angle on limitations: when a developer asks Codex 'what are you likely to get wrong about this codebase?' -- and Codex identifies its own blind spots -- that exchange is itself a governance artifact. It's logged, it's visible, and it demonstrates that we're teaching developers to interrogate the tool, not just consume its output. Responsible enablement isn't hiding limitations. It's making them visible."

[ADVANCE SLIDE]

---

## [10:00-12:00] Slide 6: Same Data. Two Audiences.

> "Now I want to show you where all of this metadata goes. This is the visibility layer -- a dashboard that turns Codex interaction data into actionable views for two audiences.

> The engineering view shows: which modules are being explored, what questions developers are asking, where they're getting stuck, which teams have the highest repeat usage, and what the workflow distribution looks like over time. For the Director of Engineering, this is an onboarding intelligence system. For the first time, you can see -- in real data, not in surveys -- where your codebase is hardest to understand, which teams are ramping fastest, and where to invest in documentation or refactoring.

> The executive view shows: usage by team and by day, risk level distribution across all interactions, compliance status -- which policies are active, which are triggering blocks, which approval events are pending review. Harness policy adherence over time. For the VP of IT, this is a governance console. You're not asking developers to self-report. You're not waiting for an incident to discover a problem. You have continuous, real-time visibility into what the tool is doing and whether it's operating within bounds.

> [PAUSE]

> Same data, two audiences, one system. That's the visibility thesis in practice.

> The key insight is that this dashboard doesn't require extra work from developers. They're not filling out forms or writing usage reports. They're doing their jobs -- asking Codex to explain code, map dependencies, generate tests. The metadata is a byproduct of productive work. Governance is a side effect of enablement.

> And I want to name one more thing: this dashboard was built using Codex. We built a working visibility prototype in 48 hours. That's not a marketing claim -- it's a demonstration of what the tool can do when you apply it to its own deployment infrastructure. The tool builds the visibility layer for the tool."

[ADVANCE SLIDE]

---

## [12:00-14:00] VP Controls -- Four Control Surfaces

> "For the VP specifically -- four control surfaces that address every concern from the prior deployment.

> Access Control. Codex ties into your existing identity provider via SAML SSO and SCIM. You don't manage a separate user directory. When someone is offboarded, Codex access is deactivated automatically. You can scope access by team, by role, by project. The visibility angle: access events are logged. You can see who has access, who's using it, and who isn't.

> Policy Management. requirements.toml gives you centralized control. AGENTS.md gives teams local control. The stricter policy always wins. What the prior tool didn't have: a policy layer at all. Codex has two -- one owned by IT, one owned by engineering, with a clear precedence model. And every policy interaction generates data.

> Audit and Compliance. The Compliance API logs every Codex action. SOX-ready audit trail. Usage analytics show who's generating what code, when, and what review status it has. Your security team can export and review. For SOX: you can prove, at any point in time, what policies were in effect and what the tool was allowed to do. The audit trail from Codex is actually more complete than what you have for manually written code -- because every interaction is instrumented by default.

> Graduated Trust. You start restrictive and expand based on evidence. On-request mode for the pilot. Untrusted mode for teams that earn it. Team-by-team decisions, not org-wide. And if something goes wrong, you can tighten any team's approval mode instantly. Rollback is a config change, not a project shutdown.

> [PAUSE]

> Here's what I want to make explicit: the prior tool had no governance architecture. It was invisible from the day it was deployed until the day it was shut down. Every one of these four control surfaces produces visibility data. You're not governing blind. You're governing with evidence.

> The net: you never lose control. And the proof that you're in control is not a policy document. It's live data."

[ADVANCE SLIDE]

---

## [14:00-16:00] Measurement -- Three Levels

> "Three levels of measurement, mapped to the three phases of rollout.

> Level one -- Usage. During the pilot, we're answering: are developers actually using it? Daily active users, sessions per week, workflow distribution, repeat usage rate. But with the visibility layer, we go deeper than simple adoption metrics. We can see which modules are generating the most questions, which teams are clustering around which workflows, and whether the usage pattern matches what we predicted. If developers try it once and don't come back, that's a signal. If they use Code Understanding every day but never ask about specific directories, that's a different signal. The data tells us not just whether they're using it, but how they're using it.

> Level two -- Behavior Shift. As we expand to three teams, we measure: are workflows actually changing? Is onboarding time dropping? Is code review turnaround improving? Is test coverage increasing? These are the metrics that prove Codex is doing what we said it would do. The visibility layer makes this measurable because we have before-and-after data for every team, every module, every workflow.

> Level three -- Business Outcomes. At scale, we measure: is it moving the needle on things the business cares about? Feature delivery velocity, incident rate from code changes, developer satisfaction. These are the metrics that justify the investment.

> [PAUSE]

> Now, the critical point. The harness evolves based on this evidence. Not on the calendar. Not on someone's opinion. On data.

> If a team's visibility data shows they're using Code Understanding responsibly, their compliance events are clean, and their code review quality is maintained -- they graduate to Test Generation. If another team's data shows risk -- unusual query patterns, policy blocks, pending review backlog -- you keep them in on-request mode longer. The evidence decides.

> This is what I mean when I say visibility IS governance. You're not governing by policy alone. You're governing by observable evidence of how the tool is being used. The harness is a living system. Every expansion is justified. Every tightening is data-driven. Every harness revision is versioned and attributable.

> Evidence-based reference points from other enterprises: Cisco saw 50% reduction in code review time. Duolingo saw 67% drop in review turnaround. 1.6 million weekly active users across the platform. 90% of the Fortune 100 are already on Codex. The point isn't to copy their numbers -- it's to define your success criteria and measure against them with the visibility system from day one."

[ADVANCE SLIDE]

---

## [16:00-17:00] Next Steps

> "Three concrete next steps.

> One: select the pilot team. My recommendation is the team most burdened by legacy code -- they have the most to gain, and their success becomes the internal proof point. Twenty to thirty developers. Code Understanding only. On-request approval mode. Full visibility dashboard from day one.

> Two: IT/Security workshop, day one, not day thirty. This is where we configure requirements.toml together, integrate SSO, set up the Compliance API, and define data classification policies. Security is a partner in the deployment, not a gate at the end. And critically -- this workshop produces the first governance artifacts before any developer touches the tool.

> Three: define pass/fail metrics in writing before the pilot starts. Example: 'Reduce new developer onboarding time from 3 months to 6 weeks.' 'Achieve 70% weekly retention among pilot users.' 'Zero unreviewed code generation events.' We agree on what success looks like, and then we measure it with the visibility layer.

> If we hit those metrics, evidence drives the expansion conversation. If we don't, you have a fair, data-driven decision. Either way, you're not making a renewal decision on vibes. You're making it on visible evidence."

---

## [17:00-18:30] Live Demo -- Three Moves

> "Let me show you what this looks like in practice."

[SWITCH TO CODEX SCREEN]

> "I've loaded RetailPOS -- an open-source Java retail peripheral platform. Think of this as a stand-in for your checkout infrastructure. Real Java, real retail domain, real complexity."

### Demo Move 1: Code Understanding (~60s)

[SUBMIT PROMPT: "Explain the device management architecture in this codebase. What are the main components, how do they interact, and what would a new developer need to understand first?"]

> "I'm asking Codex to explain the architecture to a new developer. This is the Code Understanding workflow -- entirely read-only."

[WAIT FOR RESPONSE -- narrate while waiting: "Codex is reading the Java source files, tracing the call graph, building a structured dependency map..."]

> "Look at what we get. A clear explanation of the module's purpose, its upstream and downstream dependencies, the data flow. A developer who's never seen this codebase has a working mental model in under a minute.

> But notice the metadata this interaction generates: the module queried, the number of files read, the dependency map itself, the timestamp, the user. All of that is now visible in the governance layer. One interaction. Developer value and governance data simultaneously."

### Demo Move 2: Codex Limitations -- Self-Awareness (~60s)

[SUBMIT PROMPT: "What are you likely to get wrong about this codebase? What should I verify before trusting your analysis?"]

> "This is a question I teach every developer to ask. Watch what Codex returns."

[WAIT FOR RESPONSE]

> "Codex identifies its own blind spots -- runtime behavior it can't infer from static code, configuration-driven logic, integration patterns with external systems, implicit conventions.

> This is responsible enablement. We're not selling infallibility. We're teaching developers to ask 'where should I not trust this?' And that exchange -- the question, the answer, the acknowledged limitations -- is itself a logged governance artifact. Visible. Auditable. Part of the record.

> When your compliance team asks 'how do we know developers aren't blindly trusting AI output?' -- this is the answer. The operating model includes structured self-interrogation."

### Demo Move 3: Dashboard Reveal + Live Component (~60s)

[SWITCH TO STREAMLIT DASHBOARD]

> "Now let me show you where all of this goes."

[SHOW BUBBLE CHART: workflow distribution by team, bubble size = session duration, color = workflow type]

> "This is a visibility dashboard we built in 48 hours using Codex. Every bubble is a Codex interaction from a simulated two-week pilot. You can see at a glance: workflow distribution, team activity, usage patterns over time."

[RUN PRE-SCRIPTED CHAT QUERY: "Show me security-related queries this week"]

> "Natural language queries against the usage data. The VP of IT can ask 'show me security queries this week' and see the answer instantly. The Director of Engineering can ask 'which team is using Codex most?' Same data. Different questions. Both answered instantly."

[BRIEFLY SHOW: Codex generating a dashboard visualization component -- ~15 seconds]

> "And this dashboard itself was built with Codex. The tool builds the visibility layer for its own deployment. That's not recursive cleverness -- it's a proof point. If Codex can build a governed visibility system in 48 hours, imagine what your developers build in 12 weeks."

---

## [18:30-19:00] Close

> "That's the approach. The prior tool failed because it was invisible. Codex is different not just because it's more capable, but because every interaction generates the data that makes engineering visible.

> Visibility IS governance -- because you can see every action, every policy decision, every approval event. Visibility IS enablement -- because you can see where developers are struggling, where they're succeeding, and what to expand next. Start visible, stay visible, scale on evidence.

> What questions do you have?"

---

## Timing Notes

| Segment | Target | Hard Limit |
|---|---|---|
| Opening + framing | 1:00 | 1:15 |
| Discovery recap | 2:00 | 2:20 |
| Architecture + security | 2:00 | 2:15 |
| Harness -- governance architecture | 2:00 | 2:15 |
| Workflows + highlighted | 3:00 | 3:20 |
| Visibility layer -- dashboard | 2:00 | 2:15 |
| VP controls | 2:00 | 2:15 |
| Measurement | 2:00 | 2:15 |
| Next steps | 1:00 | 1:10 |
| Demo (3 moves) | 1:30 | 2:00 |
| Close | 0:30 | 0:30 |
| **TOTAL** | **19:00** | **20:00** |

## Compression Strategy (if running long)

- **At 7:00 mark, should be entering Harness section.** If behind: compress architecture to security-only highlights, skip the "fundamentally different from autocomplete" comparison.
- **At 10:00 mark, should be entering Visibility Layer.** If behind: cut Code Understanding walkthrough to two examples instead of three. Drop the "reason five: gateway" paragraph.
- **At 14:00 mark, should be entering Measurement.** If behind: compress VP Controls to the four headers plus one sentence each. The dashboard demo will reinforce.
- **At 16:00 mark, should be entering Next Steps.** If behind: compress measurement to Level 1 and Level 3 only, skip Level 2 detail.
- **At 17:00 mark, should be entering Demo.** If behind: cut demo to 2 moves (drop Move 3 dashboard). Describe the dashboard verbally during close.
- **Demo is flexible.** If Q&A is generating better signal, shorten to 2 moves and extend the conversation.

## If VP Asks Questions Mid-Presentation

Answer them. Don't say "I'll get to that later." The best signal you can give is that you can handle interruption without losing the thread. If the question maps to a later slide, answer it briefly and say "I have more detail on this in a few minutes."

## Key Lines -- Must Hit

These carry the thesis. If you have to cut content, protect these lines:

1. "All four problems share one root cause: invisibility."
2. "Codex doesn't just write code -- it generates the data that makes engineering visible."
3. "Visibility IS governance. Visibility IS enablement. They're the same system."
4. "This is what responsible usage looks like."
5. "We built this dashboard in 48 hours using Codex."
6. "Start visible, stay visible, scale on evidence."
7. "The evidence decides, not the calendar."
8. "You're not governing blind. You're governing with evidence."

## Energy and Presence Notes

- **Opening**: calm authority. Name the tension directly. Don't soften it.
- **Discovery**: slightly compressed -- you're playing back facts. The reframe ("all four problems share one root cause") is the energy peak of this section.
- **"Does that match what you're seeing?"**: genuine question. Pause. Make eye contact. If they respond, engage.
- **Architecture**: technical confidence. Don't rush the sandbox explanation -- it matters for trust.
- **Harness**: teach the components. This is where product fluency shows.
- **Highlighted workflow**: this is the heart of the presentation. Slow down on the five reasons. Each one should land.
- **Limitations caveat**: don't hedge. State it plainly. "Codex can hallucinate." Direct language builds more trust than careful language.
- **VP Controls**: address the VP directly. "For you specifically."
- **Dashboard demo**: pace picks up. This is the payoff. Show, don't explain.
- **Close**: downward pressure. Calm. End on the thesis. Don't trail off. Don't add "so yeah" or "that's about it."
- **Q&A**: listen fully before answering. Pause. "That's a fair question." Never bluff.
