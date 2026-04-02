# Loom Recording Checklist (v2)

## Before Recording

### Environment
- [ ] Close all unnecessary apps and browser tabs
- [ ] Disable notifications (Slack, email, system, phone on silent)
- [ ] Clean desktop — no personal files visible
- [ ] Terminal history cleared (`history -c && clear`)
- [ ] Browser bookmarks bar hidden
- [ ] No passwords or API keys visible anywhere

### Loom Setup
- [ ] Loom desktop app updated and logged in
- [ ] Recording mode: Screen + Camera
- [ ] Camera: top-right corner, small circle
- [ ] Microphone: test level, ensure no background noise
- [ ] Screen: full desktop or specific window (decide which)
- [ ] Recording resolution: 1080p minimum
- [ ] Drawing tools disabled (avoid accidental marks)

### Presentation
- [ ] Slide deck v2 opens correctly in full-screen mode (`codex_enablement_v2.pptx`)
- [ ] All 7 slides render properly — no missing fonts, no overflow
- [ ] Slide advance works smoothly (keyboard shortcut mapped)
- [ ] Slide 6 supports the rollout story instead of trying to become a second demo

### Demo Surfaces (order matters)
- [ ] Codex desktop app — demo repo loaded
- [ ] Backup: screenshot or note file in case Codex output is weak

### Demo Pre-Flight
- [ ] Move 1 prompt tested: "Explain what this module does and map its dependencies" on demo repo
- [ ] Move 2 prompt tested: bounded change plan with files, tests, and review risks
- [ ] Move 2 backup prompt tested and saved nearby
- [ ] Backup prompts identified for each move (see demo_runbook_v2.md)
- [ ] Codex response time is acceptable (<15 seconds)
- [ ] Run both demo moves 30 min before recording to warm up
- [ ] Rehearsed demo completes in under 2:30 (buffer for live response variance)

### You
- [ ] Glass of water within reach
- [ ] Good lighting (face visible in camera)
- [ ] Professional appearance (at least waist-up)
- [ ] Print speaker_script_v2.md as backup reference (off-camera)
- [ ] Taken a 5-minute break since last rehearsal

---

## Recording Strategy

**Plan**: 2-3 full takes. Pick the best. Don't chase perfection.

### Take 1: Warm-Up
- Full run-through
- Accept mistakes, keep going
- Focus on pacing and transitions between slides -> demo -> close
- Time it
- Note any stumbles or slow demo responses

### Take 2: The Real Take
- Apply learnings from Take 1
- Focus on energy and clarity
- If you stumble, pause, breathe, restart the sentence
- Time it

### Take 3: Only If Needed
- If Take 2 had a major issue (demo failure, lost thread, wrong slide)
- If both Takes 1 and 2 were over 5:30

### Selection Criteria
- Under 5:00 (hard requirement)
- Clear rollout thesis delivery
- Both demo moves executed cleanly
- Code Understanding is visibly low-risk
- Bounded planning moment lands as the governance proof point
- Ends strong: "Scale based on evidence, not enthusiasm."

---

## Timing Targets

| Segment | Target | Hard Limit |
|---|---|---|
| Opening (hook first) | 0:12 | 0:15 |
| Slide 2: Four Problems. One Root Cause. | 0:18 | 0:22 |
| Slide 3: Codex in the Workflow | 0:20 | 0:25 |
| Slide 4: Your Standards = AI's Rules | 0:20 | 0:25 |
| Slide 5: Start Read-Only. Scale on Evidence. | 0:30 | 0:35 |
| Slide 6: Same Data. Two Audiences. | 0:20 | 0:25 |
| Demo Move 1: Code Understanding | 1:05 | 1:15 |
| Demo Move 2: Bounded Change Planning | 1:10 | 1:20 |
| Demo bridge back to rollout | 0:30 | 0:35 |
| Closing (with next step) | 0:15 | 0:18 |
| **TOTAL** | **5:00** | **5:30** |

---

## If Things Go Wrong During Recording

| Problem | Action |
|---|---|
| Stumble on words | Pause, breathe, restart sentence. Don't apologize. |
| Demo takes too long | Narrate while waiting. If >30s, say "response times vary" and move on. |
| Demo gives bad output | "This is why we have the review expectation" — pivot to the workflow standard. |
| Bounded planning answer is generic | "The standard still holds: scope the work, identify tests, review before code." |
| Wrong slide | Click back, don't mention it. |
| Over time at 4:00 | Cut the bridge sentence and deliver the closing line. |
| Background noise | Pause, wait for it to pass, continue. |
| Codex is down | Skip the live demo and talk through the workflow standard using your prepared slide and notes. |
| Brain freeze | Look at printed script off-camera. |

---

## After Recording

- [ ] Watch the full take before uploading
- [ ] Check audio quality throughout (no mic dropouts)
- [ ] Check that all slides are readable at normal viewing size
- [ ] Check that demo output is legible
- [ ] Verify total time is under 5:00
- [ ] Title the Loom: "Governed Codex Adoption for Retail Engineering"
- [ ] Add description: "Enterprise enablement session for deploying Codex at a Fortune 500 retail company. Covers rollout strategy, harness controls, phased adoption, and live code understanding demo."
- [ ] Set visibility: anyone with link
- [ ] Copy link
- [ ] Submit via submission link
- [ ] Confirm submission received

---

## Submission Checklist

- [ ] Loom video uploaded and accessible
- [ ] Slide deck attached (`codex_enablement_v2.pptx`)
- [ ] Both submitted
- [ ] Test the Loom link in an incognito window
- [ ] Verify the PPTX opens on a clean machine (no dependency on local fonts)
- [ ] Done. Close the laptop. Go for a walk.
