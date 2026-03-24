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
