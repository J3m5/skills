---
name: git-core
description: >-
  Create and correct local Git branches, commits and worktrees; restack dependent
  branches, inspect Git state and diagnose slow Git commands.
---

# Git Core

Carry out the requested Git operation in its intended repository and scope.
Use the user's explicit instructions and established repository policy before
this skill's defaults. Resolve routine naming, source and message choices from
context; ask only when an unresolved choice changes the work being recorded,
the branch base, or an enforced requirement. An authorized workflow does not
need a new confirmation at each local write.

## Preserve the relevant state

Inspect the current branch/HEAD, worktree and index before changing them. A dirty
tree is normal for a branch carrying current edits and does not prevent a separate
worktree. Preserve unrelated staged and unstaged content. If another Git operation
is in progress, determine whether completing it belongs to the request rather
than aborting or continuing it implicitly.

Run dependent Git mutations sequentially in the same repository, including
linked worktrees sharing refs. Do not add a push, history rewrite or removal of
local changes to a branch/commit/worktree request. Follow the active execution
permissions without treating a tool approval as authorization for unrelated work.

## Choose the workflow

- [Branches](references/branch.md): resolve the intended base, create or use the
  requested branch, control tracking, or perform requested branch cleanup.
- [Commits](references/commit.md): select index versus whole-file content,
  preserve unrelated staging, follow message policy and handle hooks.
- [Worktrees](references/worktree.md): create on new/existing branches, inspect
  isolation, and perform requested move, repair or cleanup.
- [Single-commit corrections](references/history.md): explicitly requested
  reword, staged fixup, split or drop in linear history.
- [Rebase and restacking](references/restacking.md): create or re-parent dependent
  branches, replay a branch chain, rebuild commits from final content, or recover
  children after parent rewrites and squash merges.
- [Inspection and performance](references/inspection-and-performance.md): batch
  state/history queries and requested repository performance tuning.

Read only the reference needed; the worktree reference links to branch decisions
when a new base/name must be selected. Use `github` or the available GitLab skill
for hosted PR/MR/CI state. Read the restacking reference when a correction affects
dependent branches or changes their base. History rewrites require their own
requested scope.

Verify the operation's result: the branch's commit and tracking, the commit's
actual content/message and remaining changes, or the worktree's path/HEAD/status.
Checks required by the repository still apply; do not repeat unrelated test
suites solely because a branch or commit was created. The reference commands
were checked with Git 2.56.0; consult installed help for version-sensitive options.
