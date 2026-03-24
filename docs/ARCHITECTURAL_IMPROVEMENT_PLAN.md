# Enablement System v0.3 — Architectural Improvement Plan

Date: 2026-03-24
Status: Iterations 1-2 complete, 3-5 assigned

## Input Sources

This plan synthesizes findings from four independent reviews run through the full Palette protocol (Classify → Knowledge Library → Service Routing → Route to Agent → Log):

1. **Kiro stress test** (2 critical, 2 moderate, 1 low, 19 passing across 117 modules)
2. **Codex retrospective** (4 systemic weaknesses in generation discipline)
3. **Mistral review** (10 strategic observations on system maturity)
4. **Claude Code post-fix audit** (3 remaining risks from traceability remediation)

## Palette Protocol Classification

Primary RIUs: RIU-540 (Quality Gates), RIU-534 (Audit Trail), RIU-003 (Traceability Matrix)
Service routing: internal_only — this is Palette's own quality infrastructure
Agent routing: Multi-agent coordination (Claude Code: architecture/orchestration, Kiro: infrastructure/schema, Codex: assessment/calibration, Mistral: content/credentials)

## Design Principles

1. **Fail closed** — validators catch problems and block, never silently pass
2. **Semantic over syntactic** — check meaning (KL reference validity, threshold parsability), not just structure
3. **Front-load quality** — enforce assessment contracts at creation time, not cleanup time
4. **Layer defense** — multiple independent checks with intentional overlap

---

## Iteration 1: Critical Defect Repair (COMPLETE)

### Findings
- F-002: Recommended prerequisite cycle RIU-005 ↔ RIU-006
- F-003: Dangling KL reference — RIU-082 referenced LIB-082 (game dev) instead of LIB-090 (guardrails)
- F-004: Two modules (RIU-502, RIU-511) with zero KL references
- Post-fix audit: RIU-607 and RIU-327 thresholds already tightened

### Fixes Applied
| Issue | Fix | File |
|---|---|---|
| RIU-005 ↔ RIU-006 cycle | Removed RIU-005 from RIU-006 recommended prereqs | RIU-006/module.yaml |
| RIU-082 wrong KL ref | LIB-082 → LIB-090 (guardrails entry) | RIU-082/module.yaml |
| RIU-502 zero KL | Added LIB-076 (multimodal pipelines) + LIB-023 (transcription) | RIU-502/module.yaml |
| RIU-511 zero KL | Added LIB-097 (restartability) + LIB-077 (agent reasoning) | RIU-511/module.yaml |

### Validation After Iteration 1
- integrity.py: PASS (0 errors, 0 warnings)
- prerequisite_validator.py: PASS
- coverage_report.py: PASS (100% RIU coverage)

---

## Iteration 2: Validator Hardening (COMPLETE)

### Problem
Existing validators (integrity.py, prerequisite_validator.py, coverage_report.py) all reported PASS before Iteration 1, despite real defects existing. Kiro's stress test found issues the validators couldn't detect.

### Upgrades Applied

**integrity.py** — 2 new checks:
1. **KL Reference Validation** (check 5): Loads actual KL file (all 3 sections: library_questions, gap_additions, context_specific_questions), validates every LIB-ID reference exists. Also warns on zero-KL modules.
2. **Threshold Parsability** (check 6): Imports threshold_engine.py and parse_threshold() to validate all 234 threshold strings (117 × WORKING + PRODUCTION). Fail-closed: unparseable strings are errors.

**prerequisite_validator.py** — 1 new check:
1. **Recommended Prerequisite Cycles** (check 4): DFS cycle detection on recommended prereqs, separate from the required prereq DAG check. Reports as warnings (non-blocking).

**coverage_report.py** — KL cross-validation:
1. Dangling refs: KL IDs referenced by modules that don't exist in any KL section
2. Zero-KL modules: Modules with no primary or supporting KL references
3. Unused KL entries: Entries in the library not referenced by any module
4. Fixed KL loader: Now reads all 3 sections (was only reading library_questions, missing 36 entries)

### Validation After Iteration 2
- integrity.py: PASS (0 errors, 4 warnings — 4 modules with zero KL refs)
- prerequisite_validator.py: PASS (all 5 checks pass, including recommended cycles)
- coverage_report.py: PASS (167 KL entries, 134 referenced, 80.2% utilization)
- threshold_engine.py: 89/89 self-tests pass

---

## Iteration 3: Assessment Pipeline Completion (IN PROGRESS)

### Objective
Complete the Layer 2 scoring infrastructure so the system can evaluate submissions end-to-end.

### Deliverables

| Deliverable | Owner | Status |
|---|---|---|
| Reference calibration exemplar (RIU-002) | Claude Code | DONE |
| Threshold engine | Claude Code | DONE (89/89 tests) |
| Calibration exemplars for 5+ more modules | Codex | ASSIGNED |
| Wire threshold engine into demo_runner evaluate | Kiro | ASSIGNED |
| Add KL refs to 4 zero-KL modules | Kiro | ASSIGNED |
| Layer 2 prompt assembly module | Codex | ASSIGNED |

### Quality Gate
- integrity.py reports 0 warnings (zero-KL modules resolved)
- demo_runner evaluate uses threshold engine for certification decisions
- At least 6 modules have calibration exemplars

---

## Iteration 4: Credential & Certification Integration (PLANNED)

### Objective
Wire credentials, tiers, and tracks into a complete certification workflow.

### Deliverables

| Deliverable | Owner | Status |
|---|---|---|
| Open Badges 3.0 credential schemas | Mistral | ASSIGNED |
| Validate tier/track files against module data | Kiro | ASSIGNED |
| Credential issuance workflow (submission → eval → badge) | Claude Code | PLANNED |
| Integration test: full pipeline end-to-end | Claude Code | PLANNED |

### Quality Gate
- Tier files reference only valid modules
- Track files sum to correct RIU counts
- Credential schema validates against OB 3.0 spec

---

## Iteration 5: Operational Readiness (PLANNED)

### Objective
System is demonstrable in an interview setting and has a sustainable update cadence.

### Deliverables

| Deliverable | Owner | Status |
|---|---|---|
| Content update cadence and process doc | Mistral | PLANNED |
| Interview demo script (5-minute walkthrough) | Claude Code | PLANNED |
| Remaining zero-KL modules resolved | Kiro | PLANNED |
| 33 orphan KL entries: evaluate and integrate or document exclusion | Codex | PLANNED |

### Quality Gate
- All validators pass with 0 warnings
- Demo script runs end-to-end without errors
- MANIFEST.yaml updated to v0.3.0

---

## Cross-Cutting Improvements (Codex Retrospective)

These are systemic improvements that span all iterations:

1. **Assessment contract enforcement**: The threshold engine + upgraded integrity checks now enforce threshold parsability at validation time. Future module generation must pass these checks.

2. **Calibration exemplar quality bar**: The RIU-002 reference exemplar sets the standard. Key rule: levels differ by quality of thinking, not word count. This reference is the input for Codex's exemplar scaling work.

3. **Threshold policy centralization**: The threshold engine parses all 11 patterns used across 117 modules. Modules cannot silently under-gate critical competencies because integrity.py now validates parsability.

4. **Semantic linting**: integrity.py now does KL reference validation (semantic, not just structural). The objective traceability check already does token-based semantic matching. Future work: validate that module names match taxonomy names.

---

## System State Summary

| Metric | Before | After Iteration 2 |
|---|---|---|
| Validator checks | 8 | 14 |
| Critical defects | 2 | 0 |
| KL loader coverage | 131/167 (78%) | 167/167 (100%) |
| Dangling KL refs | 1 (LIB-082 wrong) | 0 |
| Prerequisite cycles | 1 (recommended) | 0 |
| Zero-KL modules | 6 | 4 (2 fixed, 4 remaining) |
| Threshold validation | none | 234/234 parse correctly |
| Calibration exemplars | 2 (poor quality) | 1 reference + 2 legacy |
| Assessment components | evaluator prompt only | prompt + threshold engine + automated checks |
