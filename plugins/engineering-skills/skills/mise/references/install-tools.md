# Install, configure, or execute

## First project

If mise is missing, use the [installation method](https://github.com/jdx/mise/blob/v2026.11.9/docs/installing-mise.md) for the host. On Linux or macOS the official installer is `curl -fsSL https://mise.run | sh`. Keep an existing package-managed installation on its original channel. Ensure mise itself is on PATH (the installer binary is `~/.local/bin/mise` by default). Verify `mise --version` and enable [shell activation](shell-activation.md) if needed.

In an empty project, this `mise.toml` pins one tool and defines one task:

```toml
[tools]
jq = "1.8.1"

[tasks.answer]
run = "jq -n '6 * 7'"
```

Review the file, run `mise trust` if the project is untrusted, then `mise install`. From that directory, `jq --version` should print `jq-1.8.1` and `mise run answer` should print `42`. On another checkout of the same project, `mise install` reads the committed declaration. To change the pin later, use `mise use jq@<version>`, inspect the diff and rerun the task.

## Choose the operation

| Intent                       | Command                                   | Effect                                            |
| ---------------------------- | ----------------------------------------- | ------------------------------------------------- |
| Install the configured tools | `mise install`                            | Installs without changing version declarations    |
| Install one version          | `mise install <tool>@<version>`           | Does not activate an unconfigured tool            |
| Select in project config     | `mise use <tool>@<version>`               | Writes config and installs if needed              |
| Select as a personal default | `mise use -g <tool>@<version>`            | Writes user-global config and installs if needed  |
| Run once                     | `mise exec <tool>@<version> -- <command>` | May install; does not write tool declarations     |
| Run the selected tool        | `<command>`                               | Activation or a shim resolves the project version |

`mise x` aliases `mise exec`. No-config-write does not mean no side effects:
execution can install tools and the invoked command has its own effects.
Config-driven installation can update lockfiles.
Application package installation through `[deps]` is a separate workflow; use
[project dependencies](dependencies.md) for that configuration or diagnosis.

Check the [write target](configuration.md) for `use`, and consult
[tool selection](search-tools.md) when backend resolution is uncertain.
Verify the requested tool with `mise ls <tool>`, `mise which <executable>`, or
`<executable> --version` in the calling shell, as relevant. Tool names and executable
names need not match. If the user's shell still runs another executable, use
[shell activation](shell-activation.md).

Both `install` and `use` normally skip rebuilding versions already installed;
that does not imply skipping all hooks. A tool's
`postinstall = { run = "...", when = "always" }` runs on both commands even for
an existing install. Project `[hooks].postinstall` runs on `mise install` even
when no tool was installed. Distinguish these from backend/plugin installation
code before proposing a force reinstall. For a requested reinstall, inspect
the plugin/backend and use a targeted `mise install --force <tool>@<version>`
only when reinstallation and its effects are intended; an unqualified force
install can reinstall all configured tools.

## Install on first use

For requested on-demand project tools, set `lazy = true`; a bare `mise install`
skips them, while `mise install --include-lazy` or a named install preinstalls
them. Explicit backends need `lazy_bins` to name the commands that get bootstrap
shims. After hand-editing a lazy declaration, `mise reshim` updates them. The
first command can install the tool and its missing tool dependencies, even with
`not_found_auto_install` off.

Use a tool stub when an executable in the repository should carry one tool's
definition, version and optional download metadata. When a repository launcher is needed only to supply a missing tool environment, a simple `mise exec` wrapper suffices. Stubs are not discovered by ordinary
`mise install`, and first execution can install a tool. They need mise on PATH
unless generated with `--bootstrap`, which can install mise itself. Exact pins
or locked stubs provide reproducible selection; a floating `latest` does not.
Consult the stub guide for lockfile scope and cross-platform launch behavior.

## Installation identity and cache

The identity layout requires `experimental = true`; it is the
Windows default when experimental mode is enabled. Elsewhere select it with
`install_layout = "identity"`. Several artifacts or option variants of one
version can coexist. Use `mise where`, `mise which`, and `mise installs ls`
instead of constructing an install path. `mise installs select` changes the
machine-wide selection for matching unlocked requests; a project's artifact pin
keeps its own installation. Enable or migrate layouts only when requested;
`mise installs migrate --dry-run` previews migration and the real migration may
reinstall or move files. Consult compatibility before downgrading.

For CI cache work, prefer `$MISE_CACHE_DIR/downloads-cas` with pinned checksums
and locked installs over trusting restored executable directories. mise rehashes
cached downloads, but cached extracted installs are not reverified by that check.
`download_cache_max_size` limits the download cache (2GiB by default; `0` is
unlimited); `always_keep_download` is deprecated. Do not change cache policy for
an ordinary tool install.

An npm package with no executables can install successfully while producing no
shims; mise warns about that. Check that the package supplies the requested CLI
rather than repeating the installation or treating an application library as a tool.

`mise uninstall --project` previews with `--dry-run` and selects
the nearest project's requested versions, excluding parent/global declarations.
The installations themselves are shared: removing one can affect another project
that uses the same version. This is not project dependency cleanup.

- [Install](https://github.com/jdx/mise/blob/v2026.11.9/docs/cli/install.md)
- [Use and write targets](https://github.com/jdx/mise/blob/v2026.11.9/docs/cli/use.md)
- [Exec](https://github.com/jdx/mise/blob/v2026.11.9/docs/cli/exec.md)
- [Lazy tools and shim behavior](https://github.com/jdx/mise/blob/v2026.11.9/docs/dev-tools/shims.md)
- [Tool stubs, locking and bootstrap](https://github.com/jdx/mise/blob/v2026.11.9/docs/dev-tools/tool-stubs.md)
- [Tool postinstall options](https://github.com/jdx/mise/blob/v2026.11.9/docs/dev-tools/index.md)
- [Project install hooks](https://github.com/jdx/mise/blob/v2026.11.9/docs/hooks.md)
- [Identity layout and compatibility](https://github.com/jdx/mise/blob/v2026.11.9/docs/dev-tools/install-layout.md)
- [Download cache and settings](https://github.com/jdx/mise/blob/v2026.11.9/settings.toml)
