# Verify PR In Release

Use this reference when the task is to confirm whether a PR merge commit or
specific commit is included in a published release.

## Output Contract

- the compared PR merge commit and target tag
- the compare status and a plain-language inclusion verdict
- any caveat such as missing `merge_commit_sha` or unresolved tag identity

## Primary Workflow

1. Fetch the PR merge commit:

```bash
gh api repos/OWNER/REPO/pulls/PR_NUMBER --jq '{merge_commit_sha: .merge_commit_sha, merged_at: .merged_at, title: .title}'
```

2. Compare the merge commit to the release tag:

```bash
gh api repos/OWNER/REPO/compare/MERGE_COMMIT_SHA...TAG --jq '{status: .status, ahead_by: .ahead_by, behind_by: .behind_by, total_commits: .total_commits}'
```

## Interpretation

- `status = "identical"`: the tag points exactly at the merge commit
- `status = "ahead"` and `behind_by = 0`: the tag includes the merge commit and has additional commits on top
- `status = "behind"` or `behind_by > 0`: the tag does not include the merge commit

## Example Sequence

```bash
gh api repos/openai/codex/pulls/15378 --jq '{merge_commit_sha: .merge_commit_sha, merged_at: .merged_at, title: .title}'
gh api repos/openai/codex/compare/9a33e5c0a08e67b85ab80125d62bbe359c06cdd3...rust-v0.118.0-alpha.4 --jq '{status: .status, ahead_by: .ahead_by, behind_by: .behind_by, total_commits: .total_commits}'
```

## Escalate Or Switch When

- you first need to resolve the right release tag:
  switch to [Inspect Releases](../inspect/inspect-releases.md)
- you only need release metadata, not ancestry proof:
  switch to [Inspect Releases](../inspect/inspect-releases.md)

## Guardrails

- Do not infer release inclusion from dates alone when commit ancestry matters.
- Prefer `gh api compare` for inclusion questions; it is more reliable than eyeballing release lists.
- If `merge_commit_sha` is null, state that explicitly and stop rather than inventing a comparison target.
