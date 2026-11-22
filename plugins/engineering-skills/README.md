# Engineering Skills

See the [marketplace instructions](../../README.md) to install the plugin.
The two browser skills require their respective executables.

## Playwright CLI

Install the executable using the [Playwright CLI guide](https://playwright.dev/agent-cli/introduction).
In Codex, use `engineering-skills:playwright-cli`.

From the marketplace repository root, sync the official skill from the upstream
default branch's HEAD and review the diff before releasing the plugin:

```sh
mise run --raw sync:playwright-cli
mise run --raw sync:playwright-cli -- --check
```

The copy includes the [upstream license](skills/playwright-cli/LICENSE) and
[source commit](skills/playwright-cli/UPSTREAM.md). Use `--ref <commit>` to
restore or verify a specific revision. With `--check`, the task reports drift
without changing the packaged files.

## Browser Harness

Install the Browser Harness CLI through the [upstream setup guide](https://github.com/browser-use/browser-harness).
In Codex, use `engineering-skills:browser-harness`. The skill uses the CLI's
standard stdin interface and supports the optional wrapper's `--code` and
`--script` options.

The main guide, agent metadata, and notes for connections, tabs, and files are
maintained here. Selected interaction notes come from a Browser Harness release and
retain the [upstream MIT license](skills/browser-harness/LICENSE). The generated
[source record](skills/browser-harness/references/upstream.md) identifies the
exact commit.

With Python 3.11 or later, regenerate the bundled skill from the approved CLI
version and review the diff before bumping the plugin version:

```sh
python3 plugins/engineering-skills/scripts/sync_browser_harness.py --version 0.1.13
```

Use `--source PATH` to read the tag from a local Git checkout. Add `--check`
to validate without writing, and `--target PATH` with `--check` to compare a
packaged or installed skill directory with the rendered output.
