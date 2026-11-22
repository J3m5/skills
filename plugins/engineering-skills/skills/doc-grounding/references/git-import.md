# Git Source Import

Use Git when `mdzilla` cannot export the required source faithfully, including
unsupported providers, incomplete output, or loss of required Markdown, RST,
examples, or links. Record the concrete reason. Reuse a documented Git fallback
for an existing snapshot; reassess it when the source or required scope changes.

## Select and import

Establish the version target and verify the actual upstream tag or commit and
documentation subtree. Package version `x.y.z` need not map to tag `vx.y.z`.
Inspect GitHub-hosted source with the available GitHub workflow, or use the
appropriate provider connector or Git tooling.

For a managed system-tool or dependency snapshot:

```bash
python3 scripts/import_git_snapshot.py \
  --repo <repository-url> --ref <verified-ref> \
  --subdir <path/to/docs> \
  --dest <shared-destination> --name <docs-name> \
  --kind project-dependency --installed-version <version> \
  --fetch-date <YYYY-MM-DD> \
  --notes <reason-for-git-fallback-and-version-limitations>
python3 scripts/verify_snapshot.py \
  --snapshot-dir <shared-destination> \
  --expect-name <docs-name> --expect-kind project-dependency \
  --expect-installed-version <version>
python3 scripts/update_catalog.py --docs-root ~/.agents/docs/project-dependencies
```

Use `--kind system-tool` and the corresponding root for system tools. Add
`--replace` only when replacing an existing canonical snapshot is intended.
The importer stages content, verifies a minimum file count, and preserves
existing `history/`; also inspect representative files and source fidelity.
Retain licenses and other necessary supporting files from the same ref when
they lie outside the selected subtree.

The importer performs a shallow fetch of the selected ref and copies the
selected subtree. It does not use sparse checkout. If repository size or network
cost warrants a manual partial clone or sparse checkout, use the relevant Git
workflow, materialize the requested files, and retain equivalent provenance.

Repository-specific source material under `project/` is outside the managed
manifest/catalog schema. Preserve its source identity without labeling it as a
dependency snapshot merely to use these commands.
