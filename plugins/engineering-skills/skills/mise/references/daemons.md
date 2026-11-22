# Development daemons

Use for project processes managed by mise and supervised by pitchfork. Host
services installed through bootstrap use [machine setup](machine-setup.md).

## Establish the service and its owner

Check the effective project config and profile, mise's version, and pitchfork's
version when available. Daemons need `experimental = true`, trusted project
config, safe mode off, and pitchfork 2.25.0 or newer. Proxy,
task-backed daemons, templated commands and Windows features have higher minimum
versions; use the upstream requirements matrix for the requested feature.
Start/restart/register and daemon-dependent tasks can install missing tools,
including pitchfork; inspection with `mise daemons ls --json` does not register
daemons or start a supervisor.

Identify whether the daemon is a custom command, container image, preset, mise
task, project reference or shared provider before changing it. Edit the owning `[daemons]`
declaration, not the generated pitchfork config. A higher-precedence declaration
replaces the entire daemon rather than merging its keys.

## Start and diagnose the intended processes

Inspect `mise daemons ls --json`, `mise daemons status <name>`, and the relevant
logs. `logs` needs a running supervisor; its absence is distinct from an
application error. Check command/tool resolution, the owner's environment,
readiness checks, dependencies and ports before reinstalling or restarting.

Start a named daemon with `mise daemons start <name>` and confirm it becomes
ready. Starting also starts its dependencies. Without names, start uses the
`default` group if declared, otherwise every project daemon; stop without names
stops every registered project daemon. Use the intended names or groups.
An updated declaration takes effect on the next start/restart. Stop the project's
daemons and leave its shell sessions before changing its active profile.

For a shell command, use `exec` so the server receives stop signals. Configure
readiness on the daemon (`ready_port` or `ready_cmd`), not merely on its task.
A task's `daemons` starts services before its body; they remain running after
the task exits, and `--skip-deps` skips that startup. For `task = "..."` daemons,
put service dependencies on the daemon: the task's own daemon requirements are
skipped to avoid recursion. Task-backed daemons cannot run tasks or dependencies
with mise secrets grants; use the matching integration contract rather than
assuming a foreground task's grants carry over.

## Readiness, ongoing health and retries

Probe fields are forwarded to pitchfork. Check that the selected pitchfork
supports the required probe forms. Configure them on the owning daemon, not on
a `project` or `provider` reference, which accepts only its reference keys.

Readiness gates startup and dependent tasks/daemons. Ongoing health probes detect
a running process that stops doing useful work. Choose an application endpoint
or client command when an open socket does not prove the service is usable.

| Readiness field | Successful result                                                     |
| --------------- | --------------------------------------------------------------------- |
| `ready_http`    | An HTTP response with an accepted status; defaults to any 2xx.        |
| `ready_cmd`     | A command exits with status 0.                                        |
| `ready_port`    | A TCP connection to 127.0.0.1 succeeds.                               |
| `ready_output`  | A regex matches stdout or stderr.                                     |
| `ready_delay`   | The process stays alive for a delay, only when no other check exists. |

With several readiness checks, the first success marks the daemon ready: they
are alternatives, not cumulative requirements. Use one `ready_cmd` combining
conditions when all must pass. The object forms accept an overall `timeout`;
shorthand checks can wait indefinitely while the process stays alive. When all
checks expire, startup fails with code 124; one unbounded check keeps it waiting.
The HTTP object's timeout limits total readiness polling, not one request.
`ready_delay` is an integer number of seconds on the daemon (default 3); increasing
it does not extend other checks. `oneshot = true` waits for successful process
completion and cannot combine with `ready_*` or `health_*` fields.

For continuous probes, choose `health_http`, `health_cmd`, or `health_port`.
Their object forms accept `interval`, per-probe `timeout`, and `retries` for
consecutive failures before termination. Defaults are a 10s interval, 3 failures,
and a timeout of 10s for commands or 5s for HTTP/TCP. A successful probe resets
the failure counter. Multiple probe kinds must all pass; any failure makes the
cycle unhealthy. Health checks begin during startup, so give slow services a
failure budget that tolerates initialization; readiness does not pause them.

The daemon's separate `retry` controls restarts after startup/runtime failure,
including health-triggered termination: false/0 is no restart, an integer allows
that many retries after the initial attempt, and true is unlimited. A health
check without `retry` can stop an unhealthy service without restarting it.
Choose bounded or unlimited retries from the intended development workflow;
inspect the failing probe and logs rather than hiding a persistent fault.

For an application serving port 3000 with a `/health` endpoint:

```toml
[daemons.api]
run = "exec npm run dev"
port = 3000
ready_http = { url = "http://127.0.0.1:3000/health", status = [200], timeout = "30s" }
health_http = { url = "http://127.0.0.1:3000/health", status = [
  200,
], interval = "10s", timeout = "5s", retries = 3 }
retry = 3
```

Adapt the endpoint and port to the application and the worktree's resolved port;
setting `port` does not make an application listen there. Avoid copying fixed
probe URLs into a daemon using automatic ports.

mise wraps `ready_cmd` and `health_cmd`, including an object's `run`, with
`mise x` so probes receive project tools and `[env]`, unless `mise = false`.
An argument array requires pitchfork >= 2.30.0 and runs without shell expansion;
use a shell string when the command needs `$PORT`, pipes or other shell syntax.
Probe arrays preserve argument boundaries, not shell substitutions.

Global probe defaults belong to pitchfork's `[settings.supervisor]`, not mise's
`[settings]`: `health_check_interval`, `health_check_retries`, `health_cmd_timeout`,
`health_http_timeout` and `health_port_timeout`. Prefer daemon-level overrides for
one service; changing supervisor defaults affects other managed services.
`mise doctor project` is an explicit, one-off diagnostic, not a readiness gate
or continuous monitor; see [project diagnostics](diagnostics.md).

## Worktrees and sharing

Inspect resolved IDs, ports and URLs with `mise daemons ls --json` and
`mise daemons urls --json`. Preserve per-worktree namespaces and data isolation.
A custom/task automatic port needs `{ auto = true, base = ... }`; `"auto"`
alone is for presets. Fixed ports must be free. Disabling namespace suffixes
shares IDs and can cause collisions; literal qualified dependencies do not
follow a worktree suffix.

A `project` reference uses the other project's tools, environment and data;
trust is not granted automatically and preset connection variables are not
exported into the referring project. A global shared provider shares the server,
with separate checkout databases/accounts, and has different lifecycle and data
ownership. Shared providers are unsupported on Windows.
Use the sharing guide when choosing between these models.

From 2026.11.6, custom `run` and `task` daemons also accept a `ports` table.
Read each assigned port from `<DAEMON>_<NAME>_PORT` in the process. An
automatic named port needs its own base. For a collision across worktrees,
2026.11.7+ identifies the other checkout. [Custom daemon ports](https://github.com/jdx/mise/releases/tag/v2026.11.6)

Preset named ports accept `{ auto = true, base, stride }`
with their own base and per-worktree allocation. Monorepo tasks run
from the root receive their subproject daemon variables; explicit task/project
environment values still take precedence. Status/log/stop/prune also resolve
mise's pitchfork without requiring an incidental project tool pin.

## Container daemons (experimental)

Use `image` instead of `run`, `task` or `preset`; select Docker/Podman through
`runtime`. Inspect the existing runtime and image availability before starting.
mise does not provision the runtime service or build images. Containers run in
the foreground with `--rm`; stopping removes the container, not persisted data.
Use `data_mount` with a per-checkout `data_dir` when data must survive.

`port` is the host port; `container_port` is the service's internal port.
`ports` adds named published ports, including automatic per-worktree allocation.
Published ports are TCP on loopback only; container daemons are unsupported on
Windows in the checked contract. An image has no default port for bare `"auto"`.

A published port can open before the application is ready. Prefer an application
probe through `ready_cmd`, using `{{ runtime }}` and `{{ container }}` when needed;
`health_cmd` supports those placeholders too. `runtime` is shell text: use a
shell command or explicit shell script argument, not a bare argv executable.
`init` runs on the host. For databases/brokers that do not speak HTTP, set
`proxy = false` instead of assuming the default proxy is appropriate.

## Persistent data and cleanup

Stopping a daemon does not reset its data. Locate `data_dir` and `state_dir`
from `mise daemons ls --json`; changing `data_dir` does not move existing data.
Stop before copying or migrating it, and preserve data across major database
upgrades using the database's migration tools. Two live instances must not use
one data directory. Removing a worktree can delete data stored inside it.

For requested cleanup of deleted projects, preview `mise daemons prune --dry-run`.
Pruning stops/unregisters affected daemons and deletes their managed state and
default data, not just cache. A provider's data belongs to all its consumers;
resetting one checkout's database must not delete the provider's data directory.
Treat database resets and data removal as distinct from a routine restart.

- [Declarations, requirements and lifecycle](https://github.com/jdx/mise/blob/v2026.11.9/docs/daemons.md)
- [Preset behavior and platforms](https://github.com/jdx/mise/blob/v2026.11.9/docs/daemons/presets.md)
- [Ports, proxy and worktrees](https://github.com/jdx/mise/blob/v2026.11.9/docs/daemons/worktrees.md)
- [Project references and shared providers](https://github.com/jdx/mise/blob/v2026.11.9/docs/daemons/sharing.md)
- [Data locations, migration and cleanup](https://github.com/jdx/mise/blob/v2026.11.9/docs/daemons/data.md)
- [Task integration](https://github.com/jdx/mise/blob/v2026.11.9/docs/tasks/task-configuration.md)
- [Readiness contracts](https://github.com/jdx/pitchfork/blob/v2.30.1/docs/guides/ready-checks.md)
- [Health probe contracts](https://github.com/jdx/pitchfork/blob/v2.30.1/docs/guides/health-checks.md)
- [Restart policy](https://github.com/jdx/pitchfork/blob/v2.30.1/docs/guides/auto-restart.md)
- [Container lifecycle and probes](https://github.com/jdx/mise/blob/v2026.11.4/docs/daemons/containers.md)
