# Agent Skills

This repository publishes reusable Agent Skills through a Codex marketplace.

Skills are self-contained folders with instructions, scripts, and supporting assets that help agents execute recurring tasks consistently.

## Install in Codex

```bash
codex plugin marketplace add J3m5/skills
codex plugin add engineering-skills@j3m5-skills
```

Open a new Codex session to use the skills. Use `codex plugin marketplace upgrade j3m5-skills` to refresh an existing installation from GitHub.

## Included skills

| Area                             | Skills                                                             |
| -------------------------------- | ------------------------------------------------------------------ |
| Version control                  | `git-core`, `github`, `hk`                                         |
| Documentation and version checks | `documentation-policy`, `doc-grounding`, `version-first-grounding` |
| Tooling and permissions          | `mise`, `sandbox-escalation-policy`                                |
| Automated testing                | `test-engineering`                                                 |
| Collaboration and publishing     | `write-and-publish`                                                |

## Package a skill

Add packaged skills under `plugins/<plugin-name>/skills/<skill-name>/` with a `SKILL.md` and any resources they use. Add the plugin package to the [marketplace manifest](./.agents/plugins/marketplace.json) when it is ready to distribute.

An external plugin can be listed directly from Git using a `url` or `git-subdir` source. Link to the plugin package and pin its Git ref or SHA as needed. [Codex marketplace format](https://developers.openai.com/plugins/build/plugins#marketplace-metadata)

## Tooling

These skills rely on [`mise`](https://mise.jdx.dev) to provision the command-line tools they use.
The repository includes a root [`mise.toml`](./mise.toml) so the required toolchain can be installed consistently.
Source code for `mise` is available at <https://github.com/jdx/mise>.

## License

See the license information provided in each skill directory when applicable.
