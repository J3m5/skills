# Inspect Releases

Use this reference when the task is about releases, prereleases, tags, or the
published release surface of a repository.

## Output Contract

- the relevant `tagName` and release URL
- the release state: stable, prerelease, or draft
- any important `name` versus `tagName` distinction
- the downloaded asset path when asset retrieval was requested
- a switch to ancestry verification when metadata alone is insufficient

## Primary Workflow

1. Start with `gh release list` to see the actual published release objects.
2. Use `tagName` to drive follow-up `gh release view` calls.
3. Treat release `name` as presentation data, not as a reliable lookup key.
4. Use `gh release download` when the user requests published assets.

## Daily Commands

Release catalog:

```bash
gh release list -R OWNER/REPO --limit 20 --json name,tagName,isLatest,isPrerelease,publishedAt
```

Release detail by tag:

```bash
gh release view TAG -R OWNER/REPO --json tagName,name,isPrerelease,publishedAt,isDraft,author,body,url,assets
```

Minimal release detail:

```bash
gh release view TAG -R OWNER/REPO --json tagName,name,isPrerelease,publishedAt,targetCommitish
```

Download published release assets:

```bash
gh release download TAG -R OWNER/REPO
gh release download TAG -R OWNER/REPO --pattern '*.deb' --dir ./downloads
```

## Daily Interpretation

- `name` is the release display name
- `tagName` is the selector to prefer for `gh release view`
- `isLatest` exists on `gh release list`
- `isLatest` does not exist on `gh release view`
- `url` exists on `gh release view`
- `url` does not exist on `gh release list`
- in `gh` 2.96.0 and newer, `gh release download` works anonymously for public
  repositories and still uses a token when one is available

When you need both latest-state and URL, list first and then inspect the tag:

```bash
gh release list -R OWNER/REPO --limit 20 --json name,tagName,isLatest,isPrerelease,publishedAt
gh release view TAG -R OWNER/REPO --json tagName,name,publishedAt,url
```

## Escalate Or Switch When

- the user asks whether a PR or commit is included in a release:
  switch to [Verify PR In Release](../diagnose/verify-pr-in-release.md)
- a high-level release command is insufficient and you truly need tag ancestry or compare semantics:
  use the targeted API calls documented in [Verify PR In Release](../diagnose/verify-pr-in-release.md)
- you need verified field subsets for other commands:
  use [Verified `gh --json` Field Cheat Sheet](../utilities/json-fields-cheatsheet.md)

## Guardrails

- Do not assume a display name such as `0.120.0` is a valid `gh release view` selector when the real tag is something like `rust-v0.120.0`.
- Prefer `gh release list` and `gh release view` before raw tag endpoints.
- Do not require login before `gh release download` on a public repository when
  using `gh` 2.96.0 or newer; private repositories still require auth.
- Do not infer commit inclusion from release dates alone.
- Do not request `isLatest` from `gh release view` or `url` from
  `gh release list`.
