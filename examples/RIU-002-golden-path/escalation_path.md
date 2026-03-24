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
