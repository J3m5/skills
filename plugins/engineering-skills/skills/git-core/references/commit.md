# Commits

## Select what will be recorded

Derive scope from the request and inspect status, staged content and relevant
unstaged changes. Named files bound the scope; a request to commit staged work
means the index snapshot, not every current version of those files. Existing
staging does not authorize unrelated content.

When the index matches the request, commit it without restaging partially staged
files. For additional authorized content use explicit paths or selected hunks;
adding a whole file replaces its staged content with the worktree version.
Quote arguments and use `--` before paths. For exact filenames that contain Git
pathspec syntax, use `git --literal-pathspecs ...`; NUL-delimited pathspec files
are useful for generated lists. Avoid blanket add/commit-all as a default.

Ordinary `git commit` records the whole index. When unrelated staged work exists,
do not include or unstage it merely to make a scoped commit convenient. For a
request authorizing the complete worktree contents of named files, Git's
`commit --only -- <paths>` can record those files while preserving unrelated
staging. Review those paths against HEAD first. It also includes their unstaged
edits, so it is unsuitable for a staged-only or partial-hunk request. For a
remaining overlap or partial-selection conflict, preserve the index and clarify
which content belongs in the commit.

For an authorized conflict resolution, Git 2.56's `git add --resolved -- <paths>`
stages only matching unmerged paths, leaving unrelated changes unstaged. If any
selected path still has conflict markers, none are staged. Marker-free binary
files and deletions are also accepted, so review the actual resolution; absence
of markers does not prove correctness. It cannot be combined with -u or -A and
does not authorize continuing an operation outside the request.

Review the content that the chosen mode will actually record: staged diff for
an index commit, or the complete selected file changes for --only. Use diff
--check for applicable whitespace errors and inspect meaningful changes, rather
than requiring a fixed sequence of redundant summaries. An empty selection does
not justify --allow-empty unless an empty commit was requested. If detached HEAD
would make the result hard to retain, use the requested branch workflow or
clarify ownership before committing; do not invent a history rewrite.

## Follow the applicable message policy

Use the explicit user message/format and documented repository requirements,
including signing and trailers. A repository's own message convention takes
precedence over this skill's default; that difference alone needs no approval.
Ask about genuinely incompatible explicit instructions or enforced requirements,
not a conflict introduced by the fallback below.

When the repository has no commit style, use Conventional Commits with a concise body:

```text
<type>[optional scope][optional !]: <description>

# Why

<concise reason for the change>

# What changed

- <significant resulting change>

<optional breaking-change or repository-required trailers>
```

Keep the body proportional to the change and useful to a future reader. Explain
intent and resulting behavior, rather than listing files or command transcripts.
Keep required trailers contiguous at the end; include tests only when they
materially explain the change. Do not fabricate issue references or co-authors.

Use one commit invocation. A message file with `git commit -F <file>` is useful
for multiline or shell-sensitive text; safely quoted -m arguments also work.
Use real newlines, not literal backslash-n sequences. Keep scratch message files
outside the tracked change set and preserve the intended body through Git's
message cleanup rules.

## Hooks, failures and completion

Config-defined hooks arrived in Git 2.54. For diagnosis on the tested Git 2.56,
`git hook list --show-scope -z pre-commit` and the corresponding commit-msg query
inventory config-defined hooks as well
as the legacy hook without running them. Inspecting .git/hooks alone can miss
global/local configured hooks. Missing events return 1 with a warning; this is
not a failed linter. In Git 2.56, pre-commit and message-writing events remain
serial even though other events can opt into parallel hooks; increasing hook
jobs is not a way to accelerate those commit events.

Honor repository hooks and signing. A failure is a cause to diagnose, not
permission to use --no-verify, disable hooks/signing or change global identity.
If a hook formats or stages files, inspect both index and worktree, retain only
the authorized outcome, and retry after the cause is resolved. Do not repeat a
failed command without new evidence or amend a successful commit automatically.
For hook configuration/partial-commit failures involving hk, use the hk skill.

Verify the resulting commit's files, content and message, together with the
remaining staged/unstaged changes. A hook may change what was committed, so
successful exit alone is insufficient. Report the commit identifier and any
remaining relevant changes; a commit request does not imply pushing.

- [Git commit](https://git-scm.com/docs/git-commit)
- [Git add](https://git-scm.com/docs/git-add)
