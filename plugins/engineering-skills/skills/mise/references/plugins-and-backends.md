# Local plugins and custom backends

Distinguish registry/core behavior, plugin/backend installation code, and shell
activation. Inspect registration and tool state with `mise plugins ls --urls`,
`mise ls --json <tool>`, and `mise current <tool>`. For executable resolution use
`mise which <executable>`; a backend tool identifier is not necessarily a binary.

Link a local implementation when requested:

```sh
mise plugins link <name> /abs/path/to/plugin
```

This is a link: edits in the source directory take effect without reinstalling
or re-linking the plugin. `mise plugins link --force` overwrites an existing
registration; use it only when replacing that registration is intended, not as
a routine refresh after source edits. Linking does not install a tool version.

For missing install-time assets or hooks, inspect the implementation that owns
them. Already installed versions are normally skipped by both `mise use` and
`mise install`; see [targeted reinstallation](install-tools.md). Changing plugin
source does not retroactively recreate installed tool artifacts.

When the registry moves a shorthand to another backend, mise retains the locked
backend. A warning is not a failed install. For a requested migration, preview
`mise backends switch --dry-run <tool>`; the real command relocks checksums/URLs
and reinstalls already installed versions at the same versions. `--global`
targets the global lockfiles. Preserve an explicit backend chosen by the user.

For HTTP backend authentication, consult its `headers` option and the existing
credential sources rather than writing literal credentials into shared config.
For requested OCI tool packaging, use the OCI guide and its explicit
experimental gate; packaging is distinct from an ordinary backend install.

- [Plugin link semantics](https://github.com/jdx/mise/blob/v2026.11.9/docs/cli/plugins/link.md)
- [Registry backend migrations](https://github.com/jdx/mise/blob/v2026.11.9/docs/cli/backends/switch.md)
- [HTTP backend options](https://github.com/jdx/mise/blob/v2026.11.9/docs/dev-tools/backends/http.md)
- [OCI tool packaging](https://github.com/jdx/mise/blob/v2026.11.9/docs/dev-tools/mise-oci.md)
- [Backend plugin development](https://github.com/jdx/mise/blob/v2026.11.9/docs/backend-plugin-development.md)
- [Tool plugin development](https://github.com/jdx/mise/blob/v2026.11.9/docs/tool-plugin-development.md)
