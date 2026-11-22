# Machine setup and integrations

Use only for a requested mise bootstrap, dotfiles or service workflow. Toolchain
installation alone uses `mise install` or `mise use`, not a full bootstrap.

Inspect the relevant declared state with `mise bootstrap status` or
`mise bootstrap plan`, and preview the intended part's changes. Bootstrap
applies declared packages, files, services, repositories, dotfiles, tools and
hooks; it is not transactional. Earlier changes remain if a later step fails.
Hooks and the bootstrap task run on every real run, even when declarative state
already matches. Rendering dotfile templates can execute code during inspection.

`--from` applies a bootstrap project from a separate checkout; `--adopt` adopts
global config or tracked dotfiles from a repository. Preserve the requested
mode and pinned ref. Limit `--only` or a part's `apply` to the authorized scope
when the user requests one component rather than the whole setup.

Use `mise dot files` (2026.11.5+) to inspect which paths a dotfile declaration
includes or excludes. In 2026.11.8+, `bootstrap plan` lists repositories and
hooks. A dirty repository can be `unknown` and fail `--detailed-exitcode`.
A planned hook alone does not count as a change. For experimental settings
plugins, preview separately with `mise bootstrap settings apply --dry-run`.
For macOS preferences shared with older clients, retain the older spelling
until every client understands `[bootstrap.settings.macos]`. Launchd agents
remain under `[bootstrap.macos.launchd.agents]`. [Bootstrap changes](https://github.com/jdx/mise/releases/tag/v2026.11.8)

Read the relevant upstream guide when one of these features is involved:

| Need                                  | Guide and decision that matters                                                                                                                                                                          |
| ------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Dotfile defaults or partial ownership | [Managed files](https://github.com/jdx/mise/blob/v2026.11.9/docs/dotfiles/managed.md): choose merge, tracked, template or symlink behavior to fit ownership; `merge = "missing"` fills only absent keys. |
| Local or machine-specific history     | [History](https://github.com/jdx/mise/blob/v2026.11.9/docs/dotfiles/history.md): `track-local` stays on the machine; variants and tracked groups affect which paths a machine owns.                      |
| Groups and tree deployment            | [Groups](https://github.com/jdx/mise/blob/v2026.11.9/docs/dotfiles/groups.md): inspect includes, exclusions, target paths and permissions before applying a directory tree.                              |

For project development services and shared server providers, use
[daemons](daemons.md). Host services applied through bootstrap stay in this workflow.

For backend integrations and OCI packaging, use [plugins and backends](plugins-and-backends.md).
For bootstrap updates and composed dotfiles:

- `bootstrap --update` without `--from`/`--adopt` fast-forwards
  the global config checkout, then applies it. A diverged checkout stops it;
  preview with `--dry-run` and account for the subsequent bootstrap effects.
- `--save-env` persists the selected environments for later
  bootstrap updates; use [configuration](configuration.md) for `env_sets`.
- Dotfile `depends` orders groups/entries in the same apply; cycles
  and unknown names fail. Inspect ownership before using JSONC/INI merges,
  seed-only `create_if_missing`, or fnox-backed entries.

- [Bootstrap and execution order](https://github.com/jdx/mise/blob/v2026.11.9/docs/bootstrap.md)
- [From versus adopt](https://github.com/jdx/mise/blob/v2026.11.9/docs/bootstrap/from-repository.md)
- [Apply planning](https://github.com/jdx/mise/blob/v2026.11.9/docs/cli/bootstrap/plan.md)
- [Bootstrap](https://github.com/jdx/mise/blob/v2026.11.4/docs/bootstrap.md)
