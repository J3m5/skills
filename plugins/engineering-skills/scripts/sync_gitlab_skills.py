"""Sync the bundled GitLab skills and regenerate their split references."""

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath

from sync_helpers import fetch, git_reader, install, matches, read_files, write_files

SKILLS = Path(__file__).resolve().parents[1] / "skills"
UPSTREAM = {
    "glab": "https://gitlab.com/gitlab-org/cli.git",
    "gitlab-ci-skill": "https://gitlab.com/gitlab-org/ci-cd/gitlab-ci-skill.git",
}
GLAB_SOURCE = "internal/commands/skills/bundled/assets/glab/SKILL.md"
GLAB_SECTIONS = {
    "Quick reference": "commands.md",
    "Comments and discussions": "comments.md",
    "API calls": "api.md",
    "Common mistakes": "pitfalls.md",
    "Contributing improvements": "upstream-maintenance.md",
}
CI_WORKFLOWS = {
    "Workflow 1: Create initial pipeline": (
        "Create initial pipeline",
        "create-pipeline.md",
        (
            "For a first pipeline, use [Create an initial pipeline](references/create-pipeline.md) "
            "to select jobs from the project stack and verify the resulting graph."
        ),
    ),
    "Workflow 2: Add a job to an existing pipeline": (
        "Add a job to an existing pipeline",
        "add-job.md",
        (
            "For an existing pipeline, use [Add a job](references/add-job.md) "
            "to match the project's conventions and verify the affected job."
        ),
    ),
}
SOURCE_COMMIT = re.compile(r"^(  source-commit: )([0-9a-f]{40})$", re.MULTILINE)
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
HEADING = re.compile(r"^ {0,3}(#{1,6})[ \t]+(.+?)\s*$")


def headings(markdown):
    fence = None
    for index, line in enumerate(markdown.splitlines(keepends=True)):
        marker = FENCE.match(line)
        if fence:
            if marker and marker[1].startswith(fence) and not marker[2].strip():
                fence = None
        elif marker:
            fence = marker[1]
        elif match := HEADING.match(line):
            yield index, match
    if fence:
        raise ValueError("unclosed code fence in upstream Markdown")


def split_sections(markdown, depth):
    lines = markdown.splitlines(keepends=True)
    sections = {}
    starts = [(i, m[2]) for i, m in headings(markdown) if len(m[1]) == depth]
    end = len(lines)
    for index, name in reversed(starts):
        if name in sections:
            raise ValueError(f"duplicate upstream heading: {name}")
        sections[name] = "".join(lines[index:end]).rstrip() + "\n"
        end = index
    return "".join(lines[:end]), dict(reversed(sections.items()))


def put(files, path, text):
    files[PurePosixPath(path)] = text.encode(), "100644"


def require_files(files, *names):
    for name in names:
        if PurePosixPath(name) not in files:
            raise ValueError(f"required upstream file missing: {name}")


def render_glab(git, commit, target):
    files = read_files(git, commit, GLAB_SOURCE, "LICENSE")
    require_files(files, GLAB_SOURCE, "LICENSE")
    raw, _ = files.pop(PurePosixPath(GLAB_SOURCE))
    _, sections = split_sections(raw.decode(), 2)
    if set(sections) != GLAB_SECTIONS.keys():
        raise ValueError(f"review the upstream glab section mapping: {list(sections)}")
    if not re.search(r"(?mi)^### Content-type guidance$", sections["API calls"]):
        raise ValueError("review the upstream Content-type guidance anchor")
    for name, filename in GLAB_SECTIONS.items():
        body = sections[name]
        if name == "Comments and discussions":
            body = body.replace(
                "](#content-type-guidance)", "](api.md#content-type-guidance)"
            )
        if re.search(r"\]\(#[^)]+\)", body):
            raise ValueError(f"review links to upstream anchors in {name}")
        put(files, f"references/{filename}", body)

    entrypoint = (target / "SKILL.md").read_text(encoding="utf-8")
    content, count = SOURCE_COMMIT.subn(lambda match: match[1] + commit, entrypoint)
    if count != 1:
        raise ValueError("glab SKILL.md must have exactly one source-commit field")
    put(files, "SKILL.md", content)
    maintenance = PurePosixPath("references/maintenance.md")
    files[maintenance] = (target / maintenance).read_bytes(), "100644"
    return files


def render_ci(git, commit, _target):
    files = read_files(
        git,
        commit,
        "SKILL.md",
        "LICENSE",
        "README.md",
        "references",
        "scripts",
        "examples",
    )
    require_files(
        files, "SKILL.md", "LICENSE", "scripts/verify.sh", "references/verification.md"
    )
    raw, _ = files.pop(PurePosixPath("SKILL.md"))
    intro, sections = split_sections(raw.decode(), 2)
    if not intro.startswith("---\nname: gitlab-ci-skill\n"):
        raise ValueError("unexpected upstream gitlab-ci-skill frontmatter")
    if "When to use this skill" not in sections or "Workflows" not in sections:
        raise ValueError("review the upstream GitLab CI section mapping")
    del sections["When to use this skill"]
    workflow_intro, workflows = split_sections(sections["Workflows"], 3)
    for name, (heading, filename, routing) in CI_WORKFLOWS.items():
        if name not in workflows:
            raise ValueError(f"required upstream workflow missing: {name}")
        body = workflows[name].split("\n", 1)[1].lstrip("\n")
        lines = body.splitlines(keepends=True)
        for index, match in headings(body):
            if len(match[1]) >= 4:
                lines[index] = lines[index].replace(match[1], match[1][2:], 1)
        put(
            files,
            f"references/{filename}",
            f"# {heading}\n\n"
            "Paths to scripts and references below are relative to the skill directory.\n\n"
            + "".join(lines),
        )
        workflows[name] = f"### {name}\n\n{routing}\n"
    sections["Workflows"] = workflow_intro + "\n".join(workflows.values())
    content = "\n".join(sections.values())
    content = replace_once(
        content,
        "Run `scripts/verify.sh show` after every generation or edit (lint plus pipeline graph); "
        "surface failures to the user before showing the YAML.",
        "Run lint and render the pipeline graph after editing. Use `scripts/verify.sh auto` "
        "when simulation is appropriate, or run the `lint` and `show` tiers separately.",
    )
    content = replace_once(
        content,
        "It runs `glci show` (always free, offline) and then `glci run --simulate` "
        "if Docker is reachable, in one command. When Docker is absent, it stops "
        "after show and offers an OS-specific install pointer.",
        "It runs `glci lint` followed by `glci show`. It stops on either failure and "
        "simulates only when Docker is reachable and the repository has commits.",
    )
    put(
        files,
        "SKILL.md",
        "---\nname: gitlab-ci-skill\n"
        "description: Author, validate, debug, optimize, or explain GitLab CI/CD pipelines. "
        "Use for job failures, CI configuration, and CI/CD Catalog components.\n"
        "metadata:\n"
        "  source-project: gitlab-org/ci-cd/gitlab-ci-skill\n"
        f"  source-commit: {commit}\n"
        "---\n\n# GitLab CI Skill\n\n" + content,
    )
    # verify.sh parses wrapper flags before the verification tier.
    for path, (data, mode) in files.items():
        if path.suffix == ".md":
            files[path] = (
                re.sub(
                    rb"(\bscripts/verify\.sh) (auto|lint|show) -f (<file>|\.gitlab-ci\.yml)",
                    rb"\1 -f \3 \2",
                    data,
                ),
                mode,
            )
    return files


def replace_once(text, old, new):
    if text.count(old) != 1:
        raise ValueError(f"review changed upstream verification guidance: {old}")
    return text.replace(old, new, 1)


def pinned_ref(target):
    match = SOURCE_COMMIT.search((target / "SKILL.md").read_text(encoding="utf-8"))
    if not match:
        raise ValueError(f"{target.name} SKILL.md has no source-commit")
    return match[2]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill", choices=UPSTREAM)
    parser.add_argument(
        "--ref", help="upstream Git revision, defaults to recorded commit"
    )
    parser.add_argument(
        "--checkout", type=Path, help="read from a local upstream checkout"
    )
    parser.add_argument(
        "--check", action="store_true", help="report drift without writing"
    )
    args = parser.parse_args()
    target = SKILLS / args.skill
    ref = args.ref or pinned_ref(target)
    with tempfile.TemporaryDirectory(prefix="gitlab-skill-") as temp:
        root = Path(temp)
        if args.checkout:
            git = git_reader(args.checkout)
            commit = git("rev-parse", "--verify", f"{ref}^{{commit}}").decode().strip()
        else:
            repo = root / "repo"
            repo.mkdir()
            commit, git = fetch(UPSTREAM[args.skill], ref, repo)
        render = render_glab if args.skill == "glab" else render_ci
        output = root / "rendered"
        write_files(output, render(git, commit, target))
        if not matches(output, target):
            if args.check:
                sys.exit(f"{args.skill} differs from {commit}")
            install(output, target)
    print(f"{args.skill} matches {commit}")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        sys.exit(f"GitLab skill sync failed: {error}")
