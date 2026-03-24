# Open Badges 3.0 Implementation Guide

**Date**: 2026-03-24
**Purpose**: Practical guide for implementing Open Badges 3.0 (W3C Verifiable Credentials) for a new developer certification program.

---

## Table of Contents

1. [Technical Requirements](#1-technical-requirements)
2. [Platform Comparison: Accredible vs Credly vs Self-Hosted](#2-platform-comparison)
3. [Embedding Competency Metadata](#3-embedding-competency-metadata)
4. [LinkedIn Integration](#4-linkedin-integration)
5. [Employer Verification](#5-employer-verification)
6. [Cost Analysis](#6-cost-analysis)
7. [AI/Developer Certification Programs Using OB 3.0](#7-ai-developer-programs)
8. [Recommendations](#8-recommendations)

---

## 1. Technical Requirements

### What Is Open Badges 3.0?

Open Badges 3.0 (finalized by 1EdTech in June 2024) aligns digital badges with the W3C Verifiable Credentials Data Model v2.0. Each badge is a cryptographically signed JSON-LD document that can be independently verified without contacting the issuer. This is a fundamental shift from OB 2.0, which relied on hosted verification (the issuer's server had to be online for a badge to be verified).

### Infrastructure Components Required

To issue OB 3.0 badges, you need the following:

**A. Credential Issuer Service**
- A service that creates, signs, and delivers OpenBadgeCredential JSON-LD documents.
- Must implement the OB 3.0 RESTful API with dynamic client registration for transporting credentials in OpenBadgeCredential format.
- Must generate and manage cryptographic keys for signing.

**B. Cryptographic Key Infrastructure**
- OB 3.0 supports two primary proof methods:
  - **Data Integrity EdDSA Cryptosuites v1.0** (W3C Recommendation, May 2025): Uses Ed25519 keys and produces a `DataIntegrityProof` referencing a public key in `eddsa-rdf-2022` format.
  - **Data Integrity ECDSA Cryptosuites v1.0** (W3C Recommendation, May 2025): Uses ECDSA keys.
  - **JWT with RSA256**: Key material published as JSON Web Key (JWK).
- You need a key management system (KMS) or at minimum a secure key store for signing keys.

**C. Decentralized Identifiers (DIDs)**
- OB 3.0 supports DIDs for identifying both issuers and recipients.
- A DID links the badge to the issuer's verified identity without a centralized authority.
- The DID resolves to a DID Document containing the public key needed for verification.
- Common DID methods: `did:web` (easiest -- uses your domain), `did:key` (self-contained), `did:ion` (Bitcoin-anchored).

**D. Badge Hosting / Delivery**
- Signed credentials can be delivered directly to recipients (email, API, download).
- Recipients can store badges in any OB 3.0-compliant digital wallet.
- Badge images (PNG or SVG) can have the JSON-LD metadata embedded within them ("baked badges").

**E. Verification Endpoint**
- A publicly accessible endpoint where third parties can verify credentials.
- With cryptographic proofs, verification can also happen entirely offline using the embedded proof and the issuer's public key.

### Minimal Credential Structure (JSON-LD)

```json
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://purl.imsglobal.org/spec/ob/v3p0/context-3.0.3.json"
  ],
  "id": "urn:uuid:a]]1b2c3d-4e5f-6789-abcd-ef0123456789",
  "type": ["VerifiableCredential", "OpenBadgeCredential"],
  "issuer": {
    "id": "did:web:example.com",
    "type": ["Profile"],
    "name": "Palette Developer Enablement",
    "url": "https://example.com"
  },
  "validFrom": "2026-03-24T00:00:00Z",
  "credentialSubject": {
    "id": "did:example:recipient123",
    "type": ["AchievementSubject"],
    "achievement": {
      "id": "https://example.com/achievements/ai-agent-fundamentals",
      "type": ["Achievement"],
      "name": "AI Agent Fundamentals",
      "description": "Demonstrated competency in designing and deploying AI agent systems.",
      "criteria": {
        "narrative": "Complete all modules and pass the assessment with 80% or higher."
      },
      "alignment": [
        {
          "type": ["Alignment"],
          "targetName": "AI Agent Design",
          "targetUrl": "https://example.com/skills/ai-agent-design",
          "targetFramework": "Palette Skills Framework",
          "targetCode": "SKILL-AGT-101",
          "targetType": "CFItem"
        }
      ]
    }
  },
  "proof": {
    "type": "DataIntegrityProof",
    "cryptosuite": "eddsa-rdfc-2022",
    "created": "2026-03-24T00:00:00Z",
    "verificationMethod": "did:web:example.com#key-1",
    "proofPurpose": "assertionMethod",
    "proofValue": "z..."
  }
}
```

### Technology Stack Options

| Component | Self-Hosted | Managed |
|-----------|------------|---------|
| Credential signing | Custom (Node.js/Python with VC libraries) | Platform handles it |
| DID management | `did:web` (host a JSON file on your domain) | Platform provides |
| Key management | HashiCorp Vault, AWS KMS | Platform manages |
| Badge delivery | Custom API + email | Platform UI + API |
| Verification | Custom endpoint or offline | Platform-hosted page |
| JSON-LD context | Use 1EdTech published contexts | Automatic |

### Key Libraries and Tools

- **digitalcredentials/open-badges-context** (GitHub): NPM package for the OBv3 JSON-LD context.
- **1EdTech/openbadges-specification** (GitHub): Reference implementation and examples.
- **Spruce ID / DIDKit**: Toolkit for working with DIDs and Verifiable Credentials.
- **Transmute Industries VC libraries**: For VC issuance and verification in JavaScript.

---

## 2. Platform Comparison

### Overview

| Feature | Credly (by Pearson) | Accredible | Self-Hosted |
|---------|---------------------|------------|-------------|
| **OB Version** | OB 2.0 (as of early 2026) | OB 3.0 + W3C VC (announced) | OB 3.0 (you control) |
| **Target Market** | Enterprise, large programs | SMB, education, coaches | Technical teams with dev capacity |
| **Setup Fee** | ~$2,000 | ~$1,500 | $0 (your engineering time) |
| **Annual Minimum** | ~$1,000+ | ~$1,000 | Infrastructure costs only |
| **Per-Credential Cost** | $2-5/badge | Per-recipient model (~$4/yr per unique recipient) | ~$0 marginal cost |
| **LinkedIn Integration** | Direct API (deep) | Direct API (deep) | Manual (recipient shares) |
| **1EdTech Certified OB 3.0** | Not yet | Announced OB 3.0 + W3C VC support | Depends on implementation |
| **Customization** | 3,000+ icons, limited templates | 1,000+ templates, good design tools | Unlimited |

### Credly (by Pearson)

**Strengths:**
- Market leader for enterprise certification programs. Used by AWS, Google Cloud, Microsoft, IBM, OpenAI, Cisco, and hundreds of others.
- Deepest LinkedIn integration -- badges auto-sync with verification metadata and clickable verification links.
- Largest badge ecosystem -- earners can discover related credentials and employers can search the Credly network.
- Robust analytics: track badge claims, shares, and labor market insights.

**Weaknesses:**
- Still on Open Badges 2.0 as of early 2026. Not yet 1EdTech OB 3.0 certified.
- Opaque pricing -- no public pricing page; requires sales engagement.
- No free tier. Minimum annual commitment of ~$1,000+.
- Limited template customization compared to Accredible.
- Vendor lock-in risk: badges hosted on Credly's infrastructure.

**Best for:** Programs that prioritize LinkedIn visibility, enterprise credibility, and association with major tech certification brands.

### Accredible

**Strengths:**
- Announced support for Open Badges 3.0 and W3C Verifiable Credentials.
- Pricing based on unique recipients (not per credential), so issuing multiple credentials to the same person is economical.
- Strong template library with good design customization.
- Integrations: LMS (via API), Zoom, WooCommerce, Zapier.
- More transparent pricing with published tiers.
- First 20 credentials free.

**Weaknesses:**
- Smaller ecosystem and less brand recognition than Credly in the enterprise certification space.
- Setup process has been criticized as difficult by some users.
- LinkedIn integration exists but is less deeply embedded than Credly's.

**Pricing Tiers (2026):**
- Launch: $45/month (up to 50 recipients), annual commitment
- Growth / Pro / Enterprise: tiered up from there
- Approximately $1,500 setup fee

**Best for:** Programs that want OB 3.0 compliance, moderate scale, and good design tools without Credly-level enterprise pricing.

### Self-Hosted

**Strengths:**
- Full control over credential format, metadata, and verification.
- Native OB 3.0 / W3C VC compliance from day one.
- Zero per-credential marginal cost.
- No vendor lock-in. Credentials survive even if you change platforms.
- Can embed any custom metadata extensions.

**Weaknesses:**
- Requires significant engineering investment to build and maintain.
- No built-in LinkedIn integration (recipients must manually share).
- No built-in analytics dashboard.
- You must handle key management, DID infrastructure, and verification endpoints.
- Badgr Server (the main open-source option) only supports OB 2.0. There is no mature open-source OB 3.0 issuer as of early 2026.
- Badgr's free tier ended December 31, 2025 (transitioned to Parchment Digital Badges).

**Open-Source Options:**
- **Badgr Server** (Python/Django): OB 2.0 only. Fedora Infrastructure maintains a fork. Being sunset/commercialized.
- **Moodle Open Badges**: Built into Moodle LMS. OB 2.0 with some 3.0 work in progress.
- **DCC (Digital Credentials Consortium)**: MIT-led consortium building open-source VC tooling. Worth watching.

**Best for:** Technical teams that want maximum control, plan to issue at scale (thousands+), and can invest engineering time upfront.

### Other Platforms Worth Considering

| Platform | OB 3.0 | Free Tier | Notable |
|----------|--------|-----------|---------|
| **Open Badge Factory** | Yes (1EdTech certified) | No (starts at ~EUR 200/yr) | First European OB 3.0 certified platform |
| **POK** | Yes (1EdTech certified) | Yes (unlimited Web2 credentials) | $0 setup, no minimum; blockchain option for NFT badges |
| **Certifier** | Yes (OB 3.0 compliant) | Yes (forever-free plan) | Drag-and-drop designer, Zapier/API integration |
| **VirtualBadge.io** | OB 2.0 | No | Good design tools, limited standard support |
| **Acreditta** | OB 3.0 | No | Strong in Latin America |

---

## 3. Embedding Competency Metadata

### The Alignment Object

Open Badges 3.0 provides the `alignment` property on the `Achievement` object to link badges to external competency frameworks, skills taxonomies, and standards. This is the primary mechanism for embedding competency metadata.

**Alignment Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `targetName` | String | Name of the skill, competency, or standard |
| `targetUrl` | URI | URL pointing to the official description of the alignment target |
| `targetDescription` | String | Short description of the target |
| `targetFramework` | String | Name of the framework (e.g., "ESCO", "O*NET", "SFIA") |
| `targetCode` | String | Code within the framework (e.g., "K0001", "PROG-3") |
| `targetType` | String | Type of target: `CFItem`, `CFRubric`, `CFRubricCriterion`, `CTDL`, etc. |

### Example: Multiple Skill Alignments

```json
"achievement": {
  "id": "https://example.com/achievements/agentic-ai-architect",
  "type": ["Achievement"],
  "name": "Agentic AI Architect",
  "description": "Demonstrated ability to design multi-agent systems with tool use, memory, and orchestration.",
  "criteria": {
    "narrative": "Complete the capstone project demonstrating agent orchestration patterns."
  },
  "alignment": [
    {
      "type": ["Alignment"],
      "targetName": "AI Agent Design Patterns",
      "targetUrl": "https://example.com/skills/agent-design",
      "targetFramework": "Palette Skills Framework",
      "targetCode": "PSF-AGT-200",
      "targetType": "CFItem"
    },
    {
      "type": ["Alignment"],
      "targetName": "Prompt Engineering",
      "targetUrl": "https://esco.ec.europa.eu/en/classification/skills?uri=...",
      "targetFramework": "ESCO",
      "targetCode": "S5.8.1",
      "targetType": "CFItem"
    },
    {
      "type": ["Alignment"],
      "targetName": "Software Architecture",
      "targetUrl": "https://sfia-online.org/en/sfia-8/skills/software-architecture",
      "targetFramework": "SFIA 8",
      "targetCode": "ARCH-4",
      "targetType": "CFItem"
    }
  ]
}
```

### The ACE Extension

The American Council on Education (ACE) extension is a specialized OB 3.0 extension that adds credit recommendation metadata. This is relevant if your developer certification program wants academic credit equivalency.

**ACE Extension adds:**
- Recommended credit hours (e.g., "3 semester hours in lower-division baccalaureate")
- Academic level classification
- Minimum passing score
- Credit recommendation notes
- Links to ACE's National Guide to College Credit for Workforce Training

**ACE Extension Structure:**
- Top-level object: `ACEEndorsementSubject`
- Contains: learning evaluation, credit recommendations, competency alignments as `Alignment` objects with appropriate `targetType`
- JSON Schema: `https://purl.imsglobal.org/spec/ob-ace/v1p0/schema/ob_ace_v1p0_endorsementcredential_schema.json`
- JSON-LD context: `https://purl.imsglobal.org/spec/ob-ace/v1p0/context/context-1.0.0.json`

**When to use ACE:** Only if you want ACE to formally evaluate your certification for college credit equivalency. This involves an ACE review process and is most relevant for longer, more substantial certification programs. For a developer certification program starting from scratch, this is a Phase 2 or Phase 3 consideration.

### Shared Achievements and Skill Assertions

OB 3.0 introduces **Shared Achievements** -- a generic achievement definition that multiple issuers can reference. This enables:

- **Skill Assertions**: A credential that claims the earner has a specific skill, with each issuer doing their own assessment against a shared definition.
- **Interoperability**: Different organizations can issue badges referencing the same skill framework, making credentials comparable across programs.

### Recommended Frameworks for Developer Certifications

| Framework | Best For | URL |
|-----------|----------|-----|
| **SFIA 8** (Skills Framework for the Information Age) | IT professional skills at defined levels | sfia-online.org |
| **ESCO** (European Skills/Competences, Qualifications and Occupations) | EU-aligned skill taxonomy | esco.ec.europa.eu |
| **O*NET** | US labor market skill alignment | onetonline.org |
| **NICE Framework** (NIST) | Cybersecurity workforce roles | nist.gov/nice |
| **Custom (Palette Skills Framework)** | Internal taxonomy alignment | Define your own |

---

## 4. LinkedIn Integration

### Current State (March 2026)

LinkedIn's badge integration is an important consideration because it is the primary channel through which employers encounter digital credentials.

**How badges appear on LinkedIn:**
- Badges appear in the **Licenses & Certifications** section of the profile.
- LinkedIn displays the **issuer's company logo** (not the badge image itself) in the Accomplishments section.
- The credential name, issuing organization, and issue date are shown.
- A **"See Credential"** link takes viewers to the badge verification page hosted by the issuing platform.

**Key limitation:** LinkedIn does not natively parse Open Badges 3.0 metadata. It relies on established trust relationships with major badge platforms (primarily Credly and Accredible).

### Integration Paths

**Path 1: Via Credly (Deepest Integration)**
- Credly has a direct API integration with LinkedIn.
- Badges from Credly issuers auto-sync with full verification metadata, enhanced issuer branding, and clickable verification links.
- Microsoft, IBM, AWS, Google Cloud, and OpenAI all use Credly, making it the de facto standard for LinkedIn certification display.
- Recipients can add badges with one click from the Credly platform.

**Path 2: Via Accredible**
- Accredible also has LinkedIn integration allowing one-click sharing.
- Credentials appear in the Licenses & Certifications section with proper metadata.
- Google uses Accredible for some of its professional certificate programs.

**Path 3: Self-Hosted / Other Platforms**
- Recipients must manually add the credential to their LinkedIn profile.
- They can enter: credential name, issuing organization, issue date, expiration date (if any), credential ID, and credential URL.
- The credential URL should point to a public verification page.
- No automatic sync, no enhanced branding.

**Path 4: LinkedIn Verified Credentials (Emerging)**
- LinkedIn has been piloting a "Verified" program for credentials.
- As of early 2026, LinkedIn has **paused new educational institution verifications** while refining the integration process.
- Existing verified badges remain on profiles.
- This is a space to watch -- if LinkedIn adopts native OB 3.0/VC support, it would be transformative.

### Practical Recommendation

For maximum LinkedIn visibility at launch, use Credly or Accredible as your badge platform. If you self-host, ensure you provide a clean public verification URL that recipients can link from their LinkedIn profile. Plan for the possibility that LinkedIn will eventually support native VC/OB 3.0 verification, which would benefit self-hosted approaches.

---

## 5. Employer Verification

### How Verification Works in OB 3.0

Open Badges 3.0's alignment with W3C Verifiable Credentials fundamentally changes verification. Unlike OB 2.0 (where the issuer's server had to be queried), OB 3.0 enables **offline, issuer-independent verification**.

### Verification Methods

**Method 1: Cryptographic Proof Verification (Primary)**

The badge itself contains a `proof` object with a digital signature. An employer (or any verifier) can:

1. Obtain the badge (from the earner's wallet, a URL, or a baked image).
2. Extract the JSON-LD credential.
3. Resolve the issuer's DID to obtain the public key.
4. Verify the cryptographic signature against the credential content.
5. Confirm the credential has not been tampered with.

This works **without contacting the issuer**. The issuer could be offline, or even no longer exist, and the badge is still verifiable.

**Method 2: Platform-Hosted Verification Page**

Most badge platforms (Credly, Accredible, etc.) provide a public URL for each issued badge. Employers click the URL and see:
- The badge details (name, description, criteria).
- The earner's identity.
- The issuer's identity and logo.
- The issue date and expiration (if any).
- A "Verified" status indicator.

This is the most common verification method today because it requires zero technical knowledge from the employer.

**Method 3: Verifiable Presentation**

In the full W3C VC workflow:
1. An employer requests proof of a credential (e.g., via an ATS or job portal).
2. The earner uses their digital wallet to create a **Verifiable Presentation** containing the badge.
3. The presentation is cryptographically bound to the earner, proving they hold the credential.
4. The employer's system verifies the presentation automatically.

This is the most sophisticated method and is still emerging in practice. Adoption depends on employer ATS systems supporting VC verification.

### Verification Without Contacting the Issuer -- Step by Step

```
1. Earner shares badge (JSON-LD file, baked image, or URL)
        |
2. Verifier extracts the credential JSON-LD
        |
3. Verifier reads the "issuer.id" field (a DID or URL)
        |
4. Verifier resolves the DID --> obtains DID Document with public key
        |
5. Verifier reads the "proof" object --> signature + verification method
        |
6. Verifier runs signature verification algorithm
   (EdDSA, ECDSA, or JWT depending on proof type)
        |
7. If signature is valid --> credential is authentic and untampered
        |
8. Verifier checks "validFrom" / "validUntil" dates
        |
9. Optionally: check revocation status (if issuer publishes a status list)
```

### Revocation

OB 3.0 supports credential revocation through:
- **Status List 2021**: Issuers publish a bitstring at a URL; each credential has an index in the list. If the bit is flipped, the credential is revoked.
- This is the one scenario where the issuer's infrastructure must remain accessible (to host the status list).

### Practical Verification Tools

- **vc-verifier** (various implementations): Libraries for verifying VCs in JavaScript, Python, Go.
- **1EdTech Conformance Test Suite**: For testing OB 3.0 compliance.
- **Universal Verifier** services: Several providers offer hosted VC verification.

---

## 6. Cost Analysis

### Cost at Scale: 100 to 10,000 Credentials/Year

| Scale | Credly | Accredible | Open Badge Factory | POK | Certifier | Self-Hosted |
|-------|--------|------------|-------------------|-----|-----------|-------------|
| **Setup** | ~$2,000 | ~$1,500 | EUR 0 | $0 | $0 | Engineering time (est. 2-4 weeks) |
| **100/yr** | $3,000-5,000/yr | $540-1,000/yr | ~EUR 200/yr | $0 (Web2) | $0 (free tier) | ~$50-100/yr infra |
| **500/yr** | $5,000-8,000/yr | $1,000-3,000/yr | ~EUR 500/yr | $0 (Web2) | $0-500/yr | ~$50-100/yr infra |
| **1,000/yr** | $5,000-12,000/yr | $3,000-6,000/yr | ~EUR 800/yr | $0 (Web2) | ~$500-1,000/yr | ~$100-200/yr infra |
| **5,000/yr** | $10,000-20,000/yr | $6,000-11,520/yr | Custom quote | $0 (Web2) | Custom | ~$200-500/yr infra |
| **10,000/yr** | $15,000-25,000+/yr | $11,520+/yr | Custom quote | $0 (Web2) | Custom | ~$500-1,000/yr infra |

**Notes on the table above:**
- Credly pricing is opaque and based on sales negotiation. Ranges are based on user reports and competitor analysis, not published prices.
- Accredible charges per unique recipient, not per credential. Issuing 5 badges to the same person counts as 1 recipient.
- POK's free tier covers unlimited Web2 (non-blockchain) credential issuance. Blockchain/NFT badges cost extra per credential.
- Self-hosted infrastructure costs assume a small VM/container + domain + TLS. The major cost is engineering time to build and maintain.
- Certifier's free tier covers basic badge issuance; premium features require paid plans.

### Hidden Costs to Budget For

| Cost Category | Estimate |
|---------------|----------|
| Badge design (graphic design) | $500-2,000 one-time |
| Competency framework development | 2-4 weeks of specialist time |
| LMS/platform integration development | 1-4 weeks engineering |
| Ongoing badge program management (staff time) | 5-20 hrs/month |
| Assessment/exam platform (if proctored) | $5-50/exam (varies widely) |
| 1EdTech membership (for OB 3.0 certification of your platform) | $3,000-10,000/yr depending on org size |

### Cost Optimization Strategies

1. **Start with a free/low-cost platform** (POK, Certifier) to validate the program before committing to Credly/Accredible enterprise contracts.
2. **Use Accredible's per-recipient model** if you issue multiple badges per learner (e.g., module badges + a capstone badge).
3. **Self-host only if** you plan to issue 5,000+ credentials/year AND have dedicated engineering capacity AND want full control over the credential format.
4. **Avoid Credly's setup fee** by negotiating -- some programs have reported waived fees at higher volume commitments.

---

## 7. AI/Developer Certification Programs Using OB 3.0 (Since 2025)

### Programs Confirmed Using Digital Badges (OB-Compliant)

**OpenAI Certifications (2025-2026)**
- OpenAI launched "AI Foundations" and is building toward full OpenAI Certifications.
- Partners: Coursera (learning), ETS (psychometrics), **Credly by Pearson** (portable digital badges).
- Goal: Certify 10 million Americans by 2030.
- Pilot partners include Walmart, John Deere, Lowe's, BCG, Accenture, Upwork.
- Status: Teacher course live on Coursera; enterprise pilots expanding through 2026.
- Note: Uses Credly (OB 2.0), not yet confirmed OB 3.0.

**AWS AI Certifications (2025-2026)**
- AWS launched the **AWS Certified Generative AI Developer -- Professional** certification.
- Validates developer ability to integrate foundation models into applications.
- Badges issued through Credly.
- Part of AWS's expanded AI certification portfolio alongside existing ML certifications.

**Google Cloud Certifications**
- 130+ badge templates on Credly, including **Generative AI Leader Certification**.
- Skill badges earned through Google Cloud Skills Boost platform.
- Credly badges contain OBI-compliant metadata embedded in badge images.

**Microsoft Azure AI Engineer Associate**
- Continues to use Credly for digital badge issuance.
- Covers AI solution design on Azure.

**Red Hat AI Foundations Technologist Certificate**
- Available on Credly.
- Covers foundational AI concepts for Red Hat ecosystem.

### Programs Using OB 3.0 Specifically

The adoption of OB 3.0 specifically (as opposed to OB 2.0 via Credly) is still early. The programs most likely to be issuing OB 3.0 badges are those using:

- **Open Badge Factory** (1EdTech OB 3.0 certified since 2024): Primarily European educational institutions. OBF announced "your badges are now Open Badges 3.0" to all existing issuers.
- **Accredible** (announced OB 3.0 + W3C VC support): Used by Google for some professional certificates.
- **POK** (1EdTech OB 3.0 certified): Growing adoption in Latin America and Europe.
- **Italian Quality Company (IQC)**: First in Europe to achieve OB 3.0 certification.

**Other early OB 3.0 certified platforms/organizations:**
- MarkAny Chainverse
- Universities Admissions Centre (UAC, Australia)
- SWEMPIRE
- NetLearning Holdings
- Sparkplus Technologies
- eLumen

### Key Observation

As of March 2026, the major AI/developer certification programs (OpenAI, AWS, Google Cloud, Microsoft) all use **Credly**, which remains on OB 2.0. The OB 3.0 ecosystem is being led by European credentialing platforms and educational institutions rather than by the major tech certification programs. This is likely to change as Credly and other major platforms complete their OB 3.0 transitions.

---

## 8. Recommendations

### For a New Developer Certification Program Starting From Scratch

**Phase 1: Launch (Months 1-3)**

1. **Choose a platform**: Start with **Accredible** or **Certifier** for the best balance of OB 3.0 support, cost, and ease of use. If LinkedIn visibility and enterprise credibility are paramount and budget allows, use **Credly** despite its OB 2.0 limitation (it will transition to 3.0).
2. **Define your competency framework**: Map each certification to specific skills using the `alignment` property. Use an established framework (SFIA, ESCO) supplemented with your own taxonomy codes.
3. **Design 2-3 badge levels**: e.g., Foundations, Practitioner, Architect. Keep initial scope narrow.
4. **Set up LinkedIn integration**: Ensure one-click sharing from your platform to LinkedIn.

**Phase 2: Mature (Months 4-8)**

5. **Add skill assertions**: Use OB 3.0's shared achievement model to make individual skills discoverable.
6. **Implement API integrations**: Connect to your LMS/learning platform for automated badge issuance on assessment completion.
7. **Publish a public verification page**: Ensure every badge has a clean, professional verification URL.

**Phase 3: Scale (Months 9+)**

8. **Evaluate self-hosting**: If you're issuing 5,000+/year and want full control, consider building a self-hosted OB 3.0 issuer using the Digital Credentials Consortium tooling.
9. **Explore ACE credit equivalency**: If your certification program is substantial enough to warrant college credit recognition.
10. **Monitor LinkedIn VC integration**: If LinkedIn adds native OB 3.0/VC verification, shift strategy to maximize that channel.

### Decision Matrix

| If your priority is... | Choose... |
|------------------------|-----------|
| LinkedIn visibility + enterprise recognition | Credly |
| OB 3.0 compliance + moderate cost | Accredible or Open Badge Factory |
| Zero cost to start + OB 3.0 | POK or Certifier (free tiers) |
| Full control + custom metadata | Self-hosted |
| Fastest time to launch | Certifier (drag-and-drop, free tier, OB 3.0) |

---

## Sources

- [Open Badges 3.0 Specification (1EdTech/IMS Global)](https://www.imsglobal.org/spec/ob/v3p0)
- [Open Badges 3.0 Implementation Guide](https://www.imsglobal.org/spec/ob/v3p0/impl)
- [Open Badges 3.0 Certification Guide](https://www.imsglobal.org/spec/ob/v3p0/cert)
- [Open Badges ACE Extension v1.0](https://www.imsglobal.org/spec/ob-ace/v1p0)
- [1EdTech Product Certifications (filter by OB 3.0)](https://site.imsglobal.org/certifications)
- [Open Badges 3.0 Explained (Anonyome)](https://anonyome.com/resources/blog/open-badges-3-explained/)
- [Open Badges 3.0 and Verifiable Credentials (Indicio)](https://indicio.tech/open-badges/)
- [Credly Pricing Analysis 2026 (Certifier)](https://certifier.io/blog/credly-pricing-is-credly-worth-it-in-2022)
- [Digital Credentials Cost Comparison 2026 (POK)](https://www.pok.tech/blog/posts/credly-accredible-accreditta-vs-pok-digital-credentials-pricing-2026)
- [Accredible vs Credly Feature Breakdown 2025 (VirtualBadge)](https://www.virtualbadge.io/blog-articles/accredible-vs-credly--the-ultimate-feature-breakdown-of-2025)
- [Accredible OB 3.0 + W3C VC Announcement](https://www.accredible.com/blog/now-supporting-open-badge-3-0-and-w3c-verifiable-credentials)
- [Open Badge Factory OB 3.0 Announcement](https://openbadgefactory.com/en/your-badges-are-now-open-badges-3-0/)
- [OpenAI Certifications Launch](https://openai.com/index/openai-certificate-courses/)
- [OpenAI Certification Standards (AI News)](https://www.artificialintelligence-news.com/news/openai-targets-ai-skills-gap-with-new-certification-standards/)
- [AWS AI Certification Expansion](https://aws.amazon.com/blogs/training-and-certification/big-news-aws-expands-ai-certification-portfolio-and-updates-security-certification/)
- [LinkedIn Digital Badge Setup Guide (VerifyEd)](https://www.verifyed.io/blog/linkedin-badge-setup-guide)
- [Credly LinkedIn Integration Guide](https://support.credly.com/hc/en-us/articles/360021221491-How-can-I-add-my-badge-to-my-LinkedIn-profile-and-share-to-my-feed)
- [Accredible LinkedIn Integration](https://help.accredible.com/s/article/add-your-credential-to-linkedin?language=en_US)
- [OB 3.0 Simple Example (HackMD)](https://hackmd.io/@kayelle/S1qBAh8ud)
- [Digital Credentials Consortium (GitHub)](https://github.com/digitalcredentials/open-badges-context)
- [1EdTech Open Badges 3.0 Standard Announcement](https://www.1edtech.org/1edtech-article/new-open-badges-30-standard-provides-enhanced-security-and-mobility/411060)
- [Badge Platforms Comparison (Badge Wiki)](https://badge.wiki/wiki/Badge_platforms)
- [Certifier Open Badges 3.0 Guide](https://certifier.io/blog/open-badges-3-0)
- [AI Certification Landscape 2026 (Pertama Partners)](https://www.pertamapartners.com/insights/ai-certification-landscape-2026)
