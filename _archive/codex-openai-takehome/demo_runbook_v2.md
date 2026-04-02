# Demo Runbook v2 — Governed Adoption Thesis

**Demo duration**: ~2.5 minutes (within the 18-min presentation or 5-min Loom)
**Governing thesis**: Start with a workflow developers value immediately and leadership can safely approve.
**Demo repo**: JavaPOS (javapos-contracts) — open-source Java point-of-sale device API

---

## Pre-Demo Setup

### Browser Tabs (left to right)

| Tab | URL/Location | Purpose |
|---|---|---|
| 1 | Codex desktop app | Demo repo loaded — Moves 1 and 2 |
| 2 | Screenshot backup folder | Fallback if Codex output is weak |

### Environment Checklist

- [ ] Demo repo cloned locally
- [ ] Demo repo loaded in Codex desktop app
- [ ] Browser zoom at 130%
- [ ] All other tabs closed — no bookmarks bar, no extensions visible
- [ ] Notifications disabled (Slack, email, system)
- [ ] Prompts copied to clipboard manager (or open in a text file off-screen)
- [ ] Screenshots of expected outputs saved as backup

### Demo Repo Target Files

Identify these before recording — they map to the retail peripheral narrative:

| File | Why |
|---|---|
| `src/main/java/com/retailco/devicemanager/` | Core device management — peripheral integration logic |
| Any `*Controller.java` | Entry points — easy to explain dependency chains |
| Any `*Service.java` | Business logic layer — good for "what calls what" analysis |
| Configuration/properties files | Show how the system is wired together |

**Pre-flight**: Run the Move 1 prompt against the demo repo at least twice before recording. Note which files Codex references. Use those in your narration.

---

## Move 1: Code Understanding (~70 seconds)

**Platform**: Codex desktop app

### Setup
- Codex desktop app tab is active, demo repo loaded
- Cursor in the prompt field

### Prompt (copy-paste)

```text
Explain the device management architecture in this codebase.
What are the main components, how do they interact, and what
would a new developer need to understand first?
```

### Expected Output
Codex should identify:
- The device manager service layer
- Controller/service/repository patterns
- How peripheral devices (scanners, printers, card readers) are abstracted
- Key configuration and dependency injection patterns

### Narration (speak while Codex generates or after)

> "This is Code Understanding — the workflow I would teach first. I've loaded JavaPOS, an open-source Java point-of-sale device API. Think of this as a stand-in for your checkout systems.
>
> I asked Codex to explain the architecture to a new developer. Watch what comes back."

**[WAIT — if >10s, narrate:]**

> "Codex is reading the codebase, tracing the structure, mapping the dependencies."

**[WHEN OUTPUT APPEARS:]**

> "This is work that would normally require a lot of code archaeology. Codex did it in seconds. And critically — this was entirely read-only. Nothing in the codebase changed."

### VP Callout

> "Read-only. Nothing changed. This is where I start every deployment."

### Backup Prompt (if primary gives weak output)

```text
Trace the request flow when a barcode scanner reads a UPC code.
What classes are involved and in what order?
```

---

## Move 2: Bounded Change Planning (~70 seconds)

**Platform**: Codex desktop app (same session)

### Setup
- Stay in Codex desktop app, same repo context
- Type or paste the next prompt

### Prompt (copy-paste)

```text
Based on that architecture, propose a small low-risk refactor to improve
maintainability. Do not write code yet. Give me the files you would inspect,
the tests you would run, and the risks I should review before approving any change.
```

### Expected Output Themes
Codex should produce some combination of:
- A bounded refactor candidate
- The files or modules it would inspect first
- The tests or validations it would run
- Risks, dependencies, or owners to involve before approval

### Narration

> "Now I move from understanding to a bounded change plan. I'm still not asking Codex to write code. I'm asking it to scope the work and tell me what needs review first."

**[WAIT FOR RESPONSE]**

> "This is the moment that matters. Codex is helping the developer turn a vague request into a reviewable plan: what to inspect, what might break, and what evidence to gather before anyone approves a change.
>
> This is what responsible AI usage looks like. The tool accelerates planning, but the developer still owns judgment, review, and merge."

### VP Callout

> "This is where enablement and governance meet. The same workflow that helps the developer move faster also gives the organization a standard for safe usage."

### Backup Prompt (if primary gives generic output)

```text
What could break if I refactor the device management layer?
List the likely dependencies, tests, and approvals I should check first.
```

---

## Close the Loop (~20-30 seconds)

### Narration

> "In the pilot, those interactions become the evidence base for rollout. You can see which workflows teams are actually using, where they need more guidance, and whether it's safe to expand from read-only understanding into test generation and refactoring."

---

## Contingency Table

| Problem | Action |
|---|---|
| Codex slow (>15s) | Narrate while waiting: "Response times vary with codebase complexity. In practice, 5-15 seconds for most queries." |
| Codex gives bad output | "And this is exactly why we have the review expectation. The tool accelerates — it doesn't replace human judgment." |
| Codex gives a generic plan | Ask the backup prompt and narrate the workflow standard rather than the exact output |
| Internet goes down | Switch to Codex CLI (have terminal ready with demo repo loaded). |
| Demo repo gives unexpected structure | Use backup prompts which are more general. The narrative works with any Java codebase. |
| Brain freeze | Speaker script printout is off-camera. Glance at it. |
| Running over time | Cut the close-the-loop section to one sentence and move to the closing line. |

---

## Timing Checkpoints

### Within the 20-min Part 2 Presentation

| Checkpoint | Clock Time | Action |
|---|---|---|
| "Let me show you what this looks like" | 16:00 | Transition to demo — switch to Codex tab |
| Move 1 complete | 17:05 | Code understanding output visible, "read-only" callout delivered |
| Move 2 complete | 18:15 | Bounded plan visible, review standard delivered |
| Close the loop | 18:45 | Pilot evidence point delivered |
| Close | 19:00 | "Start with code understanding. Put the harness in place early." |

### Within the 5-min Loom Recording

| Checkpoint | Clock Time | Action |
|---|---|---|
| Transition to demo | 2:00 | Switch to Codex desktop app |
| Move 1 complete | 3:05 | Code understanding output visible |
| Move 2 complete | 4:15 | Bounded planning moment landed |
| Close the loop | 4:45 | Pilot evidence point delivered |
| Close | 5:00 | Thesis restatement, "thank you" |

---

## Rehearsal Protocol

### Run 1: Technical Check
- Execute both prompts against the demo repo
- Time each response
- Note exact files Codex references (use in narration)
- Record response times

### Run 2: Narration Pass
- Full run with spoken narration
- Practice transitions between slide and Codex view
- Time the full demo
- **Target: under 2:30** (leaves buffer for slow Codex responses during recording)
- Hard limit: 2:45

### Run 3: Failure Mode Rehearsal
- Deliberately slow-walk Move 1 (practice "narrate while waiting")
- Use backup prompts for Moves 1 and 2
