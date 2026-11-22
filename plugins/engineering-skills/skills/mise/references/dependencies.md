# Project dependency automation

Use for requested `[deps]` configuration or diagnosis. This feature is
experimental. `[tools]` installs the package manager;
`[deps]` invokes it for application packages. Keep the existing manager,
lockfile policy and project installation scripts rather than changing them
merely to adopt mise's automation.

## Inspect before running installers

`mise deps install --list` shows configured providers and their tracked files.
Providers are explicit, not automatically detected. Most built-ins need their
lockfile to become active; a missing required input leaves them inactive.
Preview with `mise deps install --dry-run`, or explain one provider with
`mise deps install PROVIDER --explain`. Explain runs no installer and exits 0
only when the provider is fresh; stale or inactive is non-zero, not necessarily
a failed installation.

Built-in commands are ordinary installs, not necessarily frozen-lockfile
commands. Preserve requested reproducibility, for example `run = "npm ci"`
when that is the project's policy. A pip provider does not create or choose
a virtualenv; set up the intended [environment](environments.md) first.

## Freshness and scope

Freshness tracks source contents, required outputs and the effective command
(including env/dir), not upstream releases or every installed package. On a
built-in provider, `sources`/`outputs` replace its defaults rather than adding
to them. Resolve paths from the provider's config root and `dir`; include all
inputs that actually change its result.

A custom provider with outputs but no sources stays fresh while its outputs
exist, even if its command changes. With neither sources nor outputs, it runs
every time. Use `--force` for an intended rerun, not as a default workaround for
incorrect tracking. `depends` orders configured providers; it does not enable
one or install its package manager.

`auto = true` runs a stale provider before `mise exec` and `mise run`; an
activated shell only warns. `--no-deps` skips automatic providers for one
invocation. It is different from a task's `--skip-deps`. This automation can
run install/lifecycle scripts, so enable it only in the requested scope.

Monorepo provider runs need explicit config roots. Use root-qualified provider
names and `--only`/`--skip` to target the intended packages rather than invoking
every workspace installer. Custom providers can also represent requested
code generation; preserve an existing build system's ordering where it already
owns that step.

- [Providers, commands and freshness](https://github.com/jdx/mise/blob/v2026.11.9/docs/dev-tools/deps.md)
- [Install, explain and selection](https://github.com/jdx/mise/blob/v2026.11.9/docs/cli/deps/install.md)
