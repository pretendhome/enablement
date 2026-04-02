# Perplexity Task 001: Research Queries

**From**: claude.analysis
**To**: perplexity.research
**Thread**: Palette Enablement Phase 1

---

## How This Works

Paste each query below into Perplexity. Save each result to the specified output path. Four research deliverables total.

---

## Query 1: Competitor Analysis

**Output**: `/home/mical/fde/enablement/docs/research/competitor_analysis.md`

**Paste this into Perplexity**:

> Analyze AI-specific developer education and certification programs as of March 2026. For each program, provide: target audience, assessment type (MCQ vs hands-on vs portfolio), pricing, tier structure, industry reception, and gaps. Cover these programs specifically:
>
> 1. Anthropic Claude Certified Architect (CCA-F) and Anthropic Academy
> 2. OpenAI developer training and any certification programs
> 3. Google Cloud AI/ML certifications
> 4. AWS AI Practitioner and ML specialty certifications
> 5. DeepLearning.AI programs (Andrew Ng)
> 6. Databricks GenAI Engineer certification
> 7. NVIDIA Agentic AI Professional (NCP-AAI)
> 8. LangChain Academy
> 9. Any emerging AI agent-specific certification programs
>
> Focus on: what assessment methods they use, what competencies they test, and what gaps exist in the market. Specifically note if any program uses portfolio-based assessment or LLM-as-judge for evaluating human competency.

---

## Query 2: Source Enrichment for 5 Modules

**Output**: `/home/mical/fde/enablement/docs/research/source_enrichment.md`

**Paste this into Perplexity**:

> I need 3-5 high-quality sources for each of these 5 enterprise AI competency areas. Sources must be from 2024-2026, published by authoritative organizations. Prefer: Google, Anthropic, OpenAI, AWS, Meta official docs (Tier 1), NIST/EU AI Act/peer-reviewed papers (Tier 2), or GitHub repos with >500 stars (Tier 3).
>
> 1. **Convergence Briefs / AI Project Scoping** — structured approaches to aligning stakeholders on AI project scope, goals, and non-goals before building
> 2. **Golden Sets and Offline Evaluation Harnesses** — building evaluation datasets and offline testing pipelines for RAG and LLM systems
> 3. **Multi-Agent Workflow Design** — designing systems where multiple AI agents coordinate, including handoff protocols, state management, and failure isolation
> 4. **LLM Safety Guardrails** — implementing content safety, tool-use boundaries, and prompt injection defense for production LLM systems
> 5. **Employee AI Adoption Programs** — driving actual behavior change (not just training completion) when deploying AI tools to employees
>
> For each source: title, URL, publisher, date, and a 1-sentence summary of what it covers.

---

## Query 3: AI-Augmented Assessment Deep Dive

**Output**: `/home/mical/fde/enablement/docs/research/ai_augmented_assessment.md`

**Paste this into Perplexity**:

> Deep dive on using LLMs to evaluate human competency in certification programs (not just evaluating model outputs). Cover:
>
> 1. Current state of LLM-as-judge research — what inter-rater reliability scores are achievable between LLM judges and human evaluators? What are known biases (position bias, verbosity bias, self-preference)?
> 2. Best practices for rubric-based AI evaluation — how should rubrics be structured to maximize LLM judge accuracy? What role do calibration exemplars play?
> 3. How to handle disagreement between AI and human evaluators — what's the standard protocol when scores diverge?
> 4. Existing tools and frameworks for AI-assisted grading — Braintrust, LangSmith, DeepEval, or any custom implementations
> 5. Legal and ethical considerations — can a professional certification legally use AI grading? Any precedents or regulatory guidance (US, EU)?
> 6. Has anyone published results from using LLMs to grade portfolio-based or open-ended developer assessments (not just code review)?
>
> Focus on practical, implementable findings with citations. Flag any finding that suggests LLM-as-judge is NOT reliable enough for high-stakes certification.

---

## Query 4: Open Badges 3.0 Implementation

**Output**: `/home/mical/fde/enablement/docs/research/open_badges_implementation.md`

**Paste this into Perplexity**:

> Practical guide to implementing Open Badges 3.0 (W3C Verifiable Credentials) for a new developer certification program. Cover:
>
> 1. Technical requirements — what infrastructure do you need to issue OB 3.0 badges?
> 2. Accredible vs Credly vs self-hosted — comparison for a new program starting from scratch
> 3. How to embed competency metadata in badges (ACE extension, skill alignments)
> 4. Integration with LinkedIn — how do OB 3.0 badges appear on LinkedIn profiles?
> 5. Verification — how do employers verify a badge without contacting the issuer?
> 6. Cost — what does it cost to issue badges at scale (100-10,000 credentials/year)?
> 7. Any examples of AI/developer certification programs that have adopted OB 3.0 since 2025?

---

## After Each Query

1. Copy the full Perplexity response
2. Add a header: `# {Topic} — Perplexity Research` and `**Date**: 2026-03-24` and `**Query**: [the query you pasted]`
3. Save to the specified output path
4. When all 4 are done, write a note to `/home/mical/fde/enablement/PERPLEXITY_STATUS.md`
