# Agent Skills

This repository contains local Codex skills.

Skills are self-contained folders with instructions, scripts, and supporting assets that help agents execute recurring tasks consistently.

## Structure

Each skill lives in its own directory and is typically centered around a `SKILL.md` file.

## Usage

Point Codex at this repository or copy individual skill folders into your local skills directory, depending on how you manage skill distribution.

## Tooling

These skills rely on [`mise`](https://mise.jdx.dev) to provision the command-line tools they use.
The repository includes a root [`mise.toml`](./mise.toml) so the required toolchain can be installed consistently.
Source code for `mise` is available at <https://github.com/jdx/mise>.

## License

See the license information provided in each skill directory when applicable.
