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
