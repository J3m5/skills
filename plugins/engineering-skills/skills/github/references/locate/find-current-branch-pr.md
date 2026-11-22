# Find Current Branch PR

Use this reference when the task is about the pull request associated with the
current local branch.

## Output Contract

- resolved PR number, URL, and state, or an explicit "no associated PR" result
- whether resolution came from the current branch or an explicit branch name
- the next workflow to use once the PR is known

## Primary Workflow

Run from inside the repository:

```bash
gh pr view --json number,title,url,state
```

If the branch name must be explicit:

```bash
gh pr view BRANCH_NAME -R OWNER/REPO --json number,title,url,state
```

## Interpretation

- if the command returns a PR, use that PR number or URL for the next workflow
- if the user already gave a PR number or URL, prefer the explicit user input
- if no PR resolves, treat that as a legitimate outcome rather than a GitHub failure

## Escalate Or Switch When

- you need to inspect the PR content:
  switch to [Inspect Repo, Issue, Or PR](../inspect/inspect-repo-issue-pr.md)
- you need CI checks or logs for that PR:
  switch to [Diagnose PR Checks And Logs](../diagnose/diagnose-pr-checks-and-logs.md)
- auth or repo context is unclear:
  switch to [Auth And Repo Context](../bootstrap/auth-and-repo-context.md)

## Guardrails

- Do not use this as a broad PR discovery workflow; it is specifically for the
  current local branch.
- Do not assume the absence of a PR means auth is broken; the branch may simply
  not have an associated PR.
