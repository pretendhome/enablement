# Calibration Exemplars — RIU-060: Deployment Readiness Envelope

> Reference set. Levels differ by release judgment, verification depth, and rollback realism, not by word count.

## Dimension 1: Readiness Criteria

### Insufficient
"The system is ready if tests pass and the service starts."

Why:
- Almost no readiness envelope.
- Ignores dependencies, security, and operations.

### Basic
"The deployment requires passing tests, a green build, and a successful health check."

Why:
- Some release gates exist.
- Still too shallow for production readiness.

### Competent
"The readiness envelope defines explicit gates for code quality, security review, dependency state, configuration parity, and operator readiness. A release may proceed only if each gate is satisfied or an approved exception is documented."

Why:
- Clear and operational.
- Recognizes production readiness as more than build success.

### Expert
"The readiness envelope is designed to prevent false readiness signals. It separates 'software built correctly' from 'system safe to expose to traffic,' and it makes hidden prerequisites visible: migrations, config parity, downstream availability, and rollback readiness. The release is gated on whether the whole operating system around the service is ready, not whether the app binary exists."

Why:
- Shows systemic release thinking rather than CI thinking.

## Dimension 2: Verification Depth

### Insufficient
"After deploy, we call `/health` and confirm the service returns 200."

Why:
- Liveness only.
- No business-function verification.

### Basic
"After deploy, we run a few smoke checks in addition to the health endpoint."

Why:
- Better than liveness alone.
- Still unclear whether the checks prove anything important.

### Competent
"Post-deploy verification checks the critical path end to end: dependencies respond, the service returns correct outputs for representative requests, and key alerts remain within expected thresholds. The team can tell whether the system is merely alive or actually working."

Why:
- Distinguishes liveness from functional success.

### Expert
"Verification depth is designed around the easiest way the deployment could lie. Health endpoints, basic smoke checks, and dashboard greenness are not treated as sufficient if they can all stay green while user-visible behavior is broken. The verification suite therefore targets the exact places where false positives usually hide."

Why:
- Strong release skepticism and operational realism.

## Dimension 3: Rollback Capability

### Insufficient
"If something goes wrong, we can redeploy the previous version."

Why:
- Aspirational, not operational.
- No timing, dependency, or test story.

### Basic
"Rollback steps are documented and were tested once in staging."

Why:
- Some evidence exists.
- Still weak on production realism and SLA confidence.

### Competent
"Rollback is defined per deployment step, tested in a production-like environment, and executable within the stated SLA. The team knows which artifacts are reversible, which are not, and which conditions should trigger rollback instead of continued debugging."

Why:
- Real rollback capability rather than paper rollback.

### Expert
"Rollback capability is treated as a release precondition, not an emergency improvisation. The plan distinguishes app rollback from data rollback, names the decision trigger, and preserves operator confidence by keeping rollback steps simpler than forward deploy. A strong release envelope assumes rollback will eventually be needed and optimizes for that moment before it happens."

Why:
- Shows mature thinking about reversibility under pressure.

## Dimension 4: Dependency Management

### Insufficient
"Services should be deployed in the correct order."

Why:
- True but non-actionable.

### Basic
"The team documents the order of dependent services and follows it during release."

Why:
- Better than nothing.
- Still depends on human memory and manual correctness.

### Competent
"The deployment envelope names service dependencies explicitly, enforces ordering where required, and allows parallel rollout only where dependencies are truly independent. If a dependent service is not ready, the release halts instead of hoping startup succeeds."

Why:
- Strong sequencing logic with enforcement.

### Expert
"Dependency management is designed to prevent hidden coupling from surfacing as runtime chaos. The release process knows which dependencies are hard gates, which are soft signals, and which rollbacks must happen together to preserve system coherence. This is not just an ordered checklist; it is a dependency-aware control system."

Why:
- Goes beyond sequence to system coherence.
