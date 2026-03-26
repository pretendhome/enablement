# Codex Task 003: First Filled Video Spec + Enablement Path (End-to-End Proof)

**From**: claude.analysis
**To**: codex.implementation
**Date**: 2026-03-25
**Bus Message ID**: ce-003-video-spec-e2e

---

## Context

The content engine is built. We have:
- A parameterized enablement skill: `video-enablement.md` v2.0 (learner mode, creator mode, constellations, confidence delta, verification at every level)
- A blank video spec template: `video-spec-template.yaml` v2 (signal, classification, video, enablement, post-production, checklist)
- A system design: `SYSTEM_DESIGN_v1.md` (the core loop: signal -> classify -> research -> build -> produce -> publish -> enable -> feedback)
- Market validation: `LEARNING_FROM_THE_BEST.md` (OpenAI $239-325K, Anthropic $270-365K, Mistral undisclosed — all hiring for what we're building)

What we don't have: a single real, filled video spec proving the template works end-to-end. The example in `video-enablement.md` is "Building a Taxonomy" (RIU-401). That was an illustration. This task produces the first REAL spec — a different topic, every field filled, and the enablement path generated from it.

**This is the proof that the content engine works. Signal in, enablement path out.**

---

## Key Files to Read

| File | What It Is |
|---|---|
| `/home/mical/fde/enablement/agentic-enablement-system/content-engine/video-spec-template.yaml` | The blank v2 template — fill EVERY field |
| `/home/mical/fde/enablement/agentic-enablement-system/content-engine/video-enablement.md` | The skill (v2.0) — contains the learner mode template, the filled taxonomy example, path constellations, wire contract, parameter reference |
| `/home/mical/fde/enablement/agentic-enablement-system/content-engine/SYSTEM_DESIGN_v1.md` | System design — understand the core loop before generating |
| `/home/mical/fde/enablement/agentic-enablement-system/content-engine/LEARNING_FROM_THE_BEST.md` | Market requirements from OpenAI/Anthropic/Mistral job specs |
| `/home/mical/fde/palette/taxonomy/releases/v1.3/palette_taxonomy_v1.3.yaml` | Taxonomy — 117 RIUs, pick one |
| `/home/mical/fde/palette/knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml` | Knowledge library — 163 entries, find relevant ones |
| `/home/mical/fde/palette/buy-vs-build/people-library/v1.1/people_library_v1.1.yaml` | People library — 21 profiles, 7 clusters, this is the signal network |
| `/home/mical/fde/palette/buy-vs-build/people-library/v1.1/people_library_company_signals_v1.1.yaml` | Company signals — 43 tools, 3 tiers |

---

## Deliverable 1 (P0): Filled Video Spec

**Output**: `/home/mical/fde/enablement/agentic-enablement-system/content-engine/specs/VIDEO_SPEC_001.yaml`

Create the `specs/` directory if it doesn't exist.

### Topic Selection — Requirements

1. **Signal-driven**: The topic MUST come from a real signal in the people library or company signals. Look at:
   - PERSON-019 Andrej Karpathy — recent posts on tokenization, LLM training, AI education
   - PERSON-020 Chip Huyen — MLOps, evaluation frameworks, production AI
   - PERSON-021 Matthieu Lorrain — AI production patterns
   - PERSON-022 PJ Accetturo — AI commercial applications
   - PERSON-005 Olivia Moore a16z — AI tool market trends
   - Or any other profile with a recent, strong signal
2. **NOT taxonomy (RIU-401)**: That's the existing example. Pick something different.
3. **Buildable in 5-10 minutes on camera**: The on-camera demo must be Quick Start level. The viewer goes deeper in the enablement path.
4. **Maps to an existing RIU**: Pick from the 117 RIUs in the taxonomy. If none fits, you may propose a new one — but strongly prefer an existing RIU.
5. **Strong first video**: This is the channel's debut. It needs to demonstrate Mical's unique angle — comparative linguistics background, knowledge engineering, AI system design. Not a generic tutorial.
6. **Maps to market demand**: The topic should connect to what OpenAI/Anthropic/Mistral are hiring for (see LEARNING_FROM_THE_BEST.md).

### Spec Requirements

Fill EVERY field in `video-spec-template.yaml` v2. No empty strings. No placeholders. No `""`. Specifically:

**Signal section**:
- `source`: Real person or company ID from the libraries
- `type`: One of: influencer_post, tool_update, funding, taxonomy_gap, audience_request
- `summary`: One sentence — what happened and why it matters

**Classification section**:
- `riu`: A real RIU ID from the taxonomy
- `riu_name`: The actual name from the taxonomy
- `knowledge_entries`: Real LIB-XXX IDs from the knowledge library (look up which entries are relevant)
- `new_knowledge` and `new_riu`: Boolean, honest assessment

**Video section**:
- `title`: Under 53 characters. Count them. Use one of the title formulas from LEARNING_FROM_THE_BEST.md or the system design.
- `title_chars`: Actual character count of the title
- `title_formula`: One of: challenge-journey, transformation, results, curiosity-gap, authority-test, contrarian, regret, comparison
- `duration_target`: Minutes (5-10 range)
- `thumbnail`: All four fields filled — face, visual, text (2-4 words), palette
- `hook.formula`: One of: cold-open, bold-claim, best-moment, problem-promise, contrarian
- `hook.script`: Real script text for the first 30 seconds. Three beats: pattern interrupt (0-5s), clarify the promise (5-15s), establish stakes (15-30s). Write it as if Mical would actually say these words on camera.
- `build`: What to build on camera, tools needed, difficulty level

**Enablement section** — THIS IS THE MOST IMPORTANT PART:
- `topic`: Human-readable topic name
- `output_description`: One sentence — what the learner will build
- `concept_summary`: 1-2 sentences — what this concept IS and why it matters
- `review_status`: "draft"
- `confidence_baseline_task`: Phrased as a capability question ("could you [X]?"). Must be specific to this topic. NOT generic. Must be re-askable at the end to measure delta.
- `constellation`: Pick from the 5 defined constellations in video-enablement.md. Fill name, sequence, and the full map with position markers (this/next/upcoming/done).
- **Quick Start**: output (concrete artifact), example (daily-life, not work), 3-6 steps, 2-4 failure modes (specific and practical, NOT generic warnings like "don't rush")
- **Applied**: output (work-relevant artifact), 4-8 steps, 2-4 failure modes
- **Production**: output (portfolio-grade artifact), 5-10 steps, 2-4 failure modes
- `next_if_clicked`: 2-3 paths with real RIU references and relationship descriptions
- `next_if_hard`: 1-2 paths with real RIU references and relationship descriptions

**Post-production section**:
- `workflow`: "B" ($4, 30-40min)
- `ai_images_needed`: Reasonable number
- `estimated_cost`: Dollar amount
- `estimated_edit_time`: Time string

**Competitor context**:
- Real analysis: who has covered this topic, what's their angle, what's OUR angle (Mical's unique perspective)

**Checklist**:
- `spec_complete: true`, all others `false`

---

## Deliverable 2 (P0): Filled Enablement Path

**Output**: `/home/mical/fde/enablement/paths/[RIU-ID]-[topic-slug].md`

Use the topic slug from whatever topic you chose. Example: if you chose RIU-082 on guardrails, the file would be `RIU-082-ai-guardrails.md`.

### Requirements

1. Take the **Learner Mode** template from `video-enablement.md` (the section between the first pair of triple backticks under "LEARNER MODE")
2. Replace ALL `{{parameters}}` with the concrete values from your filled video spec
3. The youtube_link can be a placeholder like `https://youtube.com/watch?v=PENDING` — that's the one exception since the video isn't recorded yet
4. All difficulty level steps must be filled with real, numbered steps
5. All failure modes must be filled with specific, practical warnings
6. The verification sections at each level must be present (they're in the template — don't remove them)
7. The "AFTER YOU BUILD" section must reference the exact confidence_baseline_task from the spec
8. The "WHAT'S NEXT" section must have filled routing (next_if_clicked, next_if_hard, constellation map)
9. The footer must have the real RIU ID, knowledge entry IDs, today's date, and status

---

## Deliverable 3 (P1): Topic Rationale

In the same commit or alongside the two files, write a brief explanation (can be at the top of VIDEO_SPEC_001.yaml as YAML comments, or as a separate section):

1. **What signal drove this topic** — which person/company, what they said/shipped
2. **Why it's a strong first video** — what makes it compelling for a debut, how it showcases Mical's unique angle
3. **How it maps to market demand** — which of the 9 requirements from LEARNING_FROM_THE_BEST.md does this topic demonstrate

---

## Quality Bar

The spec and path are ready when:

- [ ] Every field in VIDEO_SPEC_001.yaml is filled. Zero empty strings. Zero placeholders.
- [ ] The enablement path has all `{{parameters}}` replaced with concrete text.
- [ ] A complete beginner could follow Quick Start in 5 minutes and produce something real.
- [ ] Applied produces something a developer would use at work tomorrow.
- [ ] Production output would impress a hiring manager at OpenAI, Anthropic, or Mistral.
- [ ] Failure modes at all three levels are specific enough that a learner thinks "oh, I almost did that" — not generic warnings.
- [ ] The confidence baseline task is specific, re-askable, and measurable (1-5 scale makes sense for it).
- [ ] The hook script sounds like real human speech, not marketing copy.
- [ ] The title is under 53 characters (counted).
- [ ] The constellation map uses real RIU references and the correct position markers (this/next/upcoming).
- [ ] next_if_clicked and next_if_hard reference real RIUs from the taxonomy with meaningful relationship descriptions.
- [ ] The topic rationale explains signal, uniqueness, and market fit.

---

## How to Reply

1. Create the `specs/` directory: `/home/mical/fde/enablement/agentic-enablement-system/content-engine/specs/`
2. Write VIDEO_SPEC_001.yaml to that directory
3. Write the enablement path to `/home/mical/fde/enablement/paths/[RIU-ID]-[topic-slug].md`
4. Update `CODEX_STATUS.md` with progress
5. Message back on the bus when complete
