# Enablement

Reusable frameworks for helping people learn, build, and perform — from creating enablement content to deploying coaching systems at scale.

## Two Parts

### Part 1: Enablement Creation (`codex/`)

Methodology for creating enablement content for any purpose — training videos, coaching programs, onboarding flows, performance drills. The reusable engine: coaching loops, session state, content layering, video performance patterns.

Built and validated through real interview prep cycles (OpenAI, Perplexity, Glean). The patterns generalize to any skill progression context.

**Key files:**
- `codex/COACHING_LOOP.md` — Core 6-step interaction model (orient → narrow → retrieve → judge → repair → advance)
- `codex/PROGRAM_ARCHITECTURE.md` — Full system design end-to-end
- `codex/SESSION_STATE.md` — How to preserve and resume progress across sessions
- `codex/VIDEO_PERFORMANCE_LOOP.md` — Reusable loop for recorded demos, Looms, briefings
- `codex/CONTENT_LAYERING.md` — How to separate reusable framework from scenario-specific content
- `codex/USE_CASES.md` — Where the pattern applies beyond interview prep

### Part 2: Agentic Enablement System (`agentic-enablement-system/`)

A complete skill and coaching system that onboards anyone — any role, any domain — to building their own personal AI toolkit. Built in 8 iterations, each addressing one problem: learner profiling, language calibration, learning path generation, coaching loops, safety, memory architecture, generalization, and governance tiers.

The system has two layers:
- **Engine** (universal) — Learner Lens, coaching loop, progress file, verification patterns, safety principles, language rules. Works for any domain.
- **Domain Packs** (swappable) — Stage definitions, activities, translation tables, worked examples. Currently ships with Agentic Enablement (default), plus example packs for Product Analytics and CRM Automation.

**Key files:**
- `agentic-enablement-system/PROMPT.md` — The fully assembled coaching prompt (all 8 iterations)
- `agentic-enablement-system/onboarding/enablement-coach.md` — Drop-in file for Claude Projects (the deployable artifact)
- `agentic-enablement-system/iterations/` — Build history (8 iterations, each self-contained)
- `agentic-enablement-system/decisions.md` — Decision log (7 decisions)
- `agentic-enablement-system/HANDOFF.md` — Full context for any agent picking this up

## How They Relate

Part 1 provides the **methodology patterns** (coaching loops, session state, content layering).
Part 2 **applies those patterns** to build a complete deployable system.

The Codex coaching loop became the Enablement Loop (Iteration 4). The session state pattern became the progress file architecture (Iteration 6). The content layering pattern enabled the engine/domain pack separation (Iteration 7).

## Where Things Live

| What | Location | Purpose |
|---|---|---|
| Enablement frameworks | `enablement/` (here) | Reusable methodology and build artifacts |
| Enablement skill | `palette/skills/enablement/` | Palette skill pack — what agents load |
| Deployable coach | `enablement/agentic-enablement-system/onboarding/enablement-coach.md` | Drop into Claude Project, start coaching |
| Implementations | `implementations/` (monorepo only) | Specific instances where skills get applied |

## Lineage

| Source | What was used |
|---|---|
| `codex/COACHING_LOOP.md` | Coaching loop → Enablement Loop (Iteration 4) |
| `codex/SESSION_STATE.md` | State tracking → Progress file (Iteration 6) |
| `codex/CONTENT_LAYERING.md` | Layer separation → Engine/domain pack (Iteration 7) |
| `implementations/education/adaptive-learning-architecture/lenses/` | LENS-CHILD-001 → LearnerLens (Iteration 1) |
| Real learner conversations | Language calibration, safety principles (Iterations 2, 5) |
