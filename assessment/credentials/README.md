# Credential Flow — Palette Developer Enablement & Certification System

## Overview

This directory contains the schemas and documentation for the credential flow in the Palette Developer Enablement & Certification System. The system uses Open Badges 3.0 and W3C Verifiable Credentials v2.0 to issue digital credentials that are cryptographically verifiable, portable, and interoperable.

## Credential Types

### 1. Module-Level Badges

**Schema**: `badge_schema.yaml`

Module-level badges are awarded for completing individual modules within a certification track. These badges signify that the developer has demonstrated competency in the module's core principles and can apply them in practice.

**Key Features**:
- Aligned to specific skills in the Palette Skills Framework
- Requires completion of all learning objectives and passing the module assessment
- Valid for 2 years
- Includes evidence requirements for module completion and artifact submission

**Example**: A developer who completes the "Stakeholder Map + RACI-lite" module (RIU-002) would earn a badge for that module.

### 2. Track-Level Credentials

**Schema**: `track_credential_schema.yaml`

Track-level credentials are awarded for completing all modules within a certification track. These credentials signify that the developer has demonstrated competency across the track's core principles and is recognized by industry employers.

**Key Features**:
- References all module-level badges earned by the recipient
- Aligned to the track's core skills in the Palette Skills Framework
- Requires completion of all modules in the track and passing the track assessment
- Valid for 2 years
- Includes evidence requirements for track completion and portfolio review

**Example**: A developer who completes all modules in the "AI Foundations" track would earn the "Palette Certified AI Foundations Developer" credential.

### 3. Tier-Based Credentials

**Schemas**: 
- `tier_unvalidated_badge.yaml`
- `tier_working_badge.yaml`
- `tier_production_badge.yaml`

Tier-based credentials are awarded based on the developer's overall certification level. These credentials signify the developer's progression through the certification journey and their ability to lead complex enterprise AI projects.

**Key Features**:
- **UNVALIDATED Tier**: Entry-level tier for developers who have completed the placement test
- **WORKING Tier**: Mid-level tier for developers who have demonstrated competency in one or more tracks
- **PRODUCTION Tier**: Expert-level tier for developers who have demonstrated mastery across multiple tracks and completed an architecture defense

**Example**: A developer who completes two certification tracks and an architecture defense would earn the "Palette Certified Developer — PRODUCTION Tier" credential.

## Credential Flow

The credential flow in the Palette system follows a hierarchical structure:

```
Developer → Module Completion → Module-Level Badge
                          ↓
                     Track Completion → Track-Level Credential
                          ↓
                 Tier Requirements → Tier-Based Credential
```

### Step-by-Step Flow

1. **Module Completion**:
   - Developer completes all learning objectives in a module
   - Developer passes the module assessment with a score of 70% or higher
   - Developer submits and passes the required artifacts
   - **Result**: Module-Level Badge is issued

2. **Track Completion**:
   - Developer completes all modules in a certification track
   - Developer passes the track assessment with a score of 70% or higher
   - Developer submits and passes a portfolio review of work products
   - **Result**: Track-Level Credential is issued, referencing all module-level badges

3. **Tier Progression**:
   - **UNVALIDATED Tier**: Developer completes the placement test
   - **WORKING Tier**: Developer earns one or more track-level credentials
   - **PRODUCTION Tier**: Developer earns multiple track-level credentials and completes an architecture defense
   - **Result**: Tier-Based Credential is issued

## Open Badges 3.0 Features

The Palette system leverages the following features of Open Badges 3.0:

### 1. Cryptographic Signatures

Each credential is cryptographically signed using the issuer's private key. This ensures that the credential is tamper-proof and can be verified without contacting the issuer.

### 2. Self-Contained Verification

Unlike Open Badges 2.0, which required the issuer's server to be online for verification, Open Badges 3.0 credentials can be verified offline using the embedded cryptographic proof and the issuer's public key.

### 3. Structured Data

Each credential contains structured data that links the earner, issuer, and achievement. This data is machine-readable and can be used by third-party systems to verify the credential and extract relevant information.

### 4. Alignment to Competency Frameworks

Credentials include alignment to the Palette Skills Framework, which maps each credential to specific skills and competencies. This alignment is used to ensure that credentials are recognized by industry employers and can be used for career advancement.

## Verification Process

### 1. Obtain the Credential

The credential can be obtained from the earner's digital wallet, a public URL, or a baked image (an image with embedded JSON-LD metadata).

### 2. Extract the JSON-LD

The verifier extracts the JSON-LD credential from the badge.

### 3. Resolve the Issuer's DID

The verifier reads the `issuer.id` field (a DID or URL) and resolves it to obtain the DID Document containing the public key.

### 4. Verify the Cryptographic Signature

The verifier reads the `proof` object and runs the signature verification algorithm (EdDSA, ECDSA, or JWT depending on the proof type).

### 5. Check Validity Dates

The verifier checks the `validFrom` and `validUntil` dates to ensure that the credential is still valid.

### 6. Optionally Check Revocation Status

The verifier can check the revocation status by querying the issuer's status list (if published).

## Integration with Certification System

The credential flow is integrated with the Palette certification system as follows:

1. **Assessment**: Developers complete modules and tracks, and their work is assessed using the AI-augmented evaluation system.

2. **Credential Issuance**: Upon successful completion, the system issues the appropriate credentials using the schemas defined in this directory.

3. **Credential Delivery**: Credentials are delivered to the developer's digital wallet or a public URL where they can be accessed and verified.

4. **Credential Display**: Developers can display their credentials on their LinkedIn profile, personal website, or other platforms to showcase their skills and competencies.

## Quality Assurance

The credential flow includes several quality assurance mechanisms:

1. **Integrity Checks**: The system includes integrity checks to ensure that all required fields are present and that the credential is well-formed.

2. **Prerequisite Validation**: The system validates that all prerequisites are met before issuing a credential.

3. **Coverage Reports**: The system generates coverage reports to ensure that all modules and tracks are covered by the credential flow.

4. **Calibration Exemplars**: The system uses calibration exemplars to train the AI evaluator and ensure consistency and fairness in the assessment process.

## Future Enhancements

The following enhancements are planned for future versions of the credential flow:

1. **Automated Revocation**: Implement automated revocation for credentials that are no longer valid or have been revoked by the issuer.

2. **Credential Renewal**: Implement a renewal process for credentials that are about to expire, allowing developers to renew their credentials without retaking the entire assessment.

3. **Credential Stacking**: Implement a stacking mechanism that allows developers to combine multiple credentials to earn higher-level credentials or badges.

4. **Credential Portability**: Enhance the portability of credentials by integrating with additional digital wallet providers and platforms.

## Conclusion

The credential flow in the Palette Developer Enablement & Certification System is designed to be robust, scalable, and interoperable. By leveraging Open Badges 3.0 and W3C Verifiable Credentials, the system ensures that credentials are cryptographically verifiable, portable, and recognized by industry employers. The hierarchical structure of the credential flow allows developers to progress through the certification journey and earn credentials that signify their skills and competencies.

For more information about the Palette certification system, please visit the [Palette Certification Journey](https://palette.dev/certification/journey).