# Hook installation and partial commits

## First hook

In a new Git repository using mise, run `mise use hk@2.13.0`, then `hk init` from a shell with activation or shims. For a different tool manager, follow the [installation guide](https://github.com/jdx/hk/blob/v2.13.0/docs/getting_started.md) and use `hk install` for a plain Git launcher. Keep the two generated package lines in `hk.pkl` and replace the generated steps with the block below.

```pkl
steps {
  ["whitespace"] = Builtins.trailing_whitespace
}
hooks {
  ["pre-commit"] { fix = false }
}
```

This builtin ships with hk. For the mise example, run `hk validate` and `hk install --mise` to register the local hook. The launcher can now load the project tools when Git can find mise. In the disposable repository, with a Git author configured, exercise the installed hook:

```sh
printf 'hello  \n' > example.txt
git add example.txt
git commit -m 'Check fixture'    # Expected refusal for trailing whitespace
hk fix example.txt
git add example.txt
git commit -m 'Check fixture'    # Expected success
```

For a real project, commit the shared tool declaration and Pkl config. Each clone needs its hook registered according to the project's installation policy.

## Install the requested scope

Inspect Git version, `git config --show-origin --get-regexp '^hook\.hk-'` and
core.hooksPath before changing an installation. Missing settings may exit nonzero.
Inspect scripts too on legacy installations.

hk install sets up this repository. Git 2.54+ uses config-based hooks; older Git
writes script shims. --legacy requests shims. Legacy installation refuses foreign
hooks/symlinks without changing targets; --force replaces them, so preserve
existing integrations before considering it.

hk install --global requires Git 2.54+ and writes user Git configuration. Use it
when machine-wide hook installation is requested; otherwise keep scope local.
It runs project configuration in repositories with an hk config, including new
clones; repositories without one are silent no-ops. Global tool installation and
global hook installation are independent.

Use --mise when hooks need mise tools/environment without shell activation.
Global launchers record mise's absolute path; local ones require mise on Git's
runtime PATH. Global hk paths use an upgrade-stable shim where available.
HK_MISE=1 changes later init/install defaults, not existing launchers. Existing
global hk hooks normally make local install skip and clean up stale local hk hooks.
Since 2.12, an explicit --legacy or a Git older than 2.54 installs local shims
even with a global install. On Git 2.54+, shims alongside global hooks or
--force-local can cause duplicate execution. Use hk uninstall or
hk uninstall --global for the corresponding scope. Inspect the events installed;
do not assume every possible event is covered.

## Preserve staged and unstaged work

With shared top-level steps, pre-commit defaults to fixing, staging and stashing.
Ordinary hk fix leaves fixes unstaged. Manual hk run pre-commit uses the same
mutating workflow; inspect its plan first when diagnosing.

Manual `hk check --staged` selects paths from the index and checks their working-tree
contents. For a partially staged file, that result can differ from the commit.
Since 2.7.1, the global Git launcher passes `--from-hook --staged` and follows
the hook's `stash` setting even when `HK_STASH` is set. With `stash = "git"`,
pre-commit checks the staged contents and restores unstaged edits afterward.
Formatters still operate on whole files, not staged hunks. In 2.5.0 patch-file
is an alias for Git stashing.

--all includes eligible untracked files only with resolved stash=none. HK_STASH
can override hook behavior. HK_STASH_UNTRACKED=0 disables untracked discovery
as well as stashing. Intent-to-add files are preserved separately and are not
passed to staged checks.

To fix but require review before committing, set stage=false and fail_on_fix=true.
stage=false alone need not fail the hook. Step stage patterns filter paths only
after hook-level staging is enabled. Compare git diff, git diff --cached and status.

## Recovery

In 2.13.0, after a crash during stashing, the next `hk check`, `hk fix` or
`hk run` reads the worktree's Git journal (`git rev-parse --git-path hk-pending-stash`).
If the previous process is gone and there are no unstaged edits or untracked files,
hk can restore its stash automatically. If hk requests manual recovery, inspect
`git status` and `git diff --cached` before running the printed `git stash apply <commit-id>`.
Overlapping edits can conflict. Keep the stash until you verify both the index and
the working tree. Leave the journal lock in place. [Crash recovery](https://github.com/jdx/hk/blob/v2.13.0/docs/hooks.md#if-hk-is-stopped-mid-run)

For older releases or a failed restore, preserve the backup and locate it using
the version that created it.

- On 2.5.0, inspect the shared Git stash and the patches under the hk state
  directory. The stash lock lives in the common Git directory.
- Since 2.7, the default backup location inside an ordinary repository is
  `<common-git-dir>/hk/patches/`. Logs are per checkout in `<git-dir>/hk/`.
  An explicit `HK_STATE_DIR` or shared repository configuration can change
  these locations. [State locations](https://github.com/jdx/hk/releases/tag/v2.7.0)
- Since 2.8.1, hk uses private refs and a per-worktree lock. Inspect
  `git for-each-ref refs/hk/stash/` as well as older shared stash entries.
  Version 2.12 fixes recovery when another worktree empties the shared stack.
  [Private refs](https://github.com/jdx/hk/releases/tag/v2.8.1) · [Restore fix](https://github.com/jdx/hk/releases/tag/v2.12.0)

For an unstaged deletion check the 2.11.0 restoration fix. For restore errors
under `git --literal-pathspecs`, check 2.11.1. Intent-to-add recovery also
needs `git add -N` afterward.

- [Hooks and recovery](https://github.com/jdx/hk/blob/v2.13.0/docs/hooks.md)
- [Install CLI](https://github.com/jdx/hk/blob/v2.13.0/docs/cli/install.md)
- [mise integration](https://github.com/jdx/hk/blob/v2.13.0/docs/mise_integration.md)
