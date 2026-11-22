# Create Pull Request

Use this reference when the user explicitly asks to publish a pull request
after local branch and commit preparation is complete.

## Output Contract

- the target repository, base/head branches, and created PR URL and number
- the title/body source and any labels or reviewers applied
- the prepared command when execution stops before publication

## Shared Rules

- Treat PR creation and forking as external side effects.
- Use `git-core` for local branch and commit preparation.
- Validate repository context with
  [Auth And Repo Context](../bootstrap/auth-and-repo-context.md).

## Primary Workflow

1. Confirm that the branch and commits are prepared and pushed as intended.
2. Confirm the target repository and base branch.
3. Choose explicit or commit-derived title and body content.
4. Create the PR with deterministic flags.

```bash
gh pr create -R OWNER/REPO --base main --title "TITLE" --body "BODY"
gh pr create -R OWNER/REPO --base main --title "TITLE" --body "BODY" --reviewer user1 --label enhancement
gh pr create -R OWNER/REPO --base main --fill
gh pr create -R OWNER/REPO --base main --head USER:BRANCH --title "TITLE" --body "BODY"
```

When the PR body needs local images or videos and `gh` is 2.99.0 or newer,
follow [Attach Media To Issues And Pull Requests](./attach-media.md).

## Fork A Repository

Fork only when the user asks or the approved PR workflow requires it:

```bash
gh repo fork OWNER/REPO --clone=false
gh repo fork --remote=false
```

Use `--clone=false` for a named repository when no clone is wanted. Use
`--remote=false` for the current repository when no remote should be added.

## Escalate Or Switch When

- local branch or commit preparation is missing:
  use [Git Core](../../../git-core/SKILL.md)
- the task is to inspect or review an existing PR:
  use [Review Pull Request](./review-pull-request.md) or
  [Inspect Repo, Issue, Or PR](../inspect/inspect-repo-issue-pr.md)
- the task is to create or edit an issue:
  use [Manage Issues](./manage-issues.md)

## Guardrails

- Do not create a PR or fork without explicit user intent.
- `gh pr create` may push or fork when the branch is not fully published; use
  explicit `--head` when implicit behavior is unacceptable.
- Prefer explicit `--title` and `--body` unless commit-derived text is wanted.
- Make the base branch explicit when it matters.
- Link issues in the body with `Fixes #123` or `Closes #123` when requested.
- If a mutating command prints only `Usage:`, verify local help before retrying.
