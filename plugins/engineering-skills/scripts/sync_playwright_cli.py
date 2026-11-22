"""Import the official Playwright CLI skill and its license from Git."""

import argparse
import filecmp
import os
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath

UPSTREAM = "https://github.com/microsoft/playwright-cli"
SOURCE = PurePosixPath("skills/playwright-cli")
TARGET = Path(__file__).resolve().parents[1] / SOURCE


def fetch(ref, repo):
    local_vars = subprocess.check_output(
        ["git", "rev-parse", "--local-env-vars"], text=True
    ).splitlines()
    env = {key: value for key, value in os.environ.items() if key not in local_vars}

    def git(*args):
        return subprocess.check_output(["git", *args], cwd=repo, env=env)

    git("init", "--quiet")
    git("fetch", "--quiet", "--depth=1", "--", f"{UPSTREAM}.git", ref)
    commit = git("rev-parse", "--verify", "FETCH_HEAD^{commit}").decode().strip()
    return commit, git


def render(commit, git, destination):
    tree = git(
        "ls-tree", "-rz", commit, "--", str(SOURCE), "LICENSE", "NOTICE", "NOTICE.md"
    )
    files = {}
    for entry in tree.split(b"\0"):
        if not entry:
            continue
        attributes, raw_path = entry.split(b"\t", 1)
        mode, object_type, object_id = attributes.decode().split()
        upstream_path = PurePosixPath(raw_path.decode())
        if object_type != "blob" or mode not in {"100644", "100755"}:
            raise ValueError(f"expected a regular upstream file: {upstream_path}")
        path = (
            upstream_path.relative_to(SOURCE)
            if upstream_path.is_relative_to(SOURCE)
            else upstream_path
        )
        if path in files or path == PurePosixPath("UPSTREAM.md"):
            raise ValueError(f"conflicting upstream path: {path}")
        files[path] = (object_id, mode)

    for name in ("SKILL.md", "LICENSE"):
        if PurePosixPath(name) not in files:
            raise ValueError(f"required upstream file missing: {name}")
    for path, (object_id, mode) in files.items():
        output = destination / path
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(git("cat-file", "blob", object_id))
        if mode == "100755":
            output.chmod(0o755)
    (destination / "UPSTREAM.md").write_text(
        "# Upstream source\n\n"
        f"Skill files from [Microsoft Playwright CLI]({UPSTREAM}/tree/{commit}/{SOURCE}).\n\n"
        f"Commit `{commit}`. The [upstream license](LICENSE) comes from the same revision.\n",
        encoding="utf-8",
    )


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


def install(expected):
    if TARGET.is_symlink() or (TARGET.exists() and not (TARGET / "SKILL.md").is_file()):
        raise ValueError(f"expected a Playwright CLI skill directory: {TARGET}")
    transaction = TARGET.parents[1] / ".playwright-cli-sync"
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
        if TARGET.exists():
            TARGET.rename(old)
        try:
            stage.rename(TARGET)
        except OSError:
            if old.exists():
                try:
                    old.rename(TARGET)
                except OSError as error:
                    preserve_backup = True
                    raise ValueError(
                        f"could not restore the previous skill at {old}"
                    ) from error
            raise
    finally:
        if not preserve_backup:
            shutil.rmtree(transaction)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--ref", default="HEAD", help="Git revision, defaults to upstream HEAD"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if the packaged skill differs from the source",
    )
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="playwright-skill-") as temp:
        root = Path(temp)
        repo = root / "repo"
        repo.mkdir()
        commit, git = fetch(args.ref, repo)
        expected = root / "rendered"
        render(commit, git, expected)
        if not matches(expected, TARGET):
            if args.check:
                sys.exit(
                    f"Playwright CLI skill differs from {commit}. Run the sync task to review the update."
                )
            install(expected)
    print(f"Playwright CLI skill matches {commit}")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        sys.exit(f"Playwright CLI skill sync failed: {error}")
