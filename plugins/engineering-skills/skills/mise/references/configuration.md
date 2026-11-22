# Configuration and saved vars

Inspect `mise config ls` in the target directory and the relevant config before
writing. Global personal defaults normally live in `~/.config/mise/config.toml`;
XDG/MISE overrides and symlinks can change the actual destination.

`mise use` normally writes the lowest-precedence file in the nearest directory
with a supported config, for example `mise.toml` rather than `mise.local.toml`.
It can therefore modify an ancestor's config. In the home directory it targets
global config. Use `mise use --path <file> <tool>@<version>` when a particular
file is required, `-g` for requested user-global defaults, or `--env local` for
a local override. Inspect the resulting diff and effective selection.

`mise config get <key>` reads one file, not the entire merged configuration.
Use `mise settings get <key>` for an effective setting and
`mise settings ls --json-extended` when its source matters. `mise settings set`
writes globally by default; use `--local` for a project setting.
`mise config --tracked-configs` lists tracked files; ordinary `config ls` lists
files in use.

Global tool writes can follow `settings.write_targets.tools` into a loaded
`conf.d` fragment. Existing declarations stay in their declaring file; an update
spanning several global files requires `--path`. Do not assume `use -g` writes
`config.toml` merely because that is the usual default.

`mise config explain [KEY] --file PATH --json` describes keys,
flags unknown/deprecated keys and reads plain TOML even when config loading fails.
It explains one file, not the effective merged value. Global `config.override.toml`
and environment-specific override files outrank project config. Inspect them when
project edits seem ineffective; do not introduce a global override for one project.
`--override` explicitly targets them; `MISE_GLOBAL_CONFIG_FILE` disables their loading.

## Config composition and discovery

For requested formatting, `mise fmt` rewrites configs in the current directory;
`--all` expands to every loaded config, including ancestors/global files.
Use `mise fmt --check` for a non-writing CI check, or `mise fmt --stdin` to
preview one document. The formatter writes TOML 1.1 syntax; check other consumers
before adopting its output in a shared file. Formatting does not validate task
behavior; use `mise tasks validate` for task-definition diagnostics.

`conf.d` folders are self-contained config roots, including relative paths and
task working directories. Check the root of a symlinked fragment before editing.
Local `include` paths resolve from the including file; included values rank below
its own values and share its root and lockfile. Includes cannot nest or declare
`[settings]` or `[tasks]`; task catalogs use `task_config.includes` instead.
Remote includes follow the including file's trust and cache; paranoid mode
requires an immutable commit or digest and refuses local includes.
`include` accepts `zip::https://...`, loading `mise.toml`
at the archive root. A URL does not pin contents: refresh follows the branch-like
cache policy, and paranoid mode rejects ZIP config includes. Task ZIP includes
load file/TOML tasks and remain experimental; prefer immutable Git/OCI sources
when reproducible shared configuration is required.

Discovery settings such as `env` and `ceiling_paths` belong in `.miserc.toml`
or their supported environment overrides, not `[settings]` in `mise.toml`.
Use `.miserc.local.toml` for a requested checkout-specific override; check global
`miserc.local.toml` too when explaining unexpected discovery.

`MISE_GLOBAL_CONFIG_FILE` and `MISE_SYSTEM_CONFIG_FILE` each load the named
file without its environment variants or local overlays. Point at the variant
itself when selecting it deliberately. [Config discovery](https://github.com/jdx/mise/releases/tag/v2026.11.9)

`[env_sets]` in `miserc.toml` names ordered environment lists,
selected by `env`, `-E` or `MISE_ENV`. Expansion is one level and deduplicates;
project files cannot redefine globally/system-defined sets. Project discovery
cannot silently drop globally selected environments. Use an
explicit invocation selection when the requested run needs a different set.

For env files, scripts, PATH precedence and virtualenvs, use
[environments](environments.md). This reference owns config composition and write
targets; deployment overlays still follow the config hierarchy.

## Saved vars

`[vars]` feeds templates, not the process environment. `mise vars prompt` asks
for missing per-machine answers; `mise vars prompt NAME=VALUE` saves without a
terminal, and `mise vars unset NAME` forgets one. Answers are stored in
`$MISE_STATE_DIR/vars.toml`, keyed by name across projects, rather than in config.
Inspect the resolved value and its source before replacing a saved answer.
Only prompt commands ask; ordinary tasks use saved values/defaults or fail for
missing required values. `bootstrap --dry-run --prompt-vars` still saves answers.
For task discovery and changes, use the [task reference](tasks.md).

## Exact semantics

- [Config precedence and write targets](https://github.com/jdx/mise/blob/v2026.11.9/docs/configuration.md)
- [Formatting and scope](https://github.com/jdx/mise/blob/v2026.11.9/docs/cli/fmt.md)
- [Environment-specific configuration](https://github.com/jdx/mise/blob/v2026.11.9/docs/configuration/environments.md)
- [Settings guide](https://github.com/jdx/mise/blob/v2026.11.9/docs/configuration/settings.md)
- [Settings definitions](https://github.com/jdx/mise/blob/v2026.11.9/settings.toml): search a
  setting's TOML section for its type, default, environment variable and constraints;
  the site's dynamic settings table is not rendered in the Markdown source.
- [Config vars and saved answers](https://github.com/jdx/mise/blob/v2026.11.9/docs/configuration/vars.md)
- [Config precedence and includes](https://github.com/jdx/mise/blob/v2026.11.4/docs/configuration.md)
- [Environment sets](https://github.com/jdx/mise/blob/v2026.11.4/docs/configuration/environments.md)
