# Iteration 1: LearnerLens Schema + Intake

**Date**: 2026-03-16
**Focus**: Who is this person and what do they need?
**Problem it solves**: The system cannot help someone it doesn't understand. Before any enablement path is generated, the system must build a structured, evolving profile of the learner.
**Lineage**: Adapted from LENS-CHILD-001 (education-alpha) and LENS-GUIDE-001 patterns.

---

## What Changed From the Rough Draft

The original prompt defined a LearnerLens with 6 fields (role, goals, constraints, current_stack, agentic_maturity, risk_sensitivity). That's a good start but it has problems:

1. **It asks too much upfront.** A non-technical user won't know their "agentic maturity" or be able to list their "current stack" precisely. The intake must meet them where they are.
2. **It's flat.** The education lenses have input contracts, output contracts, refresh policies, and quality checks. The LearnerLens needs the same rigor.
3. **It doesn't version.** The original says "versioned" but doesn't define how. The education lenses have explicit version fields and refresh policies.
4. **It doesn't define confidence.** Some fields will be guesses early on. The system needs to know which fields are solid and which are thin.

---

## LearnerLens Schema (v0.1)

```yaml
lens_id: LENS-LEARNER-001
version: 0.1
status: pilot
name: Learner Enablement Lens
domain: enterprise-enablement

# --- IDENTITY ---
# Filled during intake conversation (first 5-10 minutes)

identity:
  role_description: ""
    # What they actually do, in their own words
    # Example: "I run a dating coaching business for tech professionals"
    # Example: "I'm a product manager for a SaaS platform"
    # NOT a job title — a description of what they spend their days doing

  organization: ""
    # Where they work and roughly how big it is
    # Example: "5-person startup" or "mid-size SaaS company, ~200 people"

  primary_tools: []
    # What they already use daily — asked as "what apps do you open every morning?"
    # Example: ["Claude", "Google Docs", "Slack", "Notion"]
    # NOT a technical inventory — just what they'd name if asked

  time_budget: ""
    # How much time they can realistically spend on this per week
    # Example: "20-40 minutes at a time, maybe 3x per week"
    # Assume they are busy and context-switched

# --- ASSESSMENT ---
# Filled by the system based on the intake conversation
# The learner does NOT fill these directly

assessment:
  comfort_level:
    # 0 = "I don't know what any of this means"
    # 1 = "I use AI chat daily but don't customize anything"
    # 2 = "I've set up some automations or custom instructions"
    # 3 = "I have a working system with steering files, memory, and multiple tools"
    score: null
    confidence: low
    signals: []
      # What the learner said or did that led to this score
      # Example: ["said 'idk what an agentic context engine is'", "uses Claude daily for writing"]

  risk_posture:
    # How worried they are about breaking things, losing data, or getting banned
    # cautious | moderate | adventurous
    level: null
    confidence: low
    signals: []
      # Example: ["asked about backup before anything else", "worried about vendor bans"]

  learning_style:
    # How they prefer to learn — observed, not asked
    # hands-on | conceptual | example-driven | mixed
    preference: null
    confidence: low
    signals: []

# --- GOALS ---
# Co-created with the learner during intake

goals:
  near_term: ""
    # One concrete thing they want to accomplish in the next 1-2 weeks
    # Example: "back up my important contexts safely"
    # Example: "understand what a steering file is and make one"
    # Must be specific enough to verify completion

  medium_term: []
    # 2-3 things they want within a month
    # Example: ["have a working verification loop", "be able to assign tasks to my system"]

  vision: ""
    # What they're ultimately trying to build — in their own words
    # Example: "a team of AI assistants that remember how to help me and can handle routine work"
    # This will be vague early on. That's fine. It sharpens over time.

# --- SYSTEM STATE ---
# Updated by the enablement system after each session

state:
  sessions_completed: 0
  current_stage: "intake"
    # intake | foundations | steering | memory | verification | building | autonomous
  last_session_date: null
  blockers: []
    # What's preventing progress right now
    # Example: ["doesn't have a dedicated machine for always-on system"]
  wins: []
    # What's working — used to maintain momentum
    # Example: ["successfully backed up first context window"]

# --- CONFIDENCE MAP ---
# Which parts of this lens are solid vs thin

confidence:
  identity: low       # becomes medium after intake, high after 3+ sessions
  assessment: low     # becomes medium after first working session
  goals: low          # becomes medium after first goal completion
  state: not_started  # becomes active after first session
```

---

## Intake Protocol

The system's first interaction with any new learner follows this sequence. The goal is to fill the lens with a usable v1 in under 15 minutes.

### Step 1: Open with context, not questions

Don't start with "tell me about yourself." Start with what the system is and what it's going to do:

> "I'm going to help you build your own personal software suite — a set of AI tools that are customized to how you work, that remember what you've taught them, and that get better over time. Think of it like having a small team of assistants that know your business, your preferences, and your workflow."
>
> "To do that well, I need to understand a few things about you first. This will take about 10 minutes."

### Step 2: Three questions (maximum five)

These are the only questions needed for a usable v1 lens:

**Q1: "What do you actually spend your days doing?"**
- Fills: `identity.role_description`
- Listen for: domain, complexity, whether they manage people or work solo
- Do NOT ask for a job title

**Q2: "What tools do you open every morning when you start work?"**
- Fills: `identity.primary_tools`
- Listen for: AI tools they already use, how technical their stack is
- This also gives signal for `assessment.comfort_level`

**Q3: "If this system worked perfectly, what would be different about your workday in a month?"**
- Fills: `goals.vision` and seeds `goals.medium_term`
- Listen for: concrete vs abstract thinking, ambition level, pain points

**Q4 (if needed): "What's the one thing you'd want to get working first?"**
- Fills: `goals.near_term`
- Only ask if Q3 didn't produce something specific enough

**Q5 (if needed): "Is there anything you're worried about — like losing work, breaking something, or a tool cutting you off?"**
- Fills: `assessment.risk_posture`
- Only ask if the learner hasn't surfaced risk concerns organically

### Step 3: Reflect and confirm

After the questions, the system reflects the lens back in plain language:

> "Here's what I understand so far:
>
> You run [role_description] at [organization]. You use [tools] daily. You're at a point where [comfort_level interpretation]. Your main goal right now is [near_term], and longer term you want [vision].
>
> Did I get that right? Anything I'm missing or got wrong?"

### Step 4: Agree on first action

End the intake with one agreed-upon next step:

> "Based on what you've told me, I think the best first step is [specific action]. It should take about [time estimate] and when we're done, you'll [concrete outcome]. Sound good?"

---

## Quality Checks

Adapted from LENS-CHILD-001:

- [ ] `role_description` is in the learner's own words, not system-generated jargon
- [ ] `near_term` goal is specific enough to verify completion (not "learn more about AI")
- [ ] `comfort_level` score has at least one signal from the actual conversation
- [ ] `risk_posture` is assessed (even if from indirect signals)
- [ ] The lens was reflected back to the learner and they confirmed it
- [ ] No field is presented to the learner as a score or rating — assessments are internal

---

## Refresh Policy

| Field | Refresh Trigger |
|---|---|
| identity | Major role change or new tool adoption |
| assessment.comfort_level | After each session (re-evaluate from behavior) |
| assessment.risk_posture | After first risky action or first failure |
| assessment.learning_style | After 3 sessions (enough signal to assess) |
| goals.near_term | After completion or abandonment of current goal |
| goals.medium_term | Monthly or after major milestone |
| goals.vision | Quarterly or when learner reframes what they want |
| state | After every session |
| confidence | After every session |

---

## What This Iteration Does NOT Address

These are explicitly deferred to later iterations:

- **Language calibration** (Iteration 2): The schema uses terms like "steering file" and "verification loop" in examples. These need translation for non-CLI users.
- **What happens after intake** (Iteration 3): The Convergence Brief — the actual learning path — is not defined here.
- **Session-to-session continuity** (Iteration 4): How the system remembers and resumes across sessions.
- **Safety concerns** (Iteration 5): The risk_posture field captures the learner's worry, but the system's actual safety mechanisms aren't defined here.

---

## Gaps (Known Unknowns)

1. **Organizational constraints are underspecified.** The schema captures `organization` but not things like "my company won't let me install anything" or "I can only use approved vendors." This matters for enterprise deployment. Likely needs a `constraints` section added in a later iteration.

2. **Multi-model reality.** Real users (like the test case) use multiple AI tools simultaneously — Claude, GPT, Codex, Perplexity. The lens captures `primary_tools` but doesn't model which tool is used for what. This may matter for the Convergence Brief (Iteration 3) when recommending specific activities.

3. **The "I don't know what I don't know" problem.** The intake asks what the learner wants, but a learner at comfort_level 0-1 literally cannot articulate what's possible. The system needs to show them possibilities before asking for goals. This is a chicken-and-egg problem that Iteration 3 (Convergence Brief) must address — possibly by offering a "menu" of outcomes other learners have achieved.

---

## Prompt Section (for assembly into PROMPT.md)

This is the section of the final prompt that Iteration 1 contributes:

```markdown
## 1. The Learner Lens

Your first job with any new learner is to build a Learner Lens — a structured,
evolving profile that you maintain.

The lens has four sections:
- **Identity**: who they are, what they do, what tools they use, how much time they have
- **Assessment**: your evaluation of their comfort level, risk posture, and learning style
  (never shown to the learner as scores — these are internal to you)
- **Goals**: one near-term goal (1-2 weeks), medium-term goals (1 month), and their vision
- **State**: sessions completed, current stage, blockers, and wins

### Building the Lens

Ask a maximum of 5 questions. Prefer 3.

1. "What do you actually spend your days doing?"
2. "What tools do you open every morning when you start work?"
3. "If this system worked perfectly, what would be different about your workday in a month?"
4. (If needed) "What's the one thing you'd want to get working first?"
5. (If needed) "Is there anything you're worried about — like losing work or a tool cutting you off?"

After the questions, reflect the lens back in plain language and ask for corrections.
End with one agreed-upon first action.

### Lens Rules

- The lens is versioned. Preserve previous versions when you update it.
- Assessment fields are filled by you from conversation signals, not by asking the learner to self-rate.
- Every assessment must have at least one signal (a quote or behavior) as evidence.
- The near-term goal must be specific enough to verify completion.
- Update the lens after every session.
- Never show the learner a score or rating. The lens is your internal tool for serving them better.
```

---

## Status

**Iteration 1: COMPLETE**
- LearnerLens schema defined (YAML, v0.1)
- Intake protocol defined (5 questions max, reflect-and-confirm)
- Quality checks defined
- Refresh policy defined
- Gaps flagged (3)
- Prompt section drafted for assembly

**Next**: Iteration 2 — Language calibration for non-CLI users
