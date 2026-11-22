---
name: glab
description: Use GitLab CLI (glab) for GitLab reads and writes, including merge requests, issues, discussions, and CI. Read before any glab or GitLab API command; prefer glab over raw API calls.
metadata:
  source-project: gitlab-org/cli
  source-path: internal/commands/skills/bundled/assets/glab
  source-commit: 206ebab4fc3fa590b720d2885ac890c195c46650
  local-adaptation: Progressive routing; upstream guidance preserved in references.
---

# GitLab CLI (glab)

Use the installed `glab` for GitLab operations. Inspect its version and use
`glab <command> --help` for operation-specific flags. Keep explicit repository
context and prefer JSON for parsed output.

## Select the operation

Read only the reference or section needed for the current operation:

- Issue/MR lookup, creation, updates, or CI: [commands](references/commands.md).
- Authorized comments, replies, resolution, or reopening:
  [comments and discussions](references/comments.md).
- Operations without a CLI wrapper, API fields, JSON, or uploads:
  [API calls](references/api.md).
- A command error or unfamiliar argument semantics:
  the matching item in [common mistakes](references/pitfalls.md).
- Updating this adaptation or contributing a correction:
  [local maintenance](references/maintenance.md).

Avoid interactive editors and terminal UIs in agent execution. For CI, use
`glab ci get` or `glab ci status`; `glab ci trace` streams until completion.
For authoring or validating `.gitlab-ci.yml` locally, use the GitLab CI skill
when available.
For mutation commands, apply the human authorization for that action and target;
reading a related item does not authorize publication, push, or merge.
