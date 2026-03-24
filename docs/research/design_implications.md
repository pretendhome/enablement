# Research → Design Implications

How the certification landscape research informs our architecture decisions.

## Validated: Our System Is in the Opportunity Space

The research confirms that **no certification program currently combines**:
1. Portfolio-based assessment (ours)
2. LLM-as-judge for human competency evaluation (ours)
3. Competency graph with adaptive pathways (ours)
4. Performance-based assessment across all tiers (CKA/CKAD comes closest)

We are building in genuinely unoccupied territory.

## Design Decisions Informed by Research

### 1. Assessment Method — Confirmed: No Multiple Choice

| What we're doing | What research says |
|---|---|
| 100% artifact/portfolio-based | CNCF CKA/CKAD (100% performance-based) is the most employer-trusted certification. HashiCorp Professional's Docker labs are second. MCQ-only programs (Databricks, NVIDIA) are respected less by hiring managers. |

**Decision**: Stay the course. Our portfolio-based approach aligns with the highest-trust certifications.

### 2. Tier Structure — Confirmed: 3 Tiers

| What we're doing | What research says |
|---|---|
| UNVALIDATED → WORKING → PRODUCTION | Mature programs use 2-4 tiers. AWS (4) is most mature but complex. CNCF (2) is simplest. 3 tiers is the sweet spot. |

**Decision**: Our 3-tier model (UNVALIDATED → WORKING → PRODUCTION) maps cleanly to:
- UNVALIDATED = Foundational (learning/placement complete)
- WORKING = Associate (demonstrated competence on one track)
- PRODUCTION = Professional (expert across 2+ tracks)

### 3. LLM-as-Judge — We're First Movers

**Key finding**: "No major certification program uses LLM-as-judge to evaluate candidate responses in production" (as of March 2026).

- LLM judges achieve 80-90% agreement with human evaluators
- Our target: >80% AI-human agreement per LIB-114
- Best practice: 30-50 expert-annotated calibration examples per dimension

**Action items**:
- Build calibration exemplar sets for each rubric dimension (this is the anchor item bank)
- Target 50 calibration examples per module for production quality
- Start with 3-5 anchor items per module (Phase 1), expand to 15-30 (Phase 2)
- Implement human calibration on 10% of submissions from day one

### 4. Credentialing — Adopt Open Badges 3.0

**Key finding**: OB 3.0 built on W3C Verifiable Credentials is the clear standard. Credly (3,600+ issuers) or Accredible (130M+ credentials) for issuance.

**Decision**: Build on OB 3.0 from day one.
- Use Accredible (better for learning pathway visualization, supports OB 3.0 + ACE extension)
- Each certification tier gets its own badge with competency metadata
- Badges are cryptographically verifiable without our server being online

### 5. Validity Period — 2 Years with Renewal Assessment

**Key finding**: Industry standard is 2 years. Google's shorter renewal exam is the most candidate-friendly.

**Decision**:
- WORKING: 2-year validity, renewal via shortened assessment (new items only)
- PRODUCTION: 2-year validity, renewal via architecture defense + portfolio update

### 6. Pricing Model — Not Yet (Phase 3+)

**Key finding**: Market clusters at $99-200 for standard, $295-445 for performance-based. Performance-based commands a premium because it's harder to build and more trusted.

**Decision**: Defer pricing to Phase 3. Our portfolio + AI-graded approach would justify premium pricing ($200-400 range) once validated.

### 7. Adaptive Assessment — Future Phase

**Key finding**: CAT requires 300-500 calibrated items minimum. No developer cert uses full CAT. ISC2 is the only precedent in adjacent fields.

**Decision**: Our placement assessment uses adaptive logic (PLACE-01 through PLACE-04). Full CAT implementation is Phase 3+ once item banks reach sufficient size (requires >200 calibrated items per track).

### 8. Anthropic CCA-F Positioning

**Key finding**: Anthropic's CCA-F is MCQ-only (60 questions, 120 min, $99). It covers agentic architecture (27%), Claude Code (20%), prompt engineering (20%), MCP (18%), context management (15%).

**Implication for our system**: Our modules RIU-510 (Multi-Agent Workflow), RIU-022 (Prompt Interface Contract), and RIU-082 (Safety Guardrails) teach the same competencies CCA-F tests — but our assessment requires the learner to actually build these things, not select from multiple choice. This is a complementary offering, not a competitor.

## Risk: What Could Invalidate Our Approach

1. **LLM-as-judge reliability at scale**: If our AI evaluator can't maintain >80% agreement with humans on portfolio artifacts (more complex than model outputs), we'll need heavier human calibration.
2. **Candidate gaming**: Portfolio artifacts are harder to game than MCQ, but AI-generated submissions are a risk. Mitigation: architecture defense (oral exam component) for PRODUCTION tier.
3. **Item bank cold start**: We need 3-5 anchor items per module × 117 modules = 350-585 calibration examples before launch. This is the bottleneck.

## Source
Based on research at `docs/research/certification_best_practices.md`, conducted 2026-03-24.
