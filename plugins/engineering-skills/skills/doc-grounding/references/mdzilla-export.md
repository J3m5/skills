# mdzilla Export

Use `mdzilla --export` directly for new Markdown mirrors. Choose the shared
destination from [mirror-storage.md](mirror-storage.md).

## Sources

| Source                  | Example                                      |
| ----------------------- | -------------------------------------------- |
| Local directory or file | `mdzilla ./docs`, `mdzilla README.md`        |
| GitHub repository       | `mdzilla gh:owner/repo`                      |
| Pinned GitHub subtree   | `mdzilla gh:owner/repo/path/to/docs#v1.2.3`  |
| Pinned GitHub commit    | `mdzilla gh:owner/repo/path/to/docs#4f3c2ab` |
| npm package             | `mdzilla npm:package-name`                   |
| HTTP documentation      | `mdzilla https://example.com`                |

For HTTP sources, `mdzilla` tries `llms.txt`, Markdown negotiation, then HTML
conversion. A section URL does not necessarily restrict the exported graph.

GitHub refs and subpaths are forwarded to `giget`. A bare repository source is
not version-aligned. Use the verified tag or commit when exact matching matters.
The CLI's Git routing uses `gh:`; other providers may require the
[Git fallback](git-import.md).

## Export and inspect

```bash
mdzilla <source> --export <shared-destination>
```

Inspect entrypoints and representative pages, not just the file count. Compare
headings, code fences, tables and link targets with the upstream source: an
export can exit successfully while flattening Markdown into plain text. Use the
Git fallback when this loses structure needed by the snapshot, or when a
non-Markdown source exports only repository metadata. Keep normative HTML, XML
or JSON raw when conversion would lose meaning. Record the concrete reason for
changing exporters.

For a managed system-tool or dependency snapshot, add provenance with:

```bash
python3 scripts/write_manifest.py \
  --output-dir <shared-destination> --name <docs-name> \
  --kind project-dependency --installed-version <version> \
  --source-type <github|http|npm|local> --chosen-docs-source <source> \
  --fetch-date <YYYY-MM-DD>
python3 scripts/verify_snapshot.py --snapshot-dir <shared-destination>
```

Use absolute paths for local sources so a later refresh works from another
working directory. Record version granularity and any fallback in `--notes`;
use `--selected-ref` and `--source-repo` when applicable. Ad hoc `project/`
material does not require managed manifests.

## Refresh

```bash
python3 scripts/refresh_snapshot.py --snapshot-dir <shared-destination>
```

The script supports `github`, `http`, `npm`, and `local`, plus existing
`mdzilla` and `mdzilla-github` manifests. Git snapshots use their recorded Git
source and ref. See [snapshot-lifecycle.md](snapshot-lifecycle.md) for history,
dry runs, and changing versions.

## OpenAI Developers mirrors

Reuse `~/.agents/docs/global/ai/openai/portal/` when it already contains the
required documentation. Verify the scope of section exports before creating
another snapshot; filtered local indexes can avoid duplicating the same graph.
