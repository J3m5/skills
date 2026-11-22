# Project environments

Use for mise-managed values, env files, scripts or Python environments. Config
write targets and overlay precedence belong to [configuration](configuration.md);
shell activation and executable conflicts use [shell activation](shell-activation.md).

## Values and files

`[env]` sets process variables; `[vars]` supplies template values without exporting
them. `false` unsets an env variable, so use a string for literal `"false"` or
`"0"`. `default` preserves a non-empty existing value. `required` checks a value
supplied by the environment or another config, and can include help text; it
cannot be combined with `value` or `default`. A missing required value fails
commands but only warns at an activated shell's prompt.

`_.file` loads env files. Missing matches are optional, and file values can replace
ambient variables. Extensions matter: `.json`, `.yaml` and `.toml` are structured
formats, while `.yml` is treated as dotenv. Values from those
structured files are literal unless `expand = true`. Use the env guide for
expansion and ordering rather than assuming shell evaluation. Entries that need
resolved tool values use `tools = true`; ordinary `[env]` resolves before tools.

Since 2026.11.6, `mise env --dotenv` quotes values as needed for reloading
with `_.file`. Check the consumer before using that output as an interchange
format. Docker `--env-file`, for example, retains literal quotes.
[Dotenv round trips](https://github.com/jdx/mise/releases/tag/v2026.11.6)

`_.source` runs a script with Bash regardless of its shebang, each time mise
computes the environment. Keep it repeatable and inspect its effects before
using it to load values. Source scripts can prepend PATH entries; mise ignores
other PATH rewrites. `_.path` prepends by default;
an entry can set `position = "append"` for fallback paths without
shadowing managed tools. `mise env --paths` inspects managed paths
without dumping unrelated environment values.

`_.file` supports `find_up`, searching from the config root. A single entry with
several names chooses the nearest directory,
then the later matching name there. Separate entries search independently and
can let a parent file override a nearer one; choose that behavior deliberately.

Verify a targeted value in the process that consumes it. To inspect a configured child from an unactivated shell, use `mise exec`. Avoid dumping unrelated secret values.
`MISE_*` variables generally configure the current process before `[env]` loads,
so setting them there does not reconfigure that mise process. For encrypted env
files use the SOPS guide; fnox task grants use [task secrets](secrets.md).

`env_cache_redacted` is an opt-in performance tradeoff, not an
ordinary repair for slow commands: cached secret values are encrypted on disk
with a key inherited by the activated shell's children. Keep it off unless the
requested caching workflow accepts that exposure; redaction is not isolation.

## Python virtualenvs

Use `_.python.venv` for existing environments or requested creation (`create = true`).
For uv projects, `python.uv_venv_auto` uses `"source"` or `"create|source"` and
requires an existing `uv.lock`; its environment follows `UV_PROJECT_ENVIRONMENT`.
Preserve the project's existing environment owner instead of creating another
venv beside one uv manages. Creation is not package installation; `[deps.uv]`
or the package manager performs that separate step.

Activation applies in an activated shell, `mise exec` and tasks; shims alone do
not put the venv on the shell's PATH. Verify `sys.executable` and `VIRTUAL_ENV`
in the affected process. A uv-created venv has no pip unless seeded; do not infer
failure from pip's absence. Tool-dependent `UV_PYTHON` can select mise's interpreter
when uv otherwise chooses its own; read the Python guide for the matching setup.

- [Values, files, sources and PATH](https://github.com/jdx/mise/blob/v2026.11.9/docs/environments/index.md)
- [Python environment mechanisms](https://github.com/jdx/mise/blob/v2026.11.9/docs/lang/python.md)
- [Encrypted SOPS env files](https://github.com/jdx/mise/blob/v2026.11.9/docs/environments/secrets/sops.md)
- [Environment directives](https://github.com/jdx/mise/blob/v2026.11.4/docs/environments/index.md)
