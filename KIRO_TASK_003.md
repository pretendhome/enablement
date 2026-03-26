# KIRO_TASK_003: Full Product Refinement
**Date:** 2026-03-25
**From:** claude.analysis
**To:** kiro.design
**Priority:** P0
**Status:** ASSIGNED
**Bus message:** 2161dbed-a257-47a9-9ef2-45f3b46e3520

---

## Context

You delivered two excellent UX reviews:
- `enablement/docs/KIRO_UX_REVIEW_2026-03-25.md` — 3-persona walkthrough
- `enablement/docs/KIRO_UX_REVIEW_PM_LENS_2026-03-25.md` — 5-iteration PM audit

Mical approved all 5 product decisions. Now we need implementation-ready specs.

## Deliverables

Save to: `/home/mical/fde/enablement/docs/KIRO_PRODUCT_REFINEMENT_2026-03-25.md`

### 1. Three-File Split Design
The current `video-enablement.md` serves 3 audiences in one file. Design the split:
- **File 1**: Published path template (what viewers see) — clean, no system internals
- **File 2**: Content engine spec (what Mical/narrator uses) — templates, parameters, wire contract, constellations
- **File 3**: Creator Mode (what educators use) — standalone, no Palette internals

For each file: exact filename, exact location, what sections move where, how cross-references update.

### 2. Onramp Copy
Exact 2-3 sentence intro that goes BEFORE the metadata header on every published path. Must:
- Explain what this is in plain English
- Set expectations (paste into AI tool, it guides you, 5-60 min)
- Not use jargon (no RIU, no constellation, no artifact)

### 3. Feedback Capture Mechanism
- Google Form field spec (exact fields, field types, required vs optional)
- Where the link appears in the path (exact location and wording)
- What the CTA copy says
- How data flows back (form → spreadsheet → what happens next)

### 4. Adaptive AFTER YOU BUILD
- Which steps are mandatory vs optional at each difficulty level
- Exact LLM instruction wording that makes it adaptive
- How to fix the time promise ("5 minutes" → honest framing)
- Where confidence re-rating moves to (Kiro suggested: immediately after verification)

### 5. What's Next Routing Strategy
- For paths that exist: how to link
- For paths that don't exist yet: exact "coming soon" or waitlist copy
- Whether to include or omit constellation map when most nodes are unpublished
- Waitlist mechanism design (if any)

### 6. RIU-021 Path Audit
Read `/home/mical/fde/enablement/paths/RIU-021-tiny-ai-eval-harness.md` (Codex's first generated path).
Flag anything that violates your UX findings. Provide exact fix copy.

### 7. Video Lineup PM Review
Apply PM lens to the first 5 video topics:
1. Multi-agent system architecture ("I built a system with 11 AI agents. Here's what broke.")
2. Taxonomy / knowledge engineering (TITLE NEEDS REWORK — current "The AI problem nobody talks about" is too vague per Mical)
3. AI coding tools comparison ("Claude Code vs Cursor vs Codex: I use all three. Here's when.")
4. Token budget management ("Your AI costs 10x what it should. Here's the fix.")
5. Enablement system demo ("I onboarded my first AI client in 60 minutes")

Questions to answer:
- Is the ordering optimal for channel growth?
- Does Video 1 establish the right identity?
- Does the mix balance discovery (high search volume) vs depth (niche positioning)?
- What title alternatives for Video 2?

## Reference Files
- `/home/mical/fde/enablement/agentic-enablement-system/content-engine/video-enablement.md`
- `/home/mical/fde/enablement/docs/KIRO_UX_REVIEW_2026-03-25.md`
- `/home/mical/fde/enablement/docs/KIRO_UX_REVIEW_PM_LENS_2026-03-25.md`
- `/home/mical/fde/enablement/paths/RIU-021-tiny-ai-eval-harness.md`
- `/home/mical/fde/enablement/agentic-enablement-system/content-engine/specs/VIDEO_SPEC_001.yaml`
- `/home/mical/fde/implementations/youtube-exploration/phase-1-research/GAP_ANALYSIS.md`
- `/home/mical/fde/implementations/youtube-exploration/phase-3-content/THE_FORMULA.md`

## Quality Bar
- Every recommendation must include exact copy, not just direction
- File specs must include exact paths and filenames
- This is implementation-ready design — Claude Code will execute directly from your specs
