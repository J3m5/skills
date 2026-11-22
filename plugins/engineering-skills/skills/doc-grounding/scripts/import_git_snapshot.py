#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path

from common import (
    copy_tree_contents,
    count_files,
    infer_kind_from_path,
    preserve_history,
    replace_tree,
    run,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Import a versioned documentation snapshot from a Git repository."
    )
    parser.add_argument("--repo", required=True)
    parser.add_argument("--ref", required=True)
    parser.add_argument("--dest", required=True)
    parser.add_argument("--name")
    parser.add_argument("--dependency")
    parser.add_argument("--kind", choices=["system-tool", "project-dependency"])
    parser.add_argument("--installed-version", required=True)
    parser.add_argument("--logical-project-name")
    parser.add_argument("--docs-directory-name")
    parser.add_argument("--subdir")
    parser.add_argument("--notes", default="")
    parser.add_argument("--fetch-date")
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Replace an existing destination directory if it already exists.",
    )
    parser.add_argument(
        "--min-files",
        type=int,
        default=1,
        help="Fail if fewer than this number of files are imported.",
    )
    return parser.parse_args()


def resolve_identity(args: argparse.Namespace) -> tuple[str, str]:
    name = args.name or args.dependency
    if not name:
        raise SystemExit("Provide --name (preferred) or --dependency (deprecated).")
    kind = args.kind or infer_kind_from_path(Path(args.dest))
    if not kind:
        raise SystemExit(
            "Could not infer snapshot kind. Provide --kind as system-tool or project-dependency."
        )
    return name, kind


def prepare_destination(dest: Path, replace: bool) -> None:
    if dest.exists() and not replace:
        raise SystemExit(
            f"Destination already exists: {dest}. Re-run with --replace to overwrite it."
        )
    dest.parent.mkdir(parents=True, exist_ok=True)


def import_snapshot(args: argparse.Namespace) -> dict:
    dest = Path(args.dest).expanduser().resolve()
    name, kind = resolve_identity(args)
    prepare_destination(dest, args.replace)

    with tempfile.TemporaryDirectory(
        prefix=".doc-source-mirror-git-", dir=dest.parent
    ) as temp_dir:
        repo_dir = Path(temp_dir) / "repo"
        staging_dir = Path(temp_dir) / "snapshot"
        run(["git", "init", str(repo_dir)])
        run(["git", "-C", str(repo_dir), "remote", "add", "origin", args.repo])
        run(["git", "-C", str(repo_dir), "fetch", "--depth", "1", "origin", args.ref])
        run(["git", "-C", str(repo_dir), "checkout", "--detach", "FETCH_HEAD"])

        source = repo_dir / args.subdir if args.subdir else repo_dir
        if not source.exists():
            raise SystemExit(
                f"Requested source path does not exist after checkout: {source}"
            )

        staging_dir.mkdir(parents=True, exist_ok=True)
        copy_tree_contents(source, staging_dir)

        git_dir = staging_dir / ".git"
        if git_dir.exists():
            shutil.rmtree(git_dir)

        file_count = count_files(staging_dir)
        if file_count < args.min_files:
            raise SystemExit(
                f"Imported snapshot looks incomplete: {file_count} files found in staged snapshot for {dest}"
            )

        preserve_history(dest, staging_dir)
        file_count = count_files(staging_dir) + int(
            not (staging_dir / "manifest.json").exists()
        )
        manifest = {
            "name": name,
            "kind": kind,
            "logical_project_name": args.logical_project_name,
            "docs_directory_name": args.docs_directory_name,
            "installed_version": args.installed_version,
            "source_type": "git",
            "source_repo": args.repo,
            "selected_ref": args.ref,
            "selected_subdir": args.subdir or "/",
            "fetch_date": args.fetch_date,
            "notes": args.notes,
            "file_count": file_count,
        }
        manifest = {
            key: value for key, value in manifest.items() if value not in (None, "")
        }
        write_json(staging_dir / "manifest.json", manifest)
        replace_tree(staging_dir, dest)
    return {
        "dest": str(dest),
        "clone_mode": "full",
        "name": name,
        "kind": kind,
        "installed_version": args.installed_version,
        "selected_ref": args.ref,
        "selected_subdir": args.subdir or "/",
        "file_count": file_count,
    }


def main() -> None:
    args = parse_args()
    summary = import_snapshot(args)
    json.dump(summary, sys.stdout, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
