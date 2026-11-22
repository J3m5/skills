# Maintain the glab adaptation

`metadata.source-commit` in [SKILL.md](../SKILL.md) pins the GitLab CLI
commit used to generate the five references from the bundled `glab` skill.
The skill's entrypoint and this file are maintained locally. The
[MIT license](../LICENSE) comes from GitLab CLI. To inspect or refresh the
references, run from the marketplace repository root:

```sh
# Verify the deployed references against the recorded upstream commit.
mise run --raw sync:glab -- --check

# Regenerate from a reviewed revision and record it in SKILL.md.
mise run --raw sync:glab -- --ref <full-upstream-sha>

# Check using a local GitLab CLI checkout with that commit available.
mise run --raw sync:glab -- --checkout /path/to/gitlab-cli --check
```

Choose the commit used by the installed `glab` release or by the release being
adopted. Review the changes before sharing the update. A changed upstream
section layout requires reviewing the section mapping in the script.

Use the script for this adaptation. `glab skills update glab` and forced
`glab skills install` can overwrite its entrypoint. See
[Contributing improvements](upstream-maintenance.md) for the upstream process
and the update commands for copies managed directly by `glab`.
