# Agent Skills

This repository publishes reusable Agent Skills through a Codex marketplace.

Skills are self-contained folders with instructions, scripts, and supporting assets that help agents execute recurring tasks consistently.

## Install in Codex

```bash
codex plugin marketplace add J3m5/skills
codex plugin add engineering-skills@j3m5-skills
```

Open a new Codex session to use the skills. Use `codex plugin marketplace upgrade j3m5-skills` to refresh an existing installation from GitHub.

Version 0.4.0 includes Playwright CLI and Browser Harness. After updating,
remove the former standalone plugins if you previously installed them:

```bash
codex plugin remove playwright-cli@j3m5-skills
codex plugin remove browser-harness@j3m5-skills
```

## Included skills

| Area                             | Skills                                                             |
| -------------------------------- | ------------------------------------------------------------------ |
| Version control                  | `git-core`, `github`, `glab`, `hk`                                 |
| Documentation and version checks | `documentation-policy`, `doc-grounding`, `version-first-grounding` |
| Tooling and permissions          | `mise`, `sandbox-escalation-policy`                                |
| Automated testing                | `test-engineering`                                                 |
| Continuous integration           | `gitlab-ci-skill`                                                  |
| Browser automation               | `playwright-cli`, `browser-harness`                                |
| Web platform guidance            | `modern-web-guidance`                                              |
| Collaboration and publishing     | `write-and-publish`                                                |

Browser automation requires the corresponding Playwright CLI or Browser Harness
executable. See the [plugin guide](./plugins/engineering-skills/README.md) for
setup and how to refresh the bundled skills.

## Package a skill

Add packaged skills under `plugins/engineering-skills/skills/<skill-name>/`
with a `SKILL.md` and any resources they use. The [marketplace
manifest](./.agents/plugins/marketplace.json) lists the plugin.

## Tooling

These skills rely on [`mise`](https://mise.jdx.dev) to provision the command-line tools they use.
The repository includes a root [`mise.toml`](./mise.toml) so the required toolchain can be installed consistently.
Source code for `mise` is available at <https://github.com/jdx/mise>.

## License

See the license information provided in each skill directory when applicable.
