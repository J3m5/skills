# Updates to managed tools

`mise upgrade <tool>` updates a managed tool; `mise self-update` updates mise.
For global/system requests, use `mise outdated --global <tool> --json` and
`mise upgrade --global <tool>`. These ignore project config,
lockfiles, environment and `MISE_<TOOL>_VERSION` overrides, even from inside a
project. `--global --bump` rewrites global declarations; do not use it for a
request that should stay within the existing constraints.

Tools with their own updater should update through mise when mise owns the
installation. Overwriting an install in place can make its directory, reported
version and lockfile disagree. For updater integration work, read the dedicated
upstream guide; an already-running process keeps its inherited executable and
PATH until it is restarted or deliberately resumed through `mise exec`.

## Automatic updates when requested

A global tool can set `auto_update = true` or a check interval such as `"6h"`.
`tool_update.global_auto` sets a global default; a tool's own value wins and
`false` opts it out. A shim or `mise exec` checks the launched tool before it
runs. With shell activation, a prompt starts due checks in the background;
the new version becomes active after completion and an environment refresh.
Use `mise doctor` to inspect failed background updates.

Project-selected tools, exact version pins, tasks, CI, offline mode and strict
locked mode do not auto-update. Updates stay within the global version request
and can move its global lock entry. The check interval and `minimum_release_age`
both delay eligibility. Do not bypass release-age policy to make an update
appear immediately.

If a user requests updates while no shell is active, the bootstrap
`tool-update` service is an option. Creating a service is a separate machine
setup operation; an ordinary tool update does not require enabling one.

- [Automatic tool updates](https://github.com/jdx/mise/blob/v2026.11.9/docs/dev-tools/index.md)
- [Upgrade scope](https://github.com/jdx/mise/blob/v2026.11.9/docs/cli/upgrade.md)
- [Self-updating tool integration](https://github.com/jdx/mise/blob/v2026.11.9/docs/dev-tools/self-updating-tools.md)
- [Bootstrap services](https://github.com/jdx/mise/blob/v2026.11.9/docs/bootstrap/services.md)
