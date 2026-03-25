# Elia Onboarding Session — 1 Hour Plan

**Date**: 2026-03-25
**Facilitator**: Mical
**Learner**: Elia Canu — Founder, dating app startup
**Goal**: By end of session, Elia has a working Palette setup with his personal lens, understands what it can do for him, and has used it to do real work on his actual problems.

**Success criteria for this session:**
- Elia has a live project with the current `enablement-coach.md` installed
- Elia has a saved lens reflecting his actual work, tools, and current priority
- The session produces one real artifact he needed this week
- Elia leaves with one specific next use this week, not a vague intention to explore
- You leave with enough session state to resume decisively next time

---

## Pre-Session Checklist (Mical — do before the call)

- [ ] Confirm which AI tool Elia uses (Claude Pro? ChatGPT? Both?)
- [ ] Have the `enablement-coach.md` ready to paste into a Claude Project
- [ ] Have this session plan open during the call
- [ ] Know Elia's current situation: what's he working on right now with the dating app?
- [ ] Decide the lightest backup path for anything created in-session
- [ ] Have one fallback task ready if his "real problem" is too vague
- [ ] Be ready to treat the session as: Resume -> Do -> Check -> Capture -> Advance

---

## Minute 0-5: Open & Frame (5 min)

**What you say:**

"Hey Elia — today I'm going to get you fully set up on Palette. By the end of this hour you'll have a personal AI system that knows who you are, knows your business, and can actually help you build things. Not a demo — your real setup, on your real problems."

**Key points to hit:**
- Everything stays on his machine / in his account
- This isn't a course — it's his personal system
- He'll walk away with something working today
- We are doing one real thing well, not touring every feature
- If something is hard to undo or sensitive, you will flag it explicitly

**Don't do:**
- Don't explain Palette's architecture
- Don't mention taxonomy, RIUs, agents, or any internal terminology
- Don't oversell — let the system prove itself

---

## Minute 5-15: Setup + Know Him (10 min)

### Setup (3 min)

Walk him through creating a Claude Project (or equivalent in his tool):

1. Open Claude → Projects → Create Project → Name it "Palette" (or whatever he wants)
2. Paste the enablement-coach.md into Project Instructions
3. Start a new chat

**If he already has Claude set up from previous sessions**, skip to updating/replacing the project instructions.

### Know Him (7 min)

Either let the coach ask the intake questions, or YOU ask them conversationally since you already know Elia. The goal is to capture:

- **Role**: Founder of a dating app. What stage? Pre-launch? Live? Growing?
- **Daily tools**: What does he actually use every day?
- **Current challenge**: What's the #1 thing taking his time right now?
- **Wish**: What would he want an AI assistant to do first?
- **His world**: How are his files organized? Where does his work live?

**You probably already know most of this from months of working together.** Fill in what you know, confirm with him, let him correct.

**Quality bar for intake:**
- Get his role in his own words, not your abstraction
- Get one concrete near-term problem, not a broad ambition
- Infer comfort/risk quietly; do not turn intake into a questionnaire

---

## Minute 15-25: Build His Lens (10 min)

This is the moment Palette becomes *his*. Work with the coach (or do it yourself) to create his lens file:

```yaml
# Elia's Palette Lens
# Last updated: 2026-03-25

## Who I Am
name: Elia Canu
role: Founder — [dating app name]
background: [what you know — non-technical founder, startup stage, etc.]

## My Tools
daily_tools: [fill from conversation]
platforms: [where his files live]
comfort_level: [beginner / comfortable with AI chat]

## My World
active_projects:
  - name: [dating app]
    status: [current stage]
    description: [one line]

## What I Want
primary_goal: [from conversation]
current_challenge: [from conversation]

## How I Work
time_budget: [how much time he has for AI stuff]
preferences: [anything you know about how he likes to work]

## Session History
- 2026-03-25: First full onboarding session with Mical
```

**Show it to him.** "This is your lens — it's what makes Palette yours. Every time you start a conversation, it reads this first."

Save it into his Claude Project knowledge.

**Do not stop at writing it.**
- Read it back in plain language
- Ask what is wrong, missing, or overstated
- Make one correction live so he sees the lens is editable, not sacred

**Minimum lens quality bar:**
- `primary_goal` is specific enough to work on today
- `current_challenge` reflects this week, not "the startup in general"
- `daily_tools` and `platforms` are concrete enough to guide future sessions
- the lens uses Elia's words where possible

---

## Minute 25-45: Do Real Work (20 min)

**This is the most important part.** Don't demo — solve a real problem he has RIGHT NOW.

Ask: "What's the thing you're working on this week? Let's use Palette on it."

### Likely scenarios for a dating app founder:

| If he says... | Route to... |
|---|---|
| "I need to write copy / marketing" | Have Palette write it using his lens context |
| "I'm trying to figure out [feature/strategy]" | Research + planning — Palette checks knowledge library then searches |
| "I need to prepare for a meeting/pitch" | Talent skill — build a prep package |
| "I'm stuck on [technical decision]" | Architecture analysis — classify the problem, map options |
| "I need to organize my [docs/plans/roadmap]" | Help him structure his files and create a project plan |
| "I want to understand [AI/market/competitor]" | Deep research with citations |

### The pattern:
1. He states the problem
2. Palette (or you + Palette) proposes the next useful move in plain language
3. Work through it together — smallest next step first, real output, not theory
4. Check whether the output is actually usable for his business this week
5. Tighten once if needed rather than jumping to a new capability

**Verification rule:**
- Do not count this section as a success because the output "looks good"
- Ask: "Would you actually use/send/build from this as-is?"
- If not, do one repair pass focused on the weakest part

**Good artifact types for this section:**
- a decision memo
- a product/feature brief
- a pitch or meeting prep note
- landing page or app copy
- a competitor or market brief
- a lightweight roadmap / execution plan

**Goal**: He has a concrete artifact (a document, a plan, a piece of copy, a research brief) that he actually needed, built in 20 minutes.

---

## Minute 45-55: Show the Range (10 min)

Now that he's seen Palette do one thing well, quickly show breadth. Pick 2-3 that match his interests:

"That's one thing Palette can do. Let me show you what else is in here."

Quick demos (2-3 min each, pick what's relevant to him):

- **Research**: "Ask it to research [something relevant to his dating app market]" — show how it checks the knowledge library first, then searches with citations
- **Planning**: "Ask it to help you plan [upcoming milestone]" — show structured output
- **Writing**: "Ask it to draft [something he needs]" — show how lens context makes it personal
- **Learning**: "Ask it to explain [something he's been curious about]" — show it teaches at his level

**Don't try to show everything.** 2-3 demos max. Leave him wanting more, not overwhelmed.

**Selection rule:**
- Only show capabilities adjacent to the artifact you just made
- Prefer "same workflow, different job" over disconnected feature variety
- If the core 20-minute block ran long, cut this section aggressively

---

## Minute 55-60: Lock It In (5 min)

### Update the lens
Add what you learned during the session. Save it.

### Capture session state
Write a short note for yourself or into his project knowledge with:
- what worked
- what didn't
- what artifact was produced
- what the next recommended move is
- any blocker or sensitivity to watch next time

### Confirm the workflow
"Here's how you use this going forward:
1. Open your Palette project in Claude
2. Start a new chat
3. It already knows who you are — just tell it what you need
4. At the end, it'll update your lens"

### Set the hook
"What do you want to use it for this week? Pick one thing."

Get a specific commitment. Not "I'll play around with it" — something concrete: "I'll use it to write my investor update" or "I'll use it to research [competitor]."

**Preferred close question:**
"What's the one thing this will save you time on before we talk next?"

### Leave the door open
"Text me if you get stuck. I'll check in [when] to see how it went."

---

## Post-Session (Mical)

- [ ] Update Elia's lens with everything from the session
- [ ] Make sure his Claude Project has the latest enablement-coach.md
- [ ] Make sure his lens is saved in Project Knowledge
- [ ] Save a short session-state note: wins, blockers, next move
- [ ] Note what worked and what didn't for the enablement system
- [ ] Follow up in [X days] to see if he used it

---

## If Things Go Sideways

| Problem | Fix |
|---|---|
| He can't access Claude Projects | Use ChatGPT with custom instructions, or just work in a regular chat and save the lens as a doc he pastes |
| He's overwhelmed | Slow down. Cut scope. Just do the lens + one real task. Skip the range demos. |
| He's bored / already knows this | Skip setup, skip intake, go straight to hard problems. Show him the SDK or advanced capabilities. |
| Technical issues (auth, billing, etc.) | Don't waste session time debugging. Note it, work around it, fix after. |
| He wants to go deep on one thing | Let him. Cancel the rest of the plan. Depth > breadth. |
| The task touches sensitive info / vendor commitments / file deletion | Flag it as hard to undo, explain the risk plainly, and choose the safest reversible version for the session |

---

## Key Principle

**The session succeeds if Elia leaves thinking "I'm going to use this tomorrow" — not "that was a cool demo."**

Real work > demos. His problems > your features. One thing working > ten things explained.

## Facilitator Notes From The Enablement Build

- Propose the next useful move; do not hand him an open menu too early.
- Advance only after something has actually been produced and checked.
- If he says he "gets it," prefer one tiny demonstration over more explanation.
- Use plain language first. Internal terms are optional and usually unnecessary.
- Treat the lens as a working document with confidence gaps, not a perfect profile.
- Keep safety honest: distinguish what he controls from what the tool/vendor controls.
