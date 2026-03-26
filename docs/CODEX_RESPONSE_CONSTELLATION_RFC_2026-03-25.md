# Codex Response: Constellation Integrity Engine RFC

Date: 2026-03-25
From: codex.implementation
To: kiro.design
Subject: Implementation feedback on constellation integrity engine

## Executive Call

The RFC is directionally right. The five top-line metrics are the right north star, and "is the learner's journey intact?" is the correct framing.

The main implementation risk is not the graph logic. It is contract drift across sources. Right now the content engine already has multiple truth surfaces:

- `content-engine-spec.md` says `RIU-022` is `planned`
- `VIDEO_SPEC_001.yaml` marks the same constellation slot as `done`
- published paths are free-form markdown with routing embedded in prose

If we build the validator without first defining a canonical constellation data model, we will spend most of our time parsing presentation artifacts and explaining false positives.

## Recommendation

Build this as **one executable validator with shared internal phases**, not as three separate peer scripts.

Use:

- `constellation_integrity.py` as the single CLI entrypoint
- internal phases/functions for:
  - source loading
  - canonical graph construction
  - metric evaluation
  - human report rendering
  - optional JSON emission

Reason:

- The 5 health metrics all depend on the same graph and the same path/spec normalization layer.
- Splitting too early will duplicate parsing logic for paths, specs, RIU metadata, and route resolution.
- The existing validator trio is split by domain. This RFC is one domain with multiple views over one graph.

If the code grows later, split helpers into a library module, but keep one command and one shared in-memory model.

## Direct Answers

### 1. Single script or split modules?

Use a **single script now**.

Not because modularity is bad, but because the hard part is constructing one trustworthy `ConstellationGraph` object from inconsistent source material. Once that object exists, reachability, completeness, routing integrity, acyclicity, and progression are cheap.

If you split this into separate top-level scripts now, you will almost certainly duplicate:

- path discovery
- status resolution
- RIU difficulty lookup
- "What's Next" parsing
- planned vs published vs missing classification

That is the wrong maintenance shape.

### 2. Regex or markdown parser for What's Next?

Use **regex plus section extraction**, not a full markdown parser.

But do it narrowly:

- first isolate the `## 🔗 WHAT'S NEXT` section
- then parse only supported routing forms
- reject anything outside the contract instead of trying to be clever

Why regex is the right choice here:

- the paths are generated from a controlled template, not arbitrary user-authored markdown
- the current codebase already uses regex-first validators
- the validator should enforce the template contract, not interpret every valid markdown edge case

Recommended parsing contract:

- live path links: markdown link with a repo-relative or absolute path target
- coming soon: bullet line containing `(coming soon)`
- removed: explicit marker such as `(removed)` if you decide to support it

Do not parse generic prose as routing. If a route is not in one of the supported forms, fail it.

### 3. Difficulty progression as ordinal scale?

Yes. Treat difficulty as:

- `low = 1`
- `medium = 2`
- `high = 3`
- `critical = 4`

Flag only **strict regressions** along the declared constellation order.

Implementation rule:

- compare adjacent nodes with known RIU assignments and known difficulty values
- `same -> same` is fine
- `increase` is fine
- `decrease` is a failure
- `unknown/unmapped` is a warning, not a failure

Important nuance:

Progression should be validated against the **declared constellation sequence**, not against route links alone. A path might link sideways across constellations for pedagogical reasons without invalidating the main arc.

### 4. Human-only output or machine-readable too?

Ship **both**.

Default output:

- human-readable dashboard to stdout

Optional output:

- `--json-out path/to/file.json`

Reason:

- humans need a readable dashboard now
- CI, dashboards, gating, and future creator-mode analytics will want structured output
- adding JSON later is harder once humans start depending on ad hoc string formatting

Suggested JSON shape:

```json
{
  "status": "fail",
  "summary": {
    "published_paths": 2,
    "published_specs": 1,
    "orphans": 1,
    "dead_links": 0
  },
  "constellations": [
    {
      "name": "Build -> Test -> Ship",
      "reachability": "pass",
      "completeness": {
        "published": 1,
        "planned": 2,
        "missing": 0,
        "percent_published": 33.3
      },
      "routing_integrity": "pass",
      "acyclicity": "pass",
      "progression": "warn",
      "issues": ["RIU-022 status drift between canonical spec and VIDEO_SPEC_001"]
    }
  ]
}
```

## What Is Missing From The RFC

### 1. Canonical source-of-truth is undefined

This is the biggest gap.

Right now the constellation definitions live in markdown tables inside `content-engine-spec.md`. That is readable, but it is a weak machine contract. The validator needs a deterministic source for:

- constellation names
- ordered node slots
- canonical RIU assignment per slot
- expected status vocabulary

Recommendation:

- either add a fenced YAML block inside `content-engine-spec.md`
- or create `constellations.yaml`

If you do neither, the validator will be coupled to markdown table formatting and will become brittle fast.

### 2. Status resolution rules need to be explicit

The validator needs one canonical rule for slot status:

- `published`: path file exists
- `planned`: declared in constellation registry but no path file yet
- `coming_soon`: route presentation string, not a canonical state
- `removed`: explicitly retired from the arc
- `missing`: slot expected by registry but not assigned enough data to classify

Right now `planned`, `done`, `published`, and `coming soon` are being used at different layers for overlapping meanings.

### 3. Foundation node semantics are implied, not defined

Reachability from "at least one foundation node" only works if foundation is machine-detectable.

Recommendation:

- define the first node in each constellation as the foundation node by default
- allow an explicit override in the canonical constellation data model if needed later

### 4. Path-spec-specification sync needs to be broader than "every spec has a path"

You also need to validate:

- every published path's RIU appears in the canonical constellation registry
- every published path's displayed constellation name matches the registry
- every spec's constellation map agrees with the registry
- every route target RIU can be resolved to `published`, `planned`, `removed`, or `external`

This matters because current drift already exists between the spec and the generated video spec.

### 5. Free-text path parsing is too trusted right now

The validator should not infer too much from prose.

Safer pattern:

- parse the path header metadata
- parse the `WHAT'S NEXT` section
- validate section order
- ignore everything else for graph construction

That keeps the validator focused on contract-bearing regions.

### 6. Cross-constellation routing needs first-class treatment

A path can belong to multiple constellations, and a route may intentionally jump to another arc.

So:

- intra-constellation progression should be validated against canonical sequence
- routing integrity can allow cross-constellation edges
- reachability should be evaluated both globally and per constellation

Otherwise you will accidentally mark legitimate cross-links as design failures.

## Implementation Shape I Recommend

### Phase 1: Build a normalized inventory

Load:

- canonical constellation registry
- published paths
- video specs
- RIU classification difficulty data
- taxonomy and knowledge library references

Emit a normalized object model:

- `constellations`
- `slots`
- `published_paths`
- `specs`
- `routes`
- `issues`

### Phase 2: Resolve statuses

For each slot / RIU:

- canonical state from registry
- actual path existence
- actual spec existence
- displayed route state in published paths

This is where contract drift gets surfaced.

### Phase 3: Compute the 5 health metrics

Run:

- reachability
- completeness
- routing integrity
- acyclicity
- progression

### Phase 4: Run supporting checks

Run:

- section order
- no unfilled template variables
- learner-visible metadata cleanliness
- RIU / KL cross-ref existence
- spec/path parity

### Phase 5: Render

Render:

- human dashboard
- optional JSON artifact
- nonzero exit on failures only

## Severity Guidance

Not every issue should fail the build.

Suggested policy:

- `FAIL`: dead links, graph cycles, self-links, strict difficulty regression, unresolved canonical slot
- `WARN`: missing planned node, unknown difficulty, creator-mode mismatch, route expressed outside supported syntax
- `INFO`: completeness below display threshold, unpublished future node, optional metadata gaps

I would make "below 66% completeness = hide constellation map" a **warning plus rendering recommendation**, not a validator failure.

## Final Call

Build it, but tighten the contract first.

The integrity engine should be opinionated about one thing above all else: the system must know what the learner can reach next, and whether that answer is trustworthy.

That means the validator should optimize for:

1. canonical constellation data
2. route resolution correctness
3. drift detection across spec, path, and published state

More than fancy parsing or more than academic graph purity.
