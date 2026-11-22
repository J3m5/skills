# Branches

## Choose the base and name

Use an explicit source when provided. For a branch intended to contain the
current edits or commits, use current HEAD, including a detached HEAD. A simple
new-branch request can normally use HEAD unless repository policy or context
specifies another base. Do not replace that intent with the default branch.

When a fresh default/integration branch is requested, resolve its remote and
branch from repository guidance and remote metadata; do not assume origin/main.
If multiple sources remain materially plausible, clarify the choice. Check only
the naming guidance/tooling relevant to this operation. Preserve a user-provided
name when valid and compatible with enforced policy; otherwise follow the local
convention, with a descriptive typed name such as fix/<slug> as a fallback.
Validate the final name with `git check-ref-format --branch <name>`.

Resolve the source to the intended commit before creation. A local branch, tag
and remote-tracking branch with the same short name are distinct; use a qualified
ref when necessary. In an unborn repository, HEAD has no commit: choose the new
unborn branch name when requested rather than inventing a base commit.

## Refresh only when needed

Creating from current HEAD or an intentionally local/pinned source needs no
fetch. If the selected source must reflect a remote, fetch that branch without
pulling, rebasing or moving the local source branch. For example:

```sh
git fetch --no-tags "$source_remote" "refs/heads/$source_branch"
git rev-parse --verify 'FETCH_HEAD^{commit}'
```

Use the resolved fetched commit as the base; do not assume a custom fetch mapping
updated refs/remotes/<remote>/<branch>. Resolve FETCH_HEAD immediately, before
another fetch can replace it. If freshness is required and the fetch fails,
report that failure rather than silently treating a stale ref as current.

## Create or use the intended branch

Check existing local refs and `git worktree list --porcelain` when relevant.
An existing requested branch is not itself an error: use it when the request is
to continue that branch. A request for a genuinely new branch must not reset or
overwrite an existing ref; report an actual collision or derive an alternative
only when naming was left to you. A matching remote branch may be the branch to
track, rather than a reason to refuse all local creation.

For a new branch that should become current, prefer transactional creation:

```sh
git switch --no-track -c "$branch_name" "$source_commit"
```

For creation without switching, use `git branch --no-track` with the name and
base. Choose --track only when the new branch should track the intended remote
branch; branching from a remote base alone should not make a feature branch
track main. Do not change upstream configuration on the source branch.

Dirty state is allowed. If switching would overwrite work, preserve it and
resolve the actual conflict; do not use forced switching, automatic stashing or
an implicit merge to bypass it. Verify the resulting branch/ref, base commit,
tracking and relevant staged/unstaged state. Reuse/continue and new-branch
creation have different outcomes; do not report success if the requested ref
was never created or selected.

For repeated state/branch comparisons, use the batched queries in
[inspection and performance](inspection-and-performance.md) instead of building
an unnecessary sequence of one-ref queries. These comparisons do not override
the source chosen from the user's intent.

## Requested branch cleanup

Git 2.56's `branch --delete-merged <upstream-pattern> [<branch-pattern>...]`
removes local branches whose tips are reachable from their configured upstreams.
Use it only for requested cleanup, with explicit upstream and branch filters;
it does not mean "all branches merged into main". Resolve the intended upstream
state, refreshing it only when freshness is required, and preview the same scope:

```sh
git branch --dry-run --delete-merged "$upstream_pattern" "$branch_pattern"
git branch --delete-merged "$upstream_pattern" "$branch_pattern"
```

Git skips branches checked out in a worktree, missing upstreams and branches
protected by branch.<name>.deleteMerged=false, among other safeguards. A branch
can also be skipped when pushing it would update its upstream; do not override
these protections with -D to force the preview's expected count. Inspect the
actual result; worktree removal and remote branch deletion are separate scopes.

- [Git branch](https://git-scm.com/docs/git-branch)
- [Git switch](https://git-scm.com/docs/git-switch)
- [Git fetch](https://git-scm.com/docs/git-fetch)
