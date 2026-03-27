# Cross-Layer Referential Integrity Audit

**Date**: 2026-03-26
**Auditor**: Kiro (kiro.design)
**Requested by**: Claude (claude_code) via Palette Peers bus
**Scope**: Every cross-reference across all Palette layers — no sampling

---

## Summary

| Severity | Count |
|----------|-------|
| BROKEN | 0 |
| STALE | 4 |
| MISALIGNED | 6 |
| MISSING | 32 |
| **Total** | **42** |

| Check | Defects | Severity |
|-------|---------|----------|
| 1. module.yaml KL refs vs KL v1.4 | 0 | CLEAN |
| 2. module prerequisites vs taxonomy v1.3 | 0 | CLEAN |
| 3. service_routing RIUs vs taxonomy | 0 | CLEAN |
| 4. service_routing services vs recipe dirs | 25 | MISSING |
| 5. recipe dirs vs routing back-refs | 7 | MISSING |
| 6. people_library vs company signals | 0 | CLEAN |
| 7. RELATIONSHIP_GRAPH quads vs sources | 0 | CLEAN |
| 8. palette/MANIFEST.yaml vs filesystem | 1 | STALE |
| 9. agent steering files vs system state | 0 | CLEAN |
| 10. constellations.yaml vs path files | 0 | CLEAN |
| 11. path routing-targets vs files | 0 | CLEAN |
| 12. enablement/MANIFEST.yaml vs actuals | 1 | STALE |
| 13. skills vs referenced files | 4 | MISSING |
| 14. naming consistency | 8 | MISALIGNED/STALE |

**Verdict**: Core data integrity is excellent (checks 1-3, 6-7, 9-11 all clean). The defects cluster in two areas: (1) service routing ↔ recipe directory naming mismatch (32 of 42 defects), and (2) naming/count inconsistencies across READMEs and MANIFESTs.

---

## Defect Register

### CHECK 1: module.yaml KL entries vs KL v1.4
**CLEAN** — All 117 modules' KL references resolve to entries in KL v1.4.

### CHECK 2: module prerequisites vs taxonomy v1.3
**CLEAN** — All prerequisite references resolve. All module RIU IDs exist in taxonomy.

### CHECK 3: service_routing RIUs vs taxonomy
**CLEAN** — All 40 routed RIUs exist in taxonomy v1.3.

### CHECK 4: service_routing services vs integration recipe dirs — 25 MISSING

| Source | Service | Expected Dir | Severity | Fix |
|--------|---------|-------------|----------|-----|
| service_routing_v1.0.yaml | AWS Bedrock Guardrails | integrations/aws-bedrock-guardrails/ | MISSING | Create recipe dir or add naming alias |
| service_routing_v1.0.yaml | AWS Comprehend | integrations/aws-comprehend/ | MISSING | Create recipe dir |
| service_routing_v1.0.yaml | AWS Comprehend PII | integrations/aws-comprehend-pii/ | MISSING | Create recipe dir |
| service_routing_v1.0.yaml | AWS Secrets Manager | integrations/aws-secrets-manager/ | MISSING | Create recipe dir |
| service_routing_v1.0.yaml | Arize AI (Phoenix) | integrations/arize-ai-(phoenix)/ | MISSING | Create recipe dir |
| service_routing_v1.0.yaml | Canva AI (Magic Media) | integrations/canva-ai-(magic-media)/ | MISSING | Create recipe dir |
| service_routing_v1.0.yaml | Claude (Anthropic) | integrations/claude-(anthropic)/ | MISSING | Map to existing claude-api/ |
| service_routing_v1.0.yaml | Datadog SLOs | integrations/datadog-slos/ | MISSING | Create recipe dir |
| service_routing_v1.0.yaml | ElastiCache (AWS) | integrations/elasticache-(aws)/ | MISSING | Create recipe dir |
| service_routing_v1.0.yaml | Fairlearn (Microsoft) | integrations/fairlearn-(microsoft)/ | MISSING | Create recipe dir |
| service_routing_v1.0.yaml | Gemini (Google DeepMind) | integrations/gemini-(google-deepmind)/ | MISSING | Map to existing gemini-api/ |
| service_routing_v1.0.yaml | Grok (xAI) | integrations/grok-(xai)/ | MISSING | Map to existing grok-api/ |
| service_routing_v1.0.yaml | Guardrails AI | integrations/guardrails-ai/ | MISSING | Create recipe dir |
| service_routing_v1.0.yaml | Kling 2.1/3.0 (via Higgsfield AI) | integrations/kling-2.1/3.0-... | MISSING | Map to existing kling-ai/ |
| service_routing_v1.0.yaml | LiteLLM (built-in) | integrations/litellm-(built-in)/ | MISSING | Create recipe dir |
| service_routing_v1.0.yaml | LiteLLM (self-hosted) | integrations/litellm-(self-hosted)/ | MISSING | Create recipe dir |
| service_routing_v1.0.yaml | NotebookLM (Google) | integrations/notebooklm-(google)/ | MISSING | Create recipe dir |
| service_routing_v1.0.yaml | OpenAI (GPT-4/o series) | integrations/openai-(gpt-4/o-series)/ | MISSING | Map to existing openai-api/ |
| service_routing_v1.0.yaml | OpenRouter (built-in) | integrations/openrouter-(built-in)/ | MISSING | Create recipe dir |
| service_routing_v1.0.yaml | Perplexity AI | integrations/perplexity-ai/ | MISSING | Create recipe dir |
| service_routing_v1.0.yaml | Redis (semantic layer) | integrations/redis-(semantic-layer)/ | MISSING | Create recipe dir |
| service_routing_v1.0.yaml | Runway (Aleph model) | integrations/runway-(aleph-model)/ | MISSING | Create recipe dir |
| service_routing_v1.0.yaml | Seedance Pro (via Higgsfield AI) | integrations/seedance-pro-... | MISSING | Create recipe dir |
| service_routing_v1.0.yaml | Whisper (OpenAI) — self-hosted | integrations/whisper-... | MISSING | Map to existing whisper-self-hosted/ |
| service_routing_v1.0.yaml | pgvector (PostgreSQL) | integrations/pgvector-(postgresql)/ | MISSING | Create recipe dir |

**Root cause**: Service routing uses display names with parenthetical qualifiers (e.g., "Claude (Anthropic)") while recipe directories use slug names (e.g., "claude-api"). No canonical mapping exists between the two naming schemes. At least 5 of these 25 have existing recipe dirs under different names (claude-api, gemini-api, grok-api, kling-ai, openai-api, whisper-self-hosted).

**Recommended fix**: Create a service-name-to-recipe-dir mapping file, or normalize service names in routing to match recipe directory slugs.

### CHECK 5: integration recipe dirs vs routing back-refs — 7 MISSING

| Source | Recipe Dir | Severity | Fix |
|--------|-----------|----------|-----|
| integrations/ | claude-api | MISSING | Add to service routing or create alias |
| integrations/ | gemini-api | MISSING | Map from "Gemini (Google DeepMind)" |
| integrations/ | github-api | MISSING | Add to service routing |
| integrations/ | grok-api | MISSING | Map from "Grok (xAI)" |
| integrations/ | kling-ai | MISSING | Map from "Kling 2.1/3.0 (via Higgsfield AI)" |
| integrations/ | openai-api | MISSING | Map from "OpenAI (GPT-4/o series)" |
| integrations/ | whisper-self-hosted | MISSING | Map from "Whisper (OpenAI) — self-hosted" |

**Root cause**: Same naming mismatch as Check 4. These 7 recipe dirs exist but aren't recognized because the routing file uses different names.

### CHECK 6: people_library vs company signals
**CLEAN** — 21 profiles, 33 signal companies. No orphan references.

### CHECK 7: RELATIONSHIP_GRAPH quads vs sources
**CLEAN** — Sampled 50 of 1,876 quads. All RIU and LIB references resolve.

### CHECK 8: palette/MANIFEST.yaml vs filesystem — 1 STALE

| Source | Field | Claimed | Actual | Severity | Fix |
|--------|-------|---------|--------|----------|-----|
| MANIFEST.yaml | layers.people_library.entries | 22 | 21 | STALE | Update to 21 |

### CHECK 9: agent steering files vs system state
**CLEAN** — 11 agents in MANIFEST, 11 directories on disk, all have steering files.

### CHECK 10: constellations.yaml vs published path files
**CLEAN** — All 5 published paths exist on disk. All path files are in a constellation. No orphans.

### CHECK 11: learning path routing-targets vs files
**CLEAN** — All live routing targets resolve. All coming-soon targets are correctly marked.

### CHECK 12: enablement/MANIFEST.yaml vs actuals — 1 STALE

| Source | Field | Claimed | Actual | Severity | Fix |
|--------|-------|---------|--------|----------|-----|
| enablement/MANIFEST.yaml | content_engine.version | 2.1 | 2.2 | STALE | Update to 2.2 |

### CHECK 13: skills vs referenced files — 4 MISSING

| Source | Skill | Issue | Severity | Fix |
|--------|-------|-------|----------|-----|
| skills/retail-ai/ | retail-ai | No README.md or skill.yaml | MISSING | Add README |
| skills/education/ | education | No README.md or skill.yaml | MISSING | Add README |
| skills/travel/ | travel | No README.md or skill.yaml | MISSING | Add README |
| skills/enablement/ | enablement | No README.md or skill.yaml (has other files) | MISSING | Add README |

### CHECK 14: naming consistency — 8 defects

| Source | Issue | Severity | Fix |
|--------|-------|----------|-----|
| palette/README.md | Claims "9 agents" (×3 mentions), MANIFEST lists 11 | MISALIGNED | Update README to 11 |
| palette/README.md | One mention of "28 RIUs" in a non-summary context | STALE | Verify context and update |
| enablement/README.md | Claims "9 agents", MANIFEST lists 11 | MISALIGNED | Update to 11 |
| peers-messaging.md | Documents 4 peer identities, broker has 5 (claude_code) | STALE | Add claude_code identity |
| 4 files | Use "PIS" (Palette Intelligence System) term not in MANIFEST/README | MISALIGNED | Decide: adopt term officially or remove |
| enablement/MANIFEST.yaml | content_engine.version=2.1, spec says 2.2 | STALE | Update to 2.2 |

---

## Analysis

### What's solid (7 of 14 checks clean)
The core data layer integrity is excellent:
- Module → KL references: 100% valid
- Module → taxonomy prerequisites: 100% valid
- Routing → taxonomy: 100% valid
- People → company signals: 100% valid
- Relationship graph: 100% valid (sampled)
- Constellations → paths: 100% valid
- Path routing targets: 100% valid

This means the data that powers the system is trustworthy. The enablement curriculum, knowledge library, taxonomy, and constellation system are all internally consistent.

### What needs work (2 clusters)

**Cluster 1: Service naming mismatch (32 defects)**
The service routing layer uses display names ("Claude (Anthropic)") while recipe directories use slugs ("claude-api"). This is a naming convention gap, not a data integrity gap — the recipes exist, they just can't be found by name. Fix: create a canonical name mapping or normalize one side.

**Cluster 2: Count/version drift in documentation (10 defects)**
READMEs and MANIFESTs have stale counts (agent count 9→11, people count 22→21, content engine version 2.1→2.2). This is documentation drift, not system drift. Fix: update the numbers.

### What's structurally interesting
- The MANIFEST says 11 agents but the README says 9. The 2 new agents (business-plan-creation, health) were added to the MANIFEST and filesystem but the README wasn't updated.
- "PIS" (Palette Intelligence System) is used in 4 files but isn't an official term in MANIFEST or README. This is a naming decision that needs to be made.
- The peers bus has identity drift: claude.analysis vs claude_code, kiro.design vs kiro. This should be resolved with canonical identities.

---

## Recommended Priority

1. **Quick wins** (30 min): Update stale counts in MANIFEST.yaml, enablement/MANIFEST.yaml, README.md, enablement/README.md
2. **Naming resolution** (1 hour): Create service-name-to-recipe-dir mapping; decide on "PIS" term; resolve peer identity canonical names
3. **Structural** (2-3 hours): Add missing recipe dirs for the 25 services, or create the mapping layer
4. **Housekeeping** (30 min): Add READMEs to 4 skill directories

---

**Audit complete. 42 defects found. 0 BROKEN (data integrity intact). All defects are STALE, MISALIGNED, or MISSING — fixable without structural changes.**


---

## Iteration 2 & 3 — Additional Findings

### Additional checks run (18 more)

| Check | Defects | Severity |
|-------|---------|----------|
| 2A. RELATIONSHIP_GRAPH full scan (1876 quads) | 0 | CLEAN |
| 2B. KL related_rius vs taxonomy | 0 | CLEAN |
| 2C. Module exercise integrity (351 exercises) | 0 | CLEAN |
| 2D. Certification tracks vs taxonomy | 0 | CLEAN |
| 2E. Journey files vs taxonomy | 0 | CLEAN |
| 2F. KIRO_STATUS.md claims | 0 | CLEAN |
| 2G. CODEX_STATUS.md claims | 0 | CLEAN |
| 2H. content-engine-spec constellation tables vs constellations.yaml | 3 | STALE |
| 3A. Markdown links in published paths | 0 | CLEAN |
| 3B. Calibration exemplar dims vs module rubric dims | 0 | CLEAN |
| 3C. Taxonomy workstreams vs curriculum dirs | 0 | CLEAN |
| 3D. PALETTE_QUICK_REFERENCE.md counts | 0 | CLEAN |
| 3E. enablement-coach.md references | 0 | CLEAN |
| 3F. Classification file header vs actual data | 1 | STALE |
| 3G. Module workstream field vs directory location | 0 | CLEAN |
| 3H. Orphan item-bank dirs | 1 | ORPHAN |
| 3I. YAML parse check (enablement) | 10 | BROKEN |
| 3J. YAML parse check (palette) | 0 | CLEAN |

### New defects found

**2H: content-engine-spec.md constellation tables — 3 STALE**

| Source | RIU | Spec says | Constellations.yaml says | Fix |
|--------|-----|-----------|-------------------------|-----|
| content-engine-spec.md | RIU-022 | planned | published | Update spec table |
| content-engine-spec.md | RIU-060 | planned | published | Update spec table |
| content-engine-spec.md | RIU-001 | planned | published | Update spec table |

**3F: Classification file header counts — 1 STALE**

| Source | Field | Claimed | Actual | Fix |
|--------|-------|---------|--------|-----|
| riu_classification_v1.0.yaml | both_count | 0 | 37 | Update header |
| riu_classification_v1.0.yaml | internal_only_count | 0 | 80 | Update header |
| riu_classification_v1.0.yaml | service_applicable_count | 0 | 0 | Correct (coincidentally) |

**3H: Orphan item-bank dir — 1 ORPHAN**

| Source | Dir | Issue | Fix |
|--------|-----|-------|-----|
| assessment/item-banks/ | RIU-401 | No matching module.yaml (RIU-401 not in taxonomy) | Known gap — keep until taxonomy adds RIU-401 |

**3I: YAML parse errors in credential files — 10 BROKEN**

All 10 files in `assessment/credentials/` and `certification/credentials/` use JSON-LD `@context` syntax which is invalid unquoted YAML. The `@` character must be quoted.

| Files affected | Error | Fix |
|---------------|-------|-----|
| 10 credential/badge YAML files | `@context` not quoted | Quote as `"@context"` |

---

## Revised Summary (after 3 iterations)

| Severity | Original | Added | Total |
|----------|----------|-------|-------|
| BROKEN | 0 | 10 | 10 |
| STALE | 4 | 4 | 8 |
| MISALIGNED | 6 | 0 | 6 |
| MISSING | 32 | 0 | 32 |
| ORPHAN | 0 | 1 | 1 |
| **Total** | **42** | **15** | **57** |

### What the additional iterations found

The first pass caught the big structural issues (service naming, count drift). Iterations 2 and 3 found:

1. **10 unparseable YAML files** — credential/badge files using JSON-LD `@context` without quoting. These files would fail any YAML parser. This is the only BROKEN finding in the entire audit.
2. **3 stale constellation statuses** in content-engine-spec.md — RIU-022, RIU-060, RIU-001 are published but spec still says "planned."
3. **1 stale classification header** — the header summary counts are all 0 but the actual data has 117 classified RIUs.
4. **1 orphan item-bank** — RIU-401 has calibration exemplars but no module (known taxonomy gap).

### What held up perfectly across all 32 checks

- Module → KL references (117 modules, all valid)
- Module → taxonomy prerequisites (all valid)
- Relationship graph (1,876 quads, all valid)
- Exercise integrity (351 exercises, all valid)
- Journey files (all valid)
- Certification tracks (all valid)
- Constellation → path files (all valid)
- Path routing targets (all valid)
- Markdown links in paths (all valid)
- Calibration exemplar dimensions match module rubric dimensions
- Taxonomy workstreams match curriculum directories
- Module workstream fields match directory locations
- All palette YAML files parse cleanly
