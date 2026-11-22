"""Import the official Playwright CLI skill and its license from Git."""

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath

from sync_helpers import fetch, install, matches, read_files, write_files

UPSTREAM = "https://github.com/microsoft/playwright-cli"
SOURCE = PurePosixPath("skills/playwright-cli")
TARGET = Path(__file__).resolve().parents[1] / SOURCE


def render(commit, git, destination):
    upstream_files = read_files(git, commit, SOURCE, "LICENSE", "NOTICE", "NOTICE.md")
    files = {}
    for upstream_path, blob in upstream_files.items():
        path = (
            upstream_path.relative_to(SOURCE)
            if upstream_path.is_relative_to(SOURCE)
            else upstream_path
        )
        if path in files or path == PurePosixPath("UPSTREAM.md"):
            raise ValueError(f"conflicting upstream path: {path}")
        files[path] = blob

    for name in ("SKILL.md", "LICENSE"):
        if PurePosixPath(name) not in files:
            raise ValueError(f"required upstream file missing: {name}")
    write_files(destination, files)
    (destination / "UPSTREAM.md").write_text(
        "# Upstream source\n\n"
        f"Skill files from [Microsoft Playwright CLI]({UPSTREAM}/tree/{commit}/{SOURCE}).\n\n"
        f"Commit `{commit}`. The [upstream license](LICENSE) comes from the same revision.\n",
        encoding="utf-8",
    )


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
        commit, git = fetch(f"{UPSTREAM}.git", args.ref, repo)
        expected = root / "rendered"
        render(commit, git, expected)
        if not matches(expected, TARGET):
            if args.check:
                sys.exit(
                    f"Playwright CLI skill differs from {commit}. Run the sync task to review the update."
                )
            install(expected, TARGET)
    print(f"Playwright CLI skill matches {commit}")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        sys.exit(f"Playwright CLI skill sync failed: {error}")
