from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


def run(cmd: list[str], cwd: Path | None = None) -> None:
    subprocess.run(cmd, cwd=cwd, check=True)


def clear_directory(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def count_files(path: Path) -> int:
    return sum(1 for item in path.rglob("*") if item.is_file())


def copy_tree_contents(source: Path, dest: Path) -> None:
    if not source.exists():
        raise FileNotFoundError(f"Source path does not exist: {source}")
    dest.mkdir(parents=True, exist_ok=True)
    for item in source.iterdir():
        target = dest / item.name
        if item.is_dir():
            shutil.copytree(item, target, dirs_exist_ok=True)
        else:
            shutil.copy2(item, target)


def preserve_history(dest: Path, staged: Path) -> None:
    history = dest / "history"
    if not history.exists():
        return
    target = staged / "history"
    if target.exists() or target.is_symlink():
        raise FileExistsError(
            f"Exported history conflicts with retained history in {dest}; destination unchanged."
        )
    shutil.copytree(history, target, symlinks=True)


def replace_tree(staged: Path, dest: Path) -> None:
    backup = dest.with_name(f".{dest.name}.refresh-backup")
    if backup.exists():
        raise FileExistsError(f"Existing snapshot backup requires inspection: {backup}")
    if dest.exists():
        dest.rename(backup)
    try:
        staged.rename(dest)
    except Exception:
        if backup.exists():
            backup.rename(dest)
        raise
    if backup.exists():
        shutil.rmtree(backup)


def write_json(path: Path, payload: dict) -> None:
    ensure_parent(path)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def infer_kind_from_path(path: Path) -> str | None:
    parts = set(path.parts)
    if "system-tools" in parts:
        return "system-tool"
    if "project-dependencies" in parts:
        return "project-dependency"
    return None


def manifest_name(manifest: dict, snapshot_dir: Path) -> str:
    return (
        manifest.get("name")
        or manifest.get("dependency")
        or manifest.get("tool")
        or snapshot_dir.parent.name
    )


def manifest_kind(manifest: dict, path_hint: Path) -> str | None:
    return (
        manifest.get("kind")
        or ("system-tool" if "tool" in manifest else None)
        or ("project-dependency" if "dependency" in manifest else None)
        or infer_kind_from_path(path_hint)
    )
