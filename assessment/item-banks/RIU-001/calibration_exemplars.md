# Calibration Exemplars — RIU-001: Convergence Brief

> Reference set. Levels differ by scoping quality, tradeoff handling, and change-control discipline, not by word count.

## Dimension 1: Completeness

### Insufficient
"We should add AI to customer service. Success means lower cost and happier customers. Next step is to evaluate chatbot vendors."

Why:
- Missing the actual five-part structure.
- No real context, non-goals, or decision framing.

### Basic
"Problem: customer service is expensive. Context: response times are slow. Success criteria: reduce cost and improve CSAT. Next step: run a pilot."

Why:
- Has some structure but still omits meaningful non-goals and operational context.
- Reads like a summary, not a convergence artifact.

### Competent
"Problem: the customer service team is overloaded with repetitive inbound questions. Context: 10,000 monthly tickets, 2-hour median response time, and disagreement between cost-reduction and CSAT priorities. Success criteria: reduce cost per ticket by 15% and improve CSAT by 8 points within six months. Non-goals: no replacement of human agents and no AI handling for complex escalation cases. Next steps: validate ticket categories, define pilot scope, and assign owners for unresolved questions."

Why:
- All five sections are materially present.
- The brief is specific enough to guide the next decision.

### Expert
"Problem: stakeholders are using 'AI for customer service' to mean three different things: deflection, agent assist, and marketing narrative. Context: cost pressure is real, but the CEO's press goal could distort scope. Success criteria: 15% lower cost per ticket, 8-point CSAT gain, and no degradation in escalation accuracy. Non-goals: no replacement of tier-2 support, no public AI announcement before pilot metrics, and no expansion into unrelated channels during phase 1. Next steps: run a bounded pilot on top three repetitive intents, document assumptions with expiry dates, and route unresolved authority conflicts through a named escalation path."

Why:
- Completeness is not just present; it controls ambiguity.
- Shows the candidate understands what belongs in the brief and what must stay out.

## Dimension 2: Stakeholder Alignment

### Insufficient
"The CTO wants cost savings, the VP of Customer Service wants better CSAT, and the CEO wants publicity. We should try to satisfy all three."

Why:
- Repeats positions without converging them.
- No reconciliation mechanism.

### Basic
"The CTO wants cost savings and the VP of Customer Service wants better CSAT. We can use the pilot to improve both. The CEO can be updated once results exist."

Why:
- Begins to reduce conflict but still assumes the priorities are naturally aligned.
- Does not surface where they can diverge.

### Competent
"The brief reframes stakeholder positions into a shared decision test: a pilot is acceptable only if it lowers cost without degrading service quality. The CEO's request for a public narrative is moved out of the success criteria and into a later communication milestone. This allows the CTO and VP of Customer Service to align on measurable operating outcomes first."

Why:
- Converts competing stakeholder narratives into a shared operating baseline.
- Prevents one stakeholder's framing from hijacking scope.

### Expert
"The alignment problem is not just different goals; it is different failure tolerances. The CTO can accept slower rollout if cost drops, the VP of Customer Service cannot accept a CSAT regression, and the CEO is vulnerable to milestone theater. The brief therefore sets a joint operating baseline, explicitly removes PR from phase-1 success, and names which disagreements escalate versus which can be deferred. Stakeholder alignment is achieved by narrowing the decision surface, not by pretending the goals are identical."

Why:
- Identifies the deeper structure of the disagreement.
- Uses the brief to govern future conflict, not merely summarize positions.

## Dimension 3: Decision Classification

### Insufficient
"Using AI for customer service is a big decision and should be treated carefully."

Why:
- No one-way/two-way distinction.
- No classification logic.

### Basic
"The decision to launch the AI assistant is one-way because customers will notice it. Vendor selection is also important."

Why:
- Recognizes irreversibility in broad terms.
- Still too vague and does not separate reversible from irreversible sub-decisions.

### Competent
"Public launch is a one-way-door decision because it changes customer expectations and creates brand risk. Vendor selection for the pilot is a two-way-door decision because the pilot can be time-boxed and replaced if quality is weak. Prompt configuration and workflow design are also two-way-door items that should be tested before they are treated as policy."

Why:
- Correctly decomposes the engagement into decisions with different reversibility.
- Makes the classification operational.

### Expert
"The mistake would be classifying 'the AI project' as one decision. The actual one-way door is exposing customers and the brand to the system. Vendor choice, pilot scope, escalation workflow, and prompt contract are deliberately framed as two-way doors so the team can learn cheaply before it crosses the irreversible launch gate. Good decision classification here is a sequencing tool, not just a label."

Why:
- Uses reversibility to shape delivery strategy.
- Demonstrates mature handling of one-way-door risk.

## Dimension 4: Scope Discipline

### Insufficient
"The AI initiative will cover customer service first and later may expand into marketing, sales, and internal helpdesk."

Why:
- Scope is already leaking.
- No boundary or change-control logic.

### Basic
"The pilot is limited to customer service FAQs. We are not replacing all agents."

Why:
- Has a basic non-goal.
- Still does not explain how new asks are handled.

### Competent
"Phase 1 is limited to repetitive inbound FAQs for one region and one support queue. Requests to expand into outbound messaging, technical troubleshooting, or marketing are explicitly deferred. New asks must be logged in `change_requests.md` and evaluated against the brief's success criteria before they are accepted."

Why:
- Defines clear boundaries.
- Introduces an explicit trace-back mechanism for scope change.

### Expert
"Scope discipline is enforced in two ways: first, the brief names what phase 1 will not do; second, every new request is routed through a trace-back test: does it improve the agreed success criteria, does it introduce a one-way door, and does it require new stakeholders? If not, it is deferred. This prevents the common failure mode where scope creep arrives disguised as urgency."

Why:
- Treats scope control as an operating behavior, not a paragraph of non-goals.
- Connects new asks to governance and reversibility.
