# Auth And Repo Context

Use this reference to establish `gh` auth, host context, and explicit
repository targeting before a deeper GitHub workflow.

## Output Contract

- current auth state, anonymous-access mode, or explicit blocker if login is required
- resolved host and repository scope
- exact scoping pattern to use next: `-R` or `--repo`
- the next workflow to enter once context is stable

## Primary Workflow

1. Check whether the selected command explicitly supports anonymous public
   access. For `gh` 2.96.0 and newer, allow `gh release download` to proceed
   against a public repository without login.
2. Otherwise, confirm auth:

```bash
gh auth status
```

3. If the command requires auth and auth is missing or expired, stop and ask
   the user to run:

```bash
gh auth login
```

4. Resolve repo context with the narrowest correct pattern:

- use local repo context when already inside the target checkout
- use `gh repo view [HOST/]OWNER/REPO` for repository inspection
- use `-R [HOST/]OWNER/REPO` for resource commands such as `gh issue view`,
  `gh pr view`, `gh run view`, and `gh release view`
- use `--repo OWNER/REPO` for `gh search ...`

## Daily Commands

Repository identity:

```bash
gh repo view OWNER/REPO --json nameWithOwner,url,description,visibility
```

Issue identity:

```bash
gh issue view 123 -R OWNER/REPO --json number,title,state,url
```

PR identity:

```bash
gh pr view 123 -R OWNER/REPO --json number,title,state,url
```

## Escalate Or Switch When

- you specifically need to find the PR for the current local branch:
  switch to [Find Current Branch PR](../locate/find-current-branch-pr.md)
- you need to inspect repo, issue, or PR details:
  switch to [Inspect Repo, Issue, Or PR](../inspect/inspect-repo-issue-pr.md)
- you need search rather than direct lookup:
  switch to [Search GitHub](../locate/search-github.md)

## Guardrails

- Do not require login for a command with documented anonymous public access.
- Confirm auth before assuming a CLI or API behavior problem for all other
  commands.
- Require auth for private repositories and authenticated-only resources.
- Prefer explicit repo scoping over guessing when outside the intended checkout.
- Treat wrong-host auth and wrong-repo context as first-class failure modes.
