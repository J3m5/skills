# Create Release

Use this reference when the user explicitly asks to create a GitHub release.

## Output Contract

- the created or prepared release tag, URL, and state
- the notes source actually used: explicit notes, file, or generated notes
- whether the tag was verified, reused, or auto-created
- any assets uploaded, or an explicit no-assets result

## Shared Rules

- Treat release creation as a high-impact external side effect.
- Validate repo context first with
  [Auth And Repo Context](../bootstrap/auth-and-repo-context.md).
- Resolve or confirm the intended tag before creating the release.
- If the user only needs to inspect existing releases, switch to
  [Inspect Releases](../inspect/inspect-releases.md).

## Primary Workflow

1. Confirm the intended tag and whether it already exists.
2. Confirm whether the release is stable, prerelease, or draft.
3. Confirm the source of release notes:
   - explicit notes
   - notes file
   - notes from tag
   - generated notes
4. Confirm whether assets must be uploaded.
5. Create the release with explicit flags.

## Example Intents

- "publish `v1.2.3` with generated notes"
- "create a draft prerelease for `v1.2.3-rc1`"
- "publish `v1.2.3` only if the tag already exists"

## Daily Commands

Minimal non-interactive release:

```bash
gh release create v1.2.3 -R OWNER/REPO --notes "Release notes"
```

Draft release:

```bash
gh release create v1.2.3 -R OWNER/REPO --draft --notes "Draft release notes"
```

Prerelease:

```bash
gh release create v1.2.3-rc1 -R OWNER/REPO --prerelease --notes "Prerelease notes"
```

Generated notes:

```bash
gh release create v1.2.3 -R OWNER/REPO --generate-notes
```

Notes from file:

```bash
gh release create v1.2.3 -R OWNER/REPO --notes-file RELEASE_NOTES.md
```

Verify existing tag instead of auto-creating one:

```bash
gh release create v1.2.3 -R OWNER/REPO --verify-tag --notes "Release notes"
```

Target a specific branch or commit for tag creation:

```bash
gh release create v1.2.3 -R OWNER/REPO --target COMMIT_OR_BRANCH --notes "Release notes"
```

Upload assets:

```bash
gh release create v1.2.3 -R OWNER/REPO --notes "Release notes" ./dist/*.tgz
```

## Release Guardrails

- `gh release create` can auto-create the tag if it does not already exist; use `--verify-tag` when implicit tag creation is not acceptable.
- Prefer explicit notes or `--generate-notes` over an interactive flow.
- Use `--draft` when the release must be reviewed before publication.
- Use `--fail-on-no-commits` when duplicate or no-op releases should be rejected.
- If assets are involved, remember that GitHub creates the release as draft first, uploads assets, then publishes it.

## Escalate Or Switch When

- the user first needs release inspection or tag resolution:
  switch to [Inspect Releases](../inspect/inspect-releases.md)
- the task is to verify whether a PR is already included in a release:
  switch to [Verify PR In Release](../diagnose/verify-pr-in-release.md)
- the task is to create or edit an issue:
  switch to [Manage Issues](./manage-issues.md)
- the task is to create a pull request:
  switch to [Create Pull Request](./create-pull-request.md)

## Guardrails

- Do not publish a release unless the user explicitly asked for creation.
- Do not assume automatic tag creation is safe; make the choice explicit.
- Keep the stable/prerelease/draft decision explicit in the command.
