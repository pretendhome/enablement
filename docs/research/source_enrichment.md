# Source Enrichment — 5 Core Modules

**Date**: 2026-03-24
**Purpose**: Curated source inventory for Palette Developer Enablement — 5 enterprise AI competency areas. Sources prioritized by tier: Tier 1 (Google, Anthropic, OpenAI, AWS, Meta official docs), Tier 2 (NIST, EU AI Act, peer-reviewed), Tier 3 (GitHub repos >500 stars, authoritative industry research).

---

## Module 1: Convergence Briefs / AI Project Scoping

Structured approaches to aligning stakeholders on AI project scope, goals, and non-goals before building.

### Source 1.1 — Anthropic Enterprise AI Transformation Guide
- **Title**: Building Trusted AI in the Enterprise: Anthropic's Guide to Starting, Scaling, and Succeeding
- **URL**: https://assets.anthropic.com/m/66daaa23018ab0fd/original/Anthropic-enterprise-ebook-digital.pdf
- **Publisher**: Anthropic (Tier 1)
- **Date**: 2025
- **Summary**: Four-stage enterprise playbook (develop strategy, create business value, build for production, deploy and iterate) with real-world case studies from NBIM, Thomson Reuters, and Cox Automotive covering governance setup, stakeholder alignment, and measurable pilot design.

### Source 1.2 — NIST AI Risk Management Framework (AI RMF 1.0) + Generative AI Profile
- **Title**: Artificial Intelligence Risk Management Framework (AI RMF 1.0) and NIST AI 600-1 Generative AI Profile
- **URL (RMF)**: https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf
- **URL (GenAI Profile)**: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf
- **Publisher**: NIST (Tier 2)
- **Date**: January 2023 (RMF 1.0); July 2024 (AI 600-1)
- **Summary**: Federal framework for AI risk identification, assessment, and mitigation across the project lifecycle, with the 2024 GenAI Profile extending coverage to generative AI risks including hallucination, data leakage, and misuse — provides structured scoping methodology for organizations to align AI initiatives with goals, legal requirements, and risk tolerances.

### Source 1.3 — Google People + AI Guidebook (PAIR)
- **Title**: People + AI Guidebook
- **URL**: https://pair.withgoogle.com/guidebook/
- **Publisher**: Google PAIR (Tier 1)
- **Date**: Updated 2024 (2nd edition)
- **Summary**: Six-chapter design framework covering User Needs + Success Definition, Data Collection + Evaluation, Mental Models, and Explainability + Trust — used by over 250,000 practitioners to scope AI products with human-centered design principles from the outset.

### Source 1.4 — EU AI Act Risk Classification and Assessment Requirements
- **Title**: EU AI Act — High-Level Summary and Article 9: Risk Management System
- **URL**: https://artificialintelligenceact.eu/high-level-summary/
- **Publisher**: European Union (Tier 2)
- **Date**: August 2024 (entered into force)
- **Summary**: Regulatory framework requiring continuous risk management throughout the AI lifecycle — mandates that organizations scope AI systems by risk tier (unacceptable, high, limited, minimal), document assessments before deployment, and establish governance processes, with full high-risk compliance required by August 2026.

### Source 1.5 — Google Cloud AI Strategy Guide
- **Title**: An Effective AI Strategy: How to Build One
- **URL**: https://cloud.google.com/transform/how-to-build-an-effective-ai-strategy
- **Publisher**: Google Cloud (Tier 1)
- **Date**: 2025
- **Summary**: Enterprise AI strategy guide recommending a dual-pronged approach — top-down alignment of AI with strategic objectives combined with bottom-up discovery of real challenges from stakeholder teams — emphasizing infrastructure readiness assessment, governance-first principles, and measurable pilot design.

---

## Module 2: Golden Sets and Offline Evaluation Harnesses

Building evaluation datasets and offline testing pipelines for RAG and LLM systems.

### Source 2.1 — Anthropic Prompt Engineering & Evaluation Guide
- **Title**: Prompt Engineering Overview — Building Evaluations
- **URL**: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview
- **Publisher**: Anthropic (Tier 1)
- **Date**: 2024 (continuously updated)
- **Summary**: Official Anthropic documentation on defining success criteria and building evaluation pipelines for Claude-based systems, including guidance on scratchpad reasoning, few-shot example curation, and systematic evaluation of prompt variations against golden reference outputs.

### Source 2.2 — Google Stax LLM Evaluation Best Practices
- **Title**: Evaluation Best Practices — Stax
- **URL**: https://developers.google.com/stax/best-practices
- **Publisher**: Google for Developers (Tier 1)
- **Date**: 2025
- **Summary**: Google's evaluation framework recommending curated datasets with happy paths, edge cases, and adversarial examples; multiple frontier LLM judges (Gemini, GPT-4o, Claude) to mitigate bias; and manual calibration of a sample set to ensure autorater alignment before scaling.

### Source 2.3 — EleutherAI Language Model Evaluation Harness
- **Title**: lm-evaluation-harness: A Framework for Few-Shot Evaluation of Language Models
- **URL**: https://github.com/EleutherAI/lm-evaluation-harness
- **Publisher**: EleutherAI / Open Source (Tier 3 — 7,900+ GitHub stars)
- **Date**: Ongoing; v0.4.0 released 2024
- **Summary**: The backend for Hugging Face's Open LLM Leaderboard, providing 60+ standard academic benchmarks with support for transformers, vLLM, and API models — the de facto open-source offline evaluation harness used by NVIDIA, Cohere, BigScience, and dozens of organizations for reproducible LLM testing.

### Source 2.4 — RAGAS: Retrieval Augmented Generation Assessment
- **Title**: RAGAS — Supercharge Your LLM Application Evaluations
- **URL**: https://www.ragas.io/ (docs); https://aclanthology.org/2024.eacl-demo.16/ (paper)
- **Publisher**: Exploding Gradients / EACL 2024 (Tier 2 — peer-reviewed; Tier 3 — 7,000+ GitHub stars)
- **Date**: 2024 (EACL publication)
- **Summary**: Open-source framework for reference-free RAG evaluation providing metrics for faithfulness, answer relevancy, context precision, and context recall — enables golden dataset construction and automated evaluation without requiring ground-truth human annotations.

### Source 2.5 — Databricks MLflow LLM Evaluation Framework
- **Title**: MLflow 2.8 LLM-as-a-Judge Metrics and Best Practices for LLM Evaluation of RAG Applications
- **URL**: https://www.databricks.com/blog/announcing-mlflow-28-llm-judge-metrics-and-best-practices-llm-evaluation-rag-applications-part
- **Publisher**: Databricks (Tier 1)
- **Date**: 2024
- **Summary**: MLflow's LLM evaluation capabilities supporting the full development lifecycle — provides out-of-the-box metrics (toxicity, latency, cost), LLM-as-a-judge scoring (faithfulness, answer_correctness), and integration with RAGAS and DeepEval for 20+ evaluation metrics, achieving 80%+ consistency with human scores in production case studies.

---

## Module 3: Multi-Agent Workflow Design

Designing systems where multiple AI agents coordinate, including handoff protocols, state management, and failure isolation.

### Source 3.1 — Anthropic: Building Effective Agents
- **Title**: Building Effective Agents
- **URL**: https://www.anthropic.com/research/building-effective-agents
- **Publisher**: Anthropic (Tier 1)
- **Date**: December 2024
- **Summary**: Foundational guide from Anthropic's deployment experience with dozens of enterprise teams — covers five workflow patterns (prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer), advocates starting simple and adding multi-agent complexity only when justified, with real examples from Coinbase, Intercom, and Thomson Reuters.

### Source 3.2 — Anthropic: How We Built Our Multi-Agent Research System
- **Title**: How We Built Our Multi-Agent Research System
- **URL**: https://www.anthropic.com/engineering/multi-agent-research-system
- **Publisher**: Anthropic Engineering (Tier 1)
- **Date**: June 2025
- **Summary**: Deep engineering walkthrough of Anthropic's orchestrator-worker research system — lead agent coordinates parallel subagents, achieving 90.2% improvement over single-agent baselines; covers task decomposition strategies, context deduplication, citation handling, and the 15x token cost tradeoff of multi-agent architectures.

### Source 3.3 — OpenAI: A Practical Guide to Building Agents
- **Title**: A Practical Guide to Building Agents
- **URL**: https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf
- **Publisher**: OpenAI (Tier 1)
- **Date**: April 2025
- **Summary**: 34-page enterprise guide covering agent architecture (model + tools + instructions), orchestration strategies (manager pattern vs. decentralized handoffs), guardrail integration, and human-in-the-loop escalation — recommends starting with single-agent systems and graduating to multi-agent only when necessary.

### Source 3.4 — Microsoft Azure AI Agent Orchestration Patterns
- **Title**: AI Agent Orchestration Patterns
- **URL**: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
- **Publisher**: Microsoft Azure Architecture Center (Tier 1)
- **Date**: 2025
- **Summary**: Enterprise architecture reference covering sequential, parallel, and supervisor orchestration patterns with Azure AI Foundry — includes guidance on persistent state management, error recovery, context sharing across agents, and the Microsoft Agent Framework for production multi-agent deployments with built-in observability and compliance.

### Source 3.5 — OpenAI Agents SDK: Handoffs Documentation
- **Title**: Handoffs — OpenAI Agents SDK
- **URL**: https://openai.github.io/openai-agents-python/handoffs/
- **Publisher**: OpenAI (Tier 1)
- **Date**: March 2025
- **Summary**: Production SDK documentation for agent handoff mechanics — handoffs represented as tools to the LLM, supporting destination specification and payload passing; covers "agents as tools" pattern (bounded subtask delegation) vs. full handoffs (specialist takes over conversation), with guardrails running input validation in parallel with agent execution.

---

## Module 4: LLM Safety Guardrails

Implementing content safety, tool-use boundaries, and prompt injection defense for production LLM systems.

### Source 4.1 — OWASP Top 10 for LLM Applications 2025
- **Title**: OWASP Top 10 for Large Language Model Applications 2025
- **URL**: https://owasp.org/www-project-top-10-for-large-language-model-applications/assets/PDF/OWASP-Top-10-for-LLMs-v2025.pdf
- **Publisher**: OWASP Foundation (Tier 2)
- **Date**: November 2024 (v2025 release)
- **Summary**: Industry-standard security risk taxonomy for LLM applications — Prompt Injection remains #1, with Sensitive Information Disclosure rising to #2 and Supply Chain Vulnerabilities to #3; provides detailed mitigation strategies including input validation, privilege restriction, human-in-the-loop for privileged operations, and separation of untrusted content.

### Source 4.2 — AWS: Securing Amazon Bedrock Agents Against Indirect Prompt Injections
- **Title**: Securing Amazon Bedrock Agents: A Guide to Safeguarding Against Indirect Prompt Injections
- **URL**: https://aws.amazon.com/blogs/machine-learning/securing-amazon-bedrock-agents-a-guide-to-safeguarding-against-indirect-prompt-injections/
- **Publisher**: AWS Machine Learning Blog (Tier 1)
- **Date**: 2024
- **Summary**: Production defense guide covering Bedrock Guardrails configuration — multi-layered approach with input guardrails screening before LLM processing, output guardrails filtering responses, input tagging for dynamic/mutated prompts, and defense-in-depth practices; includes filter strength configuration (HIGH setting) and PII detection via regex-based filters.

### Source 4.3 — NIST AI 600-1: Generative AI Risk Management Profile
- **Title**: NIST AI 600-1 — Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile
- **URL**: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf
- **Publisher**: NIST (Tier 2)
- **Date**: July 2024
- **Summary**: Federal guidance on generative AI risk management including content filter guardrails, hallucination mitigation, data leakage prevention, and misuse controls — adapts the AI RMF specifically to GenAI risks and provides suggested practices organizations can adopt based on their risk tolerances and resources.

### Source 4.4 — tldrsec/prompt-injection-defenses (GitHub)
- **Title**: Every Practical and Proposed Defense Against Prompt Injection
- **URL**: https://github.com/tldrsec/prompt-injection-defenses
- **Publisher**: tldrsec / Open Source (Tier 3 — actively maintained, 1,900+ stars)
- **Date**: Ongoing (last updated 2024-2025)
- **Summary**: Comprehensive, actively maintained catalog of every production and proposed prompt injection defense — covers six categories: Instructional Defense, Guardrails & Overseers, Firewalls & Filters, Ensemble Decisions, Canaries, and research proposals; includes references to LLM Guard, Rebuff, and architectural controls.

### Source 4.5 — Datadog: LLM Guardrails Best Practices for Production
- **Title**: LLM Guardrails: Best Practices for Deploying LLM Apps Securely
- **URL**: https://www.datadoghq.com/blog/llm-guardrails-best-practices/
- **Publisher**: Datadog (Tier 3 — major observability vendor)
- **Date**: 2024
- **Summary**: Production-focused guide covering layered guardrail implementation — input validation (static filters + ML classifiers), output filtering for data leakage prevention, execution sandboxing to contain successful attacks, and continuous monitoring for evolving attack patterns; includes real-world vulnerability case study of Slack AI API key exfiltration via indirect prompt injection (August 2024).

---

## Module 5: Employee AI Adoption Programs

Driving actual behavior change (not just training completion) when deploying AI tools to employees.

### Source 5.1 — McKinsey: Superagency in the Workplace (2025)
- **Title**: Superagency in the Workplace: Empowering People to Unlock AI's Full Potential at Work
- **URL**: https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/superagency-in-the-workplace-empowering-people-to-unlock-ais-full-potential-at-work
- **Publisher**: McKinsey & Company (Tier 2 — major consultancy)
- **Date**: January 2025
- **Summary**: Reveals critical perception gap — C-suite estimates only 4% of employees use GenAI for 30%+ of daily work, actual figure is 13%; 47% of employees say they already do or will within a year vs. 20% leadership expectation; 48% of employees rank training as most important factor but nearly half report receiving minimal or none.

### Source 5.2 — Microsoft: New Future of Work Report 2025
- **Title**: New Future of Work Report 2025
- **URL**: https://www.microsoft.com/en-us/research/wp-content/uploads/2025/12/New-Future-Of-Work-Report-2025.pdf
- **Publisher**: Microsoft Research (Tier 1)
- **Date**: December 2025
- **Summary**: Research synthesis finding AI can save 40-60 minutes daily but gains vary by task (legal/management 80-85% time savings vs. diagnostic review ~20%); identifies "workslop" problem (AI-generated content with errors) affecting 40% of employees monthly; warns employees resist top-down mandates and need psychological safety, leadership modeling, and flexible integration.

### Source 5.3 — Wharton/GBK: 2025 AI Adoption Report
- **Title**: Accountable Acceleration: Gen AI Fast-Tracks Into the Enterprise
- **URL**: https://knowledge.wharton.upenn.edu/special-report/2025-ai-adoption-report/
- **PDF**: https://ai.wharton.upenn.edu/wp-content/uploads/2025/10/2025-Wharton-GBK-AI-Adoption-Report_Full-Report.pdf
- **Publisher**: Wharton Human-AI Research (WHAIR) + GBK Collective (Tier 2 — academic)
- **Date**: October 2025
- **Summary**: Third annual survey of 800+ enterprise decision-makers — 82% of leaders use GenAI weekly, 74% see positive ROI, but 43% worry about skills proficiency decline; Chief AI Officer roles now in 61% of enterprises; adoption strongest in data analysis, document summarization, and writing, with function-specific patterns (code writing for IT, recruitment for HR).

### Source 5.4 — Prosci: AI Adoption — Driving Change With a People-First Approach
- **Title**: AI Adoption: Driving Change With a People-First Approach
- **URL**: https://www.prosci.com/blog/ai-adoption
- **Publisher**: Prosci (Tier 2 — change management authority)
- **Date**: 2025
- **Summary**: Applies the ADKAR Model (Awareness, Desire, Knowledge, Ability, Reinforcement) to AI adoption — finds user proficiency is the #1 challenge (38% of difficulties), with 56% of organizations struggling with human factors over technical ones; recommends personalized learning journeys over one-size-fits-all training and coalitions of senior sponsors modeling ethical AI behavior.

### Source 5.5 — Anthropic: Enterprise AI Transformation Guide
- **Title**: The Enterprise AI Transformation Guide
- **URL**: https://resources.anthropic.com/enterprise-ai-transformation-guide
- **Publisher**: Anthropic (Tier 1)
- **Date**: 2025
- **Summary**: Three-step blueprint for enterprise AI adoption drawn from real customer deployments — (1) lay an AI foundation with governance and stakeholder alignment, (2) launch targeted pilots that demonstrate measurable value, (3) drive impact through structured training programs; reports early adopters achieving 20-35% faster customer support, ~15% less coding time, and 30-50% faster content workflows.

---

## Source Tier Summary

| Tier | Count | Publishers |
|------|-------|-----------|
| Tier 1 (vendor docs) | 13 | Anthropic (5), Google (3), OpenAI (2), AWS (1), Microsoft (1), Databricks (1) |
| Tier 2 (standards/academic) | 8 | NIST (2), OWASP (1), EU AI Act (1), McKinsey (1), Wharton (1), Prosci (1), RAGAS/EACL (1) |
| Tier 3 (GitHub/industry) | 4 | EleutherAI (1), tldrsec (1), Datadog (1), RAGAS (1) |

**Total**: 25 sources across 5 modules (5 per module)
