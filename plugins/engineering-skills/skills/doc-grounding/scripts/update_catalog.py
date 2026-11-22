#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from common import count_files, load_json, manifest_kind, manifest_name, write_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a catalog.json inventory for a docs snapshots root."
    )
    parser.add_argument("--docs-root", required=True)
    parser.add_argument("--output", default="catalog.json")
    return parser.parse_args()


def snapshot_dirs(docs_root: Path) -> list[Path]:
    dirs: list[Path] = []
    for name_dir in sorted(path for path in docs_root.iterdir() if path.is_dir()):
        manifest_path = name_dir / "manifest.json"
        if manifest_path.exists():
            dirs.append(name_dir)
            continue
        dirs.extend(sorted(path for path in name_dir.iterdir() if path.is_dir()))
    return dirs


def main() -> None:
    args = parse_args()
    docs_root = Path(args.docs_root)
    catalog_path = docs_root / args.output
    entries = []

    for snapshot_dir in snapshot_dirs(docs_root):
        manifest_path = snapshot_dir / "manifest.json"
        manifest = load_json(manifest_path) if manifest_path.exists() else {}
        name = manifest_name(manifest, snapshot_dir)
        kind = manifest_kind(manifest, snapshot_dir)
        entries.append(
            {
                "name": name,
                "kind": kind,
                "installed_version": manifest.get("installed_version")
                or snapshot_dir.name,
                "path": str(snapshot_dir),
                "file_count": count_files(snapshot_dir),
                "status": manifest.get(
                    "status", "ready" if manifest_path.exists() else "missing-manifest"
                ),
                "source_type": manifest.get("source_type"),
                "selected_ref": manifest.get("selected_ref"),
                "selected_subdir": manifest.get("selected_subdir"),
                "notes": manifest.get("notes"),
            }
        )

    payload = {"docs_root": str(docs_root), "entries": entries}
    write_json(catalog_path, payload)
    json.dump(payload, sys.stdout, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
