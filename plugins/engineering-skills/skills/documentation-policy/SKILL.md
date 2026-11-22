---
name: documentation-policy
description: Choose canonical sources for repository documentation, preserve knowledge during consolidation, and decide what belongs in AGENTS.md.
---

# Documentation Policy

Preserve important knowledge while reducing duplication, maintenance cost, and automatically loaded agent context. Prefer executable enforcement for exact constraints and a discoverable human reference for interfaces people author, inspect, or operate.

## Scope and Execution

Follow the user's requested scope, audience, format, and repository conventions. User instructions take precedence over this skill's defaults.

- For a focused edit, inspect the affected source and its dependencies, make the correction, and validate it. A full inventory or written knowledge map is unnecessary when no material knowledge is moved or removed.
- For an audit, report evidence-backed findings and the smallest useful corrections. For a requested update, carry the changes through validation; do not stop at a proposal.
- Resolve routine placement choices from repository evidence. Ask only when an unresolved choice materially affects correctness, scope, or authorization; continue independent authorized work meanwhile.
- Treat adding enforcement, generators, or a new documentation structure as scope decisions. Recommend missing mechanisms when appropriate; implement them when needed for the requested outcome and authorized by its scope.

## Decide Whether to Write a File

Use the conversation for explanations and routine results unless the user requests a saved deliverable or future reuse, handoff, or an established workflow needs a durable record. Placement instructions alone do not require creating one.

When persistent documentation is useful:

- Update the relevant existing reference before creating another; separate reports for each step usually add maintenance without new knowledge.
- Choose the format for its reader or identified consumer. Do not duplicate prose in machine-readable reports without a concrete use.
- Keep raw inventories, logs, and consolidation maps as working material unless they are deliverables.

Keep factual references and practical guides focused on the knowledge needed to understand or use their subject. Do not mix them with task history, progress reports, investigation narratives, or raw diagnostics. Preserve useful conclusions and non-obvious constraints, not every observation or execution step. Apply this distinction regardless of file location, source, or Git tracking.

Keep necessary source citations and enduring rationale with the claims they support. Incorporate diagnostic conclusions when they explain a relevant constraint or failure mode. Preserve supporting records elsewhere only when they have an identified use. This separates reading purposes; it does not prescribe file categories, one file per category, or additional deliverables.

Establish the owning repository and intended audience before choosing a location. Git tracking, sharing, and retention are separate questions: a local agent workspace can have its own tracked history without belonging to the application's shared documentation. A `.agents/` directory does not by itself imply ignored or temporary content; use the placement reference for repository boundaries and local workspace cases.

## Apply Progressive Disclosure

Apply progressive disclosure when writing and organizing documentation for people and agents. Lead with purpose and essential information; introduce conditional procedures and deeper explanations where readers need them. Keep prerequisites and constraints visible beside the instructions they qualify.

Keep frequently read entrypoints concise, especially `AGENTS.md` and the references it routes to. Use descriptive headings and contextual links that explain when more detail is useful. Direct readers to the narrowest relevant section or canonical reference; read only what the task requires rather than loading every linked document.

Choose sections within a document or separate references according to actual reading needs. Do not impose a hierarchy, split a small coherent guide, or create files or navigation layers without a concrete benefit. Link to canonical details instead of duplicating them in each entrypoint.

## Read as Needed

- [Placement and surfaces](references/placement-and-surfaces.md): repository ownership, shared versus local agent documentation, and choosing the appropriate surface.
- [Audit and validation](references/audit-and-validation.md): broad reviews, consolidation maps, orphan detection, and documentation gates.
- [Observable contracts](references/observable-contracts.md): changing or removing examples or exact descriptions of configuration, persistent formats, CLI interfaces, APIs, or generated artifacts.

## Choose the Canonical Source

Start from the knowledge and its audience. Inspect the relevant implementation, schemas, tests, configuration, examples, and existing documentation to establish current behavior. Distinguish this evidence from validated requirements and decisions, proposed changes, and historical rationale. Report discrepancies rather than silently aligning the intended contract with the implementation; search for semantic contradictions as well as duplicate wording.

Choose the narrowest source that preserves the knowledge for its intended audience. Use the [placement table](references/placement-and-surfaces.md#source-order) when choosing among possible locations.

Keep one canonical source for each fact or rule; use contextual links for secondary mentions. An executable definition and its validated explanation serve different audiences and are not redundant copies. Avoid independently maintained exact specifications and prose inventories that merely mirror code, manifests, or directories.

## Preserve Information During Consolidation

Before removing or moving material knowledge, identify its surviving source or establish that it is obsolete, safely inferable by its audience, or intentionally unsupported. A short working note is sufficient for a small change; use the map in the audit reference for broad consolidation.

Preserve non-obvious rationale, invariants, defaults, limits, failure behavior, and useful examples. Verify that the surviving source remains discoverable, and update indexes and incoming links after moves. Keep examples beside the interface they explain.

A schema or test alone cannot replace a usable reference for configuration authors, operators, or integrators. Existing CLI help, examples, or a relevant README may already provide that reference. Keep needed constraints visible and validate affected examples with the real parser, schema, serializer, generator, or CLI when available. If a replacement is uncertain, retain the affected knowledge while completing other supported changes.

## AGENTS.md Admission

Admit a statement only when it changes agent decisions, cannot be inferred reliably and cheaply, applies broadly within its scope or has a severe omission cost, justifies automatic loading, and has an identifiable canonical source or verification path.

Keep reusable procedures in skills and detailed domain knowledge in scoped documentation. Add a routing link only when needed. Nested instructions should contain narrower rules or overrides, not inherited duplicates.

When reviewing agent instructions, distinguish requirements from recommendations. Look for conflicting rules, unconditional approval pauses, audit or testing demands disproportionate to ordinary tasks, and examples accidentally promoted to universal policy. Preserve actual operational constraints and authorization boundaries.

## Validate and Report

Run required repository checks and validation appropriate to the changed surfaces: links and anchors after moves, relevant frontmatter schemas, generated-reference freshness, and affected examples. For broad consolidation, also check reachability from canonical entrypoints and compare preserved knowledge before and after. Use the audit reference for detailed methods.

Add a validator only when the requested work needs an invariant that existing mechanisms cannot own. Once relevant checks pass, broaden or repeat them only for new changes, failures, or unresolved concerns. Report unavailable checks precisely rather than implying they passed.

For reviews, lead with findings ordered by impact, with evidence and a concrete correction. For updates, state what changed, why, relevant validation, and remaining limitations. Mention canonical-source moves, intentionally removed knowledge, and changes to permanent `AGENTS.md` context when applicable. Keep the report proportional to the task and use the user's requested format.
