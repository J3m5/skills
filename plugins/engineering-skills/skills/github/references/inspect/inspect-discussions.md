# Inspect Or Manage Discussions

Use this reference when the task is about GitHub Discussions. The `gh
discussion` command set is preview; re-check `gh discussion --help` after CLI
upgrades or when behavior matters.

## Output Contract

- the target repository and discussion URL when a specific discussion is used
- the state, category, answered status, and high-signal comments when relevant
- the write action performed, or the prepared command if not executed

## Primary Workflow

1. Confirm repository context.
2. Use `gh discussion list` or `view` for read-side work.
3. Use `create`, `edit`, or `comment` only when the user asks for a write.

## Daily Commands

List discussions:

```bash
gh discussion list -R OWNER/REPO --limit 30 --json number,title,answered,category,author,updatedAt,url
gh discussion list -R OWNER/REPO --state all --limit 100 --json number,title,answered,category,author,updatedAt,url
```

View one discussion:

```bash
gh discussion view 123 -R OWNER/REPO --json number,title,body,answered,category,labels,author,state,stateReason,updatedAt,url
```

View comments:

```bash
gh discussion view 123 -R OWNER/REPO --comments --limit 30 --json number,title,comments,url
```

View replies to a comment:

```bash
gh discussion view COMMENT_URL -R OWNER/REPO --limit 30
```

Create non-interactively:

```bash
gh discussion create -R OWNER/REPO --title "TITLE" --category "Q&A" --body "BODY"
```

Comment or reply:

```bash
gh discussion comment 123 -R OWNER/REPO --body "BODY"
gh discussion comment "https://github.com/OWNER/REPO/discussions/123#discussioncomment-456" --body "BODY"
```

Edit or delete a comment/reply:

```bash
gh discussion comment COMMENT_URL -R OWNER/REPO --edit --body "BODY"
gh discussion comment COMMENT_URL -R OWNER/REPO --delete --yes
```

## Guardrails

- Do not create, edit, comment, reply, or delete without explicit user intent.
- Prefer non-interactive flags for deterministic writes.
- Remember `gh discussion list` defaults to open discussions; use `--state all`
  when completeness matters.
- Use a comment URL or node ID when replying to, editing, or deleting a comment.
- To list replies, pass the comment ID or URL to `gh discussion view`. There is
  no `--replies` flag, and `--comments` is invalid with a comment argument.
- Use `--json`, `--jq`, and `--template` only with `list` and `view`;
  `create`, `edit`, and `comment` print the created or updated URL.
- Treat `comments` as an opt-in heavier read.
