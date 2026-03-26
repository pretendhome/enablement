# Learning From the Best: What OpenAI, Anthropic, and Mistral Want
**Date**: 2026-03-25
**Purpose**: Reverse-engineer what the three top model companies are hiring for, extract the patterns, and apply them to our enablement system and content engine.

---

## The Insight

Three companies that define AI are all hiring for the same function:

| Company | Role | Comp | What They Want |
|---------|------|------|----------------|
| **OpenAI** | Learning Systems Engineer | $239-325K + equity | AI-native learning infrastructure, adaptive experiences, analytics proving learning |
| **Anthropic** | Certification Content & Systems Architect | $270-365K | Competency measurement beyond multiple-choice, AI-augmented assessment, portfolio evaluation |
| **Mistral** | Technical Marketing Engineer | Undisclosed (Paris/London) | Turn model capability into developer confidence, enablement loops tied to real friction |

These are product specs. They're telling us what the market needs.

---

## Extracted Requirements (Union of All Three)

### 1. Adaptive Learning Experiences
- **OpenAI**: "dynamically adapt to learners' knowledge, goals, and behaviors over time"
- **Anthropic**: "learning progressions", "certification tiers with rising rigor"
- **Mistral**: "enablement loops tied to real developer friction"
- **The pattern**: Not static content. The experience changes based on who the learner is and what they already know.

### 2. Competency Measurement (Not Content Consumption)
- **OpenAI**: "assessments", "measure whether people are actually learning"
- **Anthropic**: "skeptical of multiple-choice", "demonstrations of competence", "portfolio-based assessment"
- **Mistral**: "show whether people can actually use the platform, not whether they read the launch post"
- **The pattern**: "Did they read it?" is worthless. "Can they do it?" is the only metric that matters.

### 3. Learning Analytics That Prove Outcomes
- **OpenAI**: "data pipelines and analytics systems to help educators understand learner outcomes, engagement patterns, and skill development"
- **Anthropic**: "inter-rater reliability", "calibration exemplars", "confidence scoring"
- **Mistral**: "operational feedback — use real usage and field confusion to evolve the package"
- **The pattern**: Close the loop. Measure what happened. Use that data to improve what comes next.

### 4. Non-Engineer Empowerment
- **OpenAI**: "systems that allow non-engineers to design, configure, and experiment with learning experiences without requiring direct engineering support"
- **Anthropic**: (implicit — educator-facing credentialing tools)
- **Mistral**: "problem-first enablement", "use-case-organized documentation"
- **The pattern**: The person who creates learning experiences should NOT need to be an engineer.

### 5. AI-Native (AI Is Both Subject and Tool)
- **OpenAI**: "AI-native learning experiences", "AI models into educational workflows"
- **Anthropic**: "Claude is both the product I'd be credentialing people on and the tool I'd use to build the credentialing infrastructure"
- **Mistral**: "translation from model capability to operational adoption"
- **The pattern**: AI teaches about AI. The tool IS the classroom.

### 6. Content Currency (Stays Current as Models Evolve)
- **OpenAI**: (implicit — "AI progress continues to accelerate")
- **Anthropic**: "automated staleness detection", "content currency and renewal"
- **Mistral**: "keep content, thresholds, and evaluation from drifting over time"
- **The pattern**: A learning system that's 6 months out of date is teaching the wrong thing. Currency is non-negotiable.

### 7. Structured Progressions (Beginner → Expert)
- **OpenAI**: "progress tracking", "move from curiosity to mastery"
- **Anthropic**: "foundation → retrieval → orchestration → specialization", "UNVALIDATED → WORKING → PRODUCTION"
- **Mistral**: taxonomy organized around "real developer problems, not product silos"
- **The pattern**: There is a path. The learner knows where they are and where they're going.

### 8. Artifact-Based Assessment
- **OpenAI**: "formative assessments"
- **Anthropic**: "portfolio-based assessment where every certification requires artifacts that can be inspected, rerun, challenged, and defended"
- **Mistral**: "artifact-first learning"
- **The pattern**: The learner produces something real. That output IS the evidence of learning.

### 9. Scale Without Headcount
- **OpenAI**: "millions of people around the world"
- **Anthropic**: "AI-augmented evaluation makes it scalable"
- **Mistral**: "repeatable field enablement"
- **The pattern**: One-on-one coaching doesn't scale. The system must work at 1 learner or 1 million.

---

## Gap Analysis: What Our System Has vs. What They Want

| Requirement | What We Have | Gap | Severity |
|---|---|---|---|
| **Adaptive learning** | Parameterized skill with 3 difficulty levels; LLM asks context questions at runtime | No persistent learner model across paths. Each path starts from zero. | MEDIUM |
| **Competency measurement** | Certification system: 3-layer assessment, calibration exemplars, threshold engine | Video enablement paths have no verification step. Learner builds something but nobody checks it. | HIGH |
| **Learning analytics** | Coverage reports (80.2% KL utilization), integrity validators, staleness detection | No learner-side analytics. We know what we teach, not whether anyone learned. | HIGH |
| **Non-engineer empowerment** | Paste-into-any-LLM design. Zero installation. | No way for an educator to CREATE a new path. Only Mical can author them via the video spec. | MEDIUM |
| **AI-native** | Fully AI-native. LLM generates the learning experience. AI handles post-production. AI monitors signals. | None. We're strong here. | NONE |
| **Content currency** | Staleness detection in Palette. Knowledge library versioned. Taxonomy evolves with new RIUs. | Enablement paths are generated once per video. If the knowledge library updates, old paths don't auto-refresh. | LOW |
| **Structured progressions** | Quick Start → Applied → Production within each path. Enablement coach handles cross-path progression. | The connection between individual paths and the coach's progression system isn't explicit in the viewer's experience. | MEDIUM |
| **Artifact-based assessment** | Production level asks learners to build real artifacts. Certification system has capstone projects. | Quick Start and Applied levels produce output but don't verify it. No "show me what you built" moment. | MEDIUM |
| **Scale** | Parameterized skill eliminates per-path authoring. Any LLM, any learner. | Works. The parametric design IS the scaling mechanism. | NONE |

---

## What We Should Change (Prioritized)

### Priority 1: Add Verification to Enablement Paths (HIGH impact, LOW effort)

All three companies want competency measurement. Our paths walk learners through building something but never check whether it worked.

**Change**: Add a `## Check Your Work` section to each difficulty level in the video enablement skill.

```markdown
### Quick Start — Check Your Work
When you're done, share what you built with me. I'll check:
- Does it have the right structure?
- Can you explain why you organized it this way?
- What would you change if the requirements shifted?

### Applied — Check Your Work
Share your output. I'll evaluate against these criteria:
- Does it solve a real problem from your domain?
- Could someone else use this without your explanation?
- What are the edge cases you considered?

### Production — Portfolio Review
Share your output AND your design reasoning. I'll evaluate:
- Technical soundness against known patterns
- Tradeoff awareness (what did you choose NOT to do?)
- Adaptability (how would this change if X happened?)
```

This is literally what Anthropic is paying $270-365K to build. We add it in 10 lines.

### Priority 2: Add Learner Analytics to the Feedback Loop (HIGH impact, MEDIUM effort)

OpenAI explicitly wants "data pipelines and analytics to help educators understand learner outcomes." Mistral wants "operational feedback."

**Change**: Add a lightweight feedback prompt at the end of each enablement path.

```markdown
## Before You Go
Rate your experience (tell me a number 1-5):
1. How confident are you that you could do this again without the guide?
2. What was the hardest part?
3. What would you build next with this skill?
```

Then in the video description, add: "Share what you built → [GitHub Discussion link]"

This creates a learner analytics pipeline:
- **Self-reported confidence** (1-5) → tracks learning outcomes
- **"Hardest part"** → identifies friction points → improves the path
- **"Build next"** → generates signal for next video topics
- **GitHub Discussions** → community artifacts we can measure (posts, stars, forks)

### Priority 3: Make Cross-Path Progression Explicit (MEDIUM impact, LOW effort)

All three companies want structured progressions. We have them (Quick Start → Applied → Production within paths, and the enablement coach across paths), but they're not connected in the viewer's experience.

**Change**: Add a `## What's Next` section to each path that connects to related paths and to the enablement coach.

```markdown
## What's Next

**Related paths** (if you liked this, try these):
- [Building a Knowledge Library] → organizes WHAT you know
- [Multi-Agent Routing] → routes DECISIONS through your taxonomy

**Want the full system?**
The enablement coach builds your personal AI toolkit over multiple sessions.
It remembers who you are and what you've built.
→ [Link to enablement-coach.md on GitHub]
```

This turns individual paths from dead ends into a funnel.

### Priority 4: Add a Path Creator Mode (MEDIUM impact, MEDIUM effort)

OpenAI wants "systems that allow non-engineers to design, configure, and experiment with learning experiences without engineering support."

**Change**: Add a second mode to the video enablement skill — a "creator mode" where an educator describes what they want to teach and the system generates the enablement path.

```markdown
## CREATOR MODE — Paste this to generate a new path

You are a learning experience designer. I want to create an enablement
path that someone can paste into any AI tool.

I'll tell you:
- What I want to teach
- What the learner should build at each level
- What "success" looks like

You'll generate a complete path in the standard format:
Quick Start (5 min) → Applied (15-30 min) → Production (30-60 min)
Each with steps, checks, and a verification section.
```

This means OTHER creators can generate paths using our format. The system scales beyond Mical.

### Priority 5: Add Currency Mechanism to Generated Paths (LOW impact, LOW effort)

**Change**: Each generated path includes a version date and a link to the source knowledge library entry. If the entry updates, the path shows its age.

```markdown
> **Path version**: 2026-03-25
> **Source**: RIU-401 (Taxonomy Design), KL entries: LIB-045, LIB-067
> **Currency**: Check for updates at [GitHub link]
```

Simple. No automation needed. Just transparency.

---

## Updated Video Enablement Skill (v2)

Incorporating all 5 changes, the skill becomes:

```markdown
# Video Enablement — Paste-Into-Any-LLM Skill

> Copy everything below the line and paste it as your first message
> in Claude, ChatGPT, Cursor, Codex, or any AI chat tool.
>
> **Video**: {{youtube_link}}
> **Topic**: {{topic}}
> **Source**: RIU-{{riu_id}}, Knowledge: {{kl_entries}}
> **Path version**: {{date}}

---

## PASTE THIS INTO YOUR AI TOOL

You are a hands-on guide helping me build something real.

**Topic**: {{topic}}
**What I'll build**: {{output_description}}

**Rules**:
- Start by asking me 2-3 quick questions to understand my situation
- Walk me through building this step by step
- At each step, show me what to do and wait for me to try
- Keep it practical — I want a working output, not a lecture
- Use plain language. If you need a technical term, explain it first.
- After I build something, CHECK my work — give specific feedback

**Difficulty** (ask me which I want):

### Quick Start (5 minutes)
{{quick_start_goal}}
{{quick_start_steps}}

**Check your work**: Ask me to share what I built. Verify:
- Does it have the right structure?
- Can I explain my reasoning?
- One suggestion for improvement.

### Applied (15-30 minutes)
{{applied_goal}}
{{applied_steps}}

**Check your work**: Ask me to share my output. Evaluate:
- Does it solve a real problem from my domain?
- Could someone else use this without my explanation?
- What edge cases should I consider?

### Production (30-60 minutes)
{{production_goal}}
{{production_steps}}

**Portfolio review**: Ask me to share my output AND my design reasoning. Evaluate:
- Technical soundness against known patterns
- Tradeoff awareness — what did I choose NOT to do?
- Adaptability — how would this change if requirements shifted?

## Before You Go
After completing any level, ask me:
1. Confidence (1-5): could I do this again without the guide?
2. What was the hardest part?
3. What would I build next with this skill?

## What's Next
{{related_paths}}

**Want the full system?** The Palette enablement coach builds your
personal AI toolkit over multiple sessions. It remembers who you are
and what you've built → github.com/pretendhome/palette

**Start by asking which difficulty level I want.**
```

---

## What This Means for the YouTube Channel

The system we're building IS the prototype for what these companies want to hire someone to build at scale:

| Our System | OpenAI Would Call It | Anthropic Would Call It | Mistral Would Call It |
|---|---|---|---|
| Parameterized enablement skill | AI-native learning experience | Certification assessment system | Developer enablement infrastructure |
| Quick Start → Applied → Production | Adaptive learning that meets learners where they are | Learning progressions with rising rigor | Enablement loops from awareness to adoption |
| Check Your Work sections | Formative assessment | Portfolio-based competency evaluation | Verification that people can actually use the platform |
| Confidence rating + feedback | Learning analytics pipeline | Psychometric signal | Operational feedback for content evolution |
| Creator mode | Systems for non-engineers to create learning | Educator tooling | Scalable content creation |
| Enablement coach as retention | Learner model + progress tracking | Certification journey | Full developer journey |

**Every video demonstrates a working instance of the system these companies are paying $250-365K to have someone build.**

The YouTube channel is simultaneously:
1. Content that teaches people AI skills
2. A demo of the enablement system in action
3. A portfolio proving you can build what these companies need
4. A prototype that improves with every video

---

## Implementation Order

| # | Change | Effort | Files Affected | Status |
|---|--------|--------|---------------|--------|
| 1 | Add verification sections to enablement skill | 30 min | `path-template.md` | **DONE** (v2.0) |
| 2 | Add learner analytics prompts (confidence delta) | 15 min | `path-template.md` | **DONE** (v2.0) |
| 3 | Add cross-path progression links | 15 min | `path-template.md` + `video-spec-template.yaml` | **DONE** (v2.0) |
| 4 | Add creator mode | 45 min | `creator-mode.md` (standalone file) | **DONE** (v2.1 split) |
| 5 | Add currency metadata | 10 min | `content-engine-spec.md` + `video-spec-template.yaml` | **DONE** (v2.0) |
| 6 | Update SYSTEM_DESIGN_v1 to reflect these changes | 30 min | `SYSTEM_DESIGN_v1.md` | **DONE** (v2.1) |
| 7 | Three-file split + publishing rules + adaptive debrief | — | All content engine files | **DONE** (v2.1) |
| **Total** | | **~2.5 hours** | | **ALL COMPLETE** |
