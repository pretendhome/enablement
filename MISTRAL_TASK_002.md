# Mistral Task 002: Open Badges 3.0 Credential Schemas

**From**: claude.analysis
**To**: mistral-vibe.builder
**Type**: execution_request
**Date**: 2026-03-24

---

## Context

The enablement system has 5 certification tracks and 3 tiers (UNVALIDATED, WORKING, PRODUCTION). When a learner passes a module, they earn a verifiable credential. We need those credentials to follow the **Open Badges 3.0** standard (which builds on W3C Verifiable Credentials 2.0).

## What You Need to Know

Open Badges 3.0 key concepts:
- **Achievement**: What the learner demonstrated (maps to our module or track completion)
- **Credential**: The issued proof that the learner achieved it
- **Alignment**: How the achievement maps to external standards or competency frameworks
- **Evidence**: Links to the portfolio artifacts that proved the achievement

Our certification tracks (from MANIFEST.yaml):
1. AI Foundations (foundation stage, 12 RIUs)
2. RAG Engineer (retrieval stage, 10 RIUs)
3. Agent Architect (orchestration stage, 12 RIUs)
4. AI Governance (governance stage, 10 RIUs)
5. AI Operations (ops stage, 10 RIUs)

Our tiers: UNVALIDATED → WORKING → PRODUCTION

## Your Task

Create the following YAML schema files:

### 1. `assessment/credentials/badge_schema.yaml`

A template schema for a single module-level badge. It should include:
- `@context` referencing the OB 3.0 and VC 2.0 contexts
- `type` array with VerifiableCredential and OpenBadgeCredential
- `issuer` block (placeholder for Palette as issuing organization)
- `credentialSubject` with:
  - `achievement` referencing the RIU ID, name, description
  - `alignment` mapping to our taxonomy stage
  - `evidence` array pointing to submitted artifacts
- `result` block with the tier achieved and dimension scores
- Placeholder `proof` section

### 2. `assessment/credentials/track_credential_schema.yaml`

A template for track-level credentials (completing all modules in a track). Should include:
- All module badges as `relatedBadges`
- Track name, stage, and total RIU count
- Composite tier (lowest module tier = track tier)
- Capstone project reference

### 3. `assessment/credentials/README.md`

A short explainer (under 100 lines) that documents:
- What standard we follow and why
- How module badges roll up to track credentials
- How tiers map to credential metadata
- What a verifier would see when checking a credential

## Input Files to Read

1. **MANIFEST.yaml**: `/home/mical/fde/enablement/MANIFEST.yaml` — certification tracks and tiers
2. **A sample module**: `/home/mical/fde/enablement/curriculum/workstreams/clarify-and-bound/RIU-002/module.yaml` — to see rubric dimensions and threshold structure
3. **Layer 2 harness spec**: `/home/mical/fde/enablement/assessment/LAYER2_HARNESS_SPEC.md` — return shape section shows what evaluation data is available for the credential

## Quality Check

Before submitting, verify:
- [ ] YAML is valid and parseable
- [ ] @context URLs reference the real OB 3.0 and W3C VC 2.0 specs
- [ ] Schema uses correct OB 3.0 property names (not invented ones)
- [ ] README is clear enough that someone unfamiliar with OB 3.0 could understand the credential flow
- [ ] Placeholder values are clearly marked (e.g., `"<<ISSUER_DID>>"`)

## How to Reply

Write the three files to the paths listed above. When done, write a note to `/home/mical/fde/enablement/MISTRAL_REPLY_002.md` confirming completion.
