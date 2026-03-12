# Demo Runbook v2 — Visibility Thesis

**Demo duration**: ~3 minutes (within the 18-min presentation or 5-min Loom)
**Governing thesis**: "Visibility IS governance. Visibility IS enablement."
**Demo repo**: RetailPOS — open-source Java retail peripheral platform
**Dashboard**: Pre-built Streamlit visibility dashboard

---

## Pre-Demo Setup

### Browser Tabs (left to right)

| Tab | URL/Location | Purpose |
|---|---|---|
| 1 | codex.openai.com | Codex web interface — Moves 1 and 2 |
| 2 | localhost:8501 | Streamlit dashboard — Move 3 |
| 3 | Screenshot backup folder | Fallback if either tab fails |

### Environment Checklist

- [ ] Demo repo cloned locally
- [ ] Demo repo loaded in Codex web (upload or connect)
- [ ] Dashboard running: `cd dashboard && streamlit run app.py`
- [ ] Dashboard showing data from `data/codex_usage.json` (28 engineers, 10 working days)
- [ ] Browser zoom at 130% on both tabs
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

## Move 1: Code Understanding (~60 seconds)

**Platform**: Codex web (codex.openai.com)

### Setup
- Codex web tab is active, demo repo loaded
- Cursor in the prompt field

### Prompt (copy-paste)

```
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

> "This is Code Understanding — our highlighted workflow. I've loaded RetailPOS, an open-source Java retail peripheral platform. Think of this as a stand-in for your checkout systems.
>
> I asked Codex to explain the architecture to a new developer. Watch what comes back."

**[WAIT — if >10s, narrate:]**

> "Codex is reading the codebase, tracing the structure, mapping the dependencies."

**[WHEN OUTPUT APPEARS:]**

> "This is work that would take a new developer days of code archaeology. Codex did it in seconds. And critically — this was entirely read-only. Nothing in the codebase changed. No code was generated. No risk."

### VP Callout

> "Read-only. Nothing changed. This is where we start every deployment."

### Backup Prompt (if primary gives weak output)

```
Trace the request flow when a barcode scanner reads a UPC code.
What classes are involved and in what order?
```

---

## Move 2: Codex Self-Awareness (~60 seconds)

**Platform**: Codex web (same session)

### Setup
- Stay in Codex web, same repo context
- Type or paste the next prompt

### Prompt (copy-paste)

```
What are you likely to get wrong about this codebase?
What should I verify before trusting your analysis?
```

### Expected Output Themes
Codex should acknowledge some combination of:
- It may not understand proprietary conventions or naming patterns
- Runtime behavior vs. static analysis limitations
- Configuration files it can't fully resolve
- Test coverage it hasn't verified
- External dependencies it can't inspect

### Narration

> "Now watch this. I'm asking Codex to tell me what it might get wrong."

**[WAIT FOR RESPONSE]**

> "This is the moment that matters. The tool is telling the developer where NOT to trust it. It's flagging its own limitations — incomplete context, proprietary patterns it hasn't seen, runtime behavior it can't verify.
>
> This is what responsible AI usage looks like. The tool doesn't just give you answers. It teaches you to ask better questions."

### VP Callout

> "The tool teaches responsible usage. That's not a training add-on — it's built into the interaction."

### The Moment

This is the emotional peak of the demo. Pause after the VP callout. Let it land. The audience has just seen an AI tool that is honest about its limitations. That's rare and memorable.

### Backup Prompt (if primary gives generic output)

```
What are your limitations when analyzing Java code with
proprietary retail conventions and custom annotations?
```

---

## Move 3: Dashboard Reveal + Live Component (~60 seconds)

**Platform**: Switch to Streamlit dashboard (Tab 2)

### Setup
- Switch to browser Tab 2 (localhost:8501)
- Dashboard should be loaded and showing the bubble chart / overview

### Step 1: The Reveal (~20s)

> "Now let me show you the other half of the thesis."

**[SWITCH TO DASHBOARD TAB]**

> "This is the visibility layer. Every Codex interaction from the pilot — who used it, what they asked, which workflows, which modules, what risk level — flows through the Compliance API and into this dashboard.
>
> This bubble chart shows usage by team. Size is query volume, color is workflow type. You can see Checkout and Platform are the heaviest users — that tracks, they have the most legacy code burden."

### Step 2: Live Chat Query (~25s)

- Click into the chat/filter input on the dashboard
- Type the following pre-scripted query:

```
Show me security-related queries this week
```

> "I can query the data conversationally. Show me security-related queries this week."

**[WAIT FOR FILTERED RESULT]**

> "Instantly filtered. The VP of IT can ask 'are developers asking about payment code?' and see the answer without filing a ticket. The Director of Engineering can ask 'which team has the highest adoption?' and see it in the same view."

### Step 3: Close the Loop (~15s)

> "This dashboard was built in 48 hours — using Codex. The tool built its own visibility layer.
>
> Same data, two audiences. That's visibility as governance and visibility as enablement. One system."

### VP Callout

> "You're not asking developers to report their usage. The act of using the tool IS the act of generating the data."

### Optional Bonus (only if ahead on time)
Switch back to Codex web tab, type:

```
Generate a React component that displays a pie chart of
Codex workflow distribution from a JSON data source.
```

> "And if you want to extend the dashboard, Codex can generate visualization components too. But that's Phase 2."

---

## Contingency Table

| Problem | Action |
|---|---|
| Codex slow (>15s) | Narrate while waiting: "Response times vary with codebase complexity. In practice, 5-15 seconds for most queries." |
| Codex gives bad output | "And this is exactly why we have the review expectation. The tool accelerates — it doesn't replace human judgment. Let me show you what a good response looks like." [Show screenshot backup] |
| Codex gives generic/shallow output | "Specificity matters in prompting, and that's part of what developers learn in week one. Let me refine this." [Use backup prompt] |
| Dashboard won't load | "Let me show you a screenshot of the dashboard from our last session." [Switch to Tab 3, show saved screenshots] |
| Dashboard chat query returns nothing | Pre-filter to a known category. Say: "Let me broaden the filter." Type a simpler query like "Show all queries from the Checkout team." |
| Internet goes down | Switch to Codex CLI (have terminal ready with demo repo loaded). For dashboard, show screenshots. |
| Demo repo gives unexpected structure | Use backup prompts which are more general. The narrative works with any Java codebase. |
| Brain freeze | Speaker script printout is off-camera. Glance at it. |
| Running over time | Cut Move 3 Step 3 (close the loop) to one sentence. Drop the optional bonus entirely. |

---

## Timing Checkpoints

### Within the 20-min Part 2 Presentation

| Checkpoint | Clock Time | Action |
|---|---|---|
| "Let me show you what this looks like" | 16:00 | Transition to demo — switch to Codex tab |
| Move 1 complete | 17:00 | Code understanding output visible, "read-only" callout delivered |
| Move 2 complete | 18:00 | Self-awareness response visible, "responsible usage" moment landed |
| Move 3 complete | 18:50 | Dashboard shown, live query executed, "same data, two audiences" delivered |
| Close | 19:00 | "Visibility is governance. Visibility is enablement. One system." |

### Within the 5-min Loom Recording

| Checkpoint | Clock Time | Action |
|---|---|---|
| Transition to demo | 2:00 | Switch to Codex web tab |
| Move 1 complete | 3:00 | Code understanding output visible |
| Move 2 complete | 4:00 | Self-awareness moment landed |
| Move 3 complete | 4:50 | Dashboard reveal + live query done |
| Close | 5:00 | Thesis restatement, "thank you" |

---

## Rehearsal Protocol

### Run 1: Technical Check
- Execute all 3 prompts against the demo repo
- Time each response
- Note exact files Codex references (use in narration)
- Verify dashboard loads and chat query works
- Record response times

### Run 2: Narration Pass
- Full run with spoken narration
- Practice transitions between tabs
- Time the full demo
- Must be under 3:00

### Run 3: Failure Mode Rehearsal
- Deliberately slow-walk Move 1 (practice "narrate while waiting")
- Use backup prompts for Moves 1 and 2
- Practice the dashboard screenshot fallback
- Time recovery from each failure mode

### Run 4: Dress Rehearsal
- Full demo with narration, correct pacing, all transitions
- Record it (phone video, not Loom — just for self-review)
- Watch playback for filler words, pacing issues, awkward transitions
- Must be under 3:00

---

## Screen Setup

- **Codex web**: Full browser window, dark mode, zoom 130%
- **Dashboard**: Full browser window, zoom 130%
- **Tab switching**: Use Cmd/Ctrl+Tab or click — no fumbling
- **No bookmarks bar, no extensions visible, no other tabs**
- **Font size**: All text readable at recording resolution (test by watching a 30s clip)

---

## Key Phrases to Memorize

These are the lines that carry the thesis. Deliver them with conviction, not speed.

1. "Read-only. Nothing changed. This is where we start every deployment."
2. "This is what responsible AI usage looks like."
3. "The tool teaches responsible usage."
4. "Same data, two audiences."
5. "This dashboard was built in 48 hours — using Codex."
6. "The act of using the tool IS the act of generating the data."
7. "Visibility is governance. Visibility is enablement."
