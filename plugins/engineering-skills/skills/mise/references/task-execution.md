# Task execution and diagnosis

Use existing task definitions and the requested verification scope. Definition
changes, dependencies and watch behavior belong to [tasks](tasks.md).

## Select the relevant work

Use existing tags to select checks by purpose without guessing their names.
TOML accepts `tags = "lint"` or `tags = ["test", "slow"]`; file tasks use
`#MISE tags=["test"]`. Templates add their tags to the task's tags.

```sh
mise tasks ls --tag lint --json
mise run --tag lint --tag test --dry-run
mise run --tag slow 'test:*'
```

Repeated tags match **any** tag, not all of them. With no task name, selection
uses `**`; an explicit name or pattern intersects that set and fails if no task
matches. Put run flags before the task name; flags after it go to the task.
Dependencies still run regardless of their tags. The JSON inventory includes
tags; `tasks ls --no-global` excludes global definitions and `--hidden` reveals
hidden ones. A filtered listing does not restrict the scope of a later run.

Quote task globs: `*` stays within one `:` group, while `**` crosses groups.
Separate independently requested tasks with `:::`; this schedules parallel work,
not sequential shell commands. Dependencies determine ordering.

With 2026.11.6+, `mise run --multi` offers a checklist in a TTY. For a scripted
run, name the tasks explicitly. To declare dependencies by tag in 2026.11.9+,
use `depends = [{ tag = "lint" }]`. The same selector works in `depends_post`
and `wait_for`. A list of tags matches any of them. Add `optional = true` when
zero matches are acceptable. [Task selectors](https://github.com/jdx/mise/releases/tag/v2026.11.9)

### Monorepos and affected runs

Use existing `monorepo_root = true` and `[monorepo].config_roots`; do not turn a
repository into a monorepo to narrow one ordinary test run. Explicit roots are
required by `mise install --monorepo` and `mise ls --monorepo`; filesystem task
discovery without them is deprecated. `mise tasks ls --all` inventories roots;
`//path:task` names a task from the monorepo root and `:task` from the nearest
config root. Quote patterns such as `'//...:test'` against shell expansion.
To select tags across projects, use `mise run --tag lint '//...:**'`.

For affected runs, inspect `mise tasks graph --explain` and preview with
`mise run --affected --affected-json <task>` or
`mise run --affected --affected-explain --dry-run <task>`. Selection depends on
the ecosystem workspace graph and source globs, not just changed directories.
The default includes the committed range plus staged, unstaged and untracked
unignored changes when the head is the checkout. Set the intended base/head;
use `--affected-committed` for a committed-only comparison, or the other source
flags for a working-tree-only run. A different head cannot include working-tree
sources. Affected selection needs no experimental setting.

Outside monorepos, `--affected` matches changed files against each task's
`sources`, its defining config and its file script.
Tasks without sources, or with argument-dependent `{{usage.*}}` sources, run
whenever something changed; nothing runs when nothing changed. Global tasks are
excluded from selection. Dependencies of selected tasks still run subject to
freshness checks. Monorepo selection keeps its workspace-graph behavior.

## Protect shared resources

A task's `lock = true` serializes that task across its repository's worktrees.
A named lock, or list of names, shares a resource across projects on the machine;
choose a resource-specific name. This is separate from dependency ordering.
Locks are acquired after dependencies and skip/cache checks, and released when
the holder exits. Waiting does not consume a jobs slot. Use `--lock-timeout`
or `task.lock_timeout` to bound waiting; task `timeout` starts after acquisition.
`mise tasks info` and `--dry-run` expose declared locks without running the task.

Since 2026.11.9, a named lock defaults to one slot. To share limited capacity,
declare e.g. `cpu = "8"` under `[settings.task.lock_pools]` and request
`lock = [{ name = "cpu", count = 4 }]` on a task. Acquisition is all-or-nothing,
with no fairness guarantee. Template a name with `{{ config_root | hash(len=8) }}`
when unrelated checkouts use separate resources. Inspect the rendered name with
`mise tasks info <task>`. [Lock pools](https://github.com/jdx/mise/releases/tag/v2026.11.9)

## Bound execution and interpret failures

`--timeout 5m` bounds the whole run; a task's own `timeout` still limits its
commands. Lock waiting has its separate timeout above.
By default, a failure stops running tasks and prevents new ones starting,
except eligible `depends_post` cleanup, and mise exits with the failed task's
status. Use `--continue-on-error` for intentionally independent checks: it also
allows tasks whose prerequisites failed to start, so it is unsuitable when a
failed prerequisite must block later work.

For compact terminal output and machine-readable evidence, use
[task results](task-results.md). For skipped work or restored artifacts, use
[task caching](task-caching.md); success alone does not prove a fresh execution.

## Compare another revision

`mise run --at REV <task>` uses that revision's own config and tasks in a
temporary detached worktree, including submodules, then removes the worktree.
Use it when a temporary comparison fits the host's worktree policy; an existing
managed checkout may be preferable. Ignored dependencies/build caches are absent.
`--at-setup CMD` runs before tasks, outside mise's environment and outside the
task timeout, so arrange tools/dependencies explicitly if setup needs them.
Trust comes from the main checkout; paranoid mode refuses this execution, and
`--yes` does not override it. A temporary worktree does not isolate external
services or side effects. Account for those before replaying a task at old code.

- [Run flags](https://github.com/jdx/mise/blob/v2026.11.9/docs/cli/run.md)
- [Selection and execution](https://github.com/jdx/mise/blob/v2026.11.9/docs/tasks/running-tasks.md)
- [Task locks and tags](https://github.com/jdx/mise/blob/v2026.11.9/docs/tasks/task-configuration.md)
- [Task inventory](https://github.com/jdx/mise/blob/v2026.11.9/docs/cli/tasks/ls.md)
- [Monorepo tasks](https://github.com/jdx/mise/blob/v2026.11.9/docs/tasks/monorepo.md)
- [Workspace graph and affected selection](https://github.com/jdx/mise/blob/v2026.11.9/docs/tasks/workspace-graph.md)
