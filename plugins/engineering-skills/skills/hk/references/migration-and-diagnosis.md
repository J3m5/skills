# Migration and diagnosis

## v1 to v2

hk v2 does not automatically rewrite configuration. Inspect tool/schema pins and
migrate only the requested repository/user scope, accounting for collaborators
and CI. Keep Config/Builtins imports on the adopted version.

- Removed hk.toml/yaml/yml/json become Pkl amending Config.pkl.
- Project .hkrc.pkl becomes hk.local.pkl; home .hkrc.pkl becomes XDG hk/config.pkl.
  Local overrides need an explicit shared-config amends.
- UserConfig.pkl becomes Config.pkl, environment becomes env, and runtime
  settings move from defaults to the root.
- hk generate becomes hk init; remove HK_PKL_BACKEND=pkl. The standalone
  evaluator is no longer a runtime dependency/fallback.
- Variant builtins become amended steps: gitleaks scan="staged", knip strict=true,
  pinact/pinact_update version="3". Byte-order-marker variants become
  Builtins.byte_order_marker; Regex uses Pkl's builtin Regex.

Top-level steps are optional; retain valid hook-only structures. Check staging:
pre-commit stages by default, ordinary fix/custom hooks do not. Validate, inspect
relevant plans and run affected checks; an executable upgrade does not mean older
imports support new fields.

## Diagnose the original invocation

Capture hk/Git versions, command, selected config and status; read the first real
error. For skipped work retain event/profiles/file flags and use --why <step>.
All-files checks compare behavior, not proof of a staged snapshot. Check
glob/exclude, conditions, workspace dirs, environment, skip settings and profiles.
hk validate warns about unknown properties, ineffective depends and unusable
globs; read warnings as well as exit status. Since 2.7, use
`hk validate --json` for machine-readable output. Add `--deny-warnings`
when warnings should fail the check. A 2.10+ hook `timeout` includes time
waiting on a stash lock and restores stashed changes when it interrupts the
hook. From 2.12 hk distinguishes external SIGTERM/SIGHUP from a step failure.
[Validation](https://github.com/jdx/hk/releases/tag/v2.7.0) · [Timeout](https://github.com/jdx/hk/releases/tag/v2.10.0)

Use hk config explain <key> for overrides. For evaluator-cache diagnosis use
HK_CACHE=0 HK_LOG=debug hk validate; avoid speculative cache deletion or installing
pkl. Builtins need available tools: check PATH, prefix, cwd and dependencies in
Git/editor environments before adding a different global linter.

For absent/duplicate hooks inspect Git entries, core.hooksPath and legacy scripts;
refresh only the requested scope. Consult partial-commit recovery for unexpected
index/worktree changes. Do not bypass failure with HK=0 or skip settings unless
that policy is requested.

For slowness use HK_TIMING_JSON=<path> and inspect total/per-step wall time;
parallel durations do not sum to total. Investigate broad globs, expensive tools,
unnecessary exclusive steps or internal parallelism before tuning jobs. Use
verbose/trace when useful and review logs before sharing them.

- [v2 migration](https://github.com/jdx/hk/blob/v2.13.0/docs/migration-v2.md)
- [Troubleshooting](https://github.com/jdx/hk/blob/v2.13.0/docs/logging.md)
- [CLI](https://github.com/jdx/hk/blob/v2.13.0/docs/cli/index.md)
