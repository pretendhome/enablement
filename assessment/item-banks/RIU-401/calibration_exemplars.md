# Calibration Exemplars — RIU-401: Taxonomy Design

> **Reference exemplar set.** Each snippet is written from the developer's perspective, as submitted portfolio work. Levels differ in classification rigor and systems thinking — not in word count.
>
> Note: RIU-401 does not yet exist in the taxonomy (known gap — only RIU-400 exists). Dimensions are derived from the learning path content and taxonomy design domain knowledge.
>
> Based on scenario: You're building an AI system that needs to classify customer support tickets into categories for routing. The current system uses 47 categories that evolved organically over 3 years. Some categories overlap, some are unused, and agents frequently miscategorize tickets. Design a taxonomy that an AI system could use for consistent, accurate classification.

---

## Dimension 1: Classification Logic

### Insufficient

I organized the 47 categories into 5 groups: Technical, Billing, Account, Product, and Other. Each group contains the original categories as subcategories.

> **Why this is insufficient**: This is reorganization, not redesign. The original 47 categories had overlapping boundaries — grouping them doesn't fix the overlaps. "Other" is a catch-all that will absorb everything ambiguous, making it the largest and least useful category. No classification logic is defined — just a hierarchy.

### Basic

I reduced the 47 categories to 12 by merging overlapping ones. For example, "billing question," "payment issue," and "invoice request" became "Billing & Payments." Each category has a one-sentence description. I tested by classifying 20 sample tickets and achieved 85% agreement with the original categorization.

> **Why this is basic**: Merging overlapping categories is the right instinct, and testing with sample tickets shows practical thinking. But the descriptions are for humans, not AI — "Billing & Payments" is clear to a person but ambiguous to a classifier (does a refund request go here or under "Account Management"?). The 85% agreement is measured against the original flawed categorization, not against ground truth.

### Competent

**Design process**:
1. Analyzed 1,000 historical tickets to find actual distribution (not assumed distribution)
2. Identified 8 categories that covered 92% of tickets, plus an "Unclassified" triage queue
3. Each category has: a definition (what belongs), exclusions (what doesn't), and 3 example tickets (one clear, one borderline, one that looks like it belongs but doesn't)

**Classification test**: Gave the taxonomy + descriptions to two different AI models. Both classified the same 50 tickets. Agreement between models: 88%. Agreement with human expert: 91%. Disagreements clustered in 2 categories — refined those descriptions until agreement exceeded 85% on the problem cases.

**Key design choice**: "Unclassified" is not "Other" — it's a triage queue with a 24-hour SLA for human review and reclassification. Every ticket that lands here is a signal that the taxonomy has a gap.

> **Why this is competent**: Data-driven category design (from actual distribution, not assumptions), AI-testable descriptions with exclusions and examples, and the "Unclassified as triage signal" pattern shows mature taxonomy thinking. The dual-model agreement test is a practical validation method.

### Expert

The 47-category problem isn't a taxonomy problem — it's an incentive problem. Categories accumulated because adding a new category was easier than fixing an existing one. Any redesign that doesn't address the growth mechanism will end up at 47 categories again in 3 years.

**Taxonomy design**:
- 2 levels: 6 intent categories (what the customer wants) × action types (how to resolve). Intent: get information, change something, fix something, buy something, complain, escalate. Action: self-service, agent-assisted, specialist-required.
- Classification logic: classify by intent first (what does the customer want?), then by action type (what resolution path?). This separates the routing decision (who handles it) from the content decision (what's it about).
- Each leaf node has a machine-readable description written as a decision rule: "Classify here IF the customer is requesting a change to their account AND the change requires identity verification." Decision rules are testable — you can write unit tests against them.

**Growth control**: New categories require evidence (>50 tickets/month that don't fit existing categories) and approval (taxonomy owner reviews quarterly). The taxonomy has a version number. Changes are tracked. This prevents organic accumulation.

**Escape hatch**: Every taxonomy needs a way to handle genuinely novel inputs. The triage queue captures them, but the key metric is triage queue volume over time. If it's growing, the taxonomy is falling behind reality. If it's shrinking, the taxonomy is adapting.

> **Why this is expert**: Identifies the root cause (incentive to add categories rather than fix them) and designs growth control into the taxonomy itself. The intent × action decomposition is more powerful than a flat category list because it separates orthogonal concerns. Decision-rule descriptions are unit-testable, which makes the taxonomy an engineering artifact rather than a document. The triage queue volume metric turns taxonomy maintenance into a measurable process.

---

## Dimension 2: Boundary Clarity

### Insufficient

Each category has a name and a short description. For example: "Technical Issues — problems with the product not working correctly."

> **Why this is insufficient**: "Problems with the product not working correctly" could include bugs, performance issues, compatibility problems, user errors, and feature requests. The boundary is so wide that almost anything could be classified here. No exclusions, no examples, no decision criteria.

### Basic

Each category has a description and 2-3 example tickets. For example: "Technical Issues — the product crashes, produces errors, or behaves differently than documented. Examples: app crashes on login, API returns 500 error, report shows wrong numbers. NOT: feature requests, how-to questions, or performance complaints."

> **Why this is basic**: Adding examples and exclusions is a significant improvement. But the boundary is still defined by examples rather than by rules — a new ticket type that doesn't match any example requires human judgment. The exclusions help but are incomplete (what about security vulnerabilities? data loss?).

### Competent

**Boundary specification for each category**:
- Decision rule: "Classify as Technical Issue IF the customer reports behavior that contradicts documented functionality AND the behavior is reproducible."
- Inclusion criteria: crashes, errors, incorrect outputs, data corruption, security vulnerabilities
- Exclusion criteria: feature requests (desired behavior ≠ documented behavior), performance (slow ≠ broken), user error (correct behavior misunderstood)
- Boundary cases with rulings: "App is slow" → Performance, not Technical. "App crashes when I do X" → Technical. "App doesn't have feature Y" → Feature Request. "App does X but I expected Y" → check documentation: if documented behavior matches, it's User Education; if not, it's Technical.

**Boundary test**: 10 ambiguous tickets classified by 3 people using only the written rules. Agreement: 9/10. The disagreement was on a ticket where the documentation was itself ambiguous — surfaced a documentation gap, not a taxonomy gap.

> **Why this is competent**: Decision rules are specific enough for consistent classification. The boundary cases with rulings handle the ambiguous zone explicitly. The boundary test with multiple classifiers validates that the rules work without the author's interpretation. Surfacing the documentation gap shows the taxonomy is doing its job — revealing upstream problems.

### Expert

Boundary clarity isn't about writing better descriptions — it's about designing categories whose boundaries are orthogonal. If two categories share a boundary (like "Technical Issues" and "Performance"), every ticket near that boundary will be misclassified by someone.

**Orthogonal design**: Instead of categories defined by topic (technical, billing, account), define categories by the decision they drive:
- "Needs code fix" → Engineering queue
- "Needs config change" → Ops queue
- "Needs human judgment" → Specialist queue
- "Needs information delivery" → Self-service or bot

These categories have natural boundaries because they're defined by the resolution action, not by the problem description. A slow app and a crashing app might both need a code fix — they go to the same queue. A billing question and a technical question might both need information delivery — they go to the same queue.

**Boundary validation metric**: classification entropy. For each ticket, measure how confident the classifier is. High entropy (low confidence) means the ticket is near a boundary. Track which category pairs produce the most high-entropy classifications — those are your weak boundaries. Refine those boundaries specifically, not the whole taxonomy.

> **Why this is expert**: The orthogonal design insight eliminates boundary conflicts by defining categories along a single axis (resolution action) rather than multiple overlapping axes (topic, severity, customer type). The classification entropy metric makes boundary quality measurable and identifies exactly which boundaries need work. This is taxonomy design as information theory, not as list-making.

---

## Dimension 3: Extensibility

### Insufficient

If we need new categories, we can add them to the taxonomy.

> **Why this is insufficient**: This is how the original 47-category problem happened. No process, no criteria, no version control. "We can add them" is permission, not a design.

### Basic

New categories can be proposed by any team member. The proposal must include: category name, description, 5 example tickets, and justification for why existing categories don't cover these tickets. The taxonomy owner reviews proposals monthly.

> **Why this is basic**: A proposal process is better than ad-hoc addition. But there's no criteria for when a new category is justified vs when an existing category should be expanded. Monthly review means a gap can persist for weeks. No versioning or impact analysis.

### Competent

**Extension protocol**:
1. Evidence threshold: >50 tickets/month landing in triage queue with a consistent pattern that doesn't fit existing categories
2. Impact analysis: adding a category changes routing — which team absorbs the new volume? Do they have capacity?
3. Boundary check: does the new category overlap with any existing category? If yes, the fix might be refining an existing boundary, not adding a new category
4. Version bump: taxonomy changes get a version number. All downstream consumers (routing rules, dashboards, reports) are notified
5. Rollback plan: if the new category causes more confusion than it solves (measured by misclassification rate), revert within 2 weeks

> **Why this is competent**: Evidence-based threshold prevents premature additions. Impact analysis considers downstream effects. The boundary check prevents the overlap problem that created the original 47 categories. Versioning and rollback make changes reversible.

### Expert

Extensibility is a design property, not a process. A taxonomy that requires structural changes to accommodate new inputs is brittle. A taxonomy that absorbs new inputs through its existing structure is resilient.

**Design for extensibility**:
- The taxonomy should have a fixed number of top-level categories that represent stable abstractions (intent types, resolution actions). These rarely change.
- New specificity is added at the leaf level, within existing categories. "Technical Issue" doesn't become a new top-level category — it becomes a new leaf under "Needs Code Fix."
- The triage queue is the extensibility mechanism. It captures everything the taxonomy can't classify. When a pattern emerges in the triage queue, it becomes a new leaf — not a new branch.

**Anti-pattern detection**: If someone proposes a new top-level category, that's a signal that the top-level abstraction is wrong, not that the taxonomy needs to be bigger. The correct response is to re-examine the classification axis, not to add another category.

**Versioning as a health metric**: Track the ratio of leaf additions to branch additions over time. Healthy taxonomies grow at the leaves. Unhealthy taxonomies grow at the branches. If you're adding branches, the top-level design is failing.

> **Why this is expert**: Distinguishes between leaf growth (healthy, expected) and branch growth (structural problem). The triage queue as extensibility mechanism is elegant — it's both a safety net and a growth sensor. The anti-pattern detection (new top-level category = wrong abstraction) prevents the structural drift that created the original 47-category mess. The leaf/branch ratio metric makes taxonomy health measurable over time.
