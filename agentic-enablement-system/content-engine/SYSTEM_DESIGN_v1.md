# Content Engine — System Design v1
# Status: REVIEW — refined from v0 based on Mical's design decisions
# Date: 2026-03-25
# Location: enablement/agentic-enablement-system/content-engine/

---

## What Changed from v0

| Decision | v0 | v1 |
|----------|----|----|
| Enablement delivery | Library of individual path markdown files | **One parameterized skill** (wire contract pattern) |
| Artifacts location | `palette/skills/enablement/paths/` | **`pretendhome/enablement/`** |
| Competition system | competitor_intelligence.yaml + routing logic | **Context only** — 4 profiles as reference, no system |
| Video format | Tutorials with multiple formats | **Every video = how to do X** → maps to RIU → enablement path |
| New infra | 6 new components | **Minimal** — post-production pipeline + one skill + video spec template |
| Core principle | Build new alongside existing | **Reinforce existing** — Palette IS the engine, never drift |

---

## What This Is

A content engine that turns Palette's existing signal network into YouTube videos. Each video teaches how to do one thing, maps to one RIU, and links to one enablement path that any viewer runs in any LLM tool.

**It is NOT a separate project from enablement. It IS enablement — with a camera on.**

**It is NOT a new system. Palette IS the content engine. The signal network, taxonomy, knowledge library, and agents already do this work. The only new piece is the camera and the skill that generates the viewer's enablement experience.**

---

## The Core Loop

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│   SIGNAL        What are people talking about?          │
│   (people library 21 profiles + company signals 43)     │
│       ↓                                                 │
│   CLASSIFY      Which RIU handles this? (create if new) │
│   (resolver + taxonomy 121 RIUs)                        │
│       ↓                                                 │
│   RESEARCH      What do we already know? What's new?    │
│   (knowledge library 167 entries → then Perplexity)     │
│       ↓                                                 │
│   BUILD         Actually do the thing on camera          │
│   (5-10 min, screen recording, "how to do X")          │
│       ↓                                                 │
│   PRODUCE       AI post-production pipeline              │
│   (OBS → Descript → CapCut → Leonardo AI, ~$4/video)   │
│       ↓                                                 │
│   PUBLISH       YouTube + enablement path in description │
│       ↓                                                 │
│   ENABLE        Viewer pastes the path into any LLM     │
│   (one skill, parameterized, works everywhere)          │
│       ↓                                                 │
│   FEEDBACK      Views, subs, GitHub downloads            │
│   (feeds back into signal monitoring)                   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## How It Maps to Existing Palette Components

| Engine Stage | Palette Component | Status |
|-------------|-------------------|--------|
| Signal | People Library (21 profiles, 7 clusters) | EXISTS |
| Signal | Company Signals (43 tools, 3 tiers) | EXISTS |
| Classify | Taxonomy (121 RIUs) | EXISTS |
| Classify | Resolver agent | EXISTS |
| Research | Knowledge Library (167 entries) | EXISTS |
| Research | Researcher agent (Perplexity backend) | EXISTS |
| Build | Mical builds live on camera | HUMAN |
| Produce | Post-production pipeline | **NEW** (tools selected, workflow defined) |
| Publish | YouTube + GitHub | **NEW** (accounts exist, structure needed) |
| Enable | **Video Enablement Skill** | **NEW** (one skill, parameterized) |
| Enable | Enablement Coach (meta-system) | EXISTS |
| Feedback | Monitor agent | EXISTS |

**What's actually new**: Post-production workflow, one parameterized enablement skill, video spec template. That's it. Everything else exists.

---

## Component 1: Signal → Topic Selection

### Signal sources (all existing)

**People Library** — 21 profiles, 7 clusters. When someone in the network signals something (new tool, new approach, funding round), that's a potential video topic.

**Company Signals** — 43 tools in 3 tiers. When a tool ships an update, raises a round, or gets acquired, that's a potential video topic.

**Taxonomy gaps** — When a signal doesn't map to an existing RIU, that gap IS the video. Create the RIU, build the thing, film it.

### Signal-to-topic routing

When a signal fires:

1. **Does an RIU exist for this?**
   - YES → route through existing knowledge library, check if we have depth
   - NO → create a new RIU (the video IS the creation process)

2. **Can this be built live in 5-10 minutes?**
   - YES → video candidate
   - NO → break into series, or find the 5-min slice

3. **Does this map to something a viewer can do themselves?**
   - YES → full video + enablement path
   - NO → skip (commentary/news without enablement is off-brand)

### Competitor awareness (context only, no system)

We have 4 profiles as context (Nate Jones, Matthew Berman, VelvetShark, Alex Finn). Use them informally when evaluating topics — "is this already well-covered?" — but there is no competitor_intelligence.yaml, no routing logic, no YAML structure. Just awareness.

If we need to add more competitor context later, append to a section in the project brief. No separate data structure.

---

## Component 2: The Video Enablement Skill (the key new piece)

### Design Philosophy

**One skill. Parameterized. Like the wire contract.**

Instead of a library of dozens of path markdown files (v0), there is ONE skill that takes parameters and generates the enablement experience dynamically. The LLM inference does the work at runtime — we don't pre-author every path.

This follows the exact pattern from `agents/researcher/researcher.py` — the skill defines what parameters it accepts, what it does with them, and what it outputs. The payload is the extension point.

### The Skill (Split into Three Files — v2.1)

Split from the original `video-enablement.md` into three purpose-specific files:
- `content-engine-spec.md` — canonical schema, wire contract, quality bar, publishing rules
- `path-template.md` — parameterized learner template + filled example
- `creator-mode.md` — standalone educator prompt

```markdown
# Video Enablement — Paste-Into-Any-LLM Skill

> Copy everything below the line and paste it as your first message
> in Claude, ChatGPT, Cursor, Codex, or any AI chat tool.

---

## PASTE THIS INTO YOUR AI TOOL

You are a hands-on guide helping me build something real.

**Topic**: {{topic}}
**What I'll build**: {{output_description}}
**RIU**: {{riu_id}} — {{riu_name}}
**Video**: {{youtube_link}}

**Rules**:
- Start by asking me 2-3 quick questions to understand my situation
- Walk me through building this step by step
- At each step, show me what to do and wait for me to try
- Keep it practical — I want a working output, not a lecture
- Use plain language. If you need a technical term, explain it first.

**Difficulty** (ask me which I want):

### Quick Start (5 minutes)
{{quick_start_goal}}
{{quick_start_example}}
{{quick_start_steps}}

### Applied (15-30 minutes)
{{applied_goal}}
{{applied_steps}}
{{applied_check}}

### Production (30-60 minutes)
{{production_goal}}
{{production_steps}}
{{production_extends}}

**Start by asking which difficulty I want, then ask your context questions.**
```

### How Parameters Get Filled

The parameters are filled at video creation time — when Mical creates a video, he fills the video spec (Component 3), and the spec includes the enablement path content. The `{{placeholders}}` become concrete text.

This is NOT a code template that gets rendered by a build system. It's a **skill pattern** — Mical (or a Narrator agent) fills in the parameters for each video's topic, and the result is a single markdown file that goes in the YouTube description or on GitHub.

### Wire Contract Alignment

The skill maps to a HandoffPacket:

```yaml
# HandoffPacket for video-enablement
id: "ve-001"
from: "narrator"
to: "enablement"
task: "Generate enablement path for video: Building a Taxonomy"
riu_ids: ["RIU-401"]
payload:
  topic: "Building a Taxonomy"
  output_description: "A working taxonomy that organizes any domain"
  youtube_link: "https://youtube.com/watch?v=xxx"
  difficulty_levels:
    quick_start:
      goal: "A 2-level hierarchy with 8-15 items"
      example: "Organize your kid's sports activities"
      steps: ["Pick something to organize", "List everything", "Group into 3-5 categories", "Name each category", "Verify: one item per category"]
    applied:
      goal: "A 3-level hierarchy for your professional domain"
      steps: ["Tell me about your domain", "Identify top-level categories", "Break into subcategories", "List items", "Test with 5 real inputs"]
      check: "Can you classify 10 random items? If >2 don't fit, refine."
    production:
      goal: "A machine-readable taxonomy with routing logic"
      steps: ["Start from Applied output", "Add unique IDs", "Add AI-readable descriptions", "Add routing hints", "Test with AI classification"]
      extends: "This can become the backbone of a multi-agent system"
```

### What This Means in Practice

For every video Mical makes:

1. He fills a video spec (Component 3) which includes the enablement parameters
2. The Narrator agent (or Mical manually) generates the filled-in skill markdown
3. That markdown goes in the YouTube description + on GitHub as a standalone file
4. A viewer copies it, pastes it into any LLM, and gets walked through doing what Mical just demonstrated
5. The LLM inference does all the personalization at runtime — asking the viewer about their context, adapting to their level, checking their work

**No path library to maintain. No versioning problem. No tech debt. One skill, parameterized per video.**

### How It Connects to the Enablement Coach

```
Viewer watches YouTube video
    ↓
Grabs the enablement path from description/GitHub
    ↓
Pastes into any LLM → builds one thing, gets one output
    ↓
Wants more? → discovers the full enablement-coach.md
    ↓
Coach builds their personal lens, routes them deeper
    ↓
Over time, they build their own Palette
```

The per-video paths are **top of funnel**. The enablement coach is **retention**. YouTube drives discovery, paths prove value, the coach creates ongoing engagement.

---

## Component 3: Video Spec Template

When a signal is identified and routed to an RIU, generate a video spec:

```yaml
# Video Spec
# Generated from signal → RIU classification

signal:
  source: "PERSON-019 Andrej Karpathy"
  type: "influencer_post"  # influencer_post | tool_update | funding | taxonomy_gap
  summary: "Posted about tokenization gaps in non-English languages"

classification:
  riu: "RIU-401"
  riu_name: "Taxonomy Design"
  knowledge_entries: ["LIB-045", "LIB-067"]  # relevant existing knowledge
  new_knowledge: false  # will this video add a new knowledge entry?

video:
  title: "Why your AI can't understand French (a linguist explains)"
  title_chars: 54
  title_formula: "curiosity-gap + authority-signal"
  duration_target: 7  # minutes

  thumbnail:
    face: determined
    visual: "tokenization diagram showing French vs English"
    text: "AI CAN'T READ THIS"  # 2-4 words, curiosity gap
    palette: blue-orange

  hook:
    formula: bold-claim  # cold-open | bold-claim | best-moment | problem-promise | contrarian
    script: |
      "Most AI models are secretly terrible at non-English languages.
      And I can prove it in 30 seconds."
      [show tokenization comparison on screen]

  build:
    what_to_build: "Tokenization comparison demo"
    tools_needed: [terminal, Python, tiktoken]
    difficulty_on_camera: "Level 1 — keep it simple, viewer does deeper in the path"

enablement:
  topic: "Understanding and Testing AI Tokenization"
  output_description: "A tokenization analysis for your language or domain"
  quick_start:
    goal: "Tokenize your name in 3 languages and see the difference"
    example: "Compare 'hello' vs 'bonjour' vs 'こんにちは' token counts"
    steps:
      - "Pick 3 words in different languages (or domains)"
      - "Use the tokenizer tool to count tokens for each"
      - "Compare: which language uses more tokens? Why?"
  applied:
    goal: "Analyze tokenization efficiency for your business domain"
    steps:
      - "Identify 20 key terms from your domain"
      - "Tokenize each across 2-3 models"
      - "Find which terms are undertokenized (more tokens = more cost)"
      - "Estimate cost impact on your AI usage"
    check: "Can you predict which of your terms will be expensive before tokenizing?"
  production:
    goal: "Build a language-aware routing layer"
    steps:
      - "Create a tokenization benchmark for your full domain vocabulary"
      - "Map token efficiency by model per language"
      - "Build routing logic: send French text to the model that tokenizes it best"
      - "Test with 50 real inputs from your data"
    extends: "This becomes a cost optimizer for multilingual AI systems"

post_production:
  workflow: B  # A ($0, 50-70min) | B ($4, 30-40min) | C ($8.50, 25-35min)
  ai_images_needed: 2  # tokenization diagrams via Leonardo AI
  estimated_cost: "$4"
  estimated_edit_time: "35 min"

competitor_context: |
  Karpathy has touched on tokenization (briefly, math-focused).
  3Blue1Brown covered the math angle.
  Nobody has covered it from a comparative linguistics perspective.
  Our angle: 4 languages, practitioner experience, "linguist explains" authority.
```

---

## Component 4: Post-Production Pipeline

### Recommended: Workflow B (~$4/video, 30-40 min editing)

```
RAW RECORDING                    EDIT                           POLISH                    PUBLISH
─────────────────────────────────────────────────────────────────────────────────────────────────
OBS Studio (free)          →     Descript ($16/mo)         →   CapCut (free)         →  YouTube
- Screen + webcam                - Auto-transcribe              - Final color/audio
- 1080p or 4K                    - Cut silences (text edit)     - Transitions
- Local recording                - Remove filler words          - B-roll insert points
                                 - Auto-captions (burned-in)    - Background music
                                                                - Export 4K

                                                           →   Leonardo AI (free tier)
                                                                - 2-4 diagrams/images
                                                                - Thumbnail variations
```

### Cost Breakdown (4 videos/month)

| Tool | Monthly | Per Video |
|------|---------|-----------|
| OBS Studio | $0 | $0 |
| Descript Creator | $16 | $4 |
| CapCut (free tier) | $0 | $0 |
| Leonardo AI (free tier) | $0 | $0 |
| **Total** | **$16/mo** | **~$4/video** |

### Time Per Video

| Step | Time |
|------|------|
| Record (screen + talking head) | 15-25 min raw for 5-10 min final |
| Import to Descript + auto-edit | 5 min |
| Review/adjust Descript cuts | 10-15 min |
| CapCut polish (transitions, music, color) | 10-15 min |
| Generate images (Leonardo AI) | 5 min |
| Generate thumbnail variations | 5 min |
| Upload + metadata + enablement path | 10 min |
| **Total** | **~60-80 min per video** (including recording) |

---

## Component 5: Distribution

### Primary: YouTube
- 5-10 minute videos, 1x/week
- Each video description includes the full enablement path (paste-ready)
- Link to GitHub for the markdown source
- YouTube Shorts cut from key moments (AI-extracted via Descript)

### Secondary: GitHub
- `github.com/pretendhome/enablement/content-engine/paths/` — generated paths per video
- Each is a standalone markdown file named `{riu-id}-{topic-slug}.md`
- Not a library to maintain — each file is generated once when the video publishes
- Metric: stars, forks, raw file views

### Tertiary: Social
- Clips → Twitter/LinkedIn (Descript auto-clips)
- Newsletter (later, only if traction warrants)

---

## Component 6: Feedback Loop

```
YouTube analytics (views, CTR, retention, subs)
    ↓
Which topics performed? → weight those signal clusters higher
Which dropped off? → analyze hook/content/length
    ↓
GitHub metrics (stars, forks, raw file views)
    ↓
Which paths are most downloaded? → more videos at that difficulty
    ↓
Comments
    ↓
What are viewers asking for? → direct signal for next videos
    ↓
Feed back into Signal Monitor → next cycle
```

---

## File Structure

```
pretendhome/
├── enablement/
│   ├── agentic-enablement-system/
│   │   ├── content-engine/
│   │   │   ├── SYSTEM_DESIGN_v1.md              ← this file
│   │   │   ├── SYSTEM_DESIGN_v0.md              (superseded)
│   │   │   ├── content-engine-spec.md            ← canonical schema + wire contract
│   │   │   ├── path-template.md                 ← learner template + filled example
│   │   │   ├── creator-mode.md                  ← standalone educator prompt
│   │   │   ├── video-enablement.md              (redirect → three files above)
│   │   │   └── video-spec-template.yaml         ← blank spec template
│   │   └── onboarding/
│   │       ├── enablement-coach.md
│   │       ├── elia-quickstart.md
│   │       └── elia-session-plan.md
│   └── paths/                                    ← generated per-video paths
│       ├── RIU-401-building-a-taxonomy.md
│       ├── RIU-XXX-tokenization-multilingual.md
│       └── ...                                   (one per published video)
│
├── implementations/
│   └── youtube-exploration/                      ← research + planning artifacts
│       ├── PROJECT_INDEX.md
│       ├── phase-1-research/                     (4 profiles)
│       ├── phase-3-content/                      (formula + hooks)
│       └── phase-4-production/                   (pipeline research)
│
└── palette/                                      ← THE system (untouched)
    ├── taxonomy/                                 (121 RIUs)
    ├── knowledge-library/                        (167 entries)
    ├── buy-vs-build/people-library/              (21 profiles, 43 tools)
    ├── agents/                                   (11 agents)
    ├── skills/enablement/enablement-coach.md     (meta-system, top-of-funnel destination)
    └── sdk/                                      (wire contract, HandoffPacket)
```

---

## What Needs to Be Built (Ranked)

| # | Component | Effort | Status |
|---|-----------|--------|--------|
| 1 | `content-engine-spec.md` + `path-template.md` + `creator-mode.md` — split from video-enablement.md v2.1 | Small | **COMPLETE** |
| 2 | `video-spec-template.yaml` — blank spec | Small | **COMPLETE** |
| 3 | Post-production pipeline setup (install OBS, Descript account) | Small | Tools selected |
| 4 | First video spec (fill template for Video #1) | Small | Needs topic selection |
| 5 | First enablement path (generate from Video #1 spec) | Small | Follows from #4 |
| 6 | YouTube channel setup | Small | Whenever ready |
| 7 | First video (record + produce + publish) | Medium | Follows from #3-6 |

---

## What Already Exists (the 80%)

- People library (21 profiles, 7 clusters) → signal source
- Company signals (43 tools, 3 tiers) → signal source
- Taxonomy (121 RIUs) → classification backbone
- Knowledge library (167 entries) → research depth
- 11 agents → resolver classifies, researcher fills gaps, narrator scripts, validator checks
- Enablement coach (canonical, tested with Elia) → retention system
- Wire contract (HandoffPacket/HandoffResult) → parameterization pattern
- SDK (Python + Go, 86 tests) → programmatic access
- Governed message bus (broker + 4 peers) → multi-agent coordination
- YouTube formula research (thumbnails, titles, hooks, branding) → production playbook
- Competitor profiles (4 profiles) → landscape awareness
- GitHub repo (public) → distribution channel
- VPS + Telegram bot → automation infrastructure

## What's New (the 20%)

- Content engine skill (split v2.1): `content-engine-spec.md` + `path-template.md` + `creator-mode.md` — parameterized skill with learner mode, creator mode, constellations, adaptive debrief, publishing rules — **BUILT**
- `video-spec-template.yaml` — blank template connecting signal → video → enablement — **BUILT**
- `LEARNING_FROM_THE_BEST.md` — requirements extracted from OpenAI/Anthropic/Mistral job specs, applied to our system — **BUILT**
- Post-production workflow (OBS + Descript + CapCut + Leonardo AI)
- Per-video generated paths (output of the skill, one per published video)
- YouTube channel

---

## Design Principles (from Mical's decisions)

1. **One system.** Palette IS the content engine. No parallel infrastructure.
2. **One skill, parameterized.** Like the wire contract — same base, different payload per video.
3. **Reinforce, don't rebuild.** Every iteration makes Palette better. Never drift.
4. **Every video maps to an RIU.** If there's no RIU, create one. The taxonomy grows organically.
5. **Not tutorials — enablement.** "Watch this 5 min video, then do whatever you want by following the instructions in the description."
6. **Expandable difficulty.** Quick Start (5 min) → Applied (15-30 min) → Production (30-60 min). Viewer chooses.
7. **Any LLM.** The enablement path works in Claude, ChatGPT, Cursor, Codex — anything that accepts text input.
8. **Minimize tech debt.** No path library to version. No competition system to maintain. Generated files, not maintained ones.

---

## Open Questions (reduced from v0)

1. **Path hosting**: YouTube description (full text) vs GitHub link vs both? Recommendation: both — full text in description for zero-friction, GitHub for discoverability and stars metric.

2. **Shorts strategy**: AI-extract 30-60 second clips from each video for YouTube Shorts? Descript does this automatically. Nearly free. Probably yes.

3. **Multilingual**: Write paths in EN first. FR/IT/ES later only if audience data shows demand. The linguistic authority comes from the video content, not from translated paths.

4. **Video cadence**: 1x/week sustainable? Or start 2x/month and ramp? Depends on how fast post-production gets.
