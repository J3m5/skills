# Worktrees

## Choose the checkout and branch

Inspect `git worktree list --porcelain` before creating another checkout. Reuse a
worktree when it already matches a request to continue work; create a new one
when isolation or a new checkout is requested. If the environment provides a
managed-worktree workflow, use its creation/attachment/cleanup tools for managed
checkouts rather than creating an unregistered duplicate.

For a new branch, use the relevant source/name decisions in
[branches](branch.md) without separately creating the branch. For an existing
branch, retain its history and check whether it is already checked out elsewhere.
Git normally prevents a branch being checked out twice; do not override this
with --force to work around an existing checkout.

Choose the requested or repository-conventional location. Otherwise use a
filesystem-safe folder derived from the branch, preferably alongside the main
checkout. Avoid name collisions after slug normalization. An existing directory
is not permission to overwrite it; inspect a matching checkout or choose another
path when the user left location open.

## Create with explicit inputs

A dirty main worktree does not block creating a separate checkout. The new
worktree contains the selected committed state, not uncommitted changes from
the original worktree. If the request needs those changes in the new checkout,
plan an explicit transfer that preserves its staged/unstaged distinction; do not
commit or stash them merely as an implementation shortcut.

For a new branch from a resolved commit:

```sh
git worktree add --no-track -b "$branch_name" "$worktree_path" "$source_commit"
```

For an existing unoccupied local branch, use `git worktree add <path> <branch>`
without -b. For an explicitly requested detached checkout, use --detach and the
commit. Do not use -B to turn a collision into an implicit branch reset. Refresh
remote sources only when the branch workflow calls for it.

Verify registration, path, branch/HEAD and status in the new checkout, together
with preservation of the original checkout's changes. Repository objects/refs
are shared, but HEAD and index belong to each worktree. Dependencies, ignored
files, build outputs and secrets are not automatically copied; perform only
setup needed for the requested task. Worktree creation alone does not require
installing dependencies or running the full suite.

Git 2.56 supports `includeIf "worktree:<pattern>"`, matching the checkout's real
path rather than its Git directory. Linked checkouts can therefore load different
identities, hooks or signing settings without extensions.worktreeConfig. When
diagnosing those differences, query `git config get --show-origin --show-scope
<key>` inside the affected checkout; do not assume the source checkout's effective
configuration applies there. This is not a reason to add global configuration.

The common .git/info/exclude is shared across linked worktrees, as clarified in
Git 2.55's release notes. It is not a private per-checkout ignore list; account
for its effects on other checkouts before changing it.

## Requested maintenance and cleanup

Use `git worktree move` for supported moves and `git worktree repair` to repair
administrative links after an external move; do not fix paths by editing .git
files blindly. Locked worktrees may represent removable/unavailable storage,
not abandoned work. Use --porcelain -z when parsing names that need NUL safety.

Before removal, inspect status, including untracked files and any needed ignored
artifacts. Use `git worktree remove` for an authorized clean checkout; a dirty
tree needs preservation or explicit discard authorization, not --force. Removing
a worktree does not delete its branch. `git worktree prune --dry-run` previews
stale administrative records; it is not removal of a live checkout. Do not prune
temporarily unavailable worktrees or delete branches as incidental cleanup.

- [Git worktree](https://git-scm.com/docs/git-worktree)
