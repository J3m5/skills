# Attach Media To Issues And Pull Requests

Use this reference when the user asks to upload local images or videos into an
issue, pull request, or comment body. Native attachment upload requires `gh`
2.99.0 or newer.

## Supported Commands

`--attach FILE` is repeatable on:

- `gh issue create`, `gh issue edit`, and `gh issue comment`
- `gh pr create`, `gh pr edit`, and `gh pr comment`

Use an explicit repository when context is not already established:

```bash
gh issue create -R OWNER/REPO --title "TITLE" --body "BODY" \
  --attach './repro.png#The error state'
gh pr edit 456 -R OWNER/REPO --attach ./walkthrough.mp4
gh pr comment 456 -R OWNER/REPO --body "Updated result" \
  --attach ./before.png --attach ./after.png
```

## File And Body Behavior

- Supported extensions are `png`, `jpg`, `jpeg`, `gif`, `webp`, `svg`, `mp4`,
  `mov`, and `webm`.
- Attach at most 50 files per command.
- For an image, optional alt text follows the path after `#`. Quote the whole
  value so the shell does not treat `#` as a comment. Without explicit alt
  text, `gh` uses the filename.
- If the body already references the same local path, `gh` rewrites the
  Markdown target to the uploaded URL and preserves the body's alt text.
  Otherwise, it appends the uploaded attachment to the body.

```bash
gh pr edit 456 -R OWNER/REPO \
  --body 'Before fix: ![Login error](./login.png)' \
  --attach ./login.png
```

- Videos do not accept `#alt text`. A standalone Markdown image reference to a
  video becomes a bare player URL; an inline video image becomes a link.
  Reference-style video images are rejected, so use a reference-style link
  instead.

## Compatibility And Authentication

- Uploads work on GitHub.com and GitHub Enterprise Cloud, including GHE.com
  data-residency tenants. GitHub Enterprise Server is unsupported.
- The active credential must be an OAuth token, classic personal access token,
  or fine-grained personal access token. GitHub App tokens are unsupported.
- The authenticated user needs `WRITE`, `MAINTAIN`, or `ADMIN` permission on
  the repository.
- On `gh` older than 2.99.0, stop and report that native `--attach` is
  unavailable; do not invent an upload endpoint or silently omit the media.

## Command Constraints

- `gh issue create` and `gh pr create`: do not combine `--attach` with `--web`.
- `gh pr create`: do not combine `--attach` with `--dry-run`.
- `gh issue edit`: attach media to only one issue per invocation.
- `gh issue comment` and `gh pr comment`: do not combine `--attach` with
  `--web` or `--delete-last`. It may be used alone, with `--edit-last`, or with
  one of `--body`, `--body-file`, or `--editor`.

## Partial Failure

Uploads stop at the first failed file. If earlier files succeeded, `gh` still
writes those attachments, prints the issue or pull request URL for create/edit
operations, and exits non-zero. Report the partial success and do not retry the
whole batch blindly, because that can duplicate attachments.

## Guardrails

- Attachment upload is an external side effect. Require explicit user intent
  before running a command that uploads or edits GitHub content.
- Validate each local path and extension before the mutating command.
- Prefer meaningful image alt text when the user or surrounding context
  provides it.
- Preserve shell quoting around any `FILE#ALT_TEXT` value.
