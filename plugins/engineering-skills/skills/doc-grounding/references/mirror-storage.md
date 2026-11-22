# Shared Mirror Storage

Reuse documentation under `~/.agents/docs/` across projects:

| Material                            | Snapshot root                         |
| ----------------------------------- | ------------------------------------- |
| Cross-project documentation         | `global/<group>/<docs-name>/`         |
| Current system-tool documentation   | `system-tools/<tool-name>/`           |
| Reusable versioned dependency       | `project-dependencies/<docs-name>/`   |
| Repository-specific source material | `project/<project-name>/<docs-name>/` |

Follow existing groups and canonical paths. Inspect the active snapshot and its
`history/` before exporting another copy. Keep the current snapshot at a stable
path and intentionally retained versions in `history/<version-or-ref>/`.

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

The commands in the acquisition references use paths relative to this skill
directory. Run them from that directory or resolve their script paths against it.
Use the effective project or system tooling and respect filesystem permissions;
a shared destination does not itself grant write access.
