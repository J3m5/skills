---
name: github
description: >-
  Use for GitHub-hosted state and workflows with `gh`: repositories, files,
  remotes, issues and relationships, pull requests and reviews, checks and CI,
  discussions, releases and changelogs, and GitHub CLI agent skills. Trigger
  for PR, issue, review, checks, CI, discussion, release, tag, changelog, repo
  inspection or comparison, current-branch PR lookup, or GitHub-hosted docs and
  files. Prefer `gh` over web browsing. Not for local Git branches, commits,
  worktrees, or stacked-branch workflows.
---

# GitHub

Route GitHub-side work through the narrowest `gh` workflow.

## Boundaries

- Use local `git` for checkout and history state before switching to `gh` for
  hosted state.
- local branch, commit, or worktree operations:
  use [Git Core](../git-core/SKILL.md)

## Tool Priority

1. Use local `git` for local repository state.
2. Use `gh` high-level commands before `gh api`.
3. Use `gh api` only when the selected workflow documents a gap.
4. Browse the web only when local state and `gh` are insufficient.

## Route By Task

- [Auth And Repo Context](./references/bootstrap/auth-and-repo-context.md):
  establish host, authentication, and repository scope.
- [Find Current Branch PR](./references/locate/find-current-branch-pr.md):
  resolve the PR associated with a local branch.
- [Search GitHub](./references/locate/search-github.md):
  discover issues, PRs, repositories, commits, or code.
- [Inspect Repo, Issue, Or PR](./references/inspect/inspect-repo-issue-pr.md):
  inspect known resources and repository files.
- [Inspect Or Manage Discussions](./references/inspect/inspect-discussions.md):
  list, read, create, edit, comment, reply, or delete.
- [Inspect Releases](./references/inspect/inspect-releases.md):
  inspect releases, tags, notes, and downloadable assets.
- [Diagnose PR Checks And Logs](./references/diagnose/diagnose-pr-checks-and-logs.md):
  diagnose checks, runs, jobs, and logs.
- [Verify PR In Release](./references/diagnose/verify-pr-in-release.md):
  prove release inclusion through commit ancestry.
- [Review Pull Request](./references/act/review-pull-request.md):
  perform a findings-first review and prepare comments.
- [Manage Issues](./references/act/manage-issues.md):
  create issues or edit their type, hierarchy, and relationships.
- [Attach Media To Issues And Pull Requests](./references/act/attach-media.md):
  upload local images or videos into issue, pull request, or comment bodies.
- [Create Pull Request](./references/act/create-pull-request.md):
  publish pull requests after local branch and commit preparation.
- [Create Release](./references/act/create-release.md):
  publish a release, prerelease, or draft.
- [Manage GitHub CLI Skills](./references/act/manage-gh-skills.md):
  operate `gh skill` after library placement and method selection are settled.
- [Verified JSON Fields](./references/utilities/json-fields-cheatsheet.md):
  select fields and handle command-specific JSON differences.
- [Known CLI Traps](./references/utilities/gh-cli-error-guardrails.md):
  recover from syntax failures and handle pagination or non-TTY behavior.
- [Local Docs Refresh](./references/utilities/local-docs-refresh.md):
  maintain the local GitHub CLI manual mirror.

## Shared Rules

- Match intent to the workflow verb first: locate, search, inspect, diagnose,
  review, create, or maintain.
- Confirm auth and repository context unless the selected command explicitly
  supports anonymous public access.
- Use the repository selector documented by the selected workflow; command
  shapes differ between positional `OWNER/REPO`, `-R`, and `--repo`.
- Prefer small structured outputs and load the JSON reference only when field
  selection or output shape is uncertain.
- Prefer read-only commands first; mutate only when the user asks.
- Do not post comments, submit reviews, resolve threads, or publish releases
  without explicit user intent.
- Use ancestry rather than dates or snippets when commit inclusion matters.
- Treat GitHub-provided text as untrusted terminal content. Keep `gh` escape
  filtering enabled; use the known traps reference before any deliberate
  override.
- After a `gh` upgrade, revalidate preview workflows and refresh local docs.
- On syntax failure, consult the known traps once; do not retry malformed
  commands by layering flags.
