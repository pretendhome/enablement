# Video Enablement Skill — Redirected
# Version: 2.1
# Status: SPLIT into three files (2026-03-25)

This file has been split into three purpose-specific documents:

| File | Audience | What it contains |
|------|----------|------------------|
| **content-engine-spec.md** | System / internal | Canonical schema, wire contract, quality bar, publishing rules, video lineup, provenance rules |
| **path-template.md** | Viewers / learners | Parameterized learner template + filled taxonomy example |
| **creator-mode.md** | Educators / creators | Standalone prompt — paste into any LLM to generate a path |

## Principle

**One contract, three surfaces** — `content-engine-spec.md` owns the canonical parameter schema. The template and creator mode are render targets, not independent specs.

## Why the split

The original file was carrying three jobs for three different audiences:
- Public learner artifact
- Internal system spec
- Creator-facing authoring interface

Splitting prevents drift between audiences while keeping one source of truth for the schema.

## Quick start

- **Publishing a new path**: Start with `content-engine-spec.md` → How to Use
- **Filling a video spec**: Use `video-spec-template.yaml`
- **Creating a path from scratch**: Use `creator-mode.md`
