# Review Pull Request

Use this reference when the task is to review a GitHub pull request
end-to-end with reproducible commands and safe comment posting.

## Output Contract

- a findings-first review, or an explicit "no findings"
- each finding tied to current file and line context when possible
- any proposed review comments kept separate from comments actually posted
- residual risk when the review is clean but coverage or rollout risk remains

## Primary Workflow

1. Resolve the PR.

- use an explicit PR URL or number when the user provides one
- if the request is about the current branch PR, resolve it with
  [Find Current Branch PR](../locate/find-current-branch-pr.md)

2. Collect context.

- reuse `gh pr view`, `gh pr diff`, and related `--json` fields for metadata,
  changed files, and diff context
- fetch review-thread state only when needed for unresolved or outdated thread logic

Useful commands:

```bash
gh pr view 123 -R OWNER/REPO --json number,title,state,author,files,reviewDecision,url
gh pr diff 123 -R OWNER/REPO
gh pr diff 123 -R OWNER/REPO --name-only
gh pr view 123 -R OWNER/REPO --json changedFiles,additions,deletions,files
```

3. Review with findings first.

- prioritize bugs, regressions, reliability risks, and missing coverage
- anchor findings to exact file and line context from the current head diff
- if no findings remain, state that explicitly and mention residual test or rollout risk

4. Validate uncertain claims.

- re-check shell or runtime claims with a minimal repro
- re-check GitHub behavior against official docs when the review hinges on API semantics

5. Draft comments before posting.

- draft one comment at a time
- keep comments actionable: issue, impact, and fix direction
- do not post until the user approves the write action

## Approval Policy

Ask for explicit user approval before any external side effect:

- posting or replying to comments
- resolving threads
- submitting review events such as `COMMENT`, `APPROVE`, or `REQUEST_CHANGES`
- posting final PR-thread summary comments

## Posting Mode

Set `github_skill_dir` to the directory containing this skill's `SKILL.md` to
run the bundled helper.

```bash
python3 "$github_skill_dir/scripts/post_inline_comment.py" --repo OWNER/REPO --pr 123 --mode immediate --body 'Comment text' --path path/to/file --line 42 --side RIGHT
```

Supported modes:

- `pending-create`
- `pending-submit`
- `reply`
- `immediate`

### Draft Comment Shape

- issue
- impact
- fix direction

## Escalate Or Switch When

- you only need ordinary PR inspection:
  switch to [Inspect Repo, Issue, Or PR](../inspect/inspect-repo-issue-pr.md)
- you need CI diagnosis before finalizing findings:
  switch to [Diagnose PR Checks And Logs](../diagnose/diagnose-pr-checks-and-logs.md)

## Guardrails

- Do not post comments or submit reviews without explicit user approval.
- Do not collapse a review into a generic PR summary; keep the findings-first structure.
- Do not rely on stale line anchors after the PR head changes; refresh context first.
- Do not use `gh pr diff --stat`; it is not supported. Use `--name-only`,
  `--patch`, or `gh pr view --json changedFiles,additions,deletions,files`.

## Helper

- [Post Inline Comment](../../scripts/post_inline_comment.py)
