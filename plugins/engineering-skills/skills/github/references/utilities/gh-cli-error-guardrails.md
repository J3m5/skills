# Known `gh` CLI Error Guardrails

Use this reference when composing a command that resembles a known local
failure pattern from `gh` 2.94.0 through 2.97.0 usage.

## Command Shape

| Avoid                                                | Use                                                                                                  |
| ---------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| `gh repo view -R OWNER/REPO --json ...`              | `gh repo view OWNER/REPO --json ...`                                                                 |
| `gh release view -R OWNER/REPO TAG --json ...`       | `gh release view TAG -R OWNER/REPO --json ...`                                                       |
| `gh issue view -R OWNER/REPO NUMBER --json ...`      | `gh issue view NUMBER -R OWNER/REPO --json ...`                                                      |
| `gh pr view -R OWNER/REPO NUMBER --json ...`         | `gh pr view NUMBER -R OWNER/REPO --json ...`                                                         |
| `gh api repos/OWNER/REPO/milestones --state all`     | `gh api repos/OWNER/REPO/milestones -f state=all --paginate`                                         |
| `gh milestone list ...`                              | `gh api repos/OWNER/REPO/milestones -f state=all --paginate`                                         |
| `gh workflow view FILE --json ...`                   | `gh workflow view FILE --yaml` or `gh api repos/OWNER/REPO/actions/workflows/FILE`                   |
| `gh pr diff NUMBER --stat`                           | `gh pr diff NUMBER --name-only` or `gh pr view NUMBER --json changedFiles,additions,deletions,files` |
| `gh repo read-dir PATH --json name,path --jq '.[0]'` | `gh repo read-dir PATH --json name,path --jq '.entries[0]'`                                          |

## Pagination And Truncation

List and search commands cap their results, usually at 30 by default. Set
`--limit N` explicitly whenever completeness or the result cap matters.

`gh issue list` and `gh pr list` do not expose an aggregate `totalCount`
through `--json`. Use GraphQL when an exact total is required; otherwise report
the explicit `--limit` as the cap of the current call.

For raw API calls, use pagination deliberately:

```sh
gh api --paginate repos/OWNER/REPO/issues --jq '.[] | [.number, .title] | @tsv'
gh api --paginate --slurp repos/OWNER/REPO/issues --jq 'add'
```

Use `--slurp` only when downstream processing needs one array containing all
pages.

## Non-Interactive Execution

In non-TTY contexts, `gh` suppresses the pager and ANSI color and fails instead
of prompting for missing required input. Do not set `GH_PAGER` defensively and
do not invent a `--no-pager` flag.

## Untrusted Terminal Content

`gh` 2.97.0 and later filter or reject terminal escape sequences in untrusted
output from commands such as `gh api`, `gh pr diff`, `gh release download -O -`,
and `gh skill preview`. Keep this protection enabled for routine agent
workflows.

Do not add `--allow-escape-sequences` to make a failed command succeed. Use it
only when the user explicitly needs exact raw bytes and the output is captured
for controlled, non-terminal processing. If an older `gh` version must handle
untrusted content, upgrade before rendering that content in a terminal.

## Mutating Commands

If `gh pr create`, `gh issue create`, `gh repo fork`, or another mutating
command prints only `Usage:`, stop and re-check the local manual page before
retrying. Do not layer more flags onto a malformed write command.

For search syntax, JSON field constraints, release selectors, and repository
content behavior, use the dedicated workflow reference instead of adding more
domain rules here.
