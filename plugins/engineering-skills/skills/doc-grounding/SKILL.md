---
name: doc-grounding
description: Consult primary documentation when implementing or diagnosing behavior that depends on an API, library, framework, or tool contract. Retrieve missing sources and create or refresh local documentation mirrors when useful or requested.
---

# Doc Grounding

Use the relevant documentation to establish the contracts that guide the requested
implementation or diagnosis. A request to acquire documentation can also start
directly with the mirror workflow below.

## Consult the relevant sources

Before introducing or changing the use of an external API, library, framework,
or tool, read the documentation that governs the behavior being changed. Focus
on material questions such as configuration semantics, lifecycle, supported
options, and compatibility. Scale the reading to the uncertainty and impact;
a mechanical edit need not trigger a new documentation search.

- Start with the repository's documentation entrypoints and existing local or
  shared references. Check a mirror's manifest and coverage before relying on it.
- Establish the effective version when it can change the answer. Use
  `version-first-grounding` when available; otherwise check the relevant runtime,
  lockfile, installed metadata, or deployed revision and select matching sources.
- Prefer the existing mirror when it covers the question and matches the target.
  Otherwise retrieve the relevant official documentation, tagged source, or
  release notes through the available connector or native retrieval tools.
  Read the actual page or source, rather than relying on search snippets.
- Search for the specific contract and read enough surrounding context to retain
  its conditions, examples, and version markers. Follow links or source includes
  when the answer depends on them.

Local availability and a recent fetch date do not prove version alignment.
Distinguish exact matches from documentation covering only a major or minor line.
When matching documentation is unavailable, use installed types or source and a
focused behavior check where feasible; state the remaining uncertainty instead
of treating the latest documentation as proof for an older target.

## Connect documentation to the change

Find where the documented contract applies in the project: configuration,
entrypoints, wrappers, adapters, and the tests that observe that behavior. Account
for local integration choices before copying an upstream example.

If documentation and observed behavior disagree, investigate the version, local
wrappers, and the smallest relevant reproduction. Preserve the distinction
between intended upstream behavior and the current local behavior.

Apply only what the task needs. Report the sources and version limits that
support material decisions as part of the result. A separate documentation map
or a repository documentation change is useful only when the task calls for it.

## Acquire or refresh a mirror when needed

Mirror documentation when explicitly requested, or when repeated use, offline
access, a substantial cross-page investigation, or reproducibility warrants a
durable copy. Missing local documentation alone does not require a mirror.
Choose the smallest useful scope, then resume the implementation or diagnosis
after acquiring it. For a mirror-only request, finish when the mirror is ready.

Load only the references needed for the acquisition:

- Follow the project's instructions for mirror storage when available.
  To choose a location and record provenance, see
  [mirror-storage.md](references/mirror-storage.md).
- Export a new HTTP, npm, GitHub, or local Markdown source:
  [mdzilla-export.md](references/mdzilla-export.md).
- Preserve Git-backed sources when the exporter is unsuitable:
  [git-import.md](references/git-import.md).
- Refresh an existing managed snapshot or retain multiple versions:
  [snapshot-lifecycle.md](references/snapshot-lifecycle.md).

Verify representative pages, scope, formatting, and source/version identity
before calling a mirror usable. Keep upstream content separate from local
guidance, and preserve intentionally retained versions during replacement.
