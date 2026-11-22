# Search GitHub

Use this reference when the task needs discovery through `gh search` across
pull requests, issues, commits, repositories, or code.

## Output Contract

- a short ranked result set with repository, identifier, title or path, and URL
- the exact search scope and terms that produced the result
- one recommended follow-up target, or an explicit "no strong match"

## Search Rules

- prefer dedicated flags such as `--repo`, `--author`, `--app`, `--label`, and
  `--state` for routine searches
- when full GitHub search syntax is needed, pass each qualifier as a separate
  unquoted argument; quote only multi-word free text
- never quote the whole qualifier expression because `gh` treats it as one
  keyword and can return `Invalid search query`
- prefer one or two concrete terms first
- use `--app SLUG` for GitHub App authors such as Dependabot; `--author
  dependabot` does not match app-authored items
- use `--state open` or `--state closed`; omit `--state` for both states
- use `gh search prs --merged`, not `--state merged`
- narrow with a follow-up inspection command instead of repeatedly mutating an
  over-constrained query

## Example Intents

- "find PRs about flaky CI in this repo"
- "search the issue that mentions `app-server`"
- "find where `post_inline_comment.py` is referenced"

## Daily Commands

PR search:

```bash
gh search prs --repo OWNER/REPO "term" --limit 20 --json repository,number,title,state,author,url
```

Issue search:

```bash
gh search issues --repo OWNER/REPO "term" --limit 20 --json repository,number,title,state,author,url
```

Code search:

```bash
gh search code --repo OWNER/REPO "symbol_or_key" --limit 20 --json repository,path,url
```

Search for a token that starts with `-`:

```bash
gh search code --repo OWNER/REPO --limit 20 -- "-TERM"
```

Commit search:

```bash
gh search commits --repo OWNER/REPO "term" --limit 20 --json repository,sha,url
```

Merged PR search:

```bash
gh search prs --repo OWNER/REPO "term" --merged --limit 20 --json repository,number,title,state,author,url
```

Full search syntax:

```bash
gh search issues repo:OWNER/REPO is:open label:bug "multi-word phrase" --limit 20 --json repository,number,title,state,url
```

PRs authored by a GitHub App:

```bash
gh search prs --repo OWNER/REPO --app dependabot --limit 20 --json repository,number,title,state,author,url
```

Follow-up PR inspection:

```bash
gh pr view NUMBER -R OWNER/REPO --json number,title,state,author,url
```

Follow-up issue inspection:

```bash
gh issue view NUMBER -R OWNER/REPO --json number,title,state,author,url
```

## API Fallback

Use `gh api` only when `gh search` does not expose the needed query or
aggregation cleanly.

Example:

```bash
gh api -X GET search/issues -f q='repo:OWNER/REPO is:pr term' -F per_page=20 --jq '.items[] | [.number, .title, .html_url] | @tsv'
```

## Escalate Or Switch When

- you already have a concrete issue or PR number:
  switch to [Inspect Repo, Issue, Or PR](../inspect/inspect-repo-issue-pr.md)
- you need checks or logs for a PR result:
  switch to [Diagnose PR Checks And Logs](../diagnose/diagnose-pr-checks-and-logs.md)
- repo or auth context is not stable:
  switch to [Auth And Repo Context](../bootstrap/auth-and-repo-context.md)

## Guardrails

- Do not use search when the user already supplied a concrete URL, PR number, issue number, or repository.
- Do not keep retrying malformed or over-constrained queries; simplify first.
- Do not invent a `--search` flag for `gh search prs`; the search text is the
  positional query argument.
- `gh search prs` does not expose `mergedAt`; follow a candidate with
  `gh pr view NUMBER -R OWNER/REPO --json mergedAt` when the exact merge time
  matters.
- Do not use `--path` with `gh search code`; use `--filename`, `--extension`,
  `--match file|path`, or the API fallback.
- For code search, inspect the result path next instead of endlessly tuning the query.
