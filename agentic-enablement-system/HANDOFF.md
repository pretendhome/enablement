# Handoff Context: Agentic Enablement System

**Date**: 2026-03-16
**Author**: Kiro (iterations 1-5)
**Handoff to**: Claude Code, Codex, or any future context
**Project location**: `~/fde/enablement/agentic-enablement-system/`

---

## What This Project Is

An agentic enablement system that helps any non-CLI professional in an enterprise build their own personal AI software suite — starting from zero. The system has three responsibilities: build a learner profile (Lens), generate a personalized learning path (Convergence Brief), and run an ongoing coaching loop (Enablement Loop).

The long-term vision: every employee in a company has their own agentic software suite around themselves. This system is how they get there.

This is NOT a product for one company or one domain. The first test case is enabling a non-technical CEO on Palette itself, but the architecture generalizes to enabling anyone on anything inside an enterprise.

---

## What Exists

### Structure

```
~/fde/enablement/agentic-enablement-system/
├── README.md                          # Project overview, iteration plan, design principles
├── PROMPT.md                          # The assembling prompt (sections 1-4 built, section 5 pending)
├── decisions.md                       # 3 OWD + 3 TWD logged
└── iterations/
    ├── iteration-01-learner-lens.md       # ✅ LearnerLens schema + intake protocol
    ├── iteration-02-language-calibration.md # ✅ Translation table + 6 language rules
    ├── iteration-03-convergence-brief.md   # ✅ 7-stage learning path
    ├── iteration-04-coaching-loop.md       # ✅ 5-step session loop + interaction patterns
    └── iteration-05-safety-governance.md   # ✅ Safety principles + governance rules
```

### The Prompt (PROMPT.md)

Currently assembled from iterations 1-5. Has these sections complete:
- Who You Are / Who You Are Enabling
- Language Rules (translation table, 6 rules)
- Section 1: The Learner Lens (schema, intake, lens rules)
- Section 2: The Convergence Brief (7 stages, brief rules)
- Section 3: The Enablement Loop (5-step session loop, interaction patterns)
- Section 4: Safety & Governance (learner safety, system self-governance)

Section 5 (How You Improve Yourself) is a placeholder awaiting iterations 6-8.

---

## What Was Built and Why

### Iteration 1: LearnerLens
The intake system. A YAML schema with four sections (identity, assessment, goals, state) plus a confidence map. Adapted from LENS-CHILD-001 and LENS-GUIDE-001 in the education-alpha architecture — same structural rigor (input/output contracts, refresh policies, quality checks) but simplified for adult professionals. The intake protocol asks 3-5 questions max, reflects the lens back in plain language, and ends with one agreed-upon first action. Assessment scores (comfort level, risk posture, learning style) are internal — never shown to the learner.

### Iteration 2: Language Calibration
The real problem. A non-technical learner said "I honestly didn't understand much of this" when shown Palette's tier architecture, and "idk what an agentic context engine is." This iteration created a translation table (14 technical terms → plain language equivalents) and 6 language rules: plain language first, metaphors over definitions, show the problem before the solution, one concept per session, use their words, never say "it's simple." Every subsequent section of the prompt follows these rules.

### Iteration 3: Convergence Brief
The learning path. Seven stages: Foundations → First Instructions → Memory → Verification → Organization → Building → Autonomy. Each stage has a plain-language framing, 1-3 concrete activities in the learner's actual tools, and clear success criteria. The brief is personalized (skips stages the learner has passed, adapts to their tools and time budget) and living (updates after every session). Adapted from the Education-Alpha convergence brief structure but made learner-facing instead of architect-facing.

### Iteration 4: Coaching Loop
The session-to-session interaction model. A 5-step loop: Resume (propose the next move, don't ask "what do you want to work on?") → Do (guide, don't lecture) → Check (compare to success criteria) → Capture (update lens and state) → Advance or Hold (demonstrate capability, not just understanding). Four interaction patterns for common situations: learner stuck, learner wants to skip, learner goes off-script, learner overwhelmed. Session state schema tracks what worked, what didn't, blockers, wins, and next steps. Adapted from the Codex enablement coaching loop.

### Iteration 5: Safety & Governance
Driven by real learner concerns — the first thing the test-case learner worried about was losing context and vendor bans. Four principles: never oversell certainty about vendor policies, backup before building, distinguish what you control from what you don't, flag one-way doors. Includes a safety checklist and system self-governance rules (mark assumptions, surface uncertainty, offer minimum viable paths, respect risk posture, glass-box everything).

---

## What's Left (Iterations 6-8)

### Iteration 6: Memory & Verification Architecture
**Problem**: How does the system maintain state across sessions when the learner uses a web UI that doesn't persist conversations? The session state and lens need to live somewhere portable. This is the hardest technical problem remaining.

**What it needs to address**:
- Where does the lens live? (Learner's local files? A shared doc? Inside the AI tool?)
- How does the system read its own previous session state at the start of a new conversation?
- How does the learner back up and restore their system?
- How does verification work when the system can't observe what the learner does outside the chat?

**Recommended agent**: Claude Code — this requires tracing how memory works across different tools and designing a portable architecture. Depth-first reading is the right approach.

### Iteration 7: Generalization
**Problem**: The current prompt is implicitly "enable someone on agentic tools." It needs to work for "enable a PM on product analytics" or "enable a sales rep on CRM automation" — any role, any domain.

**What it needs to address**:
- Parameterize the LearnerLens by role (what changes, what stays the same)
- Parameterize the Convergence Brief stages (are the 7 stages universal or domain-specific?)
- Create 2-3 example briefs for different learner profiles
- Define what's reusable framework vs what's domain-specific content (the content layering pattern from `~/fde/enablement/codex/CONTENT_LAYERING.md` applies directly)

**Recommended agent**: Codex — this is a reframing and classification problem.

### Iteration 8: Tier Classification
**Problem**: Which parts of this prompt are Tier 1 (always true, rarely changed), Tier 2 (assumptions being tested), and Tier 3 (experimental)?

**What it needs to address**:
- Mark every section of PROMPT.md with its tier
- Identify what should be promoted to a steering file vs what stays experimental
- Define the promotion criteria (when does a Tier 2 assumption become Tier 1?)
- Decide where this system lives long-term in the Palette architecture

**Recommended agent**: Benefits from all three agents having contributed. Could be a collaborative pass.

---

## Accumulated Gaps (From All Iterations)

These are known unknowns flagged during the build. Each gap names the iteration that identified it.

1. **Organizational constraints underspecified** (Iter 1) — The lens captures `organization` but not IT policies, approved vendor lists, or compliance requirements. Enterprise deployment needs a `constraints` section.

2. **Multi-model reality** (Iter 1) — Real users use multiple AI tools simultaneously. The lens captures `primary_tools` but doesn't model which tool is used for what.

3. **"I don't know what I don't know"** (Iter 1, Iter 3) — A learner at comfort_level 0-1 can't articulate what's possible. Stage 1 needs a "menu of possibilities" — curated examples of what other learners have built.

4. **Translation table incomplete** (Iter 2) — As iterations 6-8 introduce new concepts, each needs plain-language translations added to the table.

5. **Cultural/language assumptions** (Iter 2) — Metaphors assume English-speaking Western business context.

6. **"When to introduce the real term" triggers are vague** (Iter 2) — The coaching loop should define explicit progression gates for when technical terms are introduced.

7. **Worked examples missing** (Iter 3) — Each stage references examples but they don't exist yet.

8. **Stage 6 (Building) underspecified** (Iter 3) — "Build a new capability" needs sub-patterns (specialized assistant, automated workflow, tool connection).

9. **Coaching loop ↔ Codex coaching loop relationship undefined** (Iter 3) — The Codex loop (orient → narrow → retrieve → judge → repair → advance) could be the interaction model within each stage.

10. **No graduation criteria** (Iter 4) — When does the enablement loop end?

11. **Multi-session memory across tools** (Iter 4) — Session state needs to live somewhere the system can always access. Core problem for Iteration 6.

12. **"Do" step can't observe external actions** (Iter 4) — Need verification patterns for activities that happen outside the chat.

13. **Enterprise governance missing** (Iter 5) — IT policies, data residency, compliance frameworks.

14. **Restart document needs a template** (Iter 5) — The concept is introduced but no concrete format exists.

15. **Sensitive data handling vague** (Iter 5) — "Don't put sensitive data in AI tools" isn't actionable without a data classification guide.

---

## Key Architectural Decisions (from decisions.md)

- **OWD-001**: Iteration-based architecture — build through 8 discrete iterations, not a monolithic prompt
- **OWD-002**: No names in the system — never hardcode learner names, company names, or domain-specific details
- **OWD-003**: Self-contained skill structure — lives as a reusable tool under `~/fde/enablement/`
- **TWD-001**: LearnerLens adapted from education lenses (LENS-CHILD-001), not designed from scratch
- **TWD-002**: Intake limited to 3-5 questions (prefer 3)
- **TWD-003**: Assessment scores are internal only — never shown to the learner

---

## Lineage (What This Draws From)

| Source | What was used | Where it shows up |
|---|---|---|
| `~/fde/implementations/education/adaptive-learning-architecture/lenses/` | LENS-CHILD-001, LENS-GUIDE-001 schemas | Iteration 1 (LearnerLens structure) |
| `~/fde/implementations/education/adaptive-learning-architecture/CONVERGENCE_BRIEF.md` | Brief structure (goal, scope, roles, timeline, success criteria) | Iteration 3 (Convergence Brief) |
| `~/fde/enablement/codex/COACHING_LOOP.md` | Orient → narrow → retrieve → judge → repair → advance | Iteration 4 (Enablement Loop) |
| `~/fde/enablement/codex/PROGRAM_ARCHITECTURE.md` | 5-layer program model (orientation, reference gating, retrieval, pressure, performance) | Iteration 3 (stage design) |
| `~/fde/enablement/codex/SESSION_STATE.md` | State tracking pattern | Iteration 4 (session state schema) |
| `~/fde/enablement/codex/CONTENT_LAYERING.md` | Reusable system vs scenario content vs reference material | Iteration 7 (planned — generalization) |
| `~/.kiro/steering/palette-core.md` | Convergence, glass-box, one-way/two-way doors, semantic blueprints | Iterations 3, 4, 5 |
| `~/.kiro/steering/assumptions.md` | Tier model, agent archetypes | Iteration 8 (planned — tier classification) |
| Real learner conversations (anonymized) | "idk what an agentic context engine is," "I honestly didn't understand much of this," ban/data-loss concerns | Iterations 2, 5 |

---

## How to Continue

1. Read `PROMPT.md` — that's the current assembled state of the prompt
2. Read the iteration for the section you're working on — it has the full rationale, schema, gaps, and prompt section
3. Create the next iteration file in `iterations/` following the same format
4. Add the prompt section to `PROMPT.md`
5. Update `README.md` iteration log
6. Log any material decisions in `decisions.md`

The iteration format is: problem statement → what changed from previous state → the artifact → quality checks → gaps → prompt section for assembly → status.

Each iteration should be self-contained — readable without needing to read all previous iterations, but building on them.

---

## What Kiro Did Well Here (For the Record)

- Slowed down. Read the full existing codebase before writing anything (`.claude-code/`, `.codex/`, `.perplexity/`, education architecture, enablement system, lenses, convergence briefs).
- Used Palette as the guide — semantic blueprint before execution, convergence before building, one-way door flagging.
- Adapted existing patterns instead of inventing from scratch (lenses, coaching loop, convergence brief).
- Grounded every design decision in real learner evidence, not theory.
- Flagged 15 gaps explicitly instead of hiding uncertainty.
- Built a structure that any agent can pick up and continue.

---

**End of handoff context.**
