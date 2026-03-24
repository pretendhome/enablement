# AI Rubric Evaluator — System Prompt

You are an assessment evaluator for the Palette Developer Enablement & Certification System. You evaluate developer-submitted artifacts against module rubrics using calibrated scoring.

## Your Role

You are Layer 2 of a 3-layer evaluation system:
- **Layer 1** (automated): Already passed — artifacts are present, code runs, sources are cited
- **Layer 2** (you): Evaluate each rubric dimension against calibration exemplars
- **Layer 3** (human): 10% of submissions are double-scored by humans for calibration

## Evaluation Process

### Input
1. **Module rubric** (`module.yaml` → `rubric_dimensions`)
2. **Submitted artifacts** (the developer's work products)
3. **Calibration exemplars** (example artifacts at each rubric level — when available)

### Scoring

For each rubric dimension, assign one of four levels:

| Level | Criteria |
|---|---|
| **insufficient** | Missing, superficial, or fundamentally wrong. Does not demonstrate the competency. |
| **basic** | Present but incomplete. Shows awareness of the concept but not practical ability. |
| **competent** | Solid work that a practitioner would produce. Covers the key aspects, handles common cases, and is defensible. |
| **expert** | Goes beyond competent — anticipates edge cases, makes non-obvious tradeoffs, demonstrates deep understanding. Would serve as a calibration exemplar for others. |

### Output Format

```yaml
evaluation:
  module: "RIU-XXX"
  submission_id: "SUB-XXXXX"
  evaluator: "ai_rubric_v1"
  timestamp: "YYYY-MM-DDTHH:MM:SSZ"

  dimensions:
    dimension_name:
      level: "competent"          # One of: insufficient, basic, competent, expert
      evidence: "..."             # 2-3 sentences citing specific evidence from the submission
      calibration_note: "..."     # How this compares to calibration exemplars (if available)

  overall:
    certification_eligible: true  # Does this meet the WORKING threshold?
    production_eligible: false    # Does this meet the PRODUCTION threshold?

  feedback:
    strengths: ["...", "..."]     # 2-3 specific strengths
    improvements: ["...", "..."]  # 2-3 actionable improvements
    next_steps: "..."            # Suggested next module or skill to develop
```

## Calibration Rules

1. **Anchor to evidence, not impressions.** Every level assignment must cite specific evidence from the submission.
2. **Use calibration exemplars when available.** Compare the submission to exemplars at each level. If no exemplars exist, use the rubric description as the standard.
3. **Competent is the target, not expert.** Most working practitioners should score competent. Expert means genuinely exceptional — reserve it.
4. **Insufficient requires explanation.** If scoring insufficient, explain what is missing and what would move it to basic.
5. **Don't double-penalize.** If a single weakness affects multiple dimensions, score each dimension on its own terms.
6. **Flag uncertainty.** If you're uncertain between two levels, flag it in calibration_note for human review.
7. **Confidence scoring.** For each dimension, include a confidence score (high/medium/low). Low confidence triggers automatic escalation to human review. This is mandatory — research shows LLM expert agreement is only 64-68%, so honest uncertainty reporting is essential for system integrity.
8. **Bias awareness.** Score substance, not length (verbosity bias). Use absolute scoring against the rubric, not relative ranking (position bias). Do not favor responses that resemble your own training patterns (self-preference bias).

## Escalation Triggers

The following automatically escalate a submission to human review (Layer 3):
- Any dimension scored with **low confidence**
- Any submission where the overall result is **borderline** (e.g., exactly at the WORKING threshold)
- Any submission where **2+ dimensions** are scored at adjacent levels with medium confidence
- Any **PRODUCTION-tier** evaluation (all PRODUCTION submissions require human sign-off)

## Certification Threshold Check

After scoring all dimensions, check against the module's `certification_tier_thresholds`:

- **WORKING**: Check the specific threshold (e.g., "competent on 3/4 dimensions")
- **PRODUCTION**: Check the specific threshold (e.g., "expert on 2/4, competent on remaining")

Set `certification_eligible` and `production_eligible` accordingly.

## What You Do NOT Do

- You do not grade on style, formatting, or polish — only on competency
- You do not compare submissions to each other — only to the rubric and exemplars
- You do not add requirements beyond what the rubric specifies
- You do not penalize alternative approaches that achieve the same outcome
- You do not evaluate intent — only artifacts and demonstrated capability


---

# Evaluation Request

**Module:** RIU-002 — Stakeholder Map + RACI-lite
**Submission ID:** SUB-202603242122
**Timestamp:** 2026-03-24T21:22:10Z

## Module Rubric

```yaml
rubric_dimensions:
  stakeholder_coverage:
    description: All relevant stakeholders identified including hidden influencers
      and late-stage approvers
    levels:
    - insufficient
    - basic
    - competent
    - expert
  ownership_clarity:
    description: Every key decision and artifact has exactly one accountable owner
      with no ambiguity
    levels:
    - insufficient
    - basic
    - competent
    - expert
  escalation_design:
    description: Escalation path has clear triggers, defined paths, and prevents deadlock
    levels:
    - insufficient
    - basic
    - competent
    - expert
  practical_applicability:
    description: "Map and RACI are actionable \u2014 team can use them immediately\
      \ without further clarification"
    levels:
    - insufficient
    - basic
    - competent
    - expert
```

## Certification Thresholds

```yaml
certification_tier_thresholds:
  WORKING: competent on 3/4 dimensions
  PRODUCTION: expert on 2/4, competent on remaining
```

## Submitted Artifacts

### `escalation_path.md`

```
# Escalation Protocol — AI Customer Service Assistant

## Escalation Tiers

| Tier | Scope | Resolution SLA | Who Resolves |
|------|-------|---------------|--------------|
| **Tier 1** | Within a single domain (e.g., tech disagreement) | 48 hours | Domain Accountable (per RACI) |
| **Tier 2** | Cross-domain (e.g., security vs. timeline) | 5 business days | Joint session: both Accountable owners + project lead |
| **Tier 3** | Executive deadlock or one-way door disagreement | 10 business days | CEO (Diana Park) as tiebreaker |

## Escalation Triggers

A decision escalates when ANY of these conditions are met:

| Trigger | Example | Escalates To |
|---------|---------|-------------|
| **SLA breach** | Decision not made within 48 hours of request | Next tier up |
| **Veto exercised** | Compliance blocks a technical decision | Tier 2 joint session |
| **Scope conflict** | CTO and VP CS disagree on whether a feature is in-scope | Tier 2 joint session |
| **Budget conflict** | Requested spend exceeds approved envelope | Tier 3 (CEO + Finance) |
| **One-way door disagreement** | Stakeholders disagree on vendor selection | Tier 3 (CEO) |
| **Safety concern** | Any stakeholder flags a safety/compliance risk | Immediate Tier 2 with Compliance + CISO |

## Escalation Process

### Step 1: Document the Disagreement
Before escalating, the requesting party must write a 1-page brief:
- **What** is the decision?
- **Who** disagrees and **why**?
- **What** are the options (minimum 2)?
- **What** happens if we don't decide by [date]?

### Step 2: Route to the Right Tier
```
Is it within one domain?
  YES → Tier 1: Domain Accountable decides within 48h
  NO  → Is it a one-way door or executive-level?
          YES → Tier 3: CEO tiebreaker
          NO  → Tier 2: Joint session within 5 days
```

### Step 3: Resolution Meeting Format
- **Tier 2 format**: 30-minute facilitated session. Project lead presents options. Each Accountable has 5 minutes to state position. Decision made in the room or deferred to Tier 3.
- **Tier 3 format**: CEO receives the 1-page brief + Tier 2 notes. 15-minute decision meeting. CEO's decision is final and logged in the Decision Log.

### Step 4: Log and Communicate
Every escalation resolution is logged in the **Decision Log** (see RIU-003) with:
- Decision made
- Rationale
- Who decided
- Who was overruled (if applicable)
- Classification: ONE-WAY DOOR or TWO-WAY DOOR

## Deadlock Prevention Mechanisms

### 1. Pre-Scheduled Review Gates
Rather than waiting for conflicts, schedule mandatory alignment checkpoints:

| Gate | When | Who Must Attend | Purpose |
|------|------|-----------------|---------|
| G1: Requirements Lock | End of Phase 1 | All Accountable owners | Confirm scope and constraints |
| G2: Architecture Review | Before implementation | CTO + CISO + Compliance | Technical + security + compliance alignment |
| G3: Pre-Launch Readiness | Before public launch | All stakeholders | Final GO/NO-GO |

### 2. Silent Stakeholder Protocol
**Problem**: A stakeholder who doesn't respond is often a stakeholder who blocks later.

**Rule**: If a Consulted stakeholder does not respond within the SLA:
1. Send a reminder with explicit deadline
2. If no response by deadline, escalate to their manager
3. Document the non-response in the Decision Log
4. If the decision is TWO-WAY DOOR, proceed with documented assumption
5. If the decision is ONE-WAY DOOR, the decision **cannot proceed** without explicit sign-off

### 3. Proxy Authority
Each Accountable owner must name a **delegate** who can make decisions in their absence:

| Accountable | Delegate | Authority Scope |
|-------------|----------|-----------------|
| Sarah (CTO) | James (Data Eng Lead) | Technical decisions only, no vendor selection |
| Marcus (VP CS) | Ana (CS Team Lead) | Workflow decisions only, no budget |
| Diana (CEO) | Sarah (CTO) | TWO-WAY DOOR decisions only |
| Raj (Compliance) | *No delegate — Compliance decisions require Raj* | N/A |
| Lisa (CISO) | *No delegate — Security decisions require Lisa* | N/A |

**Note**: Compliance and Security have no delegates by design — these are areas where authority should not be diluted.

## References

- Escalation tier structure adapted from ITIL incident management framework (https://www.axelos.com/certifications/itil-service-management)
- Silent stakeholder protocol informed by Palette Knowledge Library LIB-005 (handling changing requirements) and LIB-010 (when to escalate vs continue converging)
- Review gate pattern from NASA Systems Engineering Handbook, Section 6.8 — Technical Reviews (https://www.nasa.gov/reference/systems-engineering-handbook/)
```

### `layer2_evaluation_prompt_riu-002.md`

```
# AI Rubric Evaluator — System Prompt

You are an assessment evaluator for the Palette Developer Enablement & Certification System. You evaluate developer-submitted artifacts against module rubrics using calibrated scoring.

## Your Role

You are Layer 2 of a 3-layer evaluation system:
- **Layer 1** (automated): Already passed — artifacts are present, code runs, sources are cited
- **Layer 2** (you): Evaluate each rubric dimension against calibration exemplars
- **Layer 3** (human): 10% of submissions are double-scored by humans for calibration

## Evaluation Process

### Input
1. **Module rubric** (`module.yaml` → `rubric_dimensions`)
2. **Submitted artifacts** (the developer's work products)
3. **Calibration exemplars** (example artifacts at each rubric level — when available)

### Scoring

For each rubric dimension, assign one of four levels:

| Level | Criteria |
|---|---|
| **insufficient** | Missing, superficial, or fundamentally wrong. Does not demonstrate the competency. |
| **basic** | Present but incomplete. Shows awareness of the concept but not practical ability. |
| **competent** | Solid work that a practitioner would produce. Covers the key aspects, handles common cases, and is defensible. |
| **expert** | Goes beyond competent — anticipates edge cases, makes non-obvious tradeoffs, demonstrates deep understanding. Would serve as a calibration exemplar for others. |

### Output Format

```yaml
evaluation:
  module: "RIU-XXX"
  submission_id: "SUB-XXXXX"
  evaluator: "ai_rubric_v1"
  timestamp: "YYYY-MM-DDTHH:MM:SSZ"

  dimensions:
    dimension_name:
      level: "competent"          # One of: insufficient, basic, competent, expert
      evidence: "..."             # 2-3 sentences citing specific evidence from the submission
      calibration_note: "..."     # How this compares to calibration exemplars (if available)

  overall:
    certification_eligible: true  # Does this meet the WORKING threshold?
    production_eligible: false    # Does this meet the PRODUCTION threshold?

  feedback:
    strengths: ["...", "..."]     # 2-3 specific strengths
    improvements: ["...", "..."]  # 2-3 actionable improvements
    next_steps: "..."            # Suggested next module or skill to develop
```

## Calibration Rules

1. **Anchor to evidence, not impressions.** Every level assignment must cite specific evidence from the submission.
2. **Use calibration exemplars when available.** Compare the submission to exemplars at each level. If no exemplars exist, use the rubric description as the standard.
3. **Competent is the target, not expert.** Most working practitioners should score competent. Expert means genuinely exceptional — reserve it.
4. **Insufficient requires explanation.** If scoring insufficient, explain what is missing and what would move it to basic.
5. **Don't double-penalize.** If a single weakness affects multiple dimensions, score each dimension on its own terms.
6. **Flag uncertainty.** If you're uncertain between two levels, flag it in calibration_note for human review.
7. **Confidence scoring.** For each dimension, include a confidence score (high/medium/low). Low confidence triggers automatic escalation to human review. This is mandatory — research shows LLM expert agreement is only 64-68%, so honest uncertainty reporting is essential for system integrity.
8. **Bias awareness.** Score substance, not length (verbosity bias). Use absolute scoring against the rubric, not relative ranking (position bias). Do not favor responses that resemble your own training patterns (self-preference bias).

## Escalation Triggers

The following automatically escalate a submission to human review (Layer 3):
- Any dimension scored with **low confidence**
- Any submission where the overall result is **borderline** (e.g., exactly at the WORKING threshold)
- Any submission where **2+ dimensions** are scored at adjacent levels with medium confidence
- Any **PRODUCTION-tier** evaluation (all PRODUCTION submissions require human sign-off)

## Certification Threshold Check

After scoring all dimensions, check against the module's `certification_tier_thresholds`:

- **WORKING**: Check the specific threshold (e.g., "competent on 3/4 dimensions")
- **PRODUCTION**: Check the specific threshold (e.g., "expert on 2/4, competent on remaining")

Set `certification_eligible` and `production_eligible` accordingly.

## What You Do NOT Do

- You do not grade on style, formatting, or polish — only on competency
- You do not compare submissions to each other — only to the rubric and exemplars
- You do not add requirements beyond what the rubric specifies
- You do not penalize alternative approaches that achieve the same outcome
- You do not evaluate intent — only artifacts and demonstrated capability


---

# Evaluation Request

**Module:** RIU-002 — Stakeholder Map + RACI-lite
**Submission ID:** SUB-202603241942
**Timestamp:** 2026-03-24T19:42:54Z

## Module Rubric

```yaml
rubric_dimensions:
  stakeholder_coverage:
    description: All relevant stakeholders identified including hidden influencers
      and late-stage approvers
    levels:
    - insufficient
    - basic
    - competent
    - expert
  ownership_clarity:
    description: Every key decision and artifact has exactly one accountable owner
      with no ambiguity
    levels:
    - insufficient
    - basic
    - competent
    - expert
  escalation_design:
    description: Escalation path has clear triggers, defined paths, and prevents deadlock
    levels:
    - insufficient
    - basic
    - competent
    - expert
  practical_applicability:
    description: "Map and RACI are actionable \u2014 team can use them immediately\
      \ without further clarification"
    levels:
    - insufficient
    - basic
    - competent
    - expert
```

## Certification Thresholds

```yaml
certification_tier_thresholds:
  WORKING: competent on 3/4 dimensions
  PRODUCTION: expert on 2/4, competent on remaining
```

## Submitted Artifacts

### `escalation_path.md`

```
# Escalation Protocol — AI Customer Service Assistant

## Escalation Tiers

| Tier | Scope | Resolution SLA | Who Resolves |
|------|-------|---------------|--------------|
| **Tier 1** | Within a single domain (e.g., tech disagreement) | 48 hours | Domain Accountable (per RACI) |
| **Tier 2** | Cross-domain (e.g., security vs. timeline) | 5 business days | Joint session: both Accountable owners + project lead |
| **Tier 3** | Executive deadlock or one-way door disagreement | 10 business days | CEO (Diana Park) as tiebreaker |

## Escalation Triggers

A decision escalates when ANY of these conditions are met:

| Trigger | Example | Escalates To |
|---------|---------|-------------|
| **SLA breach** | Decision not made within 48 hours of request | Next tier up |
| **Veto exercised** | Compliance blocks a technical decision | Tier 2 joint session |
| **Scope conflict** | CTO and VP CS disagree on whether a feature is in-scope | Tier 2 joint session |
| **Budget conflict** | Requested spend exceeds approved envelope | Tier 3 (CEO + Finance) |
| **One-way door disagreement** | Stakeholders disagree on vendor selection | Tier 3 (CEO) |
| **Safety concern** | Any stakeholder flags a safety/compliance risk | Immediate Tier 2 with Compliance + CISO |

## Escalation Process

### Step 1: Document the Disagreement
Before escalating, the requesting party must write a 1-page brief:
- **What** is the decision?
- **Who** disagrees and **why**?
- **What** are the options (minimum 2)?
- **What** happens if we don't decide by [date]?

### Step 2: Route to the Right Tier
```
Is it within one domain?
  YES → Tier 1: Domain Accountable decides within 48h
  NO  → Is it a one-way door or executive-level?
          YES → Tier 3: CEO tiebreaker
          NO  → Tier 2: Joint session within 5 days
```

### Step 3: Resolution Meeting Format
- **Tier 2 format**: 30-minute facilitated session. Project lead presents options. Each Accountable has 5 minutes to state position. Decision made in the room or deferred to Tier 3.
- **Tier 3 format**: CEO receives the 1-page brief + Tier 2 notes. 15-minute decision meeting. CEO's decision is final and logged in the Decision Log.

### Step 4: Log and Communicate
Every escalation resolution is logged in the **Decision Log** (see RIU-003) with:
- Decision made
- Rationale
- Who decided
- Who was overruled (if applicable)
- Classification: ONE-WAY DOOR or TWO-WAY DOOR

## Deadlock Prevention Mechanisms

### 1. Pre-Scheduled Review Gates
Rather than waiting for conflicts, schedule mandatory alignment checkpoints:

| Gate | When | Who Must Attend | Purpose |
|------|------|-----------------|---------|
| G1: Requirements Lock | End of Phase 1 | All Accountable owners | Confirm scope and constraints |
| G2: Architecture Review | Before implementation | CTO + CISO + Compliance | Technical + security + compliance alignment |
| G3: Pre-Launch Readiness | Before public launch | All stakeholders | Final GO/NO-GO |

### 2. Silent Stakeholder Protocol
**Problem**: A stakeholder who doesn't respond is often a stakeholder who blocks later.

**Rule**: If a Consulted stakeholder does not respond within the SLA:
1. Send a reminder with explicit deadline
2. If no response by deadline, escalate to their manager
3. Document the non-response in the Decision Log
4. If the decision is TWO-WAY DOOR, proceed with documented assumption
5. If the decision is ONE-WAY DOOR, the decision **cannot proceed** without explicit sign-off

### 3. Proxy Authority
Each Accountable owner must name a **delegate** who can make decisions in their absence:

| Accountable | Delegate | Authority Scope |
|-------------|----------|-----------------|
| Sarah (CTO) | James (Data Eng Lead) | Technical decisions only, no vendor selection |
| Marcus (VP CS) | Ana (CS Team Lead) | Workflow decisions only, no budget |
| Diana (CEO) | Sarah (CTO) | TWO-WAY DOOR decisions only |
| Raj (Compliance) | *No delegate — Compliance decisions require Raj* | N/A |
| Lisa (CISO) | *No delegate — Security decisions require Lisa* | N/A |

**Note**: Compliance and Security have no delegates by design — these are areas where authority should not be diluted.

## References

- Escalation tier structure adapted from ITIL incident management framework (https://www.axelos.com/certifications/itil-service-management)
- Silent stakeholder protocol informed by Palette Knowledge Library LIB-005 (handling changing requirements) and LIB-010 (when to escalate vs continue converging)
- Review gate pattern from NASA Systems Engineering Handbook, Section 6.8 — Technical Reviews (https://www.nasa.gov/reference/systems-engineering-handbook/)
```

### `raci_lite.md`

```
# RACI-Lite Matrix — AI Customer Service Assistant

## Definitions

| Role | Meaning | Rule |
|------|---------|------|
| **A** (Accountable) | Final decision-maker. Signs off. | Exactly ONE per row. |
| **R** (Responsible) | Does the work or leads the effort. | One or more per row. |
| **C** (Consulted) | Must be asked before the decision is made. Input is required. | Zero or more. |
| **I** (Informed) | Told after the decision. No input required. | Zero or more. |

## Matrix

| Decision / Artifact | Sarah (CTO) | Marcus (VP CS) | Diana (CEO) | Raj (Compliance) | Lisa (CISO) | Tom (Legal) | Ana (CS Lead) | James (Data Eng) | Priya (CX Dir) | Finance |
|---|---|---|---|---|---|---|---|---|---|---|
| **Technical architecture selection** | **A** | C | I | C | C | I | I | R | I | I |
| **AI vendor contract** | R | I | I | C | C | **A** | I | I | I | C |
| **Customer data handling policy** | C | C | I | **A** | C | C | I | R | I | I |
| **CS workflow redesign** | C | **A** | I | I | I | I | R | C | C | I |
| **Brand voice / tone for AI responses** | I | C | I | I | I | I | C | I | **A** | I |
| **Security pen test plan** | C | I | I | I | **A** | I | I | R | I | I |
| **GO/NO-GO for public launch** | R | R | **A** | C | C | C | I | I | C | I |
| **Budget approval (>$200K)** | R | I | C | I | I | I | I | I | I | **A** |
| **Escalation from AI to human agent** | C | **A** | I | C | I | I | R | C | C | I |
| **Model training data selection** | C | C | I | C | **A** | I | I | R | I | I |
| **Press release / external comms** | C | C | **A** | C | I | C | I | I | R | I |

## Ownership Verification

Every row has exactly one **A**:
- Sarah (CTO): 1 row (technical architecture)
- Marcus (VP CS): 2 rows (CS workflow, escalation design)
- Diana (CEO): 2 rows (GO/NO-GO, press release)
- Raj (Compliance): 1 row (data handling policy)
- Lisa (CISO): 2 rows (security pen test, training data)
- Tom (Legal): 1 row (vendor contract)
- Priya (CX Dir): 1 row (brand voice)
- Finance: 1 row (budget approval)

**No orphan decisions** — every decision has a named accountable owner.

## One-Way Door Decisions

These decisions are hard or impossible to reverse once made. They require the Accountable person's explicit written sign-off before proceeding:

| Decision | Why It's One-Way | Accountable | Required Before |
|----------|-----------------|-------------|-----------------|
| AI vendor contract | 12-month minimum commitment, data migration cost | Tom (Legal) | Phase 2 start |
| Customer data handling policy | Regulatory filing, audit trail established | Raj (Compliance) | Any customer data ingestion |
| GO/NO-GO for public launch | Brand reputation, customer expectations set | Diana (CEO) | Phase 3 exit |
| Model training data selection | Once trained, retraining is expensive + audit implications | Lisa (CISO) | Model training begins |

## References

- RACI framework adapted from Smith, M.L. & Erwin, J., "Role & Responsibility Charting" (https://pmicie.starchapter.com/images/downloads/raci_r_web3_1.pdf)
- One-Way Door decision classification from Palette Knowledge Library LIB-003, LIB-010
- Single-accountable-owner rule per Amazon's "single-threaded owner" principle (https://docs.aws.amazon.com/wellarchitected/latest/operational-readiness-reviews/single-threaded-owners.html)
```

### `stakeholder_map.md`

```
# Stakeholder Map — AI Customer Service Assistant

## Scenario Context

A mid-size insurance company wants to add an AI assistant for customer service. Three stakeholders have different priorities: CTO (cost reduction), VP of Customer Service (CSAT improvement), CEO (market positioning / press release). This stakeholder map was built after a compliance VP blocked a similar project at a peer company — we're doing this proactively.

## Stakeholder Registry

| # | Stakeholder | Title | Decision Authority | Influence Level | Interest Level | Discovery Method |
|---|-------------|-------|--------------------|-----------------|----------------|------------------|
| 1 | Sarah Chen | CTO | Technical architecture, vendor selection, infrastructure budget | High | High | Sponsor — named in kickoff |
| 2 | Marcus Rivera | VP Customer Service | CS workflow changes, agent training, CSAT targets | High | High | Sponsor — named in kickoff |
| 3 | Diana Park | CEO | Final GO/NO-GO on public launch, press release approval | Critical | Medium | Sponsor — named in kickoff |
| 4 | Raj Patel | VP Compliance | Data handling policy, PII rules, regulatory sign-off | Critical (veto) | Medium | **Discovered via checklist** — regulatory authority over customer data |
| 5 | Lisa Yamamoto | CISO | Security review, pen testing, data residency | Critical (veto) | Low | **Discovered via checklist** — any system touching customer PII |
| 6 | Tom Bradley | Head of Legal | Contract review for AI vendor, liability for AI responses | High (veto on legal) | Low | **Discovered via checklist** — vendor contracts + AI liability |
| 7 | Ana Ruiz | CS Team Lead (Tier 1) | Daily workflow impact, escalation handling | Medium | High | Identified as end-user representative |
| 8 | James Ko | Data Engineering Lead | Data pipeline, integration with CRM, model serving | Medium | High | Technical dependency — owns the data platform |
| 9 | Priya Sharma | Customer Experience Director | Brand voice, tone guidelines, customer communication standards | Medium | Medium | **Discovered via checklist** — any customer-facing communication |
| 10 | Finance (CFO office) | Budget Approval | Budget above $200K requires CFO sign-off | High (conditional) | Low | **Discovered via checklist** — procurement threshold |

## Hidden Stakeholders — Discovery Process

Used the **Stakeholder Discovery Checklist** (systematic sweep of 6 categories):

| Category | Question | Stakeholder Found |
|----------|----------|-------------------|
| Regulatory | Who has authority over data used by this system? | Raj Patel (VP Compliance) |
| Security | Who must approve systems that access customer PII? | Lisa Yamamoto (CISO) |
| Legal | Who reviews vendor contracts and liability exposure? | Tom Bradley (Head of Legal) |
| Brand/CX | Who owns the customer communication standards? | Priya Sharma (CX Director) |
| Budget | Who approves expenditures at the expected project scale? | CFO Office (conditional) |
| End Users | Who will the system change daily work for? | Ana Ruiz (CS Team Lead) |

**Key insight**: Stakeholders 4-6 (Compliance, CISO, Legal) have **veto power** but were not in the original kickoff. In the peer company incident, Compliance blocked deployment 3 weeks in. By surfacing them now, we avoid that failure mode entirely.

## Influence-Interest Matrix

```
                    Low Interest          Medium Interest       High Interest
                ┌─────────────────┬─────────────────────┬──────────────────┐
Critical        │  Lisa (CISO)    │  Diana (CEO)        │                  │
Authority       │                 │  Raj (Compliance)   │                  │
                ├─────────────────┼─────────────────────┼──────────────────┤
High            │  Tom (Legal)    │  Priya (CX Dir)     │  Sarah (CTO)     │
Authority       │  Finance (CFO)  │                     │  Marcus (VP CS)  │
                ├─────────────────┼─────────────────────┼──────────────────┤
Medium          │                 │                     │  Ana (CS Lead)   │
Authority       │                 │                     │  James (Data Eng)|
                └─────────────────┴─────────────────────┴──────────────────┘
```

**Engagement strategy by quadrant**:
- Critical + Low/Medium interest: **Keep satisfied** — brief monthly, escalate only when their domain is affected. Schedule dedicated review gates.
- High + High interest: **Manage closely** — weekly standups, decision authority on their domains.
- Medium + High interest: **Keep informed** — biweekly updates, input on design but not decision authority.

## References

- Stakeholder Discovery Checklist adapted from PMI stakeholder analysis framework (https://www.pmi.org/learning/library/stakeholder-analysis-pivotal-practice-projects-8905)
- Influence-Interest matrix based on Mendelow's Power/Interest Grid (source: Eden, C. & Ackermann, F., "Making Strategy", 1998)
- Hidden stakeholder identification pattern from Palette Knowledge Library LIB-001, LIB-007
```

## Instructions

Evaluate each rubric dimension using the calibration rules in the system prompt.
Output your evaluation in the YAML format specified above.
Set module to "RIU-002" and submission_id to "SUB-202603241942".
```

### `raci_lite.md`

```
# RACI-Lite Matrix — AI Customer Service Assistant

## Definitions

| Role | Meaning | Rule |
|------|---------|------|
| **A** (Accountable) | Final decision-maker. Signs off. | Exactly ONE per row. |
| **R** (Responsible) | Does the work or leads the effort. | One or more per row. |
| **C** (Consulted) | Must be asked before the decision is made. Input is required. | Zero or more. |
| **I** (Informed) | Told after the decision. No input required. | Zero or more. |

## Matrix

| Decision / Artifact | Sarah (CTO) | Marcus (VP CS) | Diana (CEO) | Raj (Compliance) | Lisa (CISO) | Tom (Legal) | Ana (CS Lead) | James (Data Eng) | Priya (CX Dir) | Finance |
|---|---|---|---|---|---|---|---|---|---|---|
| **Technical architecture selection** | **A** | C | I | C | C | I | I | R | I | I |
| **AI vendor contract** | R | I | I | C | C | **A** | I | I | I | C |
| **Customer data handling policy** | C | C | I | **A** | C | C | I | R | I | I |
| **CS workflow redesign** | C | **A** | I | I | I | I | R | C | C | I |
| **Brand voice / tone for AI responses** | I | C | I | I | I | I | C | I | **A** | I |
| **Security pen test plan** | C | I | I | I | **A** | I | I | R | I | I |
| **GO/NO-GO for public launch** | R | R | **A** | C | C | C | I | I | C | I |
| **Budget approval (>$200K)** | R | I | C | I | I | I | I | I | I | **A** |
| **Escalation from AI to human agent** | C | **A** | I | C | I | I | R | C | C | I |
| **Model training data selection** | C | C | I | C | **A** | I | I | R | I | I |
| **Press release / external comms** | C | C | **A** | C | I | C | I | I | R | I |

## Ownership Verification

Every row has exactly one **A**:
- Sarah (CTO): 1 row (technical architecture)
- Marcus (VP CS): 2 rows (CS workflow, escalation design)
- Diana (CEO): 2 rows (GO/NO-GO, press release)
- Raj (Compliance): 1 row (data handling policy)
- Lisa (CISO): 2 rows (security pen test, training data)
- Tom (Legal): 1 row (vendor contract)
- Priya (CX Dir): 1 row (brand voice)
- Finance: 1 row (budget approval)

**No orphan decisions** — every decision has a named accountable owner.

## One-Way Door Decisions

These decisions are hard or impossible to reverse once made. They require the Accountable person's explicit written sign-off before proceeding:

| Decision | Why It's One-Way | Accountable | Required Before |
|----------|-----------------|-------------|-----------------|
| AI vendor contract | 12-month minimum commitment, data migration cost | Tom (Legal) | Phase 2 start |
| Customer data handling policy | Regulatory filing, audit trail established | Raj (Compliance) | Any customer data ingestion |
| GO/NO-GO for public launch | Brand reputation, customer expectations set | Diana (CEO) | Phase 3 exit |
| Model training data selection | Once trained, retraining is expensive + audit implications | Lisa (CISO) | Model training begins |

## References

- RACI framework adapted from Smith, M.L. & Erwin, J., "Role & Responsibility Charting" (https://pmicie.starchapter.com/images/downloads/raci_r_web3_1.pdf)
- One-Way Door decision classification from Palette Knowledge Library LIB-003, LIB-010
- Single-accountable-owner rule per Amazon's "single-threaded owner" principle (https://docs.aws.amazon.com/wellarchitected/latest/operational-readiness-reviews/single-threaded-owners.html)
```

### `stakeholder_map.md`

```
# Stakeholder Map — AI Customer Service Assistant

## Scenario Context

A mid-size insurance company wants to add an AI assistant for customer service. Three stakeholders have different priorities: CTO (cost reduction), VP of Customer Service (CSAT improvement), CEO (market positioning / press release). This stakeholder map was built after a compliance VP blocked a similar project at a peer company — we're doing this proactively.

## Stakeholder Registry

| # | Stakeholder | Title | Decision Authority | Influence Level | Interest Level | Discovery Method |
|---|-------------|-------|--------------------|-----------------|----------------|------------------|
| 1 | Sarah Chen | CTO | Technical architecture, vendor selection, infrastructure budget | High | High | Sponsor — named in kickoff |
| 2 | Marcus Rivera | VP Customer Service | CS workflow changes, agent training, CSAT targets | High | High | Sponsor — named in kickoff |
| 3 | Diana Park | CEO | Final GO/NO-GO on public launch, press release approval | Critical | Medium | Sponsor — named in kickoff |
| 4 | Raj Patel | VP Compliance | Data handling policy, PII rules, regulatory sign-off | Critical (veto) | Medium | **Discovered via checklist** — regulatory authority over customer data |
| 5 | Lisa Yamamoto | CISO | Security review, pen testing, data residency | Critical (veto) | Low | **Discovered via checklist** — any system touching customer PII |
| 6 | Tom Bradley | Head of Legal | Contract review for AI vendor, liability for AI responses | High (veto on legal) | Low | **Discovered via checklist** — vendor contracts + AI liability |
| 7 | Ana Ruiz | CS Team Lead (Tier 1) | Daily workflow impact, escalation handling | Medium | High | Identified as end-user representative |
| 8 | James Ko | Data Engineering Lead | Data pipeline, integration with CRM, model serving | Medium | High | Technical dependency — owns the data platform |
| 9 | Priya Sharma | Customer Experience Director | Brand voice, tone guidelines, customer communication standards | Medium | Medium | **Discovered via checklist** — any customer-facing communication |
| 10 | Finance (CFO office) | Budget Approval | Budget above $200K requires CFO sign-off | High (conditional) | Low | **Discovered via checklist** — procurement threshold |

## Hidden Stakeholders — Discovery Process

Used the **Stakeholder Discovery Checklist** (systematic sweep of 6 categories):

| Category | Question | Stakeholder Found |
|----------|----------|-------------------|
| Regulatory | Who has authority over data used by this system? | Raj Patel (VP Compliance) |
| Security | Who must approve systems that access customer PII? | Lisa Yamamoto (CISO) |
| Legal | Who reviews vendor contracts and liability exposure? | Tom Bradley (Head of Legal) |
| Brand/CX | Who owns the customer communication standards? | Priya Sharma (CX Director) |
| Budget | Who approves expenditures at the expected project scale? | CFO Office (conditional) |
| End Users | Who will the system change daily work for? | Ana Ruiz (CS Team Lead) |

**Key insight**: Stakeholders 4-6 (Compliance, CISO, Legal) have **veto power** but were not in the original kickoff. In the peer company incident, Compliance blocked deployment 3 weeks in. By surfacing them now, we avoid that failure mode entirely.

## Influence-Interest Matrix

```
                    Low Interest          Medium Interest       High Interest
                ┌─────────────────┬─────────────────────┬──────────────────┐
Critical        │  Lisa (CISO)    │  Diana (CEO)        │                  │
Authority       │                 │  Raj (Compliance)   │                  │
                ├─────────────────┼─────────────────────┼──────────────────┤
High            │  Tom (Legal)    │  Priya (CX Dir)     │  Sarah (CTO)     │
Authority       │  Finance (CFO)  │                     │  Marcus (VP CS)  │
                ├─────────────────┼─────────────────────┼──────────────────┤
Medium          │                 │                     │  Ana (CS Lead)   │
Authority       │                 │                     │  James (Data Eng)|
                └─────────────────┴─────────────────────┴──────────────────┘
```

**Engagement strategy by quadrant**:
- Critical + Low/Medium interest: **Keep satisfied** — brief monthly, escalate only when their domain is affected. Schedule dedicated review gates.
- High + High interest: **Manage closely** — weekly standups, decision authority on their domains.
- Medium + High interest: **Keep informed** — biweekly updates, input on design but not decision authority.

## References

- Stakeholder Discovery Checklist adapted from PMI stakeholder analysis framework (https://www.pmi.org/learning/library/stakeholder-analysis-pivotal-practice-projects-8905)
- Influence-Interest matrix based on Mendelow's Power/Interest Grid (source: Eden, C. & Ackermann, F., "Making Strategy", 1998)
- Hidden stakeholder identification pattern from Palette Knowledge Library LIB-001, LIB-007
```

## Calibration Exemplars

Use these exemplars to calibrate your scoring. Each level shows what a submission
at that quality looks like for this module's rubric dimensions.

# Calibration Exemplars — RIU-002: Stakeholder Map + RACI-lite

> **Reference exemplar set.** Each snippet is written from the developer's perspective, as submitted portfolio work. Levels differ in quality of analysis and organizational thinking — not in word count. An expert answer may be shorter than a competent one if the thinking is sharper.
>
> Based on Exercise RIU-002-EX-01: You're 3 weeks into an AI deployment. The CTO approved the architecture. Suddenly, the VP of Compliance (who was never in any meeting) blocks deployment because the data handling violates internal policy. Retroactively build the stakeholder map that would have caught this, and design the process to prevent it next time.

---

## Dimension 1: Stakeholder Coverage

### Insufficient

Our stakeholder map for the project:

- CTO — technical authority, approved architecture
- VP of Engineering — manages the AI team
- Project Manager — coordinates daily work
- VP of Compliance — added after the incident

Going forward, we will make sure to include compliance people in our project meetings from the start.

> **Why this is insufficient**: This is an org chart excerpt, not a stakeholder map. It lists people who were already in the room (plus the one who just caused the problem) with no analysis of influence, interest, or decision authority. "Include compliance people in meetings" shows no understanding of why the gap existed. The student reacted to the symptom (one missing person) without diagnosing the systemic failure.

### Basic

**Stakeholder Register**

| Stakeholder | Role | Why Included |
|---|---|---|
| CTO | Technical authority | Approved architecture |
| VP Engineering | Delivery owner | Manages AI team |
| VP Compliance | Regulatory oversight | Blocked deployment — should have been included |
| Project Manager | Coordination | Tracks daily progress |
| Legal Counsel | Legal review | Contracts and data handling have legal implications |
| Data Protection Officer | Privacy | AI model processes personal data |

The compliance block happened because we only identified technical stakeholders. For future projects, we should use a checklist that includes regulatory, legal, and security roles during the kickoff phase.

> **Why this is basic**: Correctly identifies the missing stakeholder *category* (regulatory) and adds reasonable entries. But the analysis stops at job titles — there's no influence/interest assessment, no discovery methodology beyond "use a checklist," and no explanation of why the existing process failed to surface these roles. The student knows *what* to fix but not *why* it broke.

### Competent

**Stakeholder Discovery Analysis**

The compliance block reveals a process failure: initial stakeholder identification was driven by the CTO's meeting invitations, which naturally favored technical and delivery roles. Oversight roles weren't deliberately excluded — they were outside the CTO's mental model of "who matters."

**Stakeholder Map**

| Stakeholder | Interest | Influence | Decision Authority | How They Should Have Been Found |
|---|---|---|---|---|
| CTO | Cost reduction, technical credibility | High | Architecture approval | Direct — project sponsor |
| VP Engineering | Delivery timeline, team capacity | High | Resource allocation | Direct — delivery chain |
| VP Compliance | Regulatory adherence, risk exposure | High (veto) | Data handling approval | Ask: "Who can stop this project?" |
| DPO | Data classification, retention policies | Medium | Privacy impact sign-off | Ask: "Who owns data governance?" |
| InfoSec Lead | Threat surface, access controls | Medium | Security review | Ask: "Who reviews system access?" |
| Internal Audit | Process compliance | Low-Medium | Audit findings | Ask: "Who reviews us after launch?" |
| Business Unit Owner | ROI, customer impact | High | Budget continuation | Direct — business customer |

**Prevention Process**

Stakeholder discovery should use four questions during the Convergence Brief phase, before architecture work begins:

1. **Who can approve?** — decision authority holders
2. **Who can block?** — veto power holders (this catches compliance-type gaps)
3. **Who is affected?** — downstream impact stakeholders
4. **Who reviews after launch?** — oversight and audit functions

> **Why this is competent**: Diagnoses the root cause (CTO's invite list drove stakeholder selection), uses a systematic discovery framework with the four-question method, and maps stakeholders by influence and authority rather than just by title. A team could adopt this process immediately. Solid practitioner work.

### Expert

**Root Cause**

The VP of Compliance wasn't missing from a list. She was missing from the *decision model*. The project treated CTO architecture approval as deployment approval, but these are different gates: the CTO has authority over *how to build*, Compliance has authority over *whether it can ship*. Conflating the two meant three weeks of work against an incomplete authority map.

**The Discovery Failure**

The interesting question isn't "why wasn't Compliance invited?" — it's "why did nobody in the room ask 'who can kill this?'" That's a cultural signal: the team defaulted to building consensus among allies rather than mapping the full authority landscape.

**Key Missed Stakeholders (and the organizational signals that should have flagged them)**

| Who | Why Missed | Signal That Was Ignored |
|---|---|---|
| VP Compliance | Different reporting chain than Engineering | The data architecture doc on day 1 referenced customer PII — any PII handling triggers compliance review. This was knowable without asking anyone. |
| DPO | Reports to Legal, invisible to technical teams | The AI model training data required classification. Nobody asked who owns classification policy. |
| Regional Regulatory (if multi-market) | External, easy to forget | Deployment geography wasn't confirmed until week 2 — by then, regulatory mapping was already late. |

**Process Change**

A stakeholder checklist helps but is inherently fragile — it works until you encounter a category nobody thought to add. Better: before any architecture commitment, run a 30-minute **pre-mortem**: "It's 4 weeks from now and someone we never consulted just blocked the project. Who are they and why?" This forces adversarial thinking about unexplored veto power, which surfaces compliance-type gaps without requiring a pre-built category list.

Second: map stakeholders to *gates*, not to *meetings*. The question isn't "who attends standup?" — it's "what are the approval gates between here and production, and who owns each one?"

> **Why this is expert**: Identifies the deeper structural failure (conflating build approval with ship approval) rather than just the missing person. The pre-mortem technique addresses the root cause — unknown unknowns — rather than expanding a checklist that will always have gaps. The gate-mapping insight reframes stakeholder discovery from "who should we invite" to "what approvals exist whether we map them or not." This is systems thinking, not list-making.

---

## Dimension 2: Ownership Clarity

### Insufficient

The CTO is responsible for all technical decisions. The VP of Engineering is responsible for implementation. The Project Manager is responsible for coordination. The VP of Compliance is responsible for compliance issues.

Everyone should work together collaboratively to make the project successful.

> **Why this is insufficient**: Assigns vague "responsibility" to four people with no specificity about which decisions, which artifacts, or what happens when responsibilities overlap. "Work together collaboratively" is a non-answer to the ownership question. No RACI structure. The boundary between CTO and VP Compliance — the exact boundary that caused the crisis — is unaddressed.

### Basic

**RACI Matrix**

| Decision Area | CTO | VP Eng | VP Compliance | PM |
|---|---|---|---|---|
| Technical Decisions | A | R | I | I |
| Implementation | C | A | I | R |
| Compliance | I | I | A | I |
| Project Coordination | I | C | I | A |

A = Accountable, R = Responsible, I = Informed, C = Consulted.

This RACI ensures every area has one accountable owner. The CTO handles technical decisions and Compliance handles compliance decisions.

> **Why this is basic**: Has a RACI matrix with one A per row — good. But the rows are too broad. "Technical Decisions" is not a single decision — it's dozens. The data architecture decision that triggered the crisis sits at the CTO/Compliance boundary, and this RACI doesn't resolve it. "Compliance handles compliance decisions" is circular. The student understands RACI mechanics but hasn't applied them to the actual conflict.

### Competent

**RACI-lite Matrix**

| Decision | Accountable | Responsible | Consulted | Informed |
|---|---|---|---|---|
| AI model architecture (algorithms, infrastructure) | CTO | AI Team Lead | VP Eng | PM, Compliance |
| Data handling and retention policy | VP Compliance | DPO | CTO, Legal | PM, VP Eng |
| Training data selection and sourcing | CTO | AI Team Lead | VP Compliance, DPO | PM |
| Deployment environment and timeline | VP Eng | PM | CTO | Compliance, InfoSec |
| Customer data access patterns | VP Compliance | InfoSec Lead | CTO, DPO | PM |
| Budget allocation and continuation | Business Unit Owner | PM | CTO, VP Eng | Compliance |
| Incident response (post-deployment) | VP Eng | AI Team Lead | CTO, InfoSec | Compliance, PM |

**Boundary resolution**: The data architecture decision that caused the crisis spans CTO (architecture) and Compliance (data handling). This RACI splits it: the CTO owns *model architecture*, Compliance owns *data handling policy*. When a decision touches both (e.g., choosing a training data pipeline), both must be consulted, but the data policy owner (Compliance) has final authority on data handling.

**Verification**: Each row has exactly one A. No stakeholder is A on more than 3 rows. Every artifact in the required deliverables list maps to at least one decision row.

> **Why this is competent**: Rows are specific decisions rather than broad categories. The CTO/Compliance boundary is explicitly resolved with a clear rule ("data policy owner has final authority on data handling"). Each row has exactly one A. The student verified their own work against the RACI rules. This is defensible, actionable work.

### Expert

**RACI-lite Matrix**

| Decision | A | R | C | I |
|---|---|---|---|---|
| Model architecture | CTO | AI Lead | VP Eng | PM |
| Data handling policy | VP Compliance | DPO | CTO | PM, Legal |
| Training data sourcing | CTO | AI Lead | VP Compliance | DPO |
| Deployment timeline | VP Eng | PM | CTO | All |
| Customer data access | VP Compliance | InfoSec | CTO | PM |
| Budget continuation | BU Owner | PM | CTO, VP Eng | — |

**Why this RACI would have prevented the crisis**: The VP of Compliance is Accountable for data handling policy (row 2) and Consulted on training data sourcing (row 3). Under this structure, the data architecture decision on week 1 would have required Compliance consultation *before* the CTO could approve. The block would have been a 2-day review, not a 3-week surprise.

**Ownership stress tests**

I tested three scenarios against this RACI to verify it doesn't break under pressure:

1. *"The model's training data includes customer support transcripts with PII. Who decides whether to proceed?"* — VP Compliance (row 2: data handling policy). CTO is Consulted, not Accountable. This is the scenario that actually happened.

2. *"The model's accuracy degrades 10% after deployment. Who decides whether to roll back?"* — VP Eng (row 4: deployment timeline includes rollback). CTO is Consulted on whether the accuracy drop is fixable.

3. *"Legal flags a new regulation that affects data retention mid-project."* — VP Compliance (row 2) triggers a review. CTO is Consulted on technical feasibility. If they disagree on timeline, escalation triggers (see escalation design).

> **Why this is expert**: Instead of a larger matrix, the student uses a targeted RACI and then *tests it against realistic failure scenarios*, including the exact scenario that caused the original crisis. This reveals whether ownership actually holds under pressure — a RACI that looks clean on paper can still fail when two accountable parties disagree on scope. The stress tests demonstrate that the student understands ownership as a *runtime property* of the project, not a static assignment.

---

## Dimension 3: Escalation Design

### Insufficient

If stakeholders disagree, the issue should be escalated to senior management for resolution. The Project Manager should facilitate these discussions and ensure that all voices are heard.

> **Why this is insufficient**: No triggers (when to escalate), no paths (to whom), no timelines, no deadlock prevention. "Senior management" is undefined. "Ensure all voices are heard" is a sentiment, not a mechanism. This couldn't be followed by anyone on the team.

### Basic

**Escalation Path**

1. Disagreement identified → Project Manager facilitates discussion between the parties
2. If unresolved within 1 week → PM escalates to CTO
3. If CTO cannot resolve → PM escalates to CEO
4. CEO makes final decision

For the current CTO-Compliance dispute, the PM should schedule a meeting between the CTO and VP of Compliance to discuss the data handling concerns. If they can't agree, escalate to the CEO.

> **Why this is basic**: Has a defined path with a timeline (1 week). But it's a single escalation ladder that routes everything through the CTO — who is one of the disputing parties in the current crisis. It doesn't distinguish between types of disagreements (technical vs. regulatory vs. political). The CTO as escalation point for a CTO-Compliance dispute creates an obvious conflict of interest. The student has the concept of escalation but hasn't applied it to the actual situation.

### Competent

**Escalation Protocol**

| Trigger | Path | Timeline | Deadlock Prevention |
|---|---|---|---|
| Technical disagreement (architecture, implementation) | Parties → CTO → VP Eng (if CTO is a party) | 48h discussion, then escalate | Escalation authority makes binding decision within 24h |
| Regulatory/compliance disagreement | Parties → VP Compliance → General Counsel | 48h discussion, then escalate | Compliance has default authority — burden of proof is on the party requesting an exception |
| Cross-domain disagreement (technical vs. regulatory) | Parties → joint session facilitated by PM → shared executive (COO or CEO) | 24h for joint session, 48h for executive decision | If executive doesn't decide within 48h, the more conservative position wins by default |
| Budget/priority disagreement | Parties → Business Unit Owner → CFO | 1 week | — |

**Current situation resolution**: The CTO-Compliance dispute is a cross-domain disagreement (row 3). The PM should convene a joint session within 24 hours. If CTO and VP Compliance can't align, escalate to their shared executive. The compliance concern (data handling policy violation) takes precedence by default until the CTO demonstrates that the architecture can be modified to comply.

**Deadlock rule**: When no agreement is reached and no executive is available, the more conservative/risk-averse position prevails. This prevents delays from becoming implicit approvals.

> **Why this is competent**: Categorizes disagreements and provides different escalation paths for each. Timelines are specific. The cross-domain path correctly avoids making either disputing party the escalation point. The "conservative position wins by default" rule prevents the common failure mode where inaction becomes approval. Directly resolves the current CTO-Compliance dispute.

### Expert

**Escalation Design**

The current CTO-Compliance deadlock IS the escalation case — designing for it prospectively means acknowledging that we're three weeks late.

**Two types of escalation that this project needs:**

**Type 1: Authority escalation** (who decides). The CTO and VP Compliance have non-overlapping authority. This isn't actually a disagreement — it's a sequencing failure. Compliance authority over data handling doesn't conflict with CTO authority over architecture. They need to exercise their authority *in order*, not *against each other*. Resolution: the data handling review happens first (Compliance gate), then architecture proceeds within those constraints (CTO gate). This isn't escalation — it's correct sequencing.

**Type 2: Genuine conflicts** (what to do when authority holders reach incompatible conclusions). Example: Compliance says "no customer data in the training set" but the CTO says the model is worthless without it. This requires actual escalation:

| Condition | Action | Timeline |
|---|---|---|
| Two authority holders reach incompatible conclusions | PM convenes joint session; each party states their constraint in writing | Within 24h |
| Joint session fails to find a path | Escalate to shared executive with both written constraints | Within 48h of session |
| Shared executive unavailable or defers | Conservative position (higher risk-aversion) prevails by default | Immediately |

**Why most escalation protocols fail**: They assume escalation means "go up the org chart." But the CTO and VP Compliance may not share a direct executive below the CEO. Making every cross-domain dispute a CEO problem is unsustainable. Better: identify a standing "tie-breaker" for the project (often the executive sponsor or the business unit owner who controls budget) and empower them to resolve cross-domain disputes without going to the CEO.

**Immediate action for the current crisis**: Don't escalate. The VP of Compliance isn't disagreeing with the CTO — she's exercising authority the project failed to account for. The correct response is a compliance review of the data handling design (2-3 days), not an executive mediation.

> **Why this is expert**: Distinguishes between sequencing failures (which don't need escalation) and genuine authority conflicts (which do). Recognizes that the current crisis isn't actually a disagreement — it's a missed gate. The insight about "tie-breaker" roles addresses the structural weakness in most escalation protocols (they assume a clean reporting hierarchy). The student reframes the immediate situation correctly: this needs a compliance review, not an executive meeting.

---

## Dimension 4: Practical Applicability

### Insufficient

We have created a comprehensive stakeholder map and RACI-lite matrix following industry best practices. The stakeholder map categorizes stakeholders by their influence and interest levels using a standard power-interest grid. The RACI matrix assigns clear accountability for each decision domain.

These artifacts provide a solid foundation for project governance and should be reviewed quarterly to ensure they remain current.

> **Why this is insufficient**: Describes artifacts in abstract terms without producing them. The language is consultancy-speak ("comprehensive," "industry best practices," "solid foundation") with no actionable content. "Reviewed quarterly" — but the project is 3 weeks in and in crisis. There's nothing here a team could use tomorrow.

### Basic

**Recommended Next Steps**

1. Schedule a stakeholder mapping workshop with the full project team (2 hours)
2. Use the stakeholder map template to identify all stakeholders
3. Create the RACI matrix using the template provided
4. Get sign-off from the CTO and VP of Compliance
5. Review the stakeholder map monthly

The attached stakeholder map and RACI templates should be filled in during the workshop. The Project Manager should facilitate.

> **Why this is basic**: Provides a process, but it's a greenfield process for a project that's already three weeks in and in crisis. Step 1 (a 2-hour workshop) ignores the urgency — the VP of Compliance has blocked deployment. The templates are generic (not shown, just referenced). The student knows what governance artifacts look like but hasn't adapted them to the current reality.

### Competent

**Immediate Actions (This Week)**

1. **Tomorrow**: PM schedules 45-minute call with VP Compliance and DPO. Agenda: understand the specific data handling policy violations, get the compliance requirements in writing, agree on a review timeline. *Not* a negotiation — an information-gathering session.

2. **Within 48 hours**: CTO reviews whether the architecture can be modified to comply. If yes, estimate the rework. If no, escalate per the cross-domain escalation path.

3. **End of week**: Circulate the updated stakeholder map and RACI-lite to all stakeholders. Each person verifies their role assignments. Disagreements resolved in a 30-minute sync.

**Integration With Existing Project Cadence**

- Stakeholder map review becomes a standing item in the biweekly project review (5 minutes — just "anyone new? anyone's role changed?")
- RACI is referenced at the start of any decision meeting ("who's A on this?")
- The four-question stakeholder discovery runs once per phase gate, not continuously

**What the team can use right now**: The stakeholder map, RACI-lite, and escalation protocol are all in this submission. No templates to fill in — they're populated with real roles and real decisions for this project.

> **Why this is competent**: Addresses the immediate crisis (VP Compliance meeting tomorrow), provides a concrete timeline, and integrates with the existing project cadence rather than creating a parallel governance process. "No templates to fill in" — the artifacts are ready to use. The student adapted the deliverables to the reality of a project in crisis.

### Expert

**The political problem is harder than the process problem.**

The VP of Compliance was excluded for three weeks and discovered a policy violation. She is not a neutral party — she's an authority figure who was bypassed. The stakeholder map and RACI are necessary, but they solve the *future* problem. The *current* problem is relationship recovery.

**Immediate actions (in order):**

1. **Today**: CTO calls VP Compliance directly (not the PM — this requires peer-to-peer acknowledgment). Message: "We should have included you from day one. Here's what we built and here are the data handling specifics. What do you need from us to evaluate compliance?" This is not a status update — it's an acknowledgment of the process failure.

2. **Tomorrow**: Compliance review begins. DPO leads the technical review of data handling. CTO's team provides full documentation of data flows, retention, and access patterns. No negotiation on timeline — Compliance sets the pace for their own review.

3. **Within 1 week**: Compliance review complete. Three possible outcomes: (a) minor changes, project continues with 1-2 week delay; (b) major redesign required, CTO and VP Compliance jointly present options to executive sponsor; (c) project cannot comply as designed, executive sponsor decides go/no-go.

**Why I'm not leading with the RACI**: The RACI exists (see Dimension 2) and it's correct, but circulating a governance document right now signals "we're building process around you" rather than "we made a mistake." Governance artifacts get circulated *after* the immediate crisis is resolved, as part of the "here's how we prevent this next time" conversation. Leading with process when someone is justifiably frustrated makes the process feel like a defensive move.

**Transition plan by stakeholder:**

| Stakeholder | Current State | Engagement Approach |
|---|---|---|
| VP Compliance | Angry, exercising veto | Peer-to-peer acknowledgment from CTO, then compliance review on her terms |
| DPO | Neutral, needs information | Technical briefing on data flows, access to documentation |
| InfoSec | Unaware | Brief introduction via VP Compliance (let her bring her own team in) |
| Internal Audit | Not yet relevant | Flag for post-launch, do not engage now |

> **Why this is expert**: Recognizes that practical applicability in a crisis means reading the organizational dynamics, not just delivering correct artifacts. The insight that leading with a RACI would feel defensive to an excluded stakeholder shows emotional intelligence about how governance tools land in practice. The differentiated engagement approach (different tactics for angry vs. neutral vs. unaware stakeholders) reflects real-world organizational skill. The student produces the governance artifacts but knows *when* to deploy them.

## Instructions

Evaluate each rubric dimension using the calibration rules in the system prompt.
Output your evaluation in the YAML format specified above.
Set module to "RIU-002" and submission_id to "SUB-202603242122".
