---
name: hk
description: >-
  Set up hk in a new Git repository or maintain its checks, file selection,
  partial-commit behavior and CI integration. Use when the hook setup itself
  needs changing or diagnosis.
metadata:
  required_tools:
    - hk
    - git
---

# hk

## Equip a new project

Choose one check the project needs and decide whether a commit should reject or fix a failing file. The [first-hook example](references/hooks.md#first-hook) installs hk, configures a builtin and exercises both outcomes through Git. Use the project's tool manager for any external linter. Installing the executable and registering a Git hook are separate operations.

## Work on an existing project

Check `hk --version`, the installed Git launcher and the effective [Pkl configuration](references/configuration.md). Check `HK_FILE`, then the nearest configuration and its `amends` chain. Keep Config.pkl and Builtins.pkl aligned with the project pin. hk 2.x embeds the Pkl evaluator.

Change the relevant [step](references/steps.md) in that configuration. Run `hk validate`, preview selection with `hk check --plan <file>` and run the affected check. For a glob change, also preview a file that should be skipped. When behavior depends on the index, exercise the [installed hook](references/hooks.md) in a disposable checkout. Inspect both diffs after a fix. `--check` selects a command. `--safe` relies on its declared effects.

Use direct `hk` commands when PATH selects the project tool. Git launched from an IDE or CI can have a different PATH. Configure the [launcher](references/hooks.md#install-the-requested-scope) for that environment.

Release coverage through [hk 2.13.0](https://github.com/jdx/hk/releases/tag/v2.13.0), including version-specific notes for 2.5.0. For version differences, check CLI help, the [versioned documentation](https://github.com/jdx/hk/tree/v2.13.0/docs) and the matching schema.

For automation or upgrades, see [CI and agent integration](references/ci-and-agents.md) or [migration and diagnosis](references/migration-and-diagnosis.md).
