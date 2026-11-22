# Lockfiles

Inspect the relevant config, existing lockfile and effective settings first.
Preserve the project's strictness and platform policy. Do not disable global
strict mode or restrict all projects to the workstation platform to solve one
missing entry.

## Create, refresh and select scope

- `mise lock` explicitly creates or refreshes the active project root's lockfile
  without installing tools. Existing matching versions are preserved.
- `mise lock --bump [tool]` re-resolves fuzzy selectors without changing config
  declarations or installing tools. Exactly pinned versions remain unchanged.
- `mise lock TOOL@VERSION` locks an exact version and can rewrite `mise.toml`
  if it falls outside the configured request. Distinguish this from a refresh
  that must leave version declarations unchanged; inspect both diffs.
- `lockfile = true` in TOML enables automatic creation and maintenance. With the
  setting unset, existing lockfiles are updated but new ones are not automatically
  created. `MISE_LOCKFILE=1` retains that existing-file behavior and is not
  equivalent to explicit TOML `lockfile = true`.
- `--locked` / `locked = true` requires complete entries for the supported
  backend. It is not an offline-install guarantee. Backend URL and dependency
  graph requirements differ.
- `mise lock --global` targets global **and system** config lockfiles. Check the
  actual targets, including symlinks, before writing. `--local` targets local
  override lockfiles. Environment-specific configs have corresponding lockfiles.
- `--platform` explicitly selects targets. Without it, `lockfile_platforms` plus
  the current platform, existing lockfile platforms, or common defaults apply.
  Preserve the platforms needed by developers and CI.

Since 2026.11.8, a filtered lock fails if any named tool is unconfigured.
In 2026.11.9, `--bump` retains a newer locked SemVer when the remote list
lags. It also preserves an existing lock if every candidate is too recent for
`minimum_release_age`. With no existing lock, read the reported cutoff before
changing the declaration. [Lock resolution](https://github.com/jdx/mise/releases/tag/v2026.11.9)

A full lock refresh removes tools absent from active config by default. For a
lockfile intentionally shared by configs with different tools,
`lockfile_auto_prune = false` retains absent tools, not stale variants or graphs.
A tool-filtered refresh retains tools outside its filter. Keep this policy local
to the intended shared lockfile rather than changing every project's defaults.

Preview with `mise lock --dry-run` and use a tool argument to narrow an update
when appropriate. After a write, inspect the diff. Use `mise install --locked`
when an actual installation check is part of the request; a dry-run is only a
preview, not proof of a successful locked install.

## Missing entries and scope

Identify the owning config root, backend and platform before refreshing the
missing entry. If invocation-wide strict mode prevents the authorized refresh,
`MISE_LOCKED=0 mise lock ...` is a command-local override; it does not remove a
root's `[tool_config] locked = true` policy. Do not silently weaken that policy.

For an explicitly requested policy change, use global-only
`locked_scopes` (`project`, `global`, `system`) and root-specific
`[tool_config] locked = true`.

## Format compatibility

Lockfiles can refer to native dependency sidecars under `.mise/locks/`;
keep required sidecars with the lockfile. A missing graph or digest mismatch can
break strict installation even when the top-level tool version is present.
PyPI graph locking needs uv 0.12.10 or newer. Distinguish
version-only locking from replay of the complete dependency graph.
`mise lock --sidecars --json` inventories actual sidecar paths and their presence
without resolving or installing tools. Use it instead of assuming every config
layout or symlink places graphs under the project directory.
Use `mise lock --upgrade` only when a format migration is intended and all
consumers support it. Ordinary refresh preserves legacy format compatibility.

## Generation and verification

Automatic writes default to `lockfile_mode = "generate"`: rebuild from current
requests while reusing unchanged artifacts, including other platforms. Extra
metadata/download work during install can be lock generation, not another tool
install. The alternative `merge` mode updates entries as tools are installed
and is deprecated. `lockfile_mode` does not enable lockfile creation.

Locked URL entries require checksums by default; merge mode is exempt unless
`locked_require_checksum` explicitly requires them. Refresh the intended
lockfile to supply missing checksums rather than weakening verification.
Safe mode ignores project-controlled download URLs even for trusted projects;
backend resolution still checks locked checksums. Node/Python/Go can resolve
from their checksum entries. npm graphs are retained only when they use registry
sources with integrity hashes, without arbitrary URLs, Git sources or local paths.

New lockfiles use format 4. Existing files retain their format until
`mise lock --upgrade`; check that every consumer supports the target format.
npm provenance repository pins require format 4 and are recorded during
installation, not `mise lock`; see [security](security.md).

Project installs leave global lockfiles alone unless they install a global tool.
A root with `tool_config.locked` does not have its lockfile rewritten by install.
When `mise lock TOOL@VERSION` rewrites a config declaration, the lock entry binds
to the resulting request. Inspect both files together after an explicit change.

- [Lockfile behavior, backends, sidecars, scopes](https://github.com/jdx/mise/blob/v2026.11.9/docs/dev-tools/mise-lock.md)
- [Format and sidecar reference](https://github.com/jdx/mise/blob/v2026.11.9/docs/dev-tools/mise-lock-reference.md)
- [Lock command](https://github.com/jdx/mise/blob/v2026.11.9/docs/cli/lock.md)
- [Settings definitions](https://github.com/jdx/mise/blob/v2026.11.9/settings.toml)
- [Lock formats and generation](https://github.com/jdx/mise/blob/v2026.11.4/docs/dev-tools/mise-lock-reference.md)
