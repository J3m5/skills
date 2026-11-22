"""Refresh Browser Harness references and deploy the resulting skill."""

import argparse
import filecmp
import os
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
from contextlib import ExitStack
from pathlib import Path

UPSTREAM = "https://github.com/browser-use/browser-harness"
SKILL = Path(__file__).resolve().parents[1] / "skills/browser-harness"
MAINTAINED_FILES = (
    "SKILL.md",
    "agents/openai.yaml",
    "references/connection.md",
    "references/files.md",
    "references/tabs.md",
)
INTERACTION_FILES = (
    "dialogs.md",
    "make-video.md",
    "screenshots.md",
    "scrolling.md",
    "viewport.md",
)
MARKDOWN_LINK = re.compile(r"\]\(([^\s)]+\.md)(?:#[^)]+)?\)")


def git(*args, cwd=None):
    # A package postinstall can inherit repository state from a Git hook.
    local_vars = subprocess.check_output(
        ["git", "rev-parse", "--local-env-vars"], text=True
    ).splitlines()
    env = {key: value for key, value in os.environ.items() if key not in local_vars}
    result = subprocess.run(
        ["git", "--no-replace-objects", *args],
        cwd=cwd,
        env=env,
        check=False,
        capture_output=True,
    )
    if result.returncode:
        raise ValueError(result.stderr.decode(errors="replace").strip())
    return result.stdout


def resolve_version(explicit):
    tool_version = os.environ.get("MISE_TOOL_VERSION", "").removeprefix("v")
    if explicit and tool_version and explicit.removeprefix("v") != tool_version:
        raise ValueError("--version differs from MISE_TOOL_VERSION")
    version = explicit or tool_version
    if not version:
        version = subprocess.check_output(
            ["browser-harness", "--version"], text=True
        ).strip()
    version = version.removeprefix("v")
    if not re.fullmatch(r"\d+\.\d+\.\d+(?:[A-Za-z0-9.-]+)?", version):
        raise ValueError(f"invalid Browser Harness version: {version!r}")
    return version


def render(source, version, output):
    tag = f"v{version}"
    rev = (
        git("rev-parse", "--verify", f"refs/tags/{tag}^{{commit}}", cwd=source)
        .decode()
        .strip()
    )
    files = [
        "LICENSE",
        "pyproject.toml",
        *(f"interaction-skills/{name}" for name in INTERACTION_FILES),
    ]
    tree = git("ls-tree", "-r", rev, "--", *files, cwd=source).decode().splitlines()
    blobs = {}
    for entry in tree:
        attributes, path = entry.split("\t", 1)
        mode, object_type, object_id = attributes.split()
        if object_type != "blob" or mode not in {"100644", "100755"}:
            raise ValueError(f"expected a regular upstream file at {tag}: {path}")
        blobs[path] = object_id
    missing = set(files) - blobs.keys()
    if missing:
        raise ValueError(
            f"required upstream files missing at {tag}: {', '.join(sorted(missing))}"
        )

    def read(path):
        return git("cat-file", "blob", blobs[path], cwd=source)

    project = tomllib.loads(read("pyproject.toml").decode())["project"]
    if project.get("name") != "browser-harness" or project.get("version") != version:
        raise ValueError(
            f"upstream pyproject.toml does not identify browser-harness {version}"
        )

    for relative in MAINTAINED_FILES:
        dest = output / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(SKILL / relative, dest)
    (output / "LICENSE").write_bytes(read("LICENSE"))
    refs = output / "references/interaction-skills"
    refs.mkdir()
    for name in INTERACTION_FILES:
        (refs / name).write_bytes(read(f"interaction-skills/{name}"))
    (output / "references/upstream.md").write_text(
        "# Upstream references\n\n"
        f"The files in `interaction-skills/` come from [Browser Harness {tag}]"
        f"({UPSTREAM}/tree/{rev}/interaction-skills).\n\n"
        f"Commit `{rev}`. See the [upstream license](../LICENSE).\n",
        encoding="utf-8",
    )
    return rev


def validate_links(skill):
    for document in skill.rglob("*.md"):
        for href in MARKDOWN_LINK.findall(document.read_text(encoding="utf-8")):
            if "://" in href:
                continue
            target = (document.parent / href).resolve()
            if not target.is_relative_to(skill.resolve()) or not target.is_file():
                raise ValueError(f"broken skill reference: {document.name} -> {href}")


def matches(rendered, target):
    if not target.is_dir() or target.is_symlink():
        return False
    comparison = filecmp.dircmp(rendered, target, ignore=[])
    return (
        not (comparison.left_only or comparison.right_only or comparison.funny_files)
        and all(
            not (target / name).is_symlink()
            and filecmp.cmp(rendered / name, target / name, shallow=False)
            for name in comparison.common_files
        )
        and all(
            matches(rendered / name, target / name) for name in comparison.common_dirs
        )
    )


def deploy(rendered, targets):
    paths = [target.resolve() for target in targets]
    if len(paths) != len(set(paths)) or any(
        parent in paths for path in paths for parent in path.parents
    ):
        raise ValueError("deployment targets must be unique and non-overlapping")

    with ExitStack() as stack:
        staged = []
        for target in targets:
            if target.name != "browser-harness" or target.is_symlink():
                raise ValueError(
                    f"expected a real browser-harness skill directory: {target}"
                )
            if target.exists() and not (target / "SKILL.md").is_file():
                raise ValueError(f"existing target has no SKILL.md: {target}")
            if matches(rendered, target):
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            backup = target.with_name(f".{target.name}.previous")
            if backup.exists() or backup.is_symlink():
                raise ValueError(f"previous deployment backup already exists: {backup}")
            temp = stack.enter_context(
                tempfile.TemporaryDirectory(
                    prefix=".browser-harness-stage-", dir=target.parent
                )
            )
            staged.append(
                (shutil.copytree(rendered, Path(temp) / target.name), target, backup)
            )

        installed = []
        try:
            for stage, target, backup in staged:
                previous = target.exists()
                if previous:
                    target.rename(backup)
                try:
                    stage.rename(target)
                except OSError:
                    if previous:
                        backup.rename(target)
                    raise
                installed.append((target, backup if previous else None))
        except OSError:
            for target, backup in reversed(installed):
                shutil.rmtree(target)
                if backup is not None:
                    backup.rename(target)
            raise
        for _, backup in installed:
            if backup is not None:
                shutil.rmtree(backup)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source", type=Path, help="local Git checkout containing the release tag"
    )
    parser.add_argument(
        "--version", help="release version, defaults to the installed CLI"
    )
    parser.add_argument(
        "--target",
        action="append",
        type=Path,
        help="skill directory; repeat to deploy to several",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="render without writing and compare any explicit targets",
    )
    args = parser.parse_args()
    version = resolve_version(args.version)
    with tempfile.TemporaryDirectory(prefix="browser-harness-sync-") as temp:
        root = Path(temp)
        source = args.source
        if source is None:
            source = root / "source"
            git(
                "clone",
                "--quiet",
                "--depth",
                "1",
                "--branch",
                f"v{version}",
                f"{UPSTREAM}.git",
                str(source),
            )
        rendered = root / "browser-harness"
        rev = render(source, version, rendered)
        validate_links(rendered)
        if args.check:
            drift = [
                str(target)
                for target in args.target or ()
                if not matches(rendered, target)
            ]
            if drift:
                raise ValueError(f"skill differs from v{version}: {', '.join(drift)}")
        else:
            deploy(rendered, args.target or [SKILL])
    print(
        f"Browser Harness skill {'validated' if args.check else 'synchronized'} from v{version} ({rev})"
    )


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as error:
        sys.exit(f"Browser Harness skill sync failed: {error}")
