# Audit and Validation Guide

Use this reference for broad reviews, consolidation, and documentation gates. Apply only the checks relevant to the requested scope; a focused edit does not require a repository-wide audit.

## Audit Sequence

1. Identify documentation and executable sources within the requested audit scope.
2. Identify canonical entrypoints and claimed sources of truth.
3. Map material knowledge being moved or removed using the table below.
4. Detect contradictions, semantic duplication, stale status, and implementation mirrors.
5. Check whether observable interfaces remain understandable without reading implementation code.
6. Check navigation, reachability, and automated verification.
7. Classify findings and propose the smallest safe correction.

## Consolidation Map

For broad consolidation, keep a working map before editing affected sources:

| Knowledge | Audience and scope | Existing sources | Executable source | Surviving human reference | Action and reason |
| --------- | ------------------ | ---------------- | ----------------- | ------------------------- | ----------------- |

Useful actions include keep, add, move, consolidate, enforce, generate, archive, and delete. Account for each material fact being removed, including why obsolete or safely inferable knowledge needs no replacement. Compare the map against the final diff; retain or relocate facts whose replacement remains uncertain. Keep this as working material unless the user requests it as a deliverable.

## Navigation and Orphan Documents

Detect reachability from canonical roots; do not define an orphan only as a document with no incoming link.

Choose entrypoints for the audience and owning repository. A local agent workspace may have its own index and Git history; its documents need not be reachable from an application README. Treat independent application checkouts as separate audit scopes unless the request includes them.

1. Inventory Markdown files within the requested scope, tracked or untracked. Include relevant ignored files when explicitly requested or referenced; exclude dependencies and incidental outputs unless they are part of the task.
2. Parse local links and normalize paths, directory indexes, extensions, and fragments.
3. Build a directed graph.
4. Start from explicit roots such as the root README and documentation indexes.
5. Mark reachable documents.
6. Report unreachable documents; when implementing a reachability gate, fail unless a narrowly defined, validated exemption exists.

A mutually linked subgraph can still be orphaned when no canonical root reaches it. Treat redirects, ADR indexes, generated references, and deprecated documents as normal graph nodes and route them explicitly.

## Frontmatter

When frontmatter carries repository policy:

- Validate policy fields against the repository’s schema.
- Reject duplicate keys. Reject unknown keys only where the repository’s schema disallows additional fields.
- Require conditional fields, such as a successor for a superseded document.
- Validate referenced paths or identifiers where practical.
- Avoid dates such as `last_reviewed` unless a workflow consumes them.
- Do not duplicate metadata in a manually maintained index.

## Links and Markdown Structure

Check the links, anchors, and Markdown structures affected by the changes, using existing checks where available. A focused prose edit does not need a full structural audit. Check external URLs separately when deterministic offline CI is required.

Assign one owner to each check to avoid overlapping tools with contradictory behavior.

## Generated References

For generated CLI, API, manifest, or schema references:

- derive from the real built artifact where possible;
- run generation in check mode in CI;
- fail without modifying the worktree when committed output is stale;
- keep explanatory rationale outside generated blocks;
- test defaults, options, and descriptions that generators may omit.

## Executable Examples

Use existing example-validation checks when available and relevant. Otherwise, review examples against their sources and report what remains unverified. Add coverage only when warranted by the task; reading examples directly from Markdown avoids maintaining separate test copies.

Validate changed JSON examples with the real schema or parser when available and relevant. Round-trip serialization when representation or compatibility is part of the changed contract, preferably byte for byte when deterministic output is contractual. Invoke the relevant built or deployed CLI when checking user-visible CLI behavior.

## Information-Loss Review

For material knowledge removed during consolidation, at a level proportional to the change:

- enumerate facts, defaults, limits, examples, and failure behavior;
- locate an equivalent surviving source;
- verify discoverability for the original audience;
- distinguish intentional removal from accidental omission;
- preserve important information in a validated reference rather than restoring a broad design mirror.

Review the final diff as a new contributor, operator, and integration author.

## Finding Priorities

Order findings by:

1. correctness or security risk;
2. loss of an observable contract;
3. contradiction or stale behavior;
4. permanent agent-context cost;
5. maintenance cost;
6. navigation friction;
7. style.

Avoid large rewrites when a targeted move, generator, validator, or routing link solves the problem.

## Validation Report

Report relevant checks and their results, with commands when useful for reproduction. For a broad audit, identify inspected roots, reachability results, generated references and examples checked, material duplication or information removed, and remaining uncertainty. Omit inapplicable categories for focused work.
