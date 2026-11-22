# Task definitions and watch mode

Inspect TOML tasks and file tasks with `mise tasks ls --extended` and
`mise tasks info <task>` before adding or moving one. Default task directories
include `mise-tasks/`, `.mise-tasks/`, `mise/tasks/`, `.mise/tasks/`, and
`.config/mise/tasks/`. File tasks must be executable on Unix. Preserve the
project's convention and existing build-system dependency graph.
Global tasks also use the default task directories under `MISE_GLOBAL_CONFIG_ROOT`
(the home directory by default). Changing `MISE_CONFIG_DIR` alone does not
isolate task discovery; use an isolated global root for fixture-based evaluation.

After changing definitions, `mise tasks validate <task>` checks dependency
references, cycles, scripts, globs, shells and related config without running
the task. It does not prove the task's command succeeds. Validate the affected
tasks, then run the requested functional check when appropriate.
Use `mise tasks validate --json <task>` for structured diagnostics; errors exit 1,
while warnings do not fail validation. `--errors-only` hides warnings.
For a task that requires daemons, or a long-running task supervised as a daemon,
use the [daemon reference](daemons.md).

## Editing tasks

`mise tasks add`, `set` and `rm` accept `--path`, `--env` and `--global` to
select the owning file, plus `--dry-run` and `--json`. `set` changes only supplied
fields and preserves comments; `--unset FIELD` removes a property. When several
files define a task, select the intended file explicitly. `rm` can delete a file
task's script; it refuses inferred package tasks and tasks from includes. Edit
the source that owns those definitions instead.

## Arguments and reusable definitions

Use `usage` on TOML tasks or `#USAGE` on file tasks when arguments need names,
choices, validation or help. Resolved values reach scripts as `usage_*` variables
and templates as `usage.NAME`; quote shell expansions. Without a spec, extra
arguments are forwarded. For a wrapper that owns its argument parser, use the
task's `raw_args = true` or a one-off `--` separator; mise flags still belong
before the task name.

Use `[task_templates.NAME]` and `extends` for shared definitions. A template is
not a runnable task or a Tera expression. Keep team templates in the repository,
not only in personal global config. Tools/env/vars merge by key, while dependency
lists are replaced when non-empty. An empty `depends = []` inherits the template's
dependencies rather than clearing them. Inspect `mise tasks info <task>` after
merging. Templates cannot extend templates or grant task secrets.

## Ordering and watch mode

`depends` schedules prerequisites; `wait_for` only orders tasks already scheduled.
`depends_post` runs after a task that started, even on failure, but not when an
earlier prerequisite prevented it starting. A task listed before and after runs
twice. Inspect the graph with `mise tasks deps` when order is unclear.

`mise watch <task>` reruns tasks with watchexec when task/dependency sources
change; without declared sources it watches the current directory. Pass task
arguments after `--`. Select queue, restart or signal behavior according to the
process; the default ignores events while it is busy. Use `--print-events` to
diagnose a trigger before widening watched paths. Readiness-managed persistent
services use [daemons](daemons.md), rather than replacing that lifecycle with watch.
Do not install watchexec globally if a project-scoped setup meets the request.
`mise watch --once <task>` waits for the first matching change,
runs once and exits with the run's status; it does not run immediately.
`--exit-on-error` stops an ordinary watch after failure and needs watchexec >= 2.5.0.

`skip_if` can skip work based on state outside source files.
Exit 0 skips successfully; another exit status runs the task. It runs after
prerequisites, without stdin or task secret grants. Startup errors, signals and
timeouts fail the task. `--force` bypasses it; `--dry-run` only displays it.
A required prerequisite that must fail the run belongs in `run`, not `skip_if`.

For automatic package providers, use [project dependencies](dependencies.md).
`--no-deps` skips those providers; `--skip-deps` skips task dependencies (and their
daemon startup), so these flags are not interchangeable. For requested task
restrictions, use [security controls](security.md).

## Optional integrations

For requested shared task catalogs, use `task_config.includes` with local paths
or Git/OCI sources, plus HTTP(S) `zip::` archives. Remote task
sources require `experimental`. Config `include` cannot hold `[tasks]`; its
ZIP trust and refresh rules are covered in [configuration](configuration.md).

For tags, affected selection and resource locks, read
[task execution](task-execution.md). Use [task results](task-results.md) for
summary output, JSON reports, history and logs, and [task caching](task-caching.md)
for freshness versus artifact restoration and cache-key diagnosis.
Use OpenTelemetry guidance only for requested task observability, not as a
default verification step.

- [Task discovery and precedence](https://github.com/jdx/mise/blob/v2026.11.9/docs/tasks/task-discovery.md)
- [File tasks](https://github.com/jdx/mise/blob/v2026.11.9/docs/tasks/file-tasks.md)
- [Task arguments and Usage](https://github.com/jdx/mise/blob/v2026.11.9/docs/tasks/task-arguments.md)
- [Task templates and merge rules](https://github.com/jdx/mise/blob/v2026.11.9/docs/tasks/templates.md)
- [Dependency ordering and task properties](https://github.com/jdx/mise/blob/v2026.11.9/docs/tasks/task-configuration.md)
- [Watch command and events](https://github.com/jdx/mise/blob/v2026.11.9/docs/cli/watch.md)
- [Validation](https://github.com/jdx/mise/blob/v2026.11.9/docs/cli/tasks/validate.md)
- [Artifact cache and freshness](https://github.com/jdx/mise/blob/v2026.11.9/docs/tasks/caching.md)
- [Remote cache](https://github.com/jdx/mise/blob/v2026.11.9/docs/tasks/remote-cache.md)
- [OpenTelemetry](https://github.com/jdx/mise/blob/v2026.11.9/docs/tasks/opentelemetry.md)
