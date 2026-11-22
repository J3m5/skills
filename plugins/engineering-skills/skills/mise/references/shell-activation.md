# Shell activation and shims

Run the tool by name when activation or shims select the project version. This applies inside mise tasks and in scripts or CI that already inherit the right environment. If unsure, compare `command -v <executable>`, `mise which <executable>` and the version printed by the direct command. A shim and the binary it dispatches to normally have different paths.

Activation updates the calling shell's PATH and project variables. A shim selects the tool for its working directory and supplies the project environment to that child. The shim cannot export variables into the parent shell. Use `mise exec -- <command>` for a process that needs the project environment but lacks it, or `mise exec <tool>@<version> -- <command>` for a one-off override. For a declared workflow, use `mise run <task>`.

## Choose the repair that matches the cause

- Missing shims after another installer adds binaries: `mise reshim`.
- A stale Bash command hash: `hash -r`.
- Interactive Bash activation: `eval "$(mise activate bash)"`.
- Interactive Fish activation: `mise activate fish | source`.
- Bash shims: `eval "$(mise activate bash --shims)"`. Verify the actual caller when an IDE or CI does not load interactive startup files.

`reshim` does not fix an earlier conflicting PATH directory or stale activation.
Inspect PATH ordering if another tool manager wins. Test the actual affected
shell mode; do not require a login/interactive/automation matrix for every config
edit. An agent subprocess cannot change the user's already-open terminal.

If shell startup files must change, preserve the user's activation strategy and
check the relevant startup file and scope first. After a mise CLI update, check
which mise binary is resolved before adding activation changes.

When command-not-found handling installs an undeclared tool, check
`not_found_auto_install_registry`. It is opt-in and can add a uniquely matched
registry tool to global config. A shim can also use `not_found_system_fallback`
and run a system binary when a managed install is missing. Diagnose these
settings before proposing reinstallations or new global defaults.

On Unix, `shims.fallback_to_installed` (2026.11.7+, default false) can select
the latest installed version when no config declares the tool. A missing
configured version still fails. [Shim selection](https://github.com/jdx/mise/releases/tag/v2026.11.7)

- [Activation](https://github.com/jdx/mise/blob/v2026.11.9/docs/cli/activate.md)
- [Shims and non-interactive environments](https://github.com/jdx/mise/blob/v2026.11.9/docs/dev-tools/shims.md)
- [Reshim](https://github.com/jdx/mise/blob/v2026.11.9/docs/cli/reshim.md)
