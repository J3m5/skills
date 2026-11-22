# Mise security controls

Use for trust/verification failures, metadata inspection of unreviewed config,
or requested task sandboxing. Preserve existing policy and the requested scope;
ordinary tool or task work does not require introducing a new hardening workflow.

## Match the control to its boundary

| Control         | Boundary                                                              |
| --------------- | --------------------------------------------------------------------- |
| Config trust    | Whether mise may load command-bearing project config.                 |
| Safe mode       | Restricted config evaluation for version/metadata workflows.          |
| Paranoid mode   | Content-bound project trust and repeat provenance checks on installs. |
| Command sandbox | Access available to the child launched by `mise run`/`mise exec`.     |

Trust does not verify downloaded software; command sandboxing does not sandbox
mise while it loads config, installs tools or runs hooks. Download/lockfile
verification and release-age policy are separate controls; use
[lockfiles](lockfiles.md) or [tool updates](tool-updates.md) for those workflows.

## Trust and safe inspection

Inspect `mise trust --show` and the actual resolved config when trust appears
wrong, including symlink targets and inherited config. Normal mode can record
implicit trust when the user runs project code, and CI treats config as trusted;
paranoid mode removes those shortcuts, so `--yes` does not solve its trust failure.
Trust the intended reviewed scope rather than setting a blanket trusted path
or disabling paranoid mode for a single repository.

`MISE_SAFE=1` is useful for reading unreviewed config to resolve versions. It
skips project env/vars/settings, source scripts and other command-bearing
features, and refuses tasks, daemons, secrets and project diagnostic execution.
It does not make every command read-only: locking can write and installation can
run tool build scripts. Use a preview when the request is inspection only.
Paranoid mode is global-only. It accepts selected categories
(`config`, `env_files`, `plugins`, `provenance`) as well as a boolean. Its
`env_files` category requires separate content-bound trust for dotenv/source
files; changing them invalidates trust. Diagnose the applicable category and
file instead of assuming that trusting mise.toml covers every loaded file.

## Requested command restrictions

Use task properties or matching `--deny-*`/`--allow-*` flags in the intended
scope. Allow lists turn on the corresponding restriction; settings, task rules
and flags combine rather than one always replacing the others. Task paths are
relative to the task directory, CLI paths to the invocation directory. Linux
allowed paths must already exist; granting their parent widens access.

Check the platform contract: file/network restrictions apply on Linux/macOS,
not Windows; environment filtering applies on all three. Per-host `allow_net`
is unsupported and errors on Linux/macOS, so it is not a working host allowlist.
Environment filtering also drops config `[env]` values unless allowed. Use
`cache.env` for values that affect outputs; experimental `pass_through_env`
passes values without including them in the cache key and is not itself a filter.

## npm provenance

`npm.provenance` is enabled by default. With the embedded aube installer it
verifies the tool package's published Sigstore provenance, not its transitive
dependencies. Installation records its source repository in a format-4 lockfile;
a changed repository or vanished provenance for that pinned version fails.
An unpinned package that publishes no provenance can still install.

Other npm installers and checksum-only local archives do not provide this check;
paranoid's provenance category refuses those unsupported paths. Verification can
need Sigstore network access even with cached artifacts. Diagnose provenance,
repository identity, network access and backend choice separately; disabling the
check globally is not the default repair. See [lockfiles](lockfiles.md) for format
compatibility and safe-mode resolution.

- [Trust rules and safe mode](https://github.com/jdx/mise/blob/v2026.11.9/docs/security.md)
- [Paranoid trust and provenance](https://github.com/jdx/mise/blob/v2026.11.9/docs/paranoid.md)
- [Sandbox boundaries and platform support](https://github.com/jdx/mise/blob/v2026.11.9/docs/sandboxing.md)
  Since 2026.11.9, Linux 7.1+ can restrict connections to external Unix sockets
  with `--deny-unix`. Use `--allow-unix <path>` to permit a socket or directory
  and deny others. Request this explicitly even with `--deny-net` or `--deny-all`.
  Older Linux kernels and macOS reject the request. Windows warns. [Sandbox flags](https://github.com/jdx/mise/releases/tag/v2026.11.9)

- [npm provenance](https://github.com/jdx/mise/blob/v2026.11.4/docs/dev-tools/backends/npm.md)
