# Agent Skills

This repository contains local Agent Skills.

Skills are self-contained folders with instructions, scripts, and supporting assets that help agents execute recurring tasks consistently.

## Structure

Each skill lives under a category directory such as `skills/meta/` or `skills/reporting/` and is typically centered around a `SKILL.md` file.

This layout is repository-local. For installed Codex skills, prefer `~/.codex/skills/`.

## Available Skills

### `.system`

- `skill-creator`: Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Codex's capabilities with specialized knowledge, workflows, or tool integrations.
- `skill-installer`: Install Agent Skills into `$CODEX_HOME/skills` from a curated list or a GitHub repo path. Use when a user asks to list installable skills, install a curated skill, or install a skill from another repo, including a private repo.

### `meta`

- `codex-setup-report`: Gather a Codex usage-consumption report from the local machine and draft a GitHub issue comment using documented current defaults plus local config checks. Use when the user reports Codex usage limits draining too fast, wants to fill a setup template for `openai/codex` issues, or needs a reproducible workflow for collecting Codex setup details and comparing them against the documented defaults.
- `skill-review-and-auto-refactor`: Audit and improve an existing Codex or OpenAI skill bundle or `SKILL.md` for clearer routing, stricter workflow instructions, and safer repeatable execution. Use only for existing skills, not for generic code review or net-new skill creation.

### `reporting`

- `report-generator`: Generate or update a structured report from source material, then publish HTML/PDF deliverables. Use when the user asks to review a report file, analyze source inputs, write a structured report, or regenerate a styled PDF report with Pandoc and WeasyPrint.

## Usage

Point Codex at this repository or copy individual skill folders into your local `~/.codex/skills/` directory, depending on how you manage skill distribution.

## Tooling

These skills rely on [`mise`](https://mise.jdx.dev) to provision the command-line tools they use.
The repository includes a root [`mise.toml`](./mise.toml) so the required toolchain can be installed consistently.
Source code for `mise` is available at <https://github.com/jdx/mise>.

## License

See the license information provided in each skill directory when applicable.
