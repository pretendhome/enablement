# Calibration Exemplars — RIU-082: LLM Safety Guardrails (Content + Tool Use)

> Reference set. Levels differ by control design, boundary judgment, and adversarial realism, not by word count.

## Dimension 1: Policy and Evidence Design

### Insufficient
"The model should avoid harmful content and only use approved tools."

Why:
- Slogan, not policy.
- No evidence requirements, refusal rules, or user-tier distinctions.

### Basic
"The policy blocks unsafe content, limits tool use, and asks the model to provide evidence for sensitive claims."

Why:
- Names the right categories.
- Still lacks decision boundaries and enforceable conditions.

### Competent
"The policy defines what the model may say, what it may do, and what evidence it must cite before making operational claims. It distinguishes internal, partner, and public-facing users, and it makes refusal conditions explicit rather than leaving them to model intuition."

Why:
- Policy is actionable and enforceable.

### Expert
"The policy treats evidence as a control, not a style preference. High-risk claims require named evidence sources, high-risk tool actions require both policy eligibility and runtime checks, and user tiers change the allowed action surface. The policy therefore governs both content truthfulness and blast radius."

Why:
- Integrates evidence, authority, and action boundaries into one coherent control model.

## Dimension 2: Implementation Quality

### Insufficient
"Guardrails are implemented in the prompt and should stop unsafe behavior."

Why:
- Single-layer control.
- No pipeline placement or defense-in-depth.

### Basic
"The system uses a prompt plus a filter before sending outputs to users."

Why:
- Better than prompt-only.
- Still weak on where and why checks happen.

### Competent
"Guardrails are applied at the right stages: input screening, tool authorization, output review, and pre-send validation for sensitive actions. Normal traffic still flows without heavy friction because the design separates high-risk actions from low-risk ones."

Why:
- Shows pipeline placement and usability awareness.

### Expert
"Implementation quality is visible in the sequencing: the model never gets to 'self-authorize' a dangerous action. Tool-use constraints are enforced outside the model, output review is staged where it can still prevent harm, and high-risk actions require stronger checks than ordinary responses. The system is safe because the architecture assumes the model will eventually fail."

Why:
- Demonstrates architectural control thinking rather than prompt optimism.

## Dimension 3: Adversarial Robustness

### Insufficient
"We tested a few jailbreak prompts and the model refused them."

Why:
- Narrow testing.
- No prompt-injection or indirect-manipulation depth.

### Basic
"We tested direct jailbreaks, prompt injection, and some malicious file content."

Why:
- Broader coverage exists.
- Still no evidence that tests reflect realistic adversarial pathways.

### Competent
"The guardrail tests include direct jailbreaks, indirect prompt injection through retrieved content, and abuse of allowed tools. The results show where the system resists attacks and where it escalates or refuses instead of pretending the controls are perfect."

Why:
- Tests the real attack surface.
- Values safe degradation over false confidence.

### Expert
"Adversarial robustness is designed around attacker strategy, not attack examples. The evaluation checks whether a malicious user can shift the system from 'safe response' to 'unsafe action' through multi-step manipulation, role confusion, or trusted-context poisoning. A strong result is not 'the model never failed'; it is 'when it failed, the surrounding controls still contained the harm.'"

Why:
- Measures resilience, not just refusal rate.
- Shows realistic threat-model thinking.

## Dimension 4: Service Evaluation

### Insufficient
"We built custom guardrails because managed services seemed expensive."

Why:
- No real comparison.
- Decision is opinion-led.

### Basic
"We compared one managed service with our custom approach and chose the cheaper option."

Why:
- At least some comparison exists.
- Still too shallow on quality and integration tradeoffs.

### Competent
"The evaluation compares managed services and custom controls on detection quality, operational burden, latency impact, and coverage of the actual threat model. The recommendation is justified by the system's needs rather than by generic vendor preference."

Why:
- Tradeoffs are real and context-sensitive.

### Expert
"The service decision is framed as a control-allocation problem: what should be bought because it is standardized well, what should be built because it is domain-specific, and where layered use is warranted. The recommendation includes what risk remains after the chosen service mix, so the decision is honest about residual exposure rather than pretending a vendor selection solved the safety problem."

Why:
- Connects procurement choice to control design and residual risk.
