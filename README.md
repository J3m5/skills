# Agent Skills

This repository publishes reusable Agent Skills through a Codex marketplace.

Skills are self-contained folders with instructions, scripts, and supporting assets that help agents execute recurring tasks consistently.

## Add the marketplace in Codex

```bash
codex plugin marketplace add J3m5/skills
```

The catalog is currently empty. Use `codex plugin marketplace upgrade j3m5-skills` to fetch future catalog updates.

## Package a skill

Add packaged skills under `plugins/<plugin-name>/skills/<skill-name>/` with a `SKILL.md` and any resources they use. Add the plugin package to the [marketplace manifest](./.agents/plugins/marketplace.json) when it is ready to distribute.

## Tooling

These skills rely on [`mise`](https://mise.jdx.dev) to provision the command-line tools they use.
The repository includes a root [`mise.toml`](./mise.toml) so the required toolchain can be installed consistently.
Source code for `mise` is available at <https://github.com/jdx/mise>.

## License

See the license information provided in each skill directory when applicable.
