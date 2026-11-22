# Agent Skills

This repository publishes reusable Agent Skills through a Codex marketplace.

Skills are self-contained folders with instructions, scripts, and supporting assets that help agents execute recurring tasks consistently.

## Install in Codex

```bash
codex plugin marketplace add J3m5/skills
codex plugin add agent-skills@j3m5-skills
```

Start a new Codex session and select `report-generator` from the skill picker.
To refresh the catalog, run `codex plugin marketplace upgrade j3m5-skills`.

## Marketplace skills

- [`report-generator`](./plugins/agent-skills/skills/report-generator/SKILL.md) turns source material into a structured report and renders it to HTML and PDF. The render workflow uses Pandoc and WeasyPrint.

Add packaged skills under `plugins/agent-skills/skills/<skill-name>/` with a `SKILL.md` and any resources they use. The [marketplace manifest](./.agents/plugins/marketplace.json) points to the [plugin package](./plugins/agent-skills/plugin.json).

## Legacy skills

- [`codex-setup-report`](./skills/meta/codex-setup-report/SKILL.md) needs a refresh of its Codex defaults and the data it collects for shareable reports.
- [`skill-review-and-auto-refactor`](./skills/meta/skill-review-and-auto-refactor/SKILL.md) overlaps with current skill authoring guidance. Its separate workflow is most relevant for audit-only reviews.
- [`skill-creator`](./skills/.system/skill-creator/SKILL.md) and [`skill-installer`](./skills/.system/skill-installer/SKILL.md) are historical copies of Codex system skills.

## Tooling

These skills rely on [`mise`](https://mise.jdx.dev) to provision the command-line tools they use.
The repository includes a root [`mise.toml`](./mise.toml) so the required toolchain can be installed consistently.
Source code for `mise` is available at <https://github.com/jdx/mise>.

## License

See the license information provided in each skill directory when applicable.
