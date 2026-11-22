# Task freshness and artifact caching

Use for a skipped task, stale output or requested build optimization. Reuse the
project's tracking and cache policy; do not enable experimental caching merely
to run a check. Tool downloads and remote task definitions have separate caches.

## Distinguish skipping from restoration

Ordinary `sources`/`outputs` freshness uses modification times and a recorded
source list, sizes and times. It adds the defining config and file-task script.
Missing outputs or changed/added/deleted sources make the task stale. A dependency
with `sources` that runs or restores output invalidates its dependents.

With sources and no explicit outputs, `outputs = { auto = true }` uses a success
marker. `outputs = []` instead declares no output files and disables freshness
skipping; an enabled artifact cache can still reuse the result and log.
For a demonstrated timestamp problem, `task.source_freshness_hash_contents`
compares content hashes and detects output changes, without enabling artifact caching.

The experimental artifact cache needs `experimental = true`, `cache.enabled = true`,
nonempty sources and explicit outputs (or `[]`). Outputs must stay relative to
the task directory and must not contain sources. Include relevant lockfiles,
config, environment (`cache.env`) and external state (`cache.command_inputs`)
in the key. Enable caching only when identical inputs produce equivalent results;
live-service checks and side-effecting operations usually need real execution.

From 2026.11.9, a source changing during execution, including a newly matched
file, prevents storing that run's cache entry. Inspect generated files that
overlap the source globs before retrying. [Cache write conditions](https://github.com/jdx/mise/releases/tag/v2026.11.9)

## Choose per-run controls

| Intent                                                           | Command                                    |
| ---------------------------------------------------------------- | ------------------------------------------ |
| Force real execution without reading or writing artifact entries | `mise run --force --task-cache off <task>` |
| Rebuild and refresh entries under the existing cache policy      | `mise run --force <task>`                  |
| Consume entries without publishing new ones                      | `mise run --task-cache read-only <task>`   |
| Populate entries without reading old ones                        | `mise run --task-cache write-only <task>`  |
| Avoid the configured remote cache                                | `mise run --task-cache local-only <task>`  |

`--task-cache off` alone still allows ordinary freshness skipping. `--force`
also reruns dependencies and bypasses `skip_if`; assess those effects before using
it. The default artifact mode is `read-write`. `--no-cache` instead refreshes
remote task files and does not disable artifact caching.

## Diagnose keys and undeclared inputs

`mise run --dry-run --task-cache-explain-json <task>` emits **JSON Lines**, one
object per task with an opaque `cache_key`, not a run report. It requires
`--dry-run`; no task body runs and no artifacts are restored or stored, but
`cache.command_inputs` still execute to compute the key. Review those commands
before treating this inspection as side-effect free. Use `--task-cache-explain`
for a human-readable explanation; `--task-cache-stats` measures actual hits and
restored bytes during a run, excluding ordinary freshness skips.

`mise cache task <task> --json` inventories local entries. For requested eviction,
`mise cache clear --task <task>` removes that task's local entries while leaving
working outputs, other tasks and remote entries alone.

For suspected undeclared inputs on Linux, `cache.audit = true` uses `strace`.
Force an actual execution to trace it. `MISE_TASK_CACHE_AUDIT_REPORT=PATH` writes
all findings as JSON Lines (`task`, `kind`, `path`), replacing that report on
each invocation. The audit only warns; it does not prevent caching a successful
result and does not cover every external dependency. Missing strace or another
platform yields a warning and an unaudited run.

- [Freshness, cache controls and diagnosis](https://github.com/jdx/mise/blob/v2026.11.9/docs/tasks/caching.md)
- [Shared remote cache and credentials](https://github.com/jdx/mise/blob/v2026.11.9/docs/tasks/remote-cache.md)
- [Task configuration](https://github.com/jdx/mise/blob/v2026.11.9/docs/tasks/task-configuration.md)
