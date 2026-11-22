# Snapshot Lifecycle

Use this reference when managed system-tool or project-dependency snapshots may
need refreshes, replacement, or occasional retained history across multiple
versions or refs.

## Refresh and version changes

Use `python3 scripts/refresh_snapshot.py --snapshot-dir <snapshot-root>` to stage
and validate new content before replacing the canonical snapshot. The destination
and its retained `history/` are preserved on export or installation failure.
An export containing its own `history/` conflicts with retained history: resolve
the collision separately rather than merging or overwriting it silently.

- `--dry-run` exports and validates without changing the canonical snapshot;
  the returned `temp_dir` is retained for inspection.
- For Git or `gh:` sources, `--selected-ref <ref>` changes the ref actually
  fetched, and the manifest records that ref. For `gh:`, it replaces the source's
  existing `#ref` or adds the pin when none is present.
- For HTTP, npm, or local sources, use `--source <versioned-url-or-source>`;
  `--selected-ref` is rejected because it cannot change those sources.
- Use `--installed-version <version>` to record the dependency version after
  checking its correspondence to the selected source. The script does not infer
  package-version-to-tag mappings.

Both refresh and `import_git_snapshot.py --replace` preserve existing history.
They do not archive the previous current snapshot automatically. Run regressions
from the skill directory with `python3 -B -m unittest discover -s tests -v`.

## Default policy

1. Reuse the canonical snapshot when it already matches the installed version or
   ref exactly.
2. Replace the canonical snapshot in place when the path is intended to
   represent one mutable current snapshot and no historical retention is
   needed.
3. Keep additional history only when:
   - the project actively supports multiple dependency lines
   - migrations require comparison between versions
   - a ref-specific snapshot is needed for reproducibility
4. When keeping history, preserve the authoritative current snapshot at the
   stable root path and place older retained material under
   `history/<version-or-ref>/`.
5. Clean up obsolete history as a separate operation when it no longer maps to
   supported versions and no migration/debug value remains. Routine refreshes
   leave retained history intact.

## Practical rules

- Prefer one authoritative current snapshot at the stable root path.
- Do not rename the canonical snapshot directory on every version change.
- Store the matched version or ref in `manifest.json`, not in the canonical
  directory name.
- If retained history exists, do not overwrite a different version into an
  existing `history/<version-or-ref>/` directory.
- If you fetch a fallback ref because no exact tag exists, keep that fallback in
  a distinct `history/<version-or-ref>/` directory or document it clearly in
  `manifest.json`.
- When deleting stale snapshots, remove only directories that are clearly
  outside the currently supported version set.
- Do not delete historical snapshots if the user explicitly asked to preserve
  them.

## Minimal cleanup check

Before closing the task, verify:

- the current installed version has one obvious authoritative snapshot
- retained history is either intentionally preserved or intentionally removed
- the canonical snapshot path stayed stable while the manifest was updated
- provenance files still describe the surviving snapshots accurately
