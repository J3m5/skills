# Mirror Storage

Use the destination specified for the task or documented by the project.
Otherwise, reuse an existing mirror when its scope and version fit. If a new
mirror is needed, choose a root that fits its intended use.

- `~/.agents/docs/` is an example root for mirrors reused across projects.
- `.agents/docs/` at the current project's root is an example for mirrors
  scoped to that project.

Use the existing layout within the chosen root. Inspect the active snapshot
and its `history/` before exporting another copy. Keep the current snapshot
at a stable path and intentionally retained versions in
`history/<version-or-ref>/`.

For managed system-tool and dependency snapshots, use the scripts to record
source, selected ref or URL, dependency version, fetch date, and relevant
limitations in `manifest.json`. Verify the correspondence between those fields;
the manifest writer does not establish it. Record an exporter fallback and its
concrete reason so future refreshes can reuse it.

The managed scripts support `system-tool` and `project-dependency` kinds.
Cross-project and repository-specific source material does not require that
schema; retain its source and capture identity in a suitable provenance note.

Keep raw upstream files separate from local navigation and project conventions.
When refreshing a mirror with local indexes or checksums, inspect how those
files are maintained and preserve or regenerate them deliberately. Refreshing
the upstream snapshot alone does not update that local navigation.

In the acquisition references, resolve `scripts/` against the skill directory
and project-local destinations against the project root. Use absolute paths
when invoking the scripts from a different working directory.
