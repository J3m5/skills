#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from common import count_files, infer_kind_from_path, write_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write a standard manifest.json for a docs snapshot."
    )
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--logical-project-name")
    parser.add_argument("--docs-directory-name")
    parser.add_argument("--name")
    parser.add_argument("--dependency")
    parser.add_argument("--kind", choices=["system-tool", "project-dependency"])
    parser.add_argument("--installed-version", required=True)
    parser.add_argument("--source-type", required=True)
    parser.add_argument("--chosen-docs-source")
    parser.add_argument("--source-repo")
    parser.add_argument("--selected-ref")
    parser.add_argument("--selected-subdir")
    parser.add_argument("--fetch-date")
    parser.add_argument("--notes", default="")
    parser.add_argument("--status")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / "manifest.json"
    name = args.name or args.dependency
    if not name:
        raise SystemExit("Provide --name (preferred) or --dependency (deprecated).")
    kind = args.kind or infer_kind_from_path(output_dir)
    if not kind:
        raise SystemExit(
            "Could not infer snapshot kind. Provide --kind as system-tool or project-dependency."
        )

    file_count = count_files(output_dir)
    if not manifest_path.exists():
        file_count += 1

    payload = {
        "name": name,
        "kind": kind,
        "logical_project_name": args.logical_project_name,
        "docs_directory_name": args.docs_directory_name,
        "installed_version": args.installed_version,
        "source_type": args.source_type,
        "chosen_docs_source": args.chosen_docs_source,
        "source_repo": args.source_repo,
        "selected_ref": args.selected_ref,
        "selected_subdir": args.selected_subdir,
        "fetch_date": args.fetch_date,
        "status": args.status,
        "notes": args.notes,
        "file_count": file_count,
    }
    payload = {key: value for key, value in payload.items() if value not in (None, "")}
    write_json(manifest_path, payload)


if __name__ == "__main__":
    main()
