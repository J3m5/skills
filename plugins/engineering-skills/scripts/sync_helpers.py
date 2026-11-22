"""Shared Git fetch and atomic updates for bundled skills."""

import filecmp
import os
import shutil
import stat
import subprocess
from pathlib import PurePosixPath


def git_reader(repo):
    local_vars = subprocess.check_output(
        ["git", "rev-parse", "--local-env-vars"], text=True
    ).splitlines()
    env = {key: value for key, value in os.environ.items() if key not in local_vars}

    def git(*args):
        return subprocess.check_output(["git", *args], cwd=repo, env=env)

    return git


def fetch(url, ref, repo):
    git = git_reader(repo)
    git("init", "--quiet")
    git("fetch", "--quiet", "--depth=1", "--", url, ref)
    commit = git("rev-parse", "--verify", "FETCH_HEAD^{commit}").decode().strip()
    return commit, git


def read_files(git, commit, *paths):
    tree = git("ls-tree", "-rz", commit, "--", *map(str, paths))
    files = {}
    for entry in tree.split(b"\0"):
        if not entry:
            continue
        attributes, raw_path = entry.split(b"\t", 1)
        mode, object_type, object_id = attributes.decode().split()
        path = PurePosixPath(raw_path.decode())
        if object_type != "blob" or mode not in {"100644", "100755"}:
            raise ValueError(f"expected a regular upstream file: {path}")
        if path.is_absolute() or ".." in path.parts:
            raise ValueError(f"invalid upstream path: {path}")
        files[path] = git("cat-file", "blob", object_id), mode
    return files


def write_files(destination, files):
    for path, (data, mode) in files.items():
        output = destination / path
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(data)
        if mode == "100755":
            output.chmod(0o755)


def matches(expected, target):
    if not target.is_dir() or target.is_symlink():
        return False
    diff = filecmp.dircmp(expected, target, ignore=[])
    return (
        not (diff.left_only or diff.right_only or diff.funny_files)
        and all(
            not (target / name).is_symlink()
            and filecmp.cmp(expected / name, target / name, shallow=False)
            and is_executable(expected / name) == is_executable(target / name)
            for name in diff.common_files
        )
        and all(matches(expected / name, target / name) for name in diff.common_dirs)
    )


def is_executable(path):
    return bool(path.stat().st_mode & stat.S_IXUSR)


def install(expected, target):
    if target.is_symlink() or (target.exists() and not (target / "SKILL.md").is_file()):
        raise ValueError(f"expected a skill directory: {target}")
    transaction = target.parents[1] / f".{target.name}-sync"
    try:
        transaction.mkdir()
    except FileExistsError as error:
        raise ValueError(
            f"another sync may be in progress; inspect {transaction}"
        ) from error
    old = transaction / "previous"
    preserve_backup = False
    try:
        stage = shutil.copytree(expected, transaction / "incoming")
        if target.exists():
            target.rename(old)
        try:
            stage.rename(target)
        except OSError:
            if old.exists():
                try:
                    old.rename(target)
                except OSError as error:
                    preserve_backup = True
                    raise ValueError(
                        f"could not restore the previous skill at {old}"
                    ) from error
            raise
    finally:
        if not preserve_backup:
            shutil.rmtree(transaction)
