#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

from common import (
    count_files,
    load_json,
    manifest_kind,
    manifest_name,
    preserve_history,
    replace_tree,
    write_json,
)

MDZILLA_SOURCE_TYPES = {"github", "http", "npm", "local", "mdzilla", "mdzilla-github"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Refresh a managed docs snapshot from its existing manifest."
    )
    parser.add_argument("--snapshot-dir", required=True)
    parser.add_argument(
        "--source",
        help="Override docs source. Defaults to chosen_docs_source from manifest.",
    )
    parser.add_argument(
        "--installed-version",
        help="Override installed version recorded in the refreshed manifest.",
    )
    parser.add_argument(
        "--selected-ref",
        help="Fetch this Git or gh: ref, replacing any existing source pin.",
    )
    parser.add_argument(
        "--fetch-date", default=date.today().isoformat(), help="Manifest fetch date."
    )
    parser.add_argument(
        "--min-files",
        type=int,
        default=1,
        help="Fail if the staged snapshot has fewer files than this.",
    )
    parser.add_argument(
        "--keep-temp",
        action="store_true",
        help="Keep the temporary export directory for debugging.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Export and validate into temp, but do not replace the destination.",
    )
    return parser.parse_args()


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def infer_ref_from_source(source: str) -> str | None:
    if not source.startswith("gh:") or "#" not in source:
        return None
    return source.rsplit("#", 1)[1] or None


def copy_tree_contents(source: Path, dest: Path) -> None:
    if not source.exists():
        raise SystemExit(f"Requested source path does not exist: {source}")
    dest.mkdir(parents=True, exist_ok=True)
    for item in source.iterdir():
        target = dest / item.name
        if item.is_dir():
            shutil.copytree(item, target, dirs_exist_ok=True)
        else:
            shutil.copy2(item, target)


def stage_mdzilla(source: str, staged: Path) -> str | None:
    run(["mdzilla", source, "--export", str(staged)])
    return infer_ref_from_source(source)


def stage_git(
    repo: str,
    selected_ref: str,
    selected_subdir: str | None,
    temp_root: Path,
    staged: Path,
) -> None:
    repo_dir = temp_root / "repo"
    run(["git", "init", str(repo_dir)])
    run(["git", "-C", str(repo_dir), "remote", "add", "origin", repo])
    run(["git", "-C", str(repo_dir), "fetch", "--depth", "1", "origin", selected_ref])
    run(["git", "-C", str(repo_dir), "checkout", "--detach", "FETCH_HEAD"])
    source = (
        repo_dir if selected_subdir in (None, "", "/") else repo_dir / selected_subdir
    )
    copy_tree_contents(source, staged)
    git_dir = staged / ".git"
    if git_dir.exists():
        shutil.rmtree(git_dir)


def refresh(args: argparse.Namespace) -> dict:
    dest = Path(args.snapshot_dir).expanduser().resolve()
    manifest_path = dest / "manifest.json"
    if not manifest_path.exists():
        raise SystemExit(f"Missing manifest.json in {dest}")

    manifest = load_json(manifest_path)
    source_type = manifest.get("source_type")
    if source_type not in MDZILLA_SOURCE_TYPES | {"git"}:
        raise SystemExit(f"Unsupported snapshot source_type: {source_type!r}")

    source = args.source or manifest.get("chosen_docs_source")
    if source_type in MDZILLA_SOURCE_TYPES:
        if not source:
            raise SystemExit(
                "Manifest does not include chosen_docs_source; provide --source."
            )
        if source.startswith("gh:"):
            selected_ref = args.selected_ref or infer_ref_from_source(source)
            if not selected_ref and not args.source:
                selected_ref = manifest.get("selected_ref")
            if selected_ref:
                source = f"{source.partition('#')[0]}#{selected_ref}"
        elif args.selected_ref:
            raise SystemExit(
                "--selected-ref requires a Git or gh: source. For HTTP, npm, or local "
                "docs, provide --source with the desired version instead."
            )

    # Stage beside the destination so installing the snapshot uses same-filesystem renames.
    temp_root = Path(
        tempfile.mkdtemp(prefix=".doc-source-mirror-refresh-", dir=dest.parent)
    )
    staged = temp_root / "snapshot"
    try:
        if source_type in MDZILLA_SOURCE_TYPES:
            selected_ref = stage_mdzilla(source, staged)
            if selected_ref is None and not args.source:
                selected_ref = manifest.get("selected_ref")
        else:
            repo = args.source or manifest.get("source_repo")
            selected_ref = args.selected_ref or manifest.get("selected_ref")
            if not repo:
                raise SystemExit(
                    "Manifest does not include source_repo; provide --source."
                )
            if not selected_ref:
                raise SystemExit(
                    "Manifest does not include selected_ref; provide --selected-ref."
                )
            stage_git(
                repo, selected_ref, manifest.get("selected_subdir"), temp_root, staged
            )

        file_count_without_manifest = count_files(staged)
        if file_count_without_manifest < args.min_files:
            raise SystemExit(
                f"Staged snapshot looks incomplete: {file_count_without_manifest} files in {staged}; expected at least {args.min_files}"
            )

        preserve_history(dest, staged)
        payload = {
            "name": manifest_name(manifest, dest),
            "kind": manifest_kind(manifest, dest),
            "logical_project_name": manifest.get("logical_project_name"),
            "docs_directory_name": manifest.get("docs_directory_name"),
            "installed_version": args.installed_version
            or manifest.get("installed_version"),
            "source_type": source_type,
            "chosen_docs_source": source,
            "source_repo": manifest.get("source_repo")
            if source_type in MDZILLA_SOURCE_TYPES
            else (args.source or manifest.get("source_repo")),
            "selected_ref": selected_ref,
            "selected_subdir": manifest.get("selected_subdir"),
            "fetch_date": args.fetch_date,
            "status": manifest.get("status"),
            "notes": manifest.get("notes"),
            "file_count": count_files(staged)
            + int(not (staged / "manifest.json").exists()),
        }
        payload = {
            key: value for key, value in payload.items() if value not in (None, "")
        }
        write_json(staged / "manifest.json", payload)

        if not args.dry_run:
            dest.parent.mkdir(parents=True, exist_ok=True)
            replace_tree(staged, dest)

        summary = {
            "snapshot_dir": str(dest),
            "source": source or manifest.get("source_repo"),
            "selected_ref": selected_ref,
            "file_count": payload["file_count"],
            "dry_run": args.dry_run,
        }
        if args.keep_temp or args.dry_run:
            summary["temp_dir"] = str(temp_root)
        return summary
    finally:
        if not args.keep_temp and not args.dry_run and temp_root.exists():
            shutil.rmtree(temp_root)


def main() -> None:
    args = parse_args()
    summary = refresh(args)
    json.dump(summary, sys.stdout, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
