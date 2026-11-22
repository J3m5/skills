# `gh --json` Field Guide

Use this reference for stable daily field subsets and non-obvious output
shapes. Let the installed CLI provide exhaustive field inventories.

## Discover And Shape Output

- Run a command with `--json` and no field list to print its available fields.
  This discovery form exits nonzero because no fields were selected.
- Request only the fields needed for the task.
- Prefer `--jq` for filtering without a separate process.
- Use `--template` with `--json` for shaped text, but check `--help`: `-T` is a
  body-template flag on commands such as `gh pr create` and `gh issue create`.
- Re-check fields after a `gh` upgrade or when observed output disagrees with
  this guide.

## Daily Subsets

| Surface                      | Fields                                                                                          |
| ---------------------------- | ----------------------------------------------------------------------------------------------- |
| repository identity          | `name,nameWithOwner,description,url,owner,visibility,isPrivate,isArchived`                      |
| repository branch/activity   | `defaultBranchRef,pushedAt,updatedAt`                                                           |
| repository file metadata     | `name,path,size,type,htmlUrl`                                                                   |
| repository file content      | `name,path,size,type,encoding,content`                                                          |
| repository directory entries | `name,path,type,size`                                                                           |
| issue triage                 | `number,title,state,stateReason,issueType,parent,labels,assignees,author,url,updatedAt`         |
| issue relationships          | `number,title,issueType,parent,subIssues,subIssuesSummary,blockedBy,blocking,url`               |
| PR summary                   | `number,title,state,isDraft,author,baseRefName,headRefName,reviewDecision,mergeStateStatus,url` |
| PR readiness                 | `reviewDecision,reviewRequests,latestReviews,statusCheckRollup,mergeable,mergeStateStatus`      |
| PR change scope              | `changedFiles,additions,deletions,files`                                                        |
| PR checks                    | `name,state,bucket,workflow,link`                                                               |
| workflow run                 | `databaseId,workflowName,displayTitle,status,conclusion,event,headBranch,headSha,url`           |
| release catalog              | `name,tagName,publishedAt,isLatest,isPrerelease`                                                |
| release detail               | `name,tagName,publishedAt,isDraft,isPrerelease,author,body,url,assets`                          |
| issue or PR search           | `repository,number,title,state,author,createdAt,updatedAt,url`                                  |
| code search                  | `repository,path,textMatches,url`                                                               |
| discussion list              | `number,title,answered,category,author,updatedAt,url`                                           |
| discussion detail            | `number,title,body,answered,category,labels,author,state,stateReason,updatedAt,url`             |
| installed skills             | `skillName,sourceURL,scope,version,pinned,path`                                                 |

## Output Shapes And Traps

Repository contents:

- `gh repo read-file --json ...` returns one object; its `content` field is
  base64 encoded, and `--output` is mutually exclusive with `--json`.
- `gh repo read-dir --json ...` returns an object with an `entries` array. Use
  `--jq '.entries'` or `--jq '.entries[]'`.
- `read-file` and `read-dir` are preview commands; re-check help before fragile
  automation.

Issues:

- `subIssues`, `blockedBy`, and `blocking` are
  `{"nodes": [...], "totalCount": N}` objects, not arrays.
- `subIssues.nodes` is capped at 100; `blockedBy.nodes` and `blocking.nodes`
  are capped at 50. Compare node count with `totalCount`.
- Use `projectItems`, not the invalid `projects` field.

Pull requests and Actions:

- `gh search prs` has no `mergedAt`; follow with `gh pr view`.
- `gh pr view` has no `reviewThreads` or `projects`; use reviews/comments,
  `projectItems`, or GraphQL.
- `jobs` exists on `gh run view`, not `gh run list`.
- Do not request `currentBranch` from `gh run list` or `gh pr status`; use
  `headBranch`, `--branch`, or local `git`.
- `steps`, `artifacts`, and `actor` are not `gh run view` JSON fields.

Releases:

- `isLatest` exists on `gh release list`, not `gh release view`.
- `url` exists on `gh release view`, not `gh release list`.
- Drive exact release lookups with `tagName`, not the display `name`.

Repositories:

- `gh repo view` does not expose `readme`, `releases`, `viewerCanPush`, or
  `viewerCanCreateProjects`.
- Use `gh repo read-file`, `latestRelease`, `viewerPermission`, and
  `viewerCanAdminister` instead.
