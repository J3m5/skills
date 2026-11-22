---
name: mise
description: >-
  Set up mise in a new project or maintain its tools, environments, tasks and
  daemons. Use when changing or diagnosing mise itself.
metadata:
  required_tools:
    - mise
---

# mise

Release coverage through [mise 2026.11.9](https://github.com/jdx/mise/releases/tag/v2026.11.9).

## Equip a new project

Start with a project tool and a task that uses it. The [first-project example](references/install-tools.md#first-project) covers installing mise, activating a shell, declaring the tool and checking the result. Add [lockfiles](references/lockfiles.md) when the project needs reproducible artifacts.

## Work on an existing project

From the target directory, inspect `mise config ls` and the relevant declaration. Check `mise which <executable>` and the tool's own version when selection matters. Run the tool directly with activation or shims on PATH. Use the existing `mise run <task>` for a project workflow. A process without that environment can use `mise exec -- <command>`. See [shell activation](references/shell-activation.md) for diagnosis.

Change the owning configuration and verify the affected behavior, such as running the changed task or checking daemon readiness. Match version-sensitive options to `mise --version`, subcommand help and the [versioned documentation](https://github.com/jdx/mise/tree/v2026.11.9/docs).

## References by operation

- Toolchains: [selection](references/search-tools.md), [install and execute](references/install-tools.md), [updates](references/tool-updates.md), [updating mise itself](references/self-update.md), [plugins and backends](references/plugins-and-backends.md).
- Project setup: [configuration and write targets](references/configuration.md), [environments](references/environments.md), [package dependencies](references/dependencies.md), [tool-provided skills](references/tool-skills.md).
- Tasks: [definitions and validation](references/tasks.md), [execution](references/task-execution.md), [results](references/task-results.md), [caching](references/task-caching.md), [secrets](references/secrets.md).
- Operations: [daemons](references/daemons.md), [machine bootstrap](references/machine-setup.md), [diagnostics](references/diagnostics.md), [trust and security](references/security.md), [command selection](references/usage.md).
