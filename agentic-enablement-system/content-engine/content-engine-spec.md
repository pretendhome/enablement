# Content Engine Specification
# Version: 2.1
# Location: enablement/agentic-enablement-system/content-engine/content-engine-spec.md
# Status: Canonical — this file owns the parameter schema, quality bar, and publishing rules
# Related: path-template.md (render target), creator-mode.md (creator UX layer)

## What This Is

A parameterized skill that generates AI-native learning experiences from YouTube videos. One skill, infinite topics. The LLM inference does the work at runtime — personalizing to each learner's context, verifying their output, measuring whether they actually learned, and routing them to what's next.

Works in any tool that accepts text: Claude, ChatGPT, Cursor, Codex, Windsurf, or anything else.

**Design thesis**: Every video is a working demo of an enablement system that teaches, verifies, measures, routes, and improves.

## How to Use

**For each video Mical publishes:**

1. Fill the video spec template (`video-spec-template.yaml`) with the video's parameters
2. Copy the Learner Mode template from `path-template.md`
3. Replace all `{{parameters}}` with the values from the spec
4. Push the filled path to GitHub as `enablement/paths/RIU-XXX-topic-slug.md`
5. Link the path in the YouTube video description

**For educators who want to create their own paths:**

1. Copy the Creator Mode prompt from `creator-mode.md`
2. Paste it into any LLM
3. Answer the questions — the LLM generates a complete path

---

## One Contract, Three Surfaces

| File | Audience | Role |
|------|----------|------|
| `content-engine-spec.md` | System / internal | Owns canonical schema, quality bar, wire contract, publishing rules |
| `path-template.md` | Viewers / learners | Render target — parameterized template + filled example |
| `creator-mode.md` | Educators / creators | Standalone creation interface — maps back to this schema |

**Rule**: If a parameter exists in this spec, the template and creator mode must honor it. No independent parameters. No format logic duplicated across files.

---

## Path Constellations

Constellations are named learning arcs that connect individual paths into identity-forming progressions. Each path belongs to one or more constellations. The constellation name and position appear in the path header and What's Next section.

**Canonical data source**: `constellations.yaml` (machine-readable). The markdown tables below are the human-readable view. On conflict, `constellations.yaml` wins.

### Defined Constellations

| Constellation | Arc | Paths (in order) |
|---|---|---|
| **Organize → Retrieve → Route** | From structuring knowledge to using it in AI systems | Taxonomy Design → Knowledge Library → Multi-Agent Routing |
| **Prompt → Guardrail → Monitor** | From basic AI use to production safety | Writing AI Instructions → Guardrails & Safety → Monitoring & Observability |
| **Clarify → Evaluate → Automate** | From problem definition to automated solutions | Convergence Brief → Service Evaluation → Integration Recipes |
| **Build → Test → Ship** | From prototype to production | Prompt Interface Contract → Eval Harness → Deployment Readiness |
| **Signal → Story → System** | From noticing a trend to building infrastructure around it | Signal Monitoring → Content Strategy → Enablement Architecture |

New constellations emerge as paths are published. A path can belong to multiple constellations.

### Current RIU Assignments

Only constellations with concrete RIU mappings are listed. Unmapped slots are aspirational until a video spec assigns them.

| Constellation | Position | Topic | RIU | Path Status |
|---|---|---|---|---|
| **Build → Test → Ship** | 1 | Prompt Interface Contract | RIU-022 | planned |
| **Build → Test → Ship** | 2 | Golden Set + Offline Eval Harness | RIU-021 | **published** |
| **Build → Test → Ship** | 3 | Deployment Readiness Envelope | RIU-060 | planned |
| **Organize → Retrieve → Route** | 1 | Taxonomy Design | RIU-401 | example only |
| **Clarify → Evaluate → Automate** | 1 | Convergence Brief | RIU-001 | planned |

Routing targets referenced in published paths but not yet assigned to a constellation slot:

| RIU | Topic | Referenced From |
|---|---|---|
| RIU-524 | LLM Output Quality Monitoring | RIU-021 next_if_clicked |

### Display Rule

- Always show the constellation name in the path header: `Part of: Build → Test → Ship`
- Only show the detailed position map (YOU ARE HERE / Next / Then) when **at least 2 nodes** have published paths
- When fewer than 2 are published, show the constellation name only — no map with mostly "coming soon" placeholders

---

## Publishing Rules

Deterministic routing for published vs unpublished paths:

1. **Live links only** when the path file exists at `enablement/paths/RIU-XXX-topic-slug.md`
2. **"Coming soon"** when the path is planned but not yet published — use: `→ [Topic] (coming soon)`
3. **Newsletter CTA** when referencing unreleased content in contexts where it helps: `→ Join the newsletter for launch updates`
4. **No broken links**: Every hyperlink in a published path must resolve

This rule applies to:
- What's Next routing in paths
- Constellation maps
- Cross-path references
- Video descriptions

---

## Video Lineup

Approved channel launch order (2026-03-25):

| Position | Type | Purpose |
|----------|------|---------|
| 1 | Identity / multi-agent | Establishes who Mical is and why this channel exists |
| 2 | Comparison / search discovery | Algorithm-friendly, broad appeal |
| 3 | Token costs / practical | Immediately useful, shareworthy |
| 4 | Taxonomy / linguistics | Unique angle, differentiated |
| 5 | Enablement demo | Meta-video showing the system itself |

**Principle**: Identity first, search optimization second. The first public video says "I built a real thing and I can explain what broke" — not "I also evaluate tools."

**Note**: The first *generated* proof artifact (RIU-021) is separate from the first *public* video. These are different decisions.

---

## Provenance

**Learner-facing** (visible in path footer):
```
Based on the Palette Knowledge Library
```

**System-level** (HTML comment or footer metadata):
```html
<!-- Source: RIU-XXX | Knowledge: LIB-XXX, LIB-YYY | Engine: v2.1 -->
```

Rationale: Provenance is part of the trust story. Visible structure is a differentiator. But learners don't need raw IDs inline.

---

## Feedback Capture (MVP)

Google Form — 7 fields:

**Required** (click/select):
1. Path name (dropdown)
2. Level completed (Quick Start / Applied / Production)
3. Confidence before (1-5)
4. Confidence after (1-5)

**Optional** (text):
5. What was the hardest part?
6. What did you build? (proof-of-work — strongest signal)
7. What would you build next?

If constrained to 6 fields, merge 6 and 7 into one textarea. Prioritize artifact capture over intent.

---

## Adaptive AFTER YOU BUILD

The post-build sequence adapts by level to reduce completion friction while preserving learning signals.

### Mandatory for all levels

1. **Confidence delta**: Re-rate 1-5 against the exact same baseline question. Report the delta and name what drove it.
2. **Summary sentence**: "Today I built [what] which does [purpose]. The key design decision was [choice]. My confidence moved from [X] to [Y]."

### Mandatory for Applied and Production

3. **Friction capture**: "What was the single hardest part? Not the longest — the part where you felt most uncertain."

Then ask: "Want the full debrief (2 more quick questions) or are you good?"

### Optional debrief branch (all levels)

4. **Artifact capture**: "Describe what you built in 1-2 sentences, or paste a link if you saved it somewhere."
5. **Next pull**: "If you could build one more thing with this skill, what would it be?"

### Summary table

| Step | Quick Start | Applied | Production |
|------|-------------|---------|------------|
| 1. Confidence delta | mandatory | mandatory | mandatory |
| 2. Summary sentence | mandatory | mandatory | mandatory |
| 3. Friction capture | opt-in via debrief | mandatory | mandatory |
| 4. Artifact capture | opt-in via debrief | opt-in via debrief | mandatory |
| 5. Next pull | opt-in via debrief | opt-in via debrief | opt-in via debrief |

**Principle**: Do not force a long debrief on low-commitment learners. Preserve richer signals when the learner has momentum.

---

## Quality Bar

A path is ready to publish when:

- [ ] Quick Start finishes in 5 minutes with a real artifact in hand
- [ ] Applied produces something the learner would use at work tomorrow
- [ ] Production output would survive a peer review or impress a hiring manager
- [ ] Verification tests understanding and reasoning, not recall
- [ ] Common failure modes are specific enough that a learner thinks "oh, I almost did that"
- [ ] Confidence baseline question is specific to THIS skill (not generic)
- [ ] The delta measurement at the end references the exact same baseline question
- [ ] Works in any AI tool — uses only plain text conversation
- [ ] Plain language throughout — no jargon without explanation, no "it's simple"
- [ ] All What's Next links resolve (live paths) or use "coming soon" routing
- [ ] Provenance line present in footer
- [ ] System IDs in HTML comment or footer metadata only

---

## Wire Contract

The enablement skill maps to Palette's HandoffPacket:

```yaml
# HandoffPacket for video-enablement v2.1
id: "ve-{{sequence}}"
from: "narrator"
to: "enablement"
task: "Generate enablement path for video: {{topic}}"
riu_ids: ["RIU-{{riu_id}}"]
payload:
  mode: "learner"  # learner | creator
  version: "2.1"

  # --- Metadata ---
  topic: "{{topic}}"
  output_description: "{{output_description}}"
  concept_summary: "{{concept_summary}}"
  youtube_link: "{{youtube_link}}"
  kl_entry_ids: ["LIB-XXX", "LIB-YYY"]
  date: "{{date}}"
  review_status: "current"  # draft | reviewed | current

  # --- Confidence ---
  confidence_baseline_task: "{{task phrased as a capability question}}"

  # --- Constellation ---
  constellation:
    name: "{{name}}"  # e.g., "Organize → Retrieve → Route"
    sequence: "{{position}} of {{total}}"
    map:
      - { position: 1, topic: "...", riu: "RIU-XXX", status: "this|next|upcoming|done" }

  # --- Difficulty levels ---
  difficulty_levels:
    quick_start:
      output: "..."
      example: "..."
      steps: [...]
      failure_modes: [...]
    applied:
      output: "..."
      steps: [...]
      failure_modes: [...]
    production:
      output: "..."
      steps: [...]
      failure_modes: [...]

  # --- Routing ---
  next_if_clicked:
    - { riu: "RIU-XXX", topic: "...", relationship: "..." }
  next_if_hard:
    - { riu: "RIU-XXX", topic: "...", relationship: "..." }
```

HandoffResult returns the filled markdown path, ready to publish.

---

## Parameter Reference

| Parameter | Source | Example |
|-----------|--------|---------|
| `{{topic}}` | video spec → `enablement.topic` | "Building a Taxonomy" |
| `{{youtube_link}}` | Published video URL | "https://youtube.com/watch?v=XXXXX" |
| `{{output_description}}` | video spec → `enablement.output_description` | "A working taxonomy that organizes any domain" |
| `{{output_description_short}}` | Brief version for onramp | "a working taxonomy" |
| `{{concept_summary}}` | 1-2 sentences from video script | "A taxonomy is how you teach a system to classify anything consistently." |
| `{{confidence_baseline_task}}` | Skill phrased as capability | "organize a messy domain into clean, non-overlapping categories" |
| `{{riu_id}}` | video spec → `classification.riu` | "401" |
| `{{kl_entry_ids}}` | video spec → `classification.knowledge_entries` | "LIB-045, LIB-067" |
| `{{date}}` | Publication date | "2026-03-25" |
| `{{review_status}}` | Content lifecycle | "draft", "reviewed", or "current" |
| `{{constellation_name}}` | Which learning arc | "Organize → Retrieve → Route" |
| `{{constellation_sequence}}` | Position in arc | "1 of 3" |
| `{{quick_start_output}}` | Concrete artifact | "A 2-level hierarchy with 8-15 items" |
| `{{quick_start_example}}` | Universal daily-life example | "Organize your kid's sports activities" |
| `{{quick_start_steps}}` | Numbered steps | 3-6 clear steps |
| `{{quick_start_failure_modes}}` | What goes wrong | Specific, practical warnings |
| `{{applied_output}}` | Work-relevant artifact | "A 3-level hierarchy for your professional domain" |
| `{{applied_steps}}` | Numbered steps | 4-8 guided steps |
| `{{applied_failure_modes}}` | What goes wrong | Specific to this level |
| `{{production_output}}` | Portfolio-grade artifact | "A YAML taxonomy with IDs and routing logic" |
| `{{production_steps}}` | Numbered steps | 5-10 detailed steps |
| `{{production_failure_modes}}` | What goes wrong | Specific to production use |
| `{{next_if_clicked}}` | Forward routing links | 2-3 related deeper paths |
| `{{next_if_hard}}` | Backward routing links | 1-2 foundational paths |
| `{{constellation_routing}}` | Constellation position display | See display rule above |
| `{{routing_targets}}` | Machine-readable routing for validator | "RIU-022(coming-soon), RIU-060(live)" |
| `{{feedback_form_link}}` | Google Form URL | "https://forms.gle/XXXXX" |
