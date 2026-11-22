# Inspect Repo, Issue, Or PR

Use this reference for day-to-day GitHub inspection of repositories, issues,
and pull requests through high-level `gh` commands.

## Output Contract

- the exact resource inspected, with its canonical URL
- the high-signal state summary that answers the user request
- only the heavier fields that were actually needed
- the next workflow to switch to if the task turns into review or CI diagnosis

## Primary Workflow

Start with the narrowest matching high-level command:

- repository: `gh repo view`
- issue: `gh issue view`
- PR: `gh pr view`

Use small verified `--json` field subsets first. Reach for larger objects only
when the task clearly requires them.

For the full verified field inventory for the common commands, use:
[Verified `gh --json` Field Cheat Sheet](../utilities/json-fields-cheatsheet.md)

## Daily Commands

Repository summary:

```bash
gh repo view OWNER/REPO --json nameWithOwner,description,url,visibility,isPrivate,isArchived,defaultBranchRef
```

Issue summary:

```bash
gh issue view 123 -R OWNER/REPO --json number,title,state,stateReason,issueType,parent,labels,assignees,author,url,updatedAt
```

Issue list filtered by type:

```bash
gh issue list -R OWNER/REPO --type Bug --limit 30 --json number,title,state,issueType,labels,assignees,author,url,updatedAt
```

Issue detail:

```bash
gh issue view 123 -R OWNER/REPO --json number,title,body,state,stateReason,issueType,parent,subIssuesSummary,blockedBy,blocking,labels,assignees,milestone,comments,closedAt,url
```

Issue hierarchy or relationship detail:

```bash
gh issue view 123 -R OWNER/REPO --json number,title,issueType,parent,subIssues,subIssuesSummary,blockedBy,blocking,url
```

PR summary:

```bash
gh pr view 123 -R OWNER/REPO --json number,title,state,isDraft,author,baseRefName,headRefName,reviewDecision,mergeStateStatus,url
```

PR readiness:

```bash
gh pr view 123 -R OWNER/REPO --json reviewDecision,reviewRequests,latestReviews,statusCheckRollup,mergeable,mergeStateStatus,url
```

PR file/change scope:

```bash
gh pr view 123 -R OWNER/REPO --json changedFiles,additions,deletions,files
```

Repository README content:

```bash
gh repo read-file README.md --repo OWNER/REPO
gh repo read-file README.md --repo OWNER/REPO --ref TAG_OR_SHA --json name,path,size,type,htmlUrl
```

Repository file content:

```bash
gh repo read-file PATH --repo OWNER/REPO
gh repo read-file PATH --repo OWNER/REPO --ref BRANCH_OR_TAG_OR_SHA
gh repo read-file PATH --repo OWNER/REPO --output ./PATH
```

Repository directory listing:

```bash
gh repo read-dir --repo OWNER/REPO
gh repo read-dir PATH --repo OWNER/REPO --ref BRANCH_OR_TAG_OR_SHA
gh repo read-dir PATH --repo OWNER/REPO --json name,path,type,size --jq '.entries'
```

Repository release snapshot:

```bash
gh repo view OWNER/REPO --json latestRelease
gh release list -R OWNER/REPO --limit 20 --json name,tagName,isLatest,isPrerelease,publishedAt
```

## Escalate Or Switch When

- you need to find the PR first:
  switch to [Find Current Branch PR](../locate/find-current-branch-pr.md)
- you need to search before inspection:
  switch to [Search GitHub](../locate/search-github.md)
- you need GitHub Discussions:
  switch to [Inspect Or Manage Discussions](./inspect-discussions.md)
- you need CI checks, workflow runs, or logs:
  switch to [Diagnose PR Checks And Logs](../diagnose/diagnose-pr-checks-and-logs.md)
- you are doing a findings-first code review:
  switch to [Review Pull Request](../act/review-pull-request.md)

## Guardrails

- Prefer `gh repo view`, `gh issue view`, and `gh pr view` before `gh api`.
- Remember `gh repo view` takes `OWNER/REPO` as a positional argument; it does
  not support `-R`.
- Do not dump very large JSON payloads when a smaller field subset answers the question.
- Treat `files`, `comments`, and `statusCheckRollup` as opt-in heavier reads, not defaults.
- Treat `subIssues`, `blockedBy`, and `blocking` as opt-in relationship reads
  unless hierarchy or dependency state is part of the request.
- Treat those relationship fields as `{nodes,totalCount}` objects, not arrays.
  `subIssues.nodes` is capped at 100 and `blockedBy.nodes` or `blocking.nodes`
  at 50; compare node count with `totalCount` before claiming completeness.
- Prefer `gh repo read-file` and `gh repo read-dir` for repository contents
  when available; they are preview commands, so fall back to the contents API
  when the local CLI lacks them or they do not expose the needed behavior.
- In non-TTY contexts, raw `gh repo read-file` output is pipe-friendly bytes.
  Binary output is refused on a TTY, and files containing terminal escape
  sequences require `--allow-escape-sequences`.
- Decode `gh repo read-file --json content` from base64 before inspection.
  Do not combine `--json` with `--output`; use `--clobber` explicitly when an
  existing destination may be overwritten.
- Remember `gh repo read-dir --json ...` returns an object with an `entries`
  array; use `--jq '.entries'` or `--jq '.entries[]'`, not top-level array
  indexing.
- If falling back to `repos/.../contents/...` file reads, decode `.content`
  immediately with `base64 -d` before inspecting or quoting the file; the REST
  contents payload stores file bytes as base64.
- For permissions, prefer `viewerPermission` and `viewerCanAdminister`; do not
  assume GraphQL fields such as `viewerCanPush` are exposed by `gh repo view`.
