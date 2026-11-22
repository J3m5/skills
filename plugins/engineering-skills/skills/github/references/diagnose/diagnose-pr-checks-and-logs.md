# Diagnose PR Checks And Logs

Use this reference when the task is to understand failing or pending GitHub PR
checks, workflow runs, jobs, or logs.

## Output Contract

- the failing or pending check name, or an explicit all-clear result
- the run URL and provider when available
- a concise failure snippet, or an explicit note that logs are unavailable
- a confidence note when the run is pending, missing, or truncated

## Primary Workflow

Run the bundled helper from the target repository. Set `github_skill_dir` to
the directory containing this skill's `SKILL.md`.

```bash
python3 "$github_skill_dir/scripts/inspect_pr_checks.py" \
  --repo . --pr 123 --max-runs 10 --analysis-timeout 60
```

The helper prints the check inventory and per-run progress to `stderr` before
fetching logs. It analyzes each distinct GitHub Actions run once, keeps all
failing and pending checks in the result, and marks work skipped by either
limit. When a full run log is too large for `gh`, it falls back to one
representative non-aggregator job for that run. Use `0` to disable `--max-runs`
or `--analysis-timeout` deliberately.

Machine-friendly output:

```bash
python3 "$github_skill_dir/scripts/inspect_pr_checks.py" \
  --repo . --pr 123 --json
```

JSON stays on `stdout`; progress stays on `stderr`.

## Manual Fallback

Inspect checks:

```bash
gh pr checks 123 -R OWNER/REPO --json name,state,bucket,workflow,link,startedAt,completedAt
```

Inspect a run:

```bash
gh run view RUN_ID -R OWNER/REPO --json databaseId,workflowName,displayTitle,status,conclusion,event,headBranch,headSha,url
```

Inspect run jobs:

```bash
gh run view RUN_ID -R OWNER/REPO --json databaseId,workflowName,jobs,status,conclusion,url
```

Inspect logs:

```bash
gh run view RUN_ID -R OWNER/REPO --log
gh run view RUN_ID -R OWNER/REPO --job JOB_ID --log
```

List runs for a branch:

```bash
gh run list -R OWNER/REPO --branch BRANCH --json databaseId,workflowName,displayTitle,status,conclusion,headBranch,headSha,url
```

List run artifacts:

```bash
gh api repos/OWNER/REPO/actions/runs/RUN_ID/artifacts --jq '.artifacts[] | [.name, .archive_download_url] | @tsv'
```

Workflow metadata:

```bash
gh workflow list -R OWNER/REPO
gh workflow view WORKFLOW_FILE -R OWNER/REPO --yaml
gh api repos/OWNER/REPO/actions/workflows/WORKFLOW_FILE
```

## External Providers

If a check points to a non-GitHub Actions provider, report the external URL and
stop short of pretending GitHub can provide native run logs for it.

## Escalate Or Switch When

- you still need to resolve the PR for the current branch:
  switch to [Find Current Branch PR](../locate/find-current-branch-pr.md)
- you only need ordinary PR metadata, not CI diagnosis:
  switch to [Inspect Repo, Issue, Or PR](../inspect/inspect-repo-issue-pr.md)
- auth or repo context is unstable:
  switch to [Auth And Repo Context](../bootstrap/auth-and-repo-context.md)

## Guardrails

- Do not claim certainty when logs are missing, truncated, or pending.
- Do not report an all-clear while checks are pending.
- Summarize the root cause first before proposing a fix.
- Prefer the helper script first; use manual `gh` fallbacks when an analysis is
  marked skipped, times out, or does not surface the required detail cleanly.
- Do not request `steps`, `artifacts`, or `actor` as `gh run view --json`
  fields; use `jobs`, logs, or the Actions API.
- Do not request `currentBranch` from `gh run list`; use `headBranch` or
  `--branch`.
- Do not use `gh workflow view --json`; it supports summary output,
  `--yaml`, and `--web`.
