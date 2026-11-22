# Select a tool and backend

Use read-only discovery before installing:

```sh
mise registry <tool>
mise search <query>
mise ls-remote <tool-or-backend>
mise latest <tool-or-backend>
```

For package-registry discovery, `mise search npm:<query>` (or another supported
backend prefix) scopes the search; `--all` searches beyond the mise registry.

Prefer the registry shorthand when it provides the requested distribution.
Preserve an explicit source already chosen by the user or project. An explicit
backend is useful when a tool is absent from the registry or a different source
or install behavior is required; an arbitrary installation failure is not proof
that the backend should change.

Examples include `npm:pyright`, `cargo:starship`, `github:owner/repo`, and
`pypi:black`. Current documentation calls the Python CLI backend `pypi`; `pipx:`
remains supported, so existing entries need not be migrated. The two spellings
produce distinct tool identities and can have distinct install paths and lock entries. Confirm
support before using newer spelling on an older CLI. `ubi` is deprecated; prefer
`github` for new GitHub-release installs. Do not replace a working explicit
backend merely because another exists.
The spinel backend is experimental; read its guide only for a
requested use or diagnosis rather than choosing it as a routine fallback.

Backend names are not interchangeable distribution guarantees. In particular,
`pypi:owner/repo@latest` selects the latest GitHub release, falling back to the
default branch only when no releases exist. Explicit Git URLs with `latest`
resolve the default branch's HEAD instead. `npm:` Git sources also use the
default branch for `latest`; do not transfer one backend's rule to another.
Python Git sources may use `#subdirectory=...`; it is part of the tool identity,
and versions still come from the repository rather than the subdirectory.

For Java, the default distribution is Temurin. Preserve an
existing vendor requirement; check available vendor-qualified versions rather
than treating a bare Java version as a vendor-independent selection.

Once selection is clear, continue the requested installation using
[install and execute](install-tools.md); discovery alone does not authorize one.

If the project selects Go from `go.mod` or `go.work`, enable that source with
`mise settings add --local idiomatic_version_file_enable_tools go`. mise reads
`toolchain goX.Y.Z`, or an exact `go X.Y.Z` when no toolchain is declared.
A minimum such as `go 1.21` alone supplies no version. An active `go.work` takes
precedence even inside a module. With `GOWORK=off`, mise reads `go.mod` instead.
Check the selected version and source with `mise ls --current --json go`.
Projects with an explicit Go pin in `mise.toml` can keep using it.

`cmake_minimum_required` does not select a runtime. Diagnose
missing selection before installing a different runtime or changing a project's
compatibility minimum.

- [Registry](https://github.com/jdx/mise/blob/v2026.11.9/docs/registry.md)
- [Backend selection](https://github.com/jdx/mise/blob/v2026.11.9/docs/dev-tools/backends/index.md)
- [Python CLI backend](https://github.com/jdx/mise/blob/v2026.11.9/docs/dev-tools/backends/pypi.md)
- [Experimental spinel backend](https://github.com/jdx/mise/blob/v2026.11.9/docs/dev-tools/backends/spinel.md)
  For private `github:` tools, `versions_host_exclude` (2026.11.8+) accepts
  case-insensitive `owner/repo` globs. Matching repositories use GitHub directly
  for version discovery. Other repositories can still use mise-versions.
  [Repository lookup](https://github.com/jdx/mise/releases/tag/v2026.11.8)

- [Go toolchain selection](https://github.com/jdx/mise/blob/v2026.11.9/docs/lang/go.md)
