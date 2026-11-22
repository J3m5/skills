# Task output, reports and history

Choose the result surface that answers the question. A terminal summary, a run
report and historical timings serve different purposes; they are not interchangeable
JSON schemas. Keep task selection within the requested verification scope.

## Compact terminal output

For finite checks with verbose successful output, prefer `--output summary`:

```sh
mise run --tag lint --tag test --output summary --report-file /tmp/mise-checks.json
```

Choose a fresh report path per invocation when several runs may overlap.
Summary prints one success line per passing task and buffered output on failure.
It holds only the newest 64 KiB per task; interruption or timeout flushes pending
output. Raw/interactive tasks retain their terminal. For a server or watcher,
use streaming `prefix` or `interleave` so progress is visible before it exits.

`MISE_TASK_OUTPUT=summary` selects this mode for an invocation/environment;
`task.output` and a task's `output` configure defaults when that scope is intended.
Prefer a command flag for ordinary agent work rather than changing global settings.
`--quiet` hides mise's own messages, whereas `--silent` hides task output too;
neither is a substitute for a failure-preserving summary.

## Machine-readable run evidence

`--report-file PATH` writes one JSON document when execution ends on success,
failure, Ctrl-C or run timeout. `MISE_TASK_REPORT_FILE` is its environment form
and is removed from task child environments so nested mise runs do not overwrite
the outer report. Neither form combines with `--dry-run`. Read the file generated
by the current invocation rather than a leftover from an earlier attempt.

Read `version` (currently 1), top-level `status`, `duration_ms`, `started_at`,
`ended_at`, and `tasks`. Each scheduled task, including dependencies, has `name`,
redacted `args`, `status`, `exit_code`, duration and timestamps. Entries appear
in start order, followed by those never started. Treat nullable values as unknown,
not zero. Accept additive fields; a schema version change can alter semantics.

| Task status | Meaning                                                       |
| ----------- | ------------------------------------------------------------- |
| `passed`    | The command ran and exited 0.                                 |
| `failed`    | Execution failed or could not start; `exit_code` can be null. |
| `cancelled` | Stopped by interruption, timeout or another task's failure.   |
| `skipped`   | Fresh outputs or a successful `skip_if` avoided execution.    |
| `cached`    | Restored an artifact-cache result.                            |
| `not_run`   | The run ended before the task started.                        |

The run status is `passed`, `failed`, `cancelled` or `timed_out`.
Check both the process exit status and task statuses: a successful run can include
skipped/cached tasks. The report carries results, not captured stdout/stderr.
Preserve mise's exit status when a shell wrapper reads or uploads the report;
a later successful JSON parser must not turn a failed check into CI success.

## Inspect without rerunning

| Question                              | Command and interpretation                                                                                                  |
| ------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Which checks are available?           | `mise tasks ls --tag test --json`: task metadata, including tags; no execution evidence.                                    |
| What would affected selection choose? | `mise run --affected --affected-json <task>`: selection and reasons, without running tasks.                                 |
| Are definitions valid?                | `mise tasks validate --json <task>`: definition diagnostics; warnings do not fail the command, errors exit 1.               |
| Are declared prerequisites met?       | `mise doctor project --json`: executes project checks; interpret `errors` and `checks` using [diagnostics](diagnostics.md). |
| What happened recently?               | `mise tasks history --json <task>`: stored runs for the current project.                                                    |
| What is the typical cost?             | `mise tasks history --summary --json`: per-task aggregates; `median_ms` counts only executed successful runs.               |

From 2026.11.7, `tasks ls --json` and `tasks info <task> --json` include a
`history` summary, or null for a task without runs. In 2026.11.9 the listing also
includes `cache`, `lock` and `skip_if` for each task. [History fields](https://github.com/jdx/mise/releases/tag/v2026.11.7)

History recording defaults to on, keeping 20 runs per task; `task.history` and
`task.history_limit` control it. Dry runs and pure dependency aggregators are
not recorded. Duration includes environment resolution and lock waiting, but
not dependencies' separate runs. History uses its own result labels (for example
`ok` for success); do not apply the run-report status vocabulary to it. Historical
success is not evidence that the current checkout passed.

## Recover saved output

`task.logs` defaults to off. When capture is useful for the requested run,
`MISE_TASK_LOGS=1 mise run --output summary <task>` enables it for that invocation.
Read with `mise tasks log <task>`; `mise tasks log <task> --path` returns the
expected path even when no file exists. Inspect an available log before rerunning.

Logs keep the newest 4 MiB of combined stdout/stderr per task and project,
with owner-only permissions and terminal redaction rules. Each executed run
replaces the previous log; a command that never starts can leave an older log.
Correlate it with the run/history before attributing its contents to a failure.
Raw/interactive and direct-to-terminal interleave runs cannot be captured and
remove an earlier log. Logging is neither an unlimited archive nor a guarantee
that arbitrary secrets are detected.

- [Execution, report schema, summary and logs](https://github.com/jdx/mise/blob/v2026.11.9/docs/tasks/running-tasks.md)
- [Run flags](https://github.com/jdx/mise/blob/v2026.11.9/docs/cli/run.md)
- [History](https://github.com/jdx/mise/blob/v2026.11.9/docs/cli/tasks/history.md)
- [Logs](https://github.com/jdx/mise/blob/v2026.11.9/docs/cli/tasks/log.md)
- [Validation](https://github.com/jdx/mise/blob/v2026.11.9/docs/cli/tasks/validate.md)
