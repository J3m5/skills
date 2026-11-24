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
Use `engineering-skills:browser-harness` in Codex. It runs the upstream CLI
directly and passes Python on standard input.

Maintain the [skill](skills/browser-harness/SKILL.md) and its references in
this plugin. The [source record](skills/browser-harness/references/upstream.md)
identifies the upstream release used as the baseline. Keep the
[upstream MIT license](skills/browser-harness/LICENSE) with the bundled material.

## GitLab CLI and CI

Use `engineering-skills:glab` for GitLab operations through the [GitLab CLI](https://docs.gitlab.com/cli/).
Use `engineering-skills:gitlab-ci-skill` to author and debug pipelines. The CI
skill uses [glci](https://gitlab.com/gitlab-org/ci-cd/runner-tools/glci)
for local verification and offers `glab ci lint` as a fallback.

Sync and validate from the marketplace repository root:

```sh
mise run --raw sync:glab -- --check
mise run --raw sync:gitlab-ci -- --check
```

Both tasks default to the exact upstream commit recorded in their skill.
Run without `--check` to regenerate the bundled files. Pass `--ref <revision>`
to select a new commit or tag and review the diff before release. For `glab`,
choose the revision corresponding to the CLI release you intend to support.
Use `--checkout <path>` to use a Git checkout containing the revision offline.

The synchronizer preserves the maintained [glab entrypoint](skills/glab/SKILL.md)
and regenerates its five references. It copies the official CI verification script
and documentation, with the create-pipeline and add-job workflows in separate files.
