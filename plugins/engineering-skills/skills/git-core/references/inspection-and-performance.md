# Efficient inspection and optional acceleration

Choose queries that answer the actual decision. These are not a checklist for
every branch or commit; avoid repeated full-history or full-diff scans.

## Query state in batches

For machine-readable branch, upstream and staged/unstaged state, use
`git status --porcelain=v2 --branch -z`. Parse its documented record types and
NUL delimiters; ordinary human status output is not a stable parser interface.
Use `git for-each-ref --format=...` when several known branch tips/tracking
values are needed, rather than running one process per branch.

For Git-directory or worktree-link diagnostics on Git 2.56, the experimental
`git repo info -z path.gitdir.absolute path.commondir.absolute` retrieves both
paths in one query. Its NUL-delimited records contain a key, a newline and a
value; the Git directory can differ from the shared common directory in a linked
worktree. Use installed help for other keys or versions.

Git 2.54 added status.compareBranches. A one-off comparison can use:

```sh
git -c status.compareBranches="$base_ref" status --short --branch
```

This does not persist a new preference. A comparison reports relationships; it
does not determine which base the user's branch should use.

When investigating which commit last changed several paths, Git 2.52+ provides the
experimental `git last-modified --recursive -z -- <paths>`. It reports one
commit/path pair, accounting for renames and mode changes. It is file-level
history, not line authorship, and should not substitute for a targeted blame or
content diff when those are needed. Check help for version-specific output.

## Tune only the requested repository

For demonstrated status latency, inspect `git version --build-options` for
fsmonitor support. Git 2.55 adds the built-in daemon on Linux; filesystem support
and runtime permissions still matter. When enabling acceleration is in scope:

```sh
git config set --local core.fsmonitor true
git config set --local core.untrackedCache true
git status --porcelain=v2 --branch -z
git fsmonitor--daemon status
```

core.fsmonitor=true can start a background daemon automatically. Check existing
values before replacing a hook-based monitor. Local repository settings can
affect linked worktrees; choose worktree-specific configuration only when that
setup is already supported or its introduction is requested. Avoid global
defaults, automatic scheduling or system inotify-limit changes as incidental
optimizations. Network mounts and some filesystems are unsupported/experimental.

Measure a representative repeated query and confirm tracked/untracked results
before claiming a speedup. If startup fails, inspect the filesystem, IPC/socket
location and permissions rather than assuming the feature is active. Preserve
previous config when reverting; stopping the daemon alone does not disable the
setting that would start it again.

- [Status records](https://git-scm.com/docs/git-status)
- [Repository information](https://git-scm.com/docs/git-repo)
- [Last-modified](https://git-scm.com/docs/git-last-modified)
- [Filesystem monitor](https://git-scm.com/docs/git-fsmonitor--daemon)
