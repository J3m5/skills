# Local Docs Refresh

Use this reference to refresh the local GitHub CLI manual mirror for the
`github` skill.

This is maintenance-only. For auth, search, inspection, diagnosis, or review,
go back to [GitHub Skill](../../SKILL.md) and pick the matching workflow
reference.

## Primary Command

Set `github_skill_dir` to the directory containing this skill's `SKILL.md`.
Run from any directory with an explicit output root.

```bash
uv run "$github_skill_dir/scripts/update_cli_manual_docs.py" \
  --output-root ~/.agents/docs/global/platform/github
```

The script declares its Python dependencies with PEP 723 metadata. `uv` creates
the isolated environment; do not install `beautifulsoup4`, `html2text`, or
`lxml` globally.

## Incremental Behavior

- uses cached `ETag` / `Last-Modified` in `.agents/docs/global/platform/github/state.json`
- sends conditional requests and skips unchanged pages
- rebuilds only changed pages while preserving full crawl coverage
- prunes stale generated files and state entries on full-scope runs

## Full Rebuild

```bash
uv run "$github_skill_dir/scripts/update_cli_manual_docs.py" \
  --output-root ~/.agents/docs/global/platform/github --full-refresh
```

## Smoke Test

```bash
uv run "$github_skill_dir/scripts/update_cli_manual_docs.py" \
  --output-root ~/.agents/docs/global/platform/github --max-pages 5
```

## Unit Tests

```bash
uv run --with beautifulsoup4 --with html2text --with lxml python \
  "$github_skill_dir/scripts/test_update_cli_manual_docs.py"
```

## Outputs

- Markdown pages: `.agents/docs/global/platform/github/manual/`
- Manifest: `.agents/docs/global/platform/github/manifest.json`
- Incremental state cache: `.agents/docs/global/platform/github/state.json`

## Guardrails

- Use this file only for local manual mirror maintenance.
- Do not route ordinary GitHub workflows through this maintenance reference.
