# Update mise itself

Identify `mise --version`, the resolved binary, and its installation channel.
Use `mise self-update --help` to check whether the build supports self-update.
Package-manager installations should be updated through that same manager;
command availability alone does not justify changing installation ownership.

For a self-managed binary, `mise self-update <version>` selects a requested
version and skips the minimum release age. Without a version, it selects the
newest eligible stable release: `--minimum-release-age` overrides
`self_update.minimum_release_age`, then `minimum_release_age`, else 24h.
`--force` does not bypass that delay. `--yes` accepts its confirmation.
Self-update can also update plugins: use `--no-plugins` when only the CLI update
is requested. Use `--force` only for an intended reinstall.

For a package-manager install, run its targeted mise update, not a broad system
upgrade. Verify the version of the resolved binary afterward. Use
[shell activation](shell-activation.md) only if resolution is stale.

`mise upgrade [tool]` updates managed tools, not mise itself; it is a separate
operation. Updating documentation does not require updating the CLI.

For requested automatic CLI updates, use `self_update.auto` (`true` or an
interval) and `self_update.check_duration`; the top-level `auto_update` aliases
are deprecated. This is a pre-command check, not a scheduler. The
interval is the minimum delay between eligible attempts, not a daily deadline.

A terminal attached to stderr and an eligible command
are required. CI, offline/prefer-offline mode and packager-disabled builds skip
it. Activation/prompt hooks, doctor, version, settings, self-update and the
background tool updater are excluded. Ordinary non-interactive agent commands
therefore do not maintain mise itself. Automatic CLI updates skip plugins.

For diagnosis, inspect effective settings and invocation conditions, then the
mtime of `$MISE_CACHE_DIR/auto-update-last-check`. It is written before the
network check and advances even if the attempt fails; it proves neither success
nor the earlier history. Failures are non-fatal and logged at debug level.
Compare release publication time with the minimum-age policy separately from
the check interval; an update notification does not prove an update attempt.

In agent sessions, 2026.11.7+ suppresses upgrade notices and hints. Use
`mise version --json` or `mise doctor` to check what the CLI reports.
[Agent output](https://github.com/jdx/mise/releases/tag/v2026.11.7)

The built-in `tool-update` service updates managed tools, not the mise binary.
If the user requests unattended CLI maintenance, a separate user-level schedule
can run the absolute mise binary with `self-update --yes --no-plugins`, retaining
release-age policy and recording results. Do not create that service merely to
diagnose the current behavior. See [tool updates](tool-updates.md).

- [Self-update](https://github.com/jdx/mise/blob/v2026.11.9/docs/cli/self-update.md)
- [Installation channels](https://github.com/jdx/mise/blob/v2026.11.9/docs/installing-mise.md)
- [Automatic-update gates](https://github.com/jdx/mise/blob/v2026.11.4/src/cli/self_update.rs)
- [Command exclusions](https://github.com/jdx/mise/blob/v2026.11.4/src/cli/mod.rs)
