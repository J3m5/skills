# Command selection

| Need                                  | Command                                                                      |
| ------------------------------------- | ---------------------------------------------------------------------------- |
| Installed/configured tools            | `mise ls`, optionally `--current`, `--project`, `--no-global`, or `--global` |
| Active config files                   | `mise config ls`                                                             |
| Executable resolution                 | `mise which <executable>`                                                    |
| Outdated configured tools             | `mise outdated`                                                              |
| Upgrade within constraints            | `mise upgrade <tool>`                                                        |
| Rewrite version constraints           | `mise upgrade --bump <tool>`                                                 |
| Update only global/system requests    | `mise outdated --global <tool>`, `mise upgrade --global <tool>`              |
| Global task inventory                 | `mise tasks ls -g`                                                           |
| Run a task                            | `mise run <task> -- <args>`                                                  |
| Discover checks by purpose            | `mise tasks ls --tag test --json`                                            |
| Run tagged checks with compact output | `mise run --tag test --output summary`                                       |
| Save structured execution results     | `mise run --output summary --report-file PATH <task>`                        |
| Inspect historical timings            | `mise tasks history --summary --json`                                        |
| Project prerequisite checks           | `mise doctor project`, optionally `--json`                                   |
| Dependency provider inventory         | `mise deps install --list`                                                   |

`ls --project` selects the nearest project's configuration;
`--no-global` on ls/outdated/upgrade/tasks ls also includes non-global ancestors.
Do not replace every `--local`: it still selects local overrides for `mise lock`
and project writes for `settings set`. Consult each subcommand's help.

Global tasks are merged into task discovery; do not assume `mise run` has a
`-g` flag. A task can execute arbitrary project commands: run the task requested
or needed by the work, not every discovered task.

Use `-C <dir>` for directory context and `-E <env>` for configuration environment
selection. These affect the effective tools, environment, tasks and lockfiles.
For installation versus activation versus execution, read
[install and execute](install-tools.md). For PATH selection and when to use an explicit environment, see [shell activation](shell-activation.md).
For `--global` update scope and automatic updates, read [tool updates](tool-updates.md).
For task definitions and validation, read [tasks](tasks.md); for selection,
reports and history, read [task execution](task-execution.md).
For troubleshooting, distinguish [mise's own diagnostics from project checks](diagnostics.md).

- [CLI index](https://github.com/jdx/mise/blob/v2026.11.9/docs/cli/index.md)
- [Upgrade](https://github.com/jdx/mise/blob/v2026.11.9/docs/cli/upgrade.md)
- [Task execution](https://github.com/jdx/mise/blob/v2026.11.9/docs/cli/run.md)
