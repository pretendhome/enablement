# Content Engine — System Design v0
# Status: DRAFT — iterating with Mical
# Date: 2026-03-25
# Location: enablement/agentic-enablement-system/content-engine/

---

## What This Is

A content engine that turns Palette's existing signal network into YouTube videos, where each video connects to an expandable enablement path that any viewer can run in any LLM tool.

**It is NOT a separate project from enablement. It IS enablement — with a camera on.**

---

## The Core Loop

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│   SIGNAL        What are people talking about?          │
│   (people library + competitor intel)                   │
│       ↓                                                 │
│   CLASSIFY      Which RIU handles this? (create if new) │
│   (resolver + taxonomy)                                 │
│       ↓                                                 │
│   RESEARCH      What do we already know? What's new?    │
│   (knowledge library → then web)                        │
│       ↓                                                 │
│   BUILD         Actually do the thing (this IS the video)│
│   (5-10 min, screen recording)                          │
│       ↓                                                 │
│   PRODUCE       AI handles editing, captions, images     │
│   (post-production pipeline, <$20/video)                │
│       ↓                                                 │
│   PUBLISH       YouTube + GitHub path                    │
│       ↓                                                 │
│   ENABLE        Viewer grabs the path, runs it themselves│
│   (any LLM: Claude, ChatGPT, Codex, Cursor)            │
│       ↓                                                 │
│   FEEDBACK      Views, subs, GitHub downloads, comments  │
│   (feeds back into signal monitoring)                   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## How It Maps to Existing Palette Components

| Engine Stage | Palette Component | Status |
|-------------|-------------------|--------|
| Signal | People Library (21 profiles, 7 clusters) | EXISTS |
| Signal | Company Signals (43 tools) | EXISTS |
| Signal | Competitor Intelligence (AI YouTubers) | NEW |
| Classify | Taxonomy (117 RIUs) | EXISTS |
| Classify | Resolver agent | EXISTS (design spec) |
| Research | Knowledge Library (167 entries) | EXISTS |
| Research | Researcher agent (Perplexity backend) | EXISTS (Python) |
| Build | Mical builds live | HUMAN |
| Produce | Post-production pipeline | NEW (researching) |
| Publish | YouTube + GitHub | NEW (accounts needed) |
| Enable | Enablement paths | NEW (format designed below) |
| Enable | Enablement coach | EXISTS (canonical) |
| Feedback | Monitor agent | EXISTS (design spec) |

**What's actually new**: Competitor intelligence, post-production pipeline, enablement paths, and the routing logic that connects them. Everything else exists.

---

## Component 1: Signal Monitor

### What it watches

**People Library (existing, expandable)**
The 21 profiles organized in 7 clusters. Each person signals what matters in AI right now. When Ruben Hassid (774K LinkedIn) starts talking about a new tool, that's a signal. When Andrej Karpathy publishes a new approach, that's a signal. When a Lovable founder ships a feature, that's a signal.

**Expansion rules for people library:**
- High bar: must be a BUILDER or INVESTOR, not just a commentator
- Must produce original signal (not just resharing)
- Must be in a cluster or create a new one
- Target: 30-40 profiles (up from 21) to have 5-6 signals/week

**Company Signals (existing)**
43 tools in 3 tiers (integrate/evaluate/monitor). When a tool ships an update, raises a round, or gets acquired — that's a signal.

**Competitor Intelligence (NEW — separate from people library)**

AI YouTubers and content creators go here, NOT in the people library. Different purpose:
- People library = "what to cover" (signal sources)
- Competitor intel = "how to differentiate" (landscape awareness)

```yaml
# competitor_intelligence.yaml
metadata:
  version: "1.0"
  purpose: "Track AI content landscape to find gaps and avoid duplication"
  NOT: "These are not signal sources. They are competitive reference points."

competitors:
  - id: COMP-001
    name: Nate Jones
    handle: "@NateBJones"
    tier: 1  # >100K subs
    positioning: "AI news desk for executives"
    covers_well: [ai_strategy, career_impact, model_comparisons]
    covers_poorly: [implementation, multi_agent, knowledge_engineering]
    our_differentiation: "We build, he advises"

  - id: COMP-002
    name: Matthew Berman
    handle: "@matthew_berman"
    tier: 1
    positioning: "Daily AI news for generalists"
    covers_well: [ai_news, model_reviews, hardware]
    covers_poorly: [systems_architecture, production_deployment, enablement]
    our_differentiation: "We go deep where he goes wide"

  - id: COMP-003
    name: VelvetShark
    handle: "@velvetshark-com"
    tier: 3  # <25K subs but notable
    positioning: "Practitioner who builds with AI agents"
    covers_well: [openclaw, agent_workflows, honest_reviews]
    covers_poorly: [multi_agent_architecture, taxonomy, knowledge_engineering]
    our_differentiation: "We have the full system, he has one tool"

  - id: COMP-004
    name: Alex Finn
    handle: "@AlexFinn"
    tier: 2
    positioning: "Vibe coding for non-technical builders"
    covers_well: [claude_code, beginner_tutorials, vibe_coding]
    covers_poorly: [systems_design, production_architecture, enterprise]
    our_differentiation: "We teach the architecture, he teaches the shortcut"

  # ... expand as landscape evolves
```

### Signal-to-topic routing

When a signal fires:

1. **Is this already well-covered by a competitor?**
   - YES → skip, or find the angle they missed
   - NO → opportunity

2. **Does an RIU exist for this?**
   - YES → route through existing knowledge library
   - NO → create a new RIU (this keeps taxonomy current)

3. **Can this be built live in 5-10 minutes?**
   - YES → video candidate
   - NO → break into series, or cover conceptually

4. **Is there an expandable exercise here?**
   - YES → create a path
   - NO → news/commentary format (no path needed)

---

## Component 2: Expandable Paths

This is the key innovation. Every video that teaches something links to a path. A path is a single markdown file that a viewer pastes into any LLM and gets guided through doing what they just watched.

### Design Principles

1. **One file, any tool.** Works in Claude Projects, ChatGPT custom instructions, Codex CLI, Cursor, Windsurf — anything that accepts a system prompt or instructions.
2. **No installation required.** No git clone, no npm install, no dependencies.
3. **Expandable difficulty.** Every path has levels. You choose your depth.
4. **Produces a real output.** At every level, you walk away with something usable.
5. **Super user friendly.** If you can copy-paste, you can use it.

### Path Format

```markdown
# Path: [Topic Name]

> **Video**: [YouTube link]
> **What you'll build**: [One sentence — the output]
> **Time**: 5-60 minutes (you choose the depth)
> **Works in**: Claude, ChatGPT, Cursor, Codex, or any AI chat tool

---

## How to use this

1. Open your AI tool (Claude, ChatGPT, Cursor, etc.)
2. Start a new conversation
3. Copy everything below the line and paste it as your first message
4. Follow the guide — it will walk you through step by step

---

## ▶ PASTE THIS INTO YOUR AI TOOL

You are a hands-on guide helping me build [specific thing].

**My context**: [I'll tell you about myself when we start]

**What we're building**: [specific output]

**Rules**:
- Start by asking me 2-3 quick questions to understand my situation
- Then walk me through building this step by step
- At each step, show me what to do and wait for me to try
- Keep it practical — I want a working output, not a lecture
- Use plain language. If you need a technical term, explain it first.

**Levels** (ask me which I want):

### Level 1: Quick Start (5 minutes)
[Simple version anyone can do]
- Goal: [simple output]
- Example: [concrete example everyone relates to]
- Steps: [3-5 clear steps]

### Level 2: Applied (15-30 minutes)
[Apply to your own real context]
- Goal: [useful output for their actual work]
- Steps: [guided but more open-ended]
- Check: [how to verify it's working]

### Level 3: Production (30-60 minutes)
[Build something genuinely sophisticated]
- Goal: [professional-grade output]
- Steps: [detailed but assumes comfort from Levels 1-2]
- Extends: [how this connects to a larger system]

**Start by asking which level I want, then ask your context questions.**
```

### Example Path: "Building a Taxonomy"

```markdown
# Path: Building a Taxonomy

> **Video**: [link to "The AI problem nobody talks about (a linguist explains)"]
> **What you'll build**: A working taxonomy that organizes any domain
> **Time**: 5-60 minutes (you choose the depth)
> **Works in**: Claude, ChatGPT, Cursor, Codex, or any AI chat tool

---

## ▶ PASTE THIS INTO YOUR AI TOOL

You are a hands-on guide helping me build a taxonomy — a structured
way to organize knowledge in any domain.

**Rules**:
- Ask me 2-3 questions to understand what I want to organize
- Then walk me through building it step by step
- At each step, show me what to do and wait for me to try
- Use plain language. No jargon.

**Levels**:

### Level 1: Quick Start (5 minutes)
Build a simple taxonomy for something in your daily life.
- Goal: A 2-level hierarchy with 8-15 items
- Example: "Organize your kid's sports activities"
  - Categories: team sports, individual sports, water sports
  - Items under each: soccer, basketball → team; tennis, swimming → individual
- Steps:
  1. Pick something to organize (hobbies, recipes, tools you use, anything)
  2. List everything that belongs in it (don't organize yet, just list)
  3. Group the list into 3-5 categories
  4. Name each category
  5. Check: does every item fit exactly one category? If not, adjust.
- Output: A clean YAML or markdown list you can actually use

### Level 2: Applied (15-30 minutes)
Build a taxonomy for your actual work.
- Goal: A 3-level hierarchy with 20-50 items that maps your professional domain
- Steps:
  1. Tell me about your work domain (I'll ask questions)
  2. We'll identify the top-level categories together
  3. For each category, we'll break it into subcategories
  4. For each subcategory, we'll list the specific items
  5. We'll test it: can you classify 5 real things from your work?
  6. We'll refine based on what doesn't fit
- Check: Pick 10 random things from your work. Can each one be classified
  in exactly one place? If >2 don't fit, the taxonomy needs adjustment.
- Output: A working taxonomy file for your domain

### Level 3: Production (30-60 minutes)
Build a taxonomy designed for an AI system to use.
- Goal: A machine-readable taxonomy with routing logic
- This is how Palette's 117-RIU taxonomy works
- Steps:
  1. Start from your Level 2 taxonomy
  2. Add unique IDs to each node (e.g., RIU-001)
  3. Add descriptions that an AI agent could use to classify inputs
  4. Add routing hints: for each node, what should happen when something
     is classified here?
  5. Test with 10 real inputs: does the AI classify them correctly?
  6. Refine the descriptions until classification accuracy is >80%
- Extends: This taxonomy can become the backbone of a multi-agent system,
  a knowledge base, a recommendation engine, or a content strategy.
- Output: A YAML taxonomy file with IDs, descriptions, and routing logic

**Start by asking which level I want.**
```

### Path Library Structure

```
paths/
├── README.md                          (what paths are, how to use them)
├── path-template.md                   (template for creating new paths)
├── fundamentals/
│   ├── building-a-taxonomy.md
│   ├── creating-a-lens.md
│   ├── writing-ai-instructions.md
│   └── structured-research.md
├── building/
│   ├── multi-agent-routing.md
│   ├── knowledge-library-design.md
│   ├── service-evaluation.md
│   └── integration-recipes.md
├── tools/
│   ├── claude-code-workflow.md
│   ├── cursor-for-builders.md
│   ├── ai-coding-comparison.md
│   └── perplexity-research.md
└── applied/
    ├── startup-taxonomy.md
    ├── personal-knowledge-base.md
    ├── ai-for-small-business.md
    └── content-strategy-system.md
```

Each path lives on GitHub (public). Viewers clone, fork, or download individual files. GitHub stars/forks/downloads = secondary metric.

---

## Component 3: Video Spec Generator

When a signal is identified and routed to an RIU, the content engine generates a video spec:

```yaml
# Video Spec
signal_source: "PERSON-019 Andrej Karpathy posted about tokenization gaps"
riu: "RIU-XXX (create if new)"
topic: "Why your AI can't understand French (a linguist explains)"
format: tutorial  # tutorial | deep-dive | comparison | news | build

thumbnail:
  face: determined
  visual: "tokenization diagram showing French vs English"
  text: "AI CAN'T READ THIS"
  palette: blue-orange

title: "Why your AI can't understand French (a linguist explains)"
  chars: 54
  formula: curiosity-gap + authority-signal
  front_loaded: "Why your AI"

hook:
  formula: bold-claim
  script: |
    "Most AI models are secretly terrible at non-English languages.
    And I can prove it in 30 seconds."
    [show tokenization comparison on screen]

build:
  what_to_build: "Tokenization comparison demo"
  duration: 7 minutes
  tools_needed: [terminal, Python, tiktoken]
  difficulty_on_camera: simple (Level 1 in the path)

path: paths/tools/tokenization-multilingual.md
  level_1: "Tokenize your name in 3 languages"
  level_2: "Analyze tokenization efficiency for your business domain"
  level_3: "Build a language-aware routing layer for multi-language AI"

competitor_check:
  already_covered_by: ["Andrej Karpathy (briefly)", "3Blue1Brown (math angle)"]
  our_angle: "Comparative linguistics perspective — nobody else has this"

post_production:
  estimated_cost: $X
  ai_images_needed: 2 (tokenization diagrams)
  captions: auto-generate
  music: background ambient
```

---

## Component 4: Post-Production Pipeline

[RESEARCHING — background agent running]

### Requirements
- Budget: <$20/video (amortized monthly subscriptions ÷ 4 videos/month)
- Time: Minimum human editing time
- Quality bar: "Good enough to not distract" — VelvetShark level, not MrBeast level
- Capabilities needed:
  - Auto-cut silences and filler words
  - Add captions (burned-in, styled)
  - Insert AI-generated diagrams/images at marked points
  - Add background music (royalty-free)
  - Export at 4K
  - Generate thumbnail variations

### Pipeline (to be finalized after research)

```
Raw recording (OBS, free)
    ↓
AI auto-edit (cut silences, add captions)
    ↓
Insert images/diagrams at marked timestamps
    ↓
Add music track
    ↓
Export 4K
    ↓
Generate 3-5 thumbnail variations
    ↓
Upload to YouTube with optimized metadata
```

---

## Component 5: Distribution

### Primary: YouTube
- 5-10 minute videos
- 1x/week to start (sustainable)
- Each video description links to the GitHub path
- Shorts cut from key moments (AI-extracted)

### Secondary: GitHub
- `github.com/pretendhome/palette` already public
- Paths live at `palette/skills/enablement/paths/`
- OR a dedicated `enablement-paths` repo for cleaner access
- Metric: stars, forks, downloads

### Tertiary: Social
- Clips → Twitter/LinkedIn
- Newsletter (later, if traction warrants)

---

## Component 6: Feedback Loop

```
YouTube analytics (views, CTR, retention, subs)
    ↓
Which topics performed? → weight those signals higher
Which dropped off? → analyze why (hook? content? length?)
    ↓
GitHub metrics (stars, forks, path downloads)
    ↓
Which paths are most used? → create more at that level
Which paths are forked/modified? → learn from community improvements
    ↓
Comments + community
    ↓
What are viewers asking for? → direct signal for next videos
    ↓
Feed all back into Signal Monitor
```

---

## How the Enablement Coach Connects

The existing `enablement-coach.md` is the **meta-system** — it helps someone build their entire AI toolkit over multiple sessions.

Paths are **single-topic exercises** — you do one, get one output, done.

They connect like this:

```
Viewer watches YouTube video
    ↓
Grabs the path from GitHub
    ↓
Runs the path in their LLM → produces one output
    ↓
Wants more? → installs the full enablement-coach.md
    ↓
Coach reads their lens, routes them to the right next path
    ↓
Over time, they build their own Palette
```

The paths are the **top of funnel**. The enablement coach is the **retention system**. YouTube drives discovery, paths prove value, the coach creates ongoing engagement.

---

## What Needs to Be Built (Ranked)

| # | Component | Effort | Depends On |
|---|-----------|--------|------------|
| 1 | Path template + 1 example path | Small | Nothing |
| 2 | Competitor intelligence YAML | Small | Research (done) |
| 3 | Video spec template | Small | Path template |
| 4 | Post-production pipeline | Medium | Research (running) |
| 5 | Signal-to-topic routing logic | Medium | Competitor intel |
| 6 | 5 initial paths (fundamentals/) | Medium | Path template |
| 7 | GitHub repo structure for paths | Small | Paths exist |
| 8 | First video (record + produce) | Medium | Pipeline + spec |

---

## What Already Exists (the 80%)

- ✅ People library (21 profiles, 7 clusters, expandable)
- ✅ Company signals (43 tools, 3 tiers)
- ✅ Taxonomy (117 RIUs)
- ✅ Knowledge library (167 entries)
- ✅ 11 agents (resolver, researcher, architect, builder, narrator, validator, monitor, debugger, orchestrator, health, business-plan)
- ✅ Enablement coach (canonical, tested with Elia)
- ✅ SDK (Python + Go, 86 tests)
- ✅ Governed message bus (broker + 4 peers)
- ✅ GitHub repo (public)
- ✅ VPS + Telegram bot
- ✅ Formula research (thumbnails, titles, hooks, branding)
- ✅ Competitor profiles (Nate Jones, VelvetShark, Alex Finn, Matthew Berman)

## What's New (the 20%)

- 🔲 Competitor intelligence structure (YAML, separate from people library)
- 🔲 Path template + format
- 🔲 Initial paths (5-10)
- 🔲 Video spec template
- 🔲 Post-production pipeline (tools + workflow)
- 🔲 Signal-to-topic routing rules
- 🔲 YouTube channel setup
- 🔲 GitHub path distribution structure

---

## Open Design Questions

1. **Path hosting**: Should paths live inside `palette/skills/enablement/paths/` (part of the Palette repo) or in a separate `enablement-paths` repo (cleaner for viewers who just want paths)?

2. **Path versioning**: As Palette evolves, paths might need updating. Version them? Or treat as living documents?

3. **Community paths**: If viewers create their own paths, is there a contribution model? (PRs to the repo? A community directory?)

4. **Video-to-path linking**: YouTube description links to GitHub. But GitHub could also link back to the video. Bidirectional?

5. **Shorts strategy**: AI-extract 30-60 second clips from each video for YouTube Shorts? This is nearly free if automated.

6. **Multilingual paths**: Write paths in EN first. Later, translate to FR/IT/ES? Or create language-specific paths that leverage linguistic insights?
