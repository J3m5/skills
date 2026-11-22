# Manage Issues

Use this reference when the user explicitly asks to create an issue or change
its type, hierarchy, or dependency relationships.

## Output Contract

- the target repository and affected issue URLs or numbers
- the created or edited metadata and any requested fields that were skipped
- the prepared command when execution stops before publication

## Shared Rules

- Treat creation and edits as external side effects.
- Validate repository context with
  [Auth And Repo Context](../bootstrap/auth-and-repo-context.md).
- Prefer explicit non-interactive flags when the required content is known.

## Create An Issue

1. Confirm the target repository.
2. Draft the title and body.
3. Create the issue with explicit metadata.

```bash
gh issue create -R OWNER/REPO --title "TITLE" --body "BODY"
gh issue create -R OWNER/REPO --title "TITLE" --body-file ISSUE_BODY.md
gh issue create -R OWNER/REPO --title "TITLE" --body "BODY" --label bug --assignee "@me"
gh issue create -R OWNER/REPO --title "TITLE" --body "BODY" --type Bug --parent 100
gh issue create -R OWNER/REPO --title "TITLE" --body "BODY" --blocked-by 200,201 --blocking 300
```

## Edit Type And Relationships

```bash
gh issue edit 123 -R OWNER/REPO --type Bug
gh issue edit 123 -R OWNER/REPO --parent 100
gh issue edit 100 -R OWNER/REPO --add-sub-issue 123,124
gh issue edit 123 -R OWNER/REPO --add-blocked-by 200 --add-blocking 300,301
gh issue edit 123 -R OWNER/REPO --remove-type --remove-parent
gh issue edit 100 -R OWNER/REPO --remove-sub-issue 123
gh issue edit 123 -R OWNER/REPO --remove-blocked-by 200 --remove-blocking 300
```

## Attach Images Or Videos

For `gh` 2.99.0 and newer, use
[Attach Media To Issues And Pull Requests](./attach-media.md) when creating or
editing an issue, or when adding media to an issue comment.

Relationship and parent references may be issue numbers or URLs. Cross-repo
URLs must target the same GitHub host. Do not use `--add-sub-issue` while
editing more than one issue in the same command.

## Escalate Or Switch When

- inspection is needed before mutation:
  use [Inspect Repo, Issue, Or PR](../inspect/inspect-repo-issue-pr.md)
- the task is to create a pull request:
  use [Create Pull Request](./create-pull-request.md)
- the task is to manage a discussion:
  use [Inspect Or Manage Discussions](../inspect/inspect-discussions.md)

## Guardrails

- Do not create or edit an issue without explicit user intent.
- Use `--template` explicitly when a repository issue template is required.
- Project assignment may require `gh auth refresh -s project`.
- Issue types and sub-issues require GitHub.com or GHES 3.17+; issue
  relationships require GHES 3.19+.
- If a mutating command prints only `Usage:`, verify local help before retrying.
