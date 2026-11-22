# Browser Harness

Install the Codex skill through the [J3m5 marketplace](../../README.md) and the
Browser Harness CLI through the [upstream setup guide](https://github.com/browser-use/browser-harness).
The skill uses the CLI's standard stdin interface and also supports the optional
local wrapper's `--code` and `--script` options.

## Maintain the skill

The main guide, agent metadata, and notes for connections, tabs, and files are
maintained here. Selected interaction notes come from a Browser Harness release and
retain the [upstream MIT license](skills/browser-harness/LICENSE). The generated
[source record](skills/browser-harness/references/upstream.md) identifies the
exact commit.

With Python 3.11 or later, regenerate the bundled skill from the approved CLI
version and review the diff before bumping the plugin version:

```sh
python3 plugins/browser-harness/scripts/sync_skill.py --version 0.1.13
```

Use `--source PATH` to read the tag from a local Git checkout. Add `--check`
to validate without writing, and `--target PATH` with `--check` to compare a
packaged or installed skill directory with the rendered output.
