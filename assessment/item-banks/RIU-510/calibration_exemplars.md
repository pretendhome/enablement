# Calibration Exemplars — RIU-510: Multi-Agent Workflow Design

> Reference set. Levels differ by orchestration judgment, state discipline, and failure containment thinking, not by length.

## Dimension 1: Agent Boundaries

### Insufficient
"We use three agents: one researches, one analyzes, and one helps when needed."

Why:
- Responsibilities overlap immediately.
- No clear contract boundaries.

### Basic
"The workflow has separate research, analysis, and delivery agents, though they can step into each other's tasks if necessary."

Why:
- Some structure exists.
- Still preserves overlap instead of removing it.

### Competent
"Each agent has one clear responsibility and an explicit contract. The research agent gathers evidence, the analysis agent turns evidence into structured findings, and the delivery agent packages approved output. If a task requires a different capability, it is handed off rather than informally absorbed."

Why:
- Strong SRP-style boundary design.
- Clear basis for evaluation and failure isolation.

### Expert
"The boundaries are drawn around failure containment, not just task names. Each agent owns a capability that can fail independently without corrupting the others: evidence collection, reasoning, and delivery are separated because they have different failure signatures. The design avoids 'helper agents' specifically because helper agents become unbounded authority leaks."

Why:
- Shows system-design reasoning behind the boundaries.

## Dimension 2: Handoff Protocol

### Insufficient
"Agents pass messages to each other with the current task and state."

Why:
- No schema, validation, versioning, or recovery plan.

### Basic
"Agents pass JSON payloads with a simple schema and validate required fields."

Why:
- Introduces structure.
- Still weak on evolution and recovery.

### Competent
"The handoff protocol uses a defined schema, version tags, validation on both send and receive, and explicit handling for invalid or stale payloads. State transitions are recoverable because handoffs either commit cleanly or fail loudly with a retry or escalation path."

Why:
- Covers the actual corruption risks.

### Expert
"The protocol is designed so that agents cannot silently disagree about what state means. Versioning is treated as a compatibility contract, validation is symmetrical, and invalid handoffs do not advance workflow state. The goal is not just passing data; it is preventing invisible state drift across cooperating agents."

Why:
- Shows why handoff discipline matters in multi-agent systems.

## Dimension 3: Failure Isolation

### Insufficient
"If one agent fails, the system should retry or alert someone."

Why:
- Generic fallback language.
- No containment model.

### Basic
"If an agent fails, retries occur and a backup path may be used."

Why:
- Some recovery intent exists.
- Still does not show how blast radius is limited.

### Competent
"Failures are contained to the failing agent or stage. Retries are bounded, fallback paths are defined, and downstream agents receive an explicit failure state instead of partial or corrupted output. The workflow can degrade without lying about success."

Why:
- Clear containment behavior.

### Expert
"Failure isolation is designed around preserving decision integrity. A failed agent does not get infinite retries, does not emit guessed output, and does not force downstream stages to infer missing state. The workflow either recovers through a named degraded mode or escalates to a human with a preserved checkpoint."

Why:
- Demonstrates mature reliability design rather than generic resilience language.

## Dimension 4: Coordination Pattern

### Insufficient
"The workflow is sequential because that is the easiest way to build it."

Why:
- Convenience replaces tradeoff reasoning.

### Basic
"The workflow is mostly sequential, with some parallelism possible later."

Why:
- Recognizes alternatives but does not justify the choice.

### Competent
"The chosen coordination pattern matches the work. Independent evidence gathering runs in parallel to reduce latency, while synthesis and approval stay sequential to preserve ordering and accountability. The pattern is justified against cost, latency, and blast radius rather than selected by habit."

Why:
- Tradeoffs are real and aligned to workflow shape.

### Expert
"The coordination design treats parallelism as a cost, not a free optimization. Stages run in parallel only when their state can remain independent and their failures can be joined safely; otherwise the workflow stays sequential. This avoids the common mistake of adding concurrency where the real requirement is traceable accountability."

Why:
- Shows higher-order orchestration judgment.

## Dimension 5: Defense Quality

### Insufficient
"The design choices are reasonable and should work well in production."

Why:
- Assertion without defense.

### Basic
"The candidate can explain the design at a high level and name the major agents."

Why:
- Some explanation exists.
- Not enough for adversarial review.

### Competent
"The candidate can explain why each agent exists, why the handoff protocol is structured the way it is, and how the workflow behaves when assumptions fail. The defense is specific enough to survive changed constraints without collapsing into buzzwords."

Why:
- Shows real command of the design.

### Expert
"The candidate's defense demonstrates that the workflow was designed under pressure, not just diagrammed afterward. They can justify what was left out, explain which assumptions were intentionally reversible, and show how the design would be modified if latency, safety, or authority constraints changed. The design is defensible because its tradeoffs are explicit."

Why:
- Defense quality is about adaptive reasoning, not presentation polish.
