# Agent Skills

This repository publishes reusable Agent Skills through a Codex marketplace.

Skills are self-contained folders with instructions, scripts, and supporting assets that help agents execute recurring tasks consistently.

## Install in Codex

```bash
codex plugin marketplace add J3m5/skills
codex plugin add engineering-skills@j3m5-skills
```

Open a new Codex session to use the skills. Use `codex plugin marketplace upgrade j3m5-skills` to refresh an existing installation from GitHub.

Install the optional [Microsoft Playwright CLI skill](https://github.com/microsoft/playwright-cli/tree/main/skills/playwright-cli) as a separate plugin:

```bash
codex plugin add playwright-cli@j3m5-skills
```

The plugin follows Microsoft's `main` branch and updates with `codex plugin marketplace upgrade j3m5-skills`. Use `playwright-cli:playwright-cli` in Codex. The skill requires the [Playwright CLI executable](https://playwright.dev/agent-cli/introduction).

Install [Browser Harness](./plugins/browser-harness/README.md) for interactive work in a local Chrome or Chromium session:

```bash
codex plugin add browser-harness@j3m5-skills
```

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
