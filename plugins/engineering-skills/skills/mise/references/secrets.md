# Task-scoped fnox secrets

Use this reference for requested mise secrets integration or diagnosis.
The integration is experimental, requires fnox >= 1.39.0, and uses trusted
project `[secrets.fnox]` config. Global
and system declarations are ignored. Reading fnox's daemon requires fnox >= 1.43.0.
Check consumer versions before adding it.

Prefer a task's `secrets = ["KEY"]` or a one-off
`mise run --secrets KEY <task>` grant for the required keys. Grants apply to the
named tasks, not their dependencies or subtasks, which need their own grants.
Programs launched inside a granted task inherit its environment. Put mise flags
before the task name; flags after it are task arguments.

`mise secrets ls` inventories keys and grants without revealing values, and
`mise tasks validate <task>` checks grant configuration. Do not fetch or print
secret values to prove configuration. A dry task run does not fetch them.
Task output is redacted, but `mise exec --secrets KEY -- <command>` replaces
mise and does not redact the command's output. File secrets require tasks or
the appropriate fnox command, not `mise exec`.

Task-local `env` may compose literal text and `{{ secrets.KEY }}` references;
the reference itself grants access. More elaborate templating belongs in the
task script or fnox. `--secrets-all` broadens the grant to project-injectable keys;
use the user's intended grant scope, and avoid exporting all secrets through
`[env]` merely to repair one missing task grant.

Keys from personal/global or parent fnox config cannot be
granted by project task declarations, including values derived from those keys.
`--secrets-all` excludes them. An explicit one-off `--secrets NAME` can grant one
because the user names it. This distinction depends on fnox reporting each key's
source; older fnox versions may not expose that provenance. Keep personal keys
personal unless the user actually requests a project-owned definition.

- [fnox integration, inheritance and redaction](https://github.com/jdx/mise/blob/v2026.11.9/docs/environments/secrets/fnox.md)
- [Secret inventory](https://github.com/jdx/mise/blob/v2026.11.9/docs/cli/secrets/ls.md)
- [Personal keys and fnox versions](https://github.com/jdx/mise/blob/v2026.11.4/docs/environments/secrets/fnox.md)
