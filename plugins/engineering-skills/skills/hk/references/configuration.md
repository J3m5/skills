# Configuration and Pkl

## Select the file and layer

`HK_FILE` replaces normal discovery; relative paths are searched upward from the
working directory. Otherwise hk chooses one candidate in the first matching
directory, in this order: `hk.local.pkl`, `.config/hk.local.pkl`, `hk.pkl`,
`.config/hk.pkl`. To inherit shared steps, resolve `amends` from the override's
directory. Use `amends "./hk.pkl"` for sibling files or `amends "../hk.pkl"`
from `.config/hk.local.pkl` when the shared file is at the repository root.
A standalone override replaces the shared config. Even if `hk validate` succeeds,
check that `hk check --plan <file>` includes an expected inherited step for a
matching file. Keep personal overrides untracked.

Runtime settings resolve from defaults, user Pkl, project Pkl, Git configuration,
environment, then CLI. Local Git beats global/system Git. Scalars override; lists
such as exclude, skip_steps, skip_hooks and hide_warnings combine across sources.
Use `hk config explain <key>` for an effective runtime setting. `hk config sources` describes static precedence. `hk config dump` does not show the complete hook and step configuration.

The user file is normally `~/.config/hk/config.pkl`, following HK_CONFIG_DIR or
XDG_CONFIG_HOME. Its hooks/steps merge additively; project definitions win name
collisions. User config is independent of global Git hook installation.

## Extend existing checks

For a new setup, `hk init` generates matching imports; review its detected tools.
It does not install linters. Avoid `--force` on existing configuration.
`hk init --mise` also adds missing hk/pre-commit entries to mise configuration;
use it when that integration is intended, then inspect the diff.

Nonempty top-level steps supplies implicit check, fix, and pre-commit hooks.
Check reports problems; fix edits without staging; pre-commit fixes, stages, and
normally stashes unstaged work. Explicit hooks keep hook-level settings and
replace same-named inherited steps entirely. Remaining shared names still run.
Set `enabled = false` to disable an implicit hook.

Hook-only configurations remain supported. Without top-level steps, only explicit
hooks exist; adding a pre-commit step does not add it to check or fix. Preserve
existing shared mappings. Pkl object amendment keeps inherited properties;
assignment of a new mapping replaces it. Replacing a hook mapping alone does not
remove step names still inherited from top-level steps.

## Evaluation and shared packages

Pin schema and builtin imports together. For a project pinned to 2.13.0:

```pkl
amends "package://github.com/jdx/hk/releases/download/v2.13.0/hk@2.13.0#/Config.pkl"
import "package://github.com/jdx/hk/releases/download/v2.13.0/hk@2.13.0#/Builtins.pkl"
```

With hk 2.13, the embedded pklr 6 evaluator rejects some undeclared
properties and type constraint violations that pklr 5 accepted. Validate the
existing config with the target executable before adopting new schema fields.
[Evaluator compatibility](https://github.com/jdx/hk/releases/tag/v2.13.0)

Release builds are intended to seed the matching schema package. Verify offline
readiness with `HK_CACHE=0 HK_PKL_OFFLINE=1 hk validate` on the target build
and config. If it reports a missing package, check the URL and cache path in
the error, including imported packages and whether hk can write its package
cache. Even the embedded package may need seeding on disk. In a restricted
environment, verify cache access before requesting a network fetch.
`HK_PKL_OFFLINE=1`
restricts the evaluator's network access, independently of step commands. HK_CACHE=0
bypasses the resolved config cache for diagnosis without deleting package caches.

Shared configuration can use relative amends, pinned Git submodule contents or
versioned package modules. Plain HTTPS modules fetch again on evaluation. hk
does not resolve Pkl project `@dependency/...` imports; use full package URLs.
Publish a new version rather than replacing a cached URL. The pkl CLI helps with
package creation, not as an hk runtime fallback. For requested mirrors/proxies,
consult HK_PKL_HTTP_REWRITE, HK_PKL_CA_CERTIFICATES and proxy variables; rewrites
with credentials can expose them in errors.

Pkl evaluation can read local files/environment and fetch imports. Validation
evaluates configuration; plans can also evaluate executable conditions. Review
unknown configurations before treating these as passive inspection.

- [Configuration](https://github.com/jdx/hk/blob/v2.13.0/docs/configuration.md)
- [Pkl](https://github.com/jdx/hk/blob/v2.13.0/docs/pkl_introduction.md)
- [Environment controls](https://github.com/jdx/hk/blob/v2.13.0/docs/environment_variables.md)
