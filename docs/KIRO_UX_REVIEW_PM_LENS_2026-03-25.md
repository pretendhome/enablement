# UX Review: video-enablement.md v2.0 — PM Lens Deep Audit
**Date:** 2026-03-25
**Reviewer:** Kiro (kiro.design)
**Lens:** LENS-PM-001 (Product Decision)
**Method:** 5 iterative passes, each progressively harder. Each pass re-reads the full skill and attacks from a different product angle.
**File reviewed:** `enablement/agentic-enablement-system/content-engine/video-enablement.md`

---

## The 5 Biggest Product Mistakes

Before the iteration detail — here are the verdicts, ranked by user loss:

| # | Mistake | Who it kills | Severity |
|---|---------|-------------|----------|
| 1 | The skill has no onramp — it drops you into a system prompt with zero warmup | Every first-time user | CRITICAL |
| 2 | Learner Mode and Creator Mode are in the same document, creating a "who is this for?" crisis | Everyone — beginners are overwhelmed, educators can't find their section | CRITICAL |
| 3 | There is no feedback loop back to the product — the skill generates value and then loses it | The business (Mical) | HIGH |
| 4 | The skill optimizes for completeness instead of completion — too many steps, too many sections, too many words | Beginners who quit mid-flow, developers who skim and miss key parts | HIGH |
| 5 | The "What's Next" routing is aspirational, not functional — it points to paths that don't exist yet | Anyone who finishes and wants more | MEDIUM |

---

## Iteration 1: First Contact Audit
*Question: What happens in the first 60 seconds for someone who has never seen this?*

### Finding: There is no onramp.

A viewer watches a YouTube video. They see a link in the description. They click it (or copy text from the description). Then they're looking at this:

```
# Building a Taxonomy

> **Video**: https://youtube.com/watch?v=XXXXX
> **What you'll build**: A working taxonomy that organizes any domain
> **Time**: 5-60 minutes (you choose)
> **Works in**: Claude, ChatGPT, Cursor, Codex, or any AI tool
> **Source**: RIU-401 | Knowledge: LIB-045, LIB-067
> **Version**: 2026-03-25 | Status: current
> **Path constellation**: Organize → Retrieve → Route (1 of 3)
```

Within the first 5 lines, they've encountered:
- "RIU-401" — meaningless
- "LIB-045, LIB-067" — meaningless
- "Path constellation" — meaningless
- "Organize → Retrieve → Route (1 of 3)" — intriguing but unexplained

Then they get 5 steps that say "copy and paste." But copy WHAT? They're looking at a markdown file. Is the whole thing the paste? Just part of it? The "START HERE" marker is buried below the fold.

**The product failure:** The skill assumes the user already understands what they're looking at and why. There is no "here's what this is and here's what you're about to do" moment. It jumps straight to mechanics.

**What a PM would demand:** A 2-3 sentence plain-English intro BEFORE the metadata. Something like:

> *This is a hands-on exercise from [video title]. You'll paste the text below into any AI tool (Claude, ChatGPT, etc.) and it will walk you through building [thing]. Takes 5-60 minutes depending on how deep you go. No experience needed.*

That's the onramp. Without it, you're asking cold traffic to trust a wall of markdown.

**Severity:** CRITICAL. This is the moment where you have the user's attention or you don't. Every second of confusion here is a lost user.

---

## Iteration 2: Information Architecture Audit
*Question: Is the document organized for the user, or for the system builder?*

### Finding: Two products are jammed into one document.

The file contains:
1. Internal instructions for Mical ("How to Use" — fill template, push to GitHub)
2. Learner Mode template (the paste-into-LLM experience)
3. A filled example (Building a Taxonomy)
4. Creator Mode template (for educators)
5. Path Constellations reference
6. Wire Contract (HandoffPacket spec)
7. Parameter Reference table

These serve completely different audiences:

| Section | Audience | When they need it |
|---------|----------|-------------------|
| Internal instructions | Mical | When publishing a new video |
| Learner Mode template | Content engine | When generating a path |
| Filled example | YouTube viewer | When they click the link |
| Creator Mode | Educators | When they want to create their own |
| Constellations | System designer | When planning learning arcs |
| Wire Contract | Developer | When integrating with Palette SDK |
| Parameter Reference | Developer | When filling templates |

**The product failure:** A YouTube viewer who lands on this file sees ALL of it. They see internal instructions, template variables (`{{topic}}`), wire contracts, and YAML schemas. They have to mentally parse "which part is for me?" That's a product design failure — the user should never have to figure out what's relevant.

**What a PM would demand:** Split this into at minimum 3 files:

1. **The published path** (what the viewer sees) — ONLY the filled example, clean, no templates, no system internals
2. **The content engine spec** (what Mical/narrator uses) — templates, parameters, wire contract, constellations
3. **Creator Mode** (what educators use) — standalone, no Palette internals visible

Right now, Creator Mode is buried at line ~250 of a 500+ line document that starts with developer instructions. An educator would never find it. And if they did, they'd have scrolled past wire contracts and YAML schemas to get there.

**Severity:** CRITICAL. This is a "who is this for?" problem. The answer right now is "everyone and no one."

---

## Iteration 3: Conversion Funnel Audit
*Question: Where does the product capture value, and where does it leak?*

### Finding: The skill generates enormous value and captures none of it.

Walk through the funnel:

```
YouTube video (awareness)
  → Video description link (interest)
    → Paste into LLM (activation)
      → Complete Quick Start (engagement)
        → AFTER YOU BUILD sequence (measurement)
          → What's Next (retention)
            → ??? (revenue)
```

The AFTER YOU BUILD sequence collects:
- Confidence baseline and delta (learning measurement)
- Friction point (product improvement signal)
- Artifact description (proof of work)
- "What would you build next?" (demand signal)

This is gold. This is the data that tells you which paths work, which don't, where learners struggle, and what they want next. **And it all stays inside the LLM conversation.** It's never captured. It's never sent anywhere. It evaporates when the user closes the tab.

**The product failure:** The skill has a measurement system with no data pipeline. The confidence delta is measured but not recorded. The friction data is surfaced but not collected. The "what would you build next?" demand signal is generated but never reaches the product team.

**What a PM would demand:**

Option A (minimal): Add a Google Form link at the end. "Share your results (optional, 30 seconds): [link]". Fields: topic, level completed, confidence before, confidence after, hardest part, what you'd build next. This is a 🔄 TWO-WAY DOOR — easy to add, easy to remove.

Option B (better): The summary in Step 5 ("Today I built X which does Y. My confidence moved from A to B.") is designed to be copy-pasteable. Add: "Share this on Twitter/LinkedIn with #PaletteBuilt" or "Post in our GitHub Discussions: [link]". This turns private learning into public proof, which drives awareness back to the top of the funnel.

Option C (best): Build a lightweight `/api/enablement/result` endpoint that the LLM can suggest the user hit (or that a future Palette integration could auto-submit). But this is a 🚨 ONE-WAY DOOR (infrastructure commitment) — don't do it until Option A proves there's demand.

**Severity:** HIGH. You're building a product that generates its own market research and then throws it away.

---

## Iteration 4: Completion Rate Audit
*Question: What percentage of users who start will actually finish?*

### Finding: The skill optimizes for completeness, not completion.

Let me count what a Quick Start user encounters after pasting:

1. The LLM reads the system prompt (invisible to user, but takes a moment)
2. BEFORE WE START: 2-3 context questions + confidence baseline = **3-4 exchanges before any building starts**
3. Quick Start steps 1-5 = **5 steps**
4. Verification: artifact check + reasoning check + one improvement + advance/exit = **4 more exchanges**
5. AFTER YOU BUILD: confidence delta + friction capture + artifact capture + next pull + summary = **5 more exchanges**

That's **~17 conversational turns** for a "5-minute" Quick Start. At ~30 seconds per exchange (user types + LLM responds), that's 8-9 minutes of conversation alone, not counting the actual building time.

For a beginner who was told "5 minutes," this is a broken promise. They'll bail somewhere around step 3 of AFTER YOU BUILD, thinking "I already built the thing, why is it still asking me questions?"

**The product failure:** The skill front-loads value (building) but back-loads measurement (AFTER YOU BUILD). By the time the measurement happens, the user's attention budget is spent. The 5-minute promise is for the building, but the full experience is 15-20 minutes.

**What a PM would demand:**

1. **Be honest about time.** Quick Start building is 5 minutes. The full experience with onboarding + verification + reflection is 15 minutes. Say that. "5 minutes to build, 15 minutes for the full guided experience."

2. **Make AFTER YOU BUILD collapsible.** The LLM should ask: "Want the full debrief (5 more minutes) or just your summary?" Most beginners want the summary. Developers definitely want just the summary. Only engaged learners want all 5 steps.

3. **Move the confidence re-rating to immediately after verification.** Right now it's Step 1 of AFTER YOU BUILD, which feels like a new section. If it came right after "Your taxonomy looks solid" in the verification, it would feel like a natural conclusion, not a new task.

4. **Cut Step 4 ("Surface the next pull") from Quick Start.** A beginner who just finished their first taxonomy doesn't know what they'd build next. That question is meaningful at Applied/Production level. At Quick Start, it's premature and adds a turn that delays the satisfying summary.

**Severity:** HIGH. The completion rate of the AFTER YOU BUILD sequence is probably <30% for beginners. That means 70% of your measurement data never gets generated.

---

## Iteration 5: Competitive Moat Audit
*Question: What makes this defensible? What stops someone from copying the format?*

### Finding: The "What's Next" routing is the moat — and it doesn't work yet.

The skill's unique value proposition vs. a generic "paste this prompt" approach:

| Feature | Generic prompt | This skill |
|---------|---------------|------------|
| Three difficulty tiers | ❌ | ✅ |
| Confidence measurement | ❌ | ✅ |
| Failure mode warnings | ❌ | ✅ |
| Verification that tests understanding | ❌ | ✅ |
| Routing to next learning path | ❌ | ✅ (in theory) |
| Connected learning arcs (constellations) | ❌ | ✅ (in theory) |
| Creator Mode for educators | ❌ | ✅ |

The first four are genuinely good and hard to replicate without the pedagogical thinking behind them. But they're also copyable — someone could read this skill and build their own version.

The last three are the moat. Constellations (connected learning arcs), routing ("if this clicked → try X"), and Creator Mode (educators generating paths in the standard format) create a network effect: more paths → better routing → more value per path → more creators → more paths.

**But the routing doesn't work yet.** The "What's Next" section says:

> **If this clicked** — go deeper:
> - Building a Knowledge Library
> - Writing AI Instructions

These paths don't exist. There's no link. There's no file. The user hits a dead end. The constellation map shows "Next → Building a Knowledge Library" but there's nothing to click.

**The product failure:** The moat feature is designed but not built. The skill promises a connected learning system and delivers a single path with aspirational links. This is worse than having no routing at all — it sets an expectation and then breaks it. A user who finishes and wants more gets... nothing.

**What a PM would demand:**

1. **Don't show routing to paths that don't exist.** If "Building a Knowledge Library" isn't published, don't list it. Show only live links. An empty "What's Next" with a waitlist signup is better than a broken promise.

2. **Build the second path before launching the first.** The minimum viable constellation is 2 paths. Launch "Taxonomy Design" and "Knowledge Library" together. Then the routing actually works and the user experiences the connected system.

3. **Add a waitlist/notification mechanism.** "Building a Knowledge Library is coming soon. Drop your email to get notified: [link]." This captures the demand signal AND gives you a distribution channel for the next path.

4. **Prioritize Creator Mode paths from real educators.** If Elia (or another early user) creates a path via Creator Mode, that's a second path in the system that proves the format works beyond Mical's topics. Creator Mode is the scaling mechanism — but it needs at least one non-Mical path to prove it.

**Severity:** MEDIUM (because the skill works fine standalone — but the growth engine is broken).

---

## Summary: 5 Product Decisions Required

Applying LENS-PM-001 output contract:

### Decision 1: Add an onramp
**Why now:** First video launch is imminent. Without it, cold traffic bounces.
**Reversibility:** 🔄 TWO-WAY DOOR — 3 sentences of text.
**Owner:** Mical
**Success metric:** >50% of viewers who open the link proceed to paste.
**Risk:** None.

### Decision 2: Split the document into 3 files
**Why now:** Educators can't find Creator Mode. Viewers see system internals.
**Reversibility:** 🔄 TWO-WAY DOOR — file reorganization, no content loss.
**Owner:** Mical + Claude (content engine refactor)
**Success metric:** Creator Mode discoverable without scrolling past wire contracts.
**Risk:** Breaking existing references to the single file. Mitigate: redirect or symlink.

### Decision 3: Add a feedback capture mechanism
**Why now:** The first cohort of users will generate the most valuable signal. If you don't capture it, it's gone.
**Reversibility:** 🔄 TWO-WAY DOOR — Google Form takes 10 minutes to build.
**Owner:** Mical
**Success metric:** >10% of completers submit feedback.
**Risk:** Form fatigue. Mitigate: make it 4 fields max, optional.

### Decision 4: Fix the time promise and make AFTER YOU BUILD adaptive
**Why now:** A broken time promise on the first video kills trust for all future paths.
**Reversibility:** 🔄 TWO-WAY DOOR — wording changes + one instruction to the LLM.
**Owner:** Mical
**Success metric:** >60% of Quick Start users reach the summary step.
**Risk:** Losing measurement data if too many users skip. Mitigate: always do confidence delta (1 question), make the rest optional.

### Decision 5: Don't ship routing to nonexistent paths
**Why now:** Broken links on day 1 undermine the "connected system" promise.
**Reversibility:** 🔄 TWO-WAY DOOR — remove or replace with waitlist.
**Owner:** Mical
**Success metric:** Zero dead-end links in published paths.
**Risk:** The skill looks smaller without routing. Mitigate: "More paths coming — join the waitlist" is honest and creates anticipation.

---

## Iteration Log

| Pass | Angle | Key finding | Time spent |
|------|-------|-------------|------------|
| 1 | First contact (60-second test) | No onramp — user hits system metadata before understanding what this is | Re-read full intro + example header |
| 2 | Information architecture | Two products in one file — learner, educator, and developer all see everything | Re-read full document structure, mapped audiences per section |
| 3 | Conversion funnel | Value generated but never captured — no feedback pipeline | Traced the full user journey from YouTube to "What's Next" |
| 4 | Completion rate | 17 conversational turns for "5 minutes" — AFTER YOU BUILD is where users bail | Counted every exchange in Quick Start flow |
| 5 | Competitive moat | Routing is the defensible feature and it points to paths that don't exist | Checked What's Next links against actual published paths |

---

## Open Assumptions

- `ASSUMPTION:` The YouTube description will link directly to the filled path (not the template file). If it links to the template, every finding above is 10x worse.
- `ASSUMPTION:` The first video will use the "Building a Taxonomy" example. If a different topic is first, the filled example needs to be updated or a new one created.
- `ASSUMPTION:` Mical will record the video before the paths are finalized. If paths ship first (e.g., on GitHub), they need to work without the video context.
