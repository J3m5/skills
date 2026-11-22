# Single-commit corrections

Use only when the request includes rewriting an existing commit. An ordinary
commit request still creates a new commit. For dependent branches or moving a
commit range onto another base, use [rebase and restacking](restacking.md).

## Select the supported operation

`git history` is experimental; the operations below were checked on Git 2.56.
Check installed help before using it on another version. It edits a commit and
replays descendants without a stateful rebase, but cannot handle merge histories
or conflicts. It is not a replacement for rebasing onto a different base.

- `reword <commit>` opens the editor for the target message; current index and
  worktree are untouched.
- `split <commit> -- <paths>` interactively selects hunks for a new parent commit
  and edits both messages. Neither all nor no hunks can be selected. Paths limit
  candidates; they do not remove the interactive selection. Current index and
  worktree are untouched.
- `fixup <commit>` folds the current staged delta into that earlier commit,
  preserving its message and authorship unless --reedit-message is used. It
  consumes the staged delta on success while retaining unstaged work. Review the
  entire staged delta first; there is no path argument to isolate unrelated
  staging. Use the scoped-commit decisions in [commits](commit.md) for ambiguity.
- `drop <commit>` removes an explicitly selected commit and replays descendants
  onto its parent. It cannot remove a root or merge commit. When HEAD is affected,
  it updates the index and worktree to match the rewritten history, preserving
  unrelated edits and refusing changes that would overwrite local work. Review
  those effects before acting; it is not equivalent to reword/split's untouched
  index and worktree.

## Bound the rewrite

Resolve the target, affected ancestry and refs before acting. These operations
change commit identifiers and can require separate coordination for published
history. Do not infer push or force-push authorization from a local rewrite.

The default --update-refs=branches moves descendant local branch refs. For a
single-branch correction, choose --update-refs=head explicitly; it moves only
the current HEAD ref. Moving other branches must fit the request. Record the
old tips; if a backup ref is needed, refs/backup/<name> avoids the descendant
branch set that --update-refs=branches would itself rewrite.
On Git 2.56, `git refs create "refs/backup/$backup_name" "$old_tip"` creates such
a ref while refusing an existing name; do not overwrite a backup on collision.

Preview the same operation and ref scope before applying it. --dry-run leaves
refs/index/worktree unchanged but can write new objects; it is not a read-only
repository operation. For reword/split it can still invoke an editor or hunk
selection. Do not pipe its output to update-ref without reviewing the scope.

```sh
git history fixup "$target_commit" --dry-run --update-refs=head --empty=abort
git history fixup "$target_commit" --update-refs=head --empty=abort
```

For fixup/drop, choose --empty deliberately for commits that become empty:
drop is the default, keep retains them, and abort stops instead. A fixup can
also make its target empty; dropping an empty root commit remains unsupported.

These commands do not run Git hooks. Respect required validation and signing;
do not select this workflow to evade them or assume rewritten signatures remain
valid. If the operation cannot meet repository requirements, use its approved
rewrite workflow. A conflict or merge-history refusal is a reason to reassess
the operation, not to reset the worktree or apply unrelated staged changes.

Verify final history, changed refs and relevant index/worktree state. A reword
should change the intended message while retaining content; a split should
retain the combined content; a fixup should incorporate the reviewed delta and
leave the remaining edits available; a drop should remove the intended change
while preserving unrelated staged/unstaged content.

- [Git history manual](https://git-scm.com/docs/git-history)
