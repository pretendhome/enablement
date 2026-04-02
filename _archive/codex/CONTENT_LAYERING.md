# Content Layering
**Purpose**: Keep the reusable system separate from the instance-specific content.

## Layer 1: Reusable System

This layer is stable.

Examples:
- coaching loop
- scoring model
- session modes
- progression logic
- refinement protocol

## Layer 2: Scenario Content

This layer changes by context.

Examples:
- interview question bank
- onboarding scenarios
- certification tasks
- role-play prompts
- demo tasks

## Layer 3: Reference Material

This layer changes fastest.

Examples:
- product docs
- stats cards
- story banks
- case-study notes
- objection-handling notes

## Rule

Do not bury the reusable system inside a one-off content instance.

If the loop works for multiple contexts, the loop belongs in the reusable layer.

## Example

Interview prep for one company:
- reusable layer: coaching loop
- scenario layer: round types and question tracks
- reference layer: company-specific product notes, story bank, safe stats

## Design Benefit

This separation lets you:
- keep the engine stable
- swap the content
- reuse the same learning UX across multiple domains
