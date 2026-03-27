# Calibration Exemplars — RIU-500: Multimodal Data Pipeline Design

> **Reference exemplar set.** Each snippet is written from the developer's perspective, as submitted portfolio work. Levels differ in architectural maturity and failure-mode awareness — not in word count.
>
> Based on Exercise RIU-500-EX-01: Your multimodal pipeline processes documents with embedded images. The text extraction works but images are silently dropped because the pipeline only handles text. Users get answers based on text alone, missing critical information in diagrams, charts, and screenshots.

---

## Dimension 1: Modality Coverage

### Insufficient

We should add image processing to the pipeline. We can use an OCR library for text in images and a vision model for diagrams.

> **Why this is insufficient**: Jumps to a solution without diagnosing the problem. The issue isn't "we need image processing" — it's "the pipeline silently drops data it can't handle." Adding image processing fixes one modality but doesn't prevent the same silent-drop failure when the next modality appears (audio, video, embedded files).

### Basic

**Modality inventory**: Documents can contain text, images, tables, embedded PDFs, and hyperlinks. Currently we only process text. We need to add: image extraction (OCR + vision model), table extraction (structured parsing), and embedded PDF extraction (recursive processing). Hyperlinks can be flagged but not followed.

For each modality, we need a processing step and a quality check to verify extraction worked.

> **Why this is basic**: Good modality inventory and recognition that each needs its own processing step. But no detection mechanism — how does the pipeline know which modalities are present in a given document? And no handling for unknown modalities (what happens when someone uploads a document with embedded video?).

### Competent

**Modality detection layer**: Before any processing, scan each document to identify all modalities present. Output a manifest: `{text: true, images: 3, tables: 1, embedded_files: 0, unknown: 0}`. This manifest drives the processing pipeline — only invoke processors for modalities that are present.

**Completeness check**: After processing, compare the output manifest against the input manifest. If any detected modality has no corresponding output, flag the document as incomplete. This catches the silent-drop problem structurally — it doesn't matter which modality was dropped or why.

**Unknown modality handling**: If the detector finds a modality it doesn't recognize, log it, flag the document, and process what it can. The unknown modality count becomes a monitoring metric — when it spikes, a new processor is needed.

> **Why this is competent**: The manifest-based approach catches silent drops for any modality, not just images. The completeness check is structural — it works regardless of which modality fails. Unknown modality handling prevents the pipeline from breaking on new input types while providing a signal for when to extend it.

### Expert

The silent-drop problem is an instance of a broader pattern: pipelines that assume their input matches their capabilities. The fix isn't "add more processors" — it's "design the pipeline to be aware of the gap between what it receives and what it can process."

**Architecture**:
- Input layer: modality-agnostic document ingestion. Every document gets a content manifest before any processing.
- Detection layer: identifies modalities using lightweight heuristics (file headers, MIME types, structural markers). This layer is cheap and fast — it doesn't process content, just identifies what's there.
- Processing layer: modality-specific processors registered in a handler registry. Each processor declares what it handles. The pipeline routes each modality to its registered handler.
- Completeness layer: compares detected modalities against processed modalities. Any gap is a first-class event — logged, alerted, and included in the output metadata.

**The key insight**: The completeness layer should exist even if you only process text. It tells you what you're missing. Without it, you don't know what you don't know — which is exactly how the silent-drop problem persists undetected.

**Metric**: modality coverage ratio = processed modalities / detected modalities. Track per document and in aggregate. A ratio below 1.0 means information is being lost. The ratio tells you how much of the input you're actually using.

> **Why this is expert**: Frames the problem as a gap-awareness architecture rather than a feature-addition task. The handler registry pattern makes the pipeline extensible without structural changes. The completeness layer as a permanent fixture (even for text-only pipelines) prevents the silent-drop class of failure from ever recurring. The coverage ratio metric makes information loss visible and measurable.

---

## Dimension 2: Pipeline Isolation

### Insufficient

We should process images and text in the same pipeline so we can combine the results.

> **Why this is insufficient**: Processing everything in the same pipeline means a failure in image processing blocks text processing. The original scenario's silent drop would become a loud crash — better in some ways, but the text results (which were working fine) would also be lost.

### Basic

We should separate image processing and text processing into different pipeline stages. If image processing fails, text processing can still complete. We can use a try/catch around each stage and log failures.

> **Why this is basic**: Correct instinct to separate stages. But try/catch is error handling, not isolation. If the image processor consumes all available memory before failing, the text processor running in the same process is still affected. True isolation requires process or resource boundaries.

### Competent

**Isolation design**:
- Each modality processor runs in its own worker (separate process or container). Resource limits per worker: memory cap, CPU time limit, timeout.
- Shared nothing: processors communicate through a message queue, not shared memory. Each processor reads from an input queue and writes to an output queue.
- Failure containment: if the image processor crashes, its worker restarts. Text processing is unaffected because it's a different worker reading from a different queue.
- Partial results: the pipeline produces results for every modality that succeeded. Failed modalities are flagged in the output metadata, not silently dropped and not blocking.

**Resource-based routing**: Large files (>100MB) route to high-memory workers. Small files route to standard workers. This prevents a single large file from starving other processing.

> **Why this is competent**: True process-level isolation with resource limits. The shared-nothing architecture via message queues prevents cascading failures. Partial results with metadata flags give downstream consumers the information they need to decide whether the output is sufficient. Resource-based routing handles the practical problem of heterogeneous input sizes.

### Expert

Isolation isn't just about preventing crashes from cascading — it's about making the pipeline's failure modes predictable and observable.

**Isolation as observability**:
- Each processor emits structured metrics: processing time, memory usage, success/failure, input size, output size. Because processors are isolated, these metrics are per-modality — you can see exactly which modality is slow, failing, or consuming resources.
- Circuit breaker per modality: if a processor fails 3 times in 10 minutes, stop sending it work and route to a degraded-mode handler (e.g., "image processing unavailable — text-only results"). This prevents a broken processor from consuming retry resources indefinitely.
- Backpressure: if one processor is slow (video processing takes 10x longer than text), the pipeline doesn't wait — it delivers text results immediately and appends video results when ready. The consumer gets progressive results, not all-or-nothing.

**The deeper design principle**: Isolation enables independent scaling, independent deployment, and independent failure. You can upgrade the image processor without touching the text processor. You can scale video processing independently when video volume spikes. Each modality has its own SLA.

> **Why this is expert**: Connects isolation to observability (per-modality metrics), resilience (circuit breakers), and user experience (progressive results). The independent scaling/deployment insight shows architectural maturity — isolation isn't just a safety measure, it's a velocity enabler. The progressive results pattern is particularly sophisticated — it turns a limitation (some modalities are slower) into a feature (fast results now, complete results later).

---

## Dimension 3: Cross-Modal Linking

### Insufficient

After processing text and images separately, we combine the results into one output.

> **Why this is insufficient**: "Combine" doesn't address the core challenge — maintaining the relationship between a diagram and the text that references it. If page 5 says "see Figure 3" and Figure 3 is on page 7, the combined output needs to preserve that link. Simple concatenation loses it.

### Basic

We maintain a document structure map that records where each element appears: text on pages 1-10, images on pages 3, 5, 7, tables on pages 4, 8. Each processed element includes its page number and position so we can reconstruct the original layout.

> **Why this is basic**: Position tracking is necessary but not sufficient. Knowing that an image is on page 5 doesn't tell you which text references it. The cross-modal link is semantic ("Figure 3 shows the architecture") not positional ("there's an image at coordinates X,Y on page 5").

### Competent

**Cross-modal linking protocol**:
1. During text extraction, identify cross-modal references: "see Figure 3," "as shown in the diagram below," "Table 2 summarizes." Parse these into structured references: `{type: "figure", id: "3", context: "architecture overview"}`.
2. During image/table extraction, assign IDs that match the document's numbering scheme. Figure 3 in the document becomes `figure-3` in the output.
3. Link resolution: match text references to extracted elements. `{text_ref: "Figure 3", resolved_to: "figure-3", confidence: 0.95}`.
4. Unresolved links: if text references "Figure 3" but no figure-3 was extracted, flag it as a broken cross-modal link. This catches the case where an image was silently dropped but the text referencing it was preserved.

**Traceability**: Every element in the output includes its source location (page, position) and any cross-modal links (what references it, what it references). Downstream consumers can verify that the output is complete by checking for unresolved links.

> **Why this is competent**: Semantic linking (not just positional) preserves the document's information structure. The unresolved link detection catches a subtle failure mode — text that references missing content. The traceability metadata enables downstream quality checks.

### Expert

Cross-modal linking is the hardest part of multimodal pipelines because it requires understanding intent, not just structure. "See Figure 3" is easy to parse. "The results above" is ambiguous — above in the document? above in the current section? The previous table? The previous chart?

**Linking architecture**:
- Explicit references (numbered figures, named tables): regex + structural matching. High confidence, low cost.
- Implicit references ("the diagram below," "as shown above"): requires spatial reasoning within the document layout. Medium confidence, medium cost.
- Semantic references ("the architecture" when there's an architecture diagram somewhere in the document): requires content understanding. Low confidence, high cost.

**Design choice**: Process all three tiers but tag each link with its confidence level. Downstream consumers can filter by confidence — high-stakes applications use only explicit links, exploratory applications use all three.

**The completeness test for cross-modal linking**: For every extracted element (image, table, diagram), ask: "Is this element referenced by any text?" If not, it might be decorative (fine to ignore) or it might be critical context that the text assumes the reader can see. Flag unreferenced non-decorative elements as potential information gaps.

The reverse test: for every cross-modal reference in the text, ask: "Was the referenced element successfully extracted?" If not, the text is making claims that the output can't support. This is worse than a missing image — it's misleading text.

> **Why this is expert**: The three-tier linking model (explicit, implicit, semantic) with confidence tagging gives downstream consumers control over the precision/recall tradeoff. The bidirectional completeness test (elements without references AND references without elements) catches both directions of information loss. The insight that unreferenced text is worse than missing images — because it's actively misleading — shows deep understanding of how multimodal information degrades.

---

## Dimension 4: Extensibility

### Insufficient

If we need to add a new modality, we can write a new processor and add it to the pipeline.

> **Why this is insufficient**: "Write a new processor and add it" describes the work but not the design that makes it possible. Without an extensibility architecture, adding a new processor means modifying the pipeline's routing logic, output format, and monitoring — touching code that's already working.

### Basic

We use a plugin architecture: each modality processor implements a standard interface (detect, process, validate). To add a new modality, write a new plugin that implements the interface and register it with the pipeline. No changes to existing code.

> **Why this is basic**: Plugin architecture is the right pattern. But the interface definition is too vague — what does "detect" return? What format does "process" output? What does "validate" check? Without a precise contract, each plugin will implement the interface differently, and integration will require custom glue code.

### Competent

**Modality handler contract**:
```
interface ModalityHandler:
  name: string                    # "image", "table", "audio"
  detect(document) → manifest     # what modalities are present, with counts
  process(element) → output       # standardized output format
  validate(output) → report       # completeness, quality, confidence
  resource_requirements → limits  # memory, CPU, timeout
```

**Standardized output format**: Every handler produces the same structure: `{modality, source_location, content, cross_modal_refs, confidence, metadata}`. This means downstream consumers don't need to know which handler produced the output — they all look the same.

**Onboarding checklist for new modalities**: (1) implement the handler contract, (2) register in the handler registry, (3) add detection rules to the manifest builder, (4) add monitoring dashboards, (5) run the integration test suite. Estimated time for a new modality: 1-2 weeks.

> **Why this is competent**: The handler contract is specific enough to implement against. The standardized output format means downstream code doesn't change when new modalities are added. The onboarding checklist makes the process repeatable and estimable.

### Expert

True extensibility means the pipeline doesn't know how many modalities exist and doesn't care. The architecture should be modality-agnostic at every layer except the handlers themselves.

**Design**:
- The pipeline core knows about "elements" — typed chunks of content with metadata. It doesn't know about images, text, or audio.
- Handlers register themselves with the pipeline at startup, declaring what element types they process. The pipeline routes elements to handlers based on type matching.
- New modalities are added by deploying a new handler and registering it. Zero changes to the pipeline core, zero changes to existing handlers, zero changes to downstream consumers.

**The extensibility test**: Can I add a new modality (say, 3D models) by writing one new handler and changing zero existing files? If yes, the architecture is truly extensible. If I need to modify routing logic, output schemas, or monitoring config, the extensibility is partial.

**Version compatibility**: When a handler's output format changes, it bumps its version. The pipeline supports multiple handler versions simultaneously during migration. This prevents the "upgrade everything at once" problem that makes teams afraid to improve individual handlers.

**Metric**: time-to-new-modality. How long from "we need to process 3D models" to "3D models are in production"? If the answer is weeks (handler development time), the architecture is extensible. If the answer is months (pipeline changes + integration + testing), it's not.

> **Why this is expert**: The modality-agnostic core is the key architectural insight — the pipeline operates on typed elements, not on specific modalities. The zero-existing-files test is a concrete, verifiable extensibility criterion. Version compatibility for handlers prevents the upgrade-everything-at-once problem. The time-to-new-modality metric makes extensibility measurable rather than aspirational.
