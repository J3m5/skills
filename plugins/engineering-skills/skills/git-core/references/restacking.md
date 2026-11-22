# Rebase and dependent branches

Choose the history change that matches the request: create a child, change its
base, or move a set of dependent branches together. For creation, resolve the
intended parent through [branches](branch.md). Work from the actual local tips;
a clean checkout or a remote-tracking ref does not account for unpushed work.

## Establish the replayed work

Identify which branch refs may move and which commits belong to them. For recovery
after a parent rewrite or squash merge, distinguish:

- `old_parent_tip`: the parent boundary actually included in the child history.
- `new_parent_tip`: the intended destination, including the squash when relevant.
- `child`: the local branch whose own changes should be replayed.

Recover the old boundary from history, reflogs or existing recovery refs. The
current parent tip or a fresh merge-base can identify a different range after a
rewrite; patch equivalence alone does not prove ownership of the commits. Inspect
the candidate range. Ask only when unresolved alternatives change the work to
replay, rather than treating a missing stack tool or metadata as a blocker.

Record original tips and any boundaries needed by later operations. For a
sequential restack A → B → C, retain the old B boundary before moving B so that C
does not replay B's old commits. Use dedicated backup refs when the value or
complexity of the work warrants durable recovery beyond the recorded tips and
reflogs. `git refs create refs/backup/<name> <old-tip>` refuses name collisions;
keep any such backups through verification rather than requiring one for every
routine branch move.

## Choose the ref and topology scope

Git's `rebase --update-refs` can move intermediate branch refs along with a linear
stack in one operation. Use it when those affected refs match the requested scope.
Check rebase.updateRefs and linked worktrees: Git skips automatic updates to
branches checked out in other worktrees, while other local branch refs on the
replayed range may move. Choose `--no-update-refs` when moving only the selected branch or when
descendants need separate handling.

For example, once the old boundary and destination are verified, a linear child
can be moved without automatically changing other branches:

```sh
git rebase --no-update-refs --onto "$new_parent_tip" "$old_parent_tip" "$child"
```

If the range contains merges, choose deliberately whether to preserve or change
that topology. `--rebase-merges` recreates merges; their previous conflict
resolutions may need to be reapplied. The linear example is not a topology policy.

Use a suitable checkout, accounting for branches already checked out elsewhere.
Dirty state in another worktree is not a reason to block the operation or reset
it. Preserve unrelated work using the [worktree guidance](worktree.md) or a
preservation strategy appropriate to the request. Respect signing and hooks.

## Rebuild commits from final content

When the user asks to rebuild a branch’s commits from its final content,
establish the intended base, final content to preserve, affected refs, and
unrelated local work. Group that content into coherent commits describing the
resulting change rather than the editing chronology; include formatting in the
corresponding final scope. Preserve a recoverable reference to the original work
and compare the reconstructed result with the intended final content, explaining
any deliberate omissions. Follow the existing hook, signing, descendant-branch,
and publication requirements. Do not infer a history rewrite from an ordinary
commit request, or a push from permission to rebuild locally.

## Resolve and verify the result

Resolve conflicts according to the intended changes, stage the reviewed paths
using the [commit guidance](commit.md), and continue or abort as appropriate.
Skipping a commit needs a content-based reason; it is not a way to bypass a
resolution. An abort unwinds the current rebase, not earlier successful moves in
a sequence.

Rebase can omit clean cherry-picks or commits that become empty because their
changes are already upstream. That can preserve the requested work correctly;
do not force reapplication or an identical commit count merely because a commit
was local. Choose --reapply-cherry-picks or --empty when the intended history
requires different behavior.

Check the resulting ancestry, branch refs, content and remaining local work.
Compare the old and new child ranges with `git range-diff` when useful, and
explain meaningful omissions or changed patches. After a squash, verify that
old parent patches were not replayed as child work.

When publication is requested, use the hosting workflow and an explicit lease
against the observed remote tip for a rewritten branch. Reconcile an unexpected
remote change before replacing published history.

- [Git rebase](https://git-scm.com/docs/git-rebase)
- [Compare rewritten ranges](https://git-scm.com/docs/git-range-diff)
- [Reference creation](https://git-scm.com/docs/git-refs)
