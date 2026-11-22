#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from collections.abc import Iterable, Sequence
from pathlib import Path
from shutil import which
from typing import Any

FAILURE_CONCLUSIONS = {
    "failure",
    "cancelled",
    "timed_out",
    "action_required",
}

FAILURE_STATES = {
    "failure",
    "error",
    "cancelled",
    "timed_out",
    "action_required",
}

FAILURE_BUCKETS = {"fail"}

PENDING_STATES = {
    "pending",
    "queued",
    "in_progress",
    "waiting",
    "requested",
}

PENDING_BUCKETS = {"pending"}

SKIPPING_STATES = {"skipped", "neutral"}
SKIPPING_BUCKETS = {"skipping"}

FAILURE_MARKERS = (
    "error",
    "fail",
    "failed",
    "traceback",
    "exception",
    "assert",
    "panic",
    "fatal",
    "timeout",
    "segmentation fault",
)

DEFAULT_MAX_LINES = 160
DEFAULT_CONTEXT_LINES = 30
DEFAULT_MAX_RUNS = 10
DEFAULT_ANALYSIS_TIMEOUT_SECONDS = 60.0
DEFAULT_COMMAND_TIMEOUT_SECONDS = 30.0
PENDING_LOG_MARKERS = (
    "still in progress",
    "log will be available when it is complete",
)
JOB_FALLBACK_LOG_MARKERS = PENDING_LOG_MARKERS + (
    "too many api requests needed to fetch logs",
)
LOW_SIGNAL_CHECK_MARKERS = (
    "ci results",
    "required",
    "platform result",
    "postmerge ci results",
)


class GhResult:
    def __init__(self, returncode: int, stdout: str, stderr: str):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def run_gh_command(
    args: Sequence[str],
    cwd: Path,
    timeout_seconds: float = DEFAULT_COMMAND_TIMEOUT_SECONDS,
) -> GhResult:
    try:
        process = subprocess.run(
            ["gh", *args],
            cwd=cwd,
            text=True,
            capture_output=True,
            check=False,
            timeout=max(0.1, timeout_seconds),
        )
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
        if isinstance(stdout, bytes):
            stdout = stdout.decode(errors="replace")
        if isinstance(stderr, bytes):
            stderr = stderr.decode(errors="replace")
        message = f"gh command timed out after {timeout_seconds:.1f}s"
        return GhResult(124, str(stdout), str(stderr).strip() or message)
    return GhResult(process.returncode, process.stdout, process.stderr)


def run_gh_command_raw(
    args: Sequence[str],
    cwd: Path,
    timeout_seconds: float = DEFAULT_COMMAND_TIMEOUT_SECONDS,
) -> tuple[int, bytes, str]:
    try:
        process = subprocess.run(
            ["gh", *args],
            cwd=cwd,
            capture_output=True,
            check=False,
            timeout=max(0.1, timeout_seconds),
        )
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or b""
        stderr = exc.stderr or b""
        if isinstance(stdout, str):
            stdout = stdout.encode()
        if isinstance(stderr, bytes):
            stderr = stderr.decode(errors="replace")
        message = f"gh command timed out after {timeout_seconds:.1f}s"
        return 124, stdout, str(stderr).strip() or message
    stderr = process.stderr.decode(errors="replace")
    return process.returncode, process.stdout, stderr


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Inspect failing GitHub PR checks, fetch GitHub Actions logs, and extract a "
            "failure snippet."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--repo", default=".", help="Path inside the target Git repository."
    )
    parser.add_argument(
        "--pr", default=None, help="PR number or URL (defaults to current branch PR)."
    )
    parser.add_argument("--max-lines", type=int, default=DEFAULT_MAX_LINES)
    parser.add_argument("--context", type=int, default=DEFAULT_CONTEXT_LINES)
    parser.add_argument(
        "--max-runs",
        type=int,
        default=DEFAULT_MAX_RUNS,
        help="Maximum distinct GitHub Actions runs whose logs are fetched (0 disables the cap).",
    )
    parser.add_argument(
        "--analysis-timeout",
        type=float,
        default=DEFAULT_ANALYSIS_TIMEOUT_SECONDS,
        help="Overall seconds allowed for run metadata and log analysis (0 disables the budget).",
    )
    parser.add_argument(
        "--command-timeout",
        type=float,
        default=DEFAULT_COMMAND_TIMEOUT_SECONDS,
        help="Maximum seconds for one gh command.",
    )
    parser.add_argument(
        "--json", action="store_true", help="Emit JSON instead of text output."
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = find_git_root(Path(args.repo))
    if repo_root is None:
        print("Error: not inside a Git repository.", file=sys.stderr)
        return 1

    command_timeout = max(0.1, args.command_timeout)
    if not ensure_gh_available(repo_root, timeout_seconds=command_timeout):
        return 1

    pr_value = resolve_pr(args.pr, repo_root, timeout_seconds=command_timeout)
    if pr_value is None:
        return 1

    checks = fetch_checks(pr_value, repo_root, timeout_seconds=command_timeout)
    if checks is None:
        return 1

    summary = summarize_checks(checks)
    actionable = [
        check for check in checks if check_kind(check) in {"failing", "pending"}
    ]
    print(
        f"PR #{pr_value}: {summary['failing']} failing, {summary['pending']} pending, "
        f"{summary['passing']} passing, {summary['skipping']} skipped.",
        file=sys.stderr,
    )

    deadline = None
    if args.analysis_timeout > 0:
        deadline = time.monotonic() + args.analysis_timeout
    results = analyze_checks(
        actionable,
        repo_root=repo_root,
        max_lines=max(1, args.max_lines),
        context=max(1, args.context),
        max_runs=max(0, args.max_runs),
        deadline=deadline,
        command_timeout=command_timeout,
    )

    if args.json:
        print(
            json.dumps(
                {"pr": pr_value, "summary": summary, "results": results}, indent=2
            )
        )
    else:
        render_results(pr_value, summary, results)

    return 1 if summary["failing"] else 0


def find_git_root(start: Path) -> Path | None:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=start,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    return Path(result.stdout.strip())


def ensure_gh_available(
    repo_root: Path,
    timeout_seconds: float = DEFAULT_COMMAND_TIMEOUT_SECONDS,
) -> bool:
    if which("gh") is None:
        print("Error: gh is not installed or not on PATH.", file=sys.stderr)
        return False
    result = run_gh_command(
        ["auth", "status"], cwd=repo_root, timeout_seconds=timeout_seconds
    )
    if result.returncode == 0:
        return True
    message = (result.stderr or result.stdout or "").strip()
    print(message or "Error: gh not authenticated.", file=sys.stderr)
    return False


def resolve_pr(
    pr_value: str | None,
    repo_root: Path,
    timeout_seconds: float = DEFAULT_COMMAND_TIMEOUT_SECONDS,
) -> str | None:
    if pr_value:
        return pr_value
    result = run_gh_command(
        ["pr", "view", "--json", "number"],
        cwd=repo_root,
        timeout_seconds=timeout_seconds,
    )
    if result.returncode != 0:
        message = (result.stderr or result.stdout or "").strip()
        print(message or "Error: unable to resolve PR.", file=sys.stderr)
        return None
    try:
        data = json.loads(result.stdout or "{}")
    except json.JSONDecodeError:
        print("Error: unable to parse PR JSON.", file=sys.stderr)
        return None
    number = data.get("number")
    if not number:
        print("Error: no PR number found.", file=sys.stderr)
        return None
    return str(number)


def fetch_checks(
    pr_value: str,
    repo_root: Path,
    timeout_seconds: float = DEFAULT_COMMAND_TIMEOUT_SECONDS,
) -> list[dict[str, Any]] | None:
    primary_fields = [
        "name",
        "state",
        "conclusion",
        "detailsUrl",
        "startedAt",
        "completedAt",
    ]
    result = run_gh_command(
        ["pr", "checks", pr_value, "--json", ",".join(primary_fields)],
        cwd=repo_root,
        timeout_seconds=timeout_seconds,
    )
    if result.returncode != 0:
        message = "\n".join(filter(None, [result.stderr, result.stdout])).strip()
        available_fields = parse_available_fields(message)
        if available_fields:
            fallback_fields = [
                "name",
                "state",
                "bucket",
                "link",
                "startedAt",
                "completedAt",
                "workflow",
            ]
            selected_fields = [
                field for field in fallback_fields if field in available_fields
            ]
            if not selected_fields:
                print(
                    "Error: no usable fields available for gh pr checks.",
                    file=sys.stderr,
                )
                return None
            result = run_gh_command(
                ["pr", "checks", pr_value, "--json", ",".join(selected_fields)],
                cwd=repo_root,
                timeout_seconds=timeout_seconds,
            )
            if result.returncode != 0:
                message = (result.stderr or result.stdout or "").strip()
                print(message or "Error: gh pr checks failed.", file=sys.stderr)
                return None
        else:
            print(message or "Error: gh pr checks failed.", file=sys.stderr)
            return None
    try:
        data = json.loads(result.stdout or "[]")
    except json.JSONDecodeError:
        print("Error: unable to parse checks JSON.", file=sys.stderr)
        return None
    if not isinstance(data, list):
        print("Error: unexpected checks JSON shape.", file=sys.stderr)
        return None
    return data


def is_failing(check: dict[str, Any]) -> bool:
    conclusion = normalize_field(check.get("conclusion"))
    if conclusion in FAILURE_CONCLUSIONS:
        return True
    state = normalize_field(check.get("state") or check.get("status"))
    if state in FAILURE_STATES:
        return True
    bucket = normalize_field(check.get("bucket"))
    return bucket in FAILURE_BUCKETS


def is_pending(check: dict[str, Any]) -> bool:
    state = normalize_field(check.get("state") or check.get("status"))
    if state in PENDING_STATES:
        return True
    bucket = normalize_field(check.get("bucket"))
    return bucket in PENDING_BUCKETS


def check_kind(check: dict[str, Any]) -> str:
    if is_failing(check):
        return "failing"
    if is_pending(check):
        return "pending"
    state = normalize_field(check.get("state") or check.get("status"))
    bucket = normalize_field(check.get("bucket"))
    if state in SKIPPING_STATES or bucket in SKIPPING_BUCKETS:
        return "skipping"
    if state in {"success", "completed"} or bucket in {"pass", "passing"}:
        return "passing"
    return "other"


def summarize_checks(checks: Iterable[dict[str, Any]]) -> dict[str, int]:
    summary = {
        "total": 0,
        "failing": 0,
        "pending": 0,
        "passing": 0,
        "skipping": 0,
        "other": 0,
    }
    run_ids: set[str] = set()
    for check in checks:
        summary["total"] += 1
        kind = check_kind(check)
        summary[kind] += 1
        if kind == "failing":
            url = check.get("detailsUrl") or check.get("link") or ""
            run_id = extract_run_id(url)
            if run_id:
                run_ids.add(run_id)
    summary["failingRuns"] = len(run_ids)
    return summary


def analyze_checks(
    checks: Iterable[dict[str, Any]],
    repo_root: Path,
    max_lines: int,
    context: int,
    max_runs: int,
    deadline: float | None,
    command_timeout: float,
) -> list[dict[str, Any]]:
    checks_list = list(checks)
    failing_run_ids = {
        run_id
        for check in checks_list
        if check_kind(check) == "failing"
        for run_id in [
            extract_run_id(check.get("detailsUrl") or check.get("link") or "")
        ]
        if run_id
    }
    representative_jobs = choose_representative_jobs(checks_list)
    run_analyses: dict[str, dict[str, Any]] = {}
    analyzed_runs = 0
    results: list[dict[str, Any]] = []

    for check in checks_list:
        kind = check_kind(check)
        url = check.get("detailsUrl") or check.get("link") or ""
        run_id = extract_run_id(url)
        job_id = extract_job_id(url)
        base: dict[str, Any] = {
            "name": check.get("name", ""),
            "detailsUrl": url,
            "runId": run_id,
            "jobId": job_id,
            "checkState": kind,
        }

        if kind == "pending":
            base["status"] = "pending"
            base["note"] = "Check is pending; logs may be incomplete or unavailable."
            results.append(base)
            continue

        if run_id is None:
            base["status"] = "external"
            base["note"] = "No GitHub Actions run id detected in detailsUrl."
            results.append(base)
            continue

        if run_id not in run_analyses:
            if max_runs and analyzed_runs >= max_runs:
                run_analyses[run_id] = {
                    "status": "analysis_skipped",
                    "note": f"Run analysis skipped after reaching --max-runs={max_runs}.",
                }
            elif deadline is not None and time.monotonic() >= deadline:
                run_analyses[run_id] = {
                    "status": "analysis_skipped",
                    "note": "Run analysis skipped because the overall analysis budget was exhausted.",
                }
            else:
                analyzed_runs += 1
                print(
                    f"Analyzing GitHub Actions run {run_id} "
                    f"({analyzed_runs}/{len(failing_run_ids)})...",
                    file=sys.stderr,
                )
                run_analyses[run_id] = analyze_run(
                    run_id=run_id,
                    job_id=representative_jobs.get(run_id),
                    repo_root=repo_root,
                    max_lines=max_lines,
                    context=context,
                    deadline=deadline,
                    command_timeout=command_timeout,
                )

        base.update(run_analyses[run_id])
        results.append(base)

    return results


def choose_representative_jobs(checks: Iterable[dict[str, Any]]) -> dict[str, str]:
    candidates: dict[str, list[tuple[bool, str]]] = {}
    for check in checks:
        if check_kind(check) != "failing":
            continue
        url = check.get("detailsUrl") or check.get("link") or ""
        run_id = extract_run_id(url)
        job_id = extract_job_id(url)
        if not run_id or not job_id:
            continue
        name = normalize_field(check.get("name"))
        low_signal = any(marker in name for marker in LOW_SIGNAL_CHECK_MARKERS)
        candidates.setdefault(run_id, []).append((low_signal, job_id))

    return {
        run_id: min(run_candidates, key=lambda candidate: candidate[0])[1]
        for run_id, run_candidates in candidates.items()
    }


def analyze_run(
    run_id: str,
    job_id: str | None,
    repo_root: Path,
    max_lines: int,
    context: int,
    deadline: float | None,
    command_timeout: float,
) -> dict[str, Any]:
    timeout = remaining_timeout(deadline, command_timeout)
    if timeout is None:
        return {
            "status": "analysis_skipped",
            "note": "Run analysis skipped because the overall analysis budget was exhausted.",
        }

    metadata = fetch_run_metadata(run_id, repo_root, timeout_seconds=timeout)
    timeout = remaining_timeout(deadline, command_timeout)
    if timeout is None:
        result: dict[str, Any] = {
            "status": "analysis_skipped",
            "note": "Log analysis skipped because the overall analysis budget was exhausted.",
        }
        if metadata:
            result["run"] = metadata
        return result

    log_text, log_error, log_status = fetch_check_log(
        run_id=run_id,
        job_id=job_id,
        repo_root=repo_root,
        timeout_seconds=timeout,
    )
    result = {}
    if metadata:
        result["run"] = metadata

    if log_status == "pending":
        result["status"] = "log_pending"
        result["note"] = log_error or "Logs are not available yet."
        return result
    if log_error:
        result["status"] = "log_unavailable"
        result["error"] = log_error
        return result

    result["status"] = "ok"
    result["logSnippet"] = extract_failure_snippet(
        log_text,
        max_lines=max_lines,
        context=context,
    )
    result["logTail"] = tail_lines(log_text, max_lines)
    return result


def remaining_timeout(deadline: float | None, command_timeout: float) -> float | None:
    if deadline is None:
        return command_timeout
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        return None
    return max(0.1, min(command_timeout, remaining))


def analyze_check(
    check: dict[str, Any],
    repo_root: Path,
    max_lines: int,
    context: int,
) -> dict[str, Any]:
    return analyze_checks(
        [check],
        repo_root=repo_root,
        max_lines=max_lines,
        context=context,
        max_runs=0,
        deadline=None,
        command_timeout=DEFAULT_COMMAND_TIMEOUT_SECONDS,
    )[0]


def extract_run_id(url: str) -> str | None:
    if not url:
        return None
    for pattern in (r"/actions/runs/(\d+)", r"/runs/(\d+)"):
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def extract_job_id(url: str) -> str | None:
    if not url:
        return None
    match = re.search(r"/actions/runs/\d+/job/(\d+)", url)
    if match:
        return match.group(1)
    match = re.search(r"/job/(\d+)", url)
    if match:
        return match.group(1)
    return None


def fetch_run_metadata(
    run_id: str,
    repo_root: Path,
    timeout_seconds: float = DEFAULT_COMMAND_TIMEOUT_SECONDS,
) -> dict[str, Any] | None:
    fields = [
        "conclusion",
        "status",
        "workflowName",
        "name",
        "event",
        "headBranch",
        "headSha",
        "url",
    ]
    result = run_gh_command(
        ["run", "view", run_id, "--json", ",".join(fields)],
        cwd=repo_root,
        timeout_seconds=timeout_seconds,
    )
    if result.returncode != 0:
        return None
    try:
        data = json.loads(result.stdout or "{}")
    except json.JSONDecodeError:
        return None
    if not isinstance(data, dict):
        return None
    return data


def fetch_check_log(
    run_id: str,
    job_id: str | None,
    repo_root: Path,
    timeout_seconds: float = DEFAULT_COMMAND_TIMEOUT_SECONDS,
) -> tuple[str, str, str]:
    log_text, log_error = fetch_run_log(
        run_id, repo_root, timeout_seconds=timeout_seconds
    )
    if not log_error:
        return log_text, "", "ok"

    if should_fetch_job_log(log_error) and job_id:
        job_log, job_error = fetch_job_log(
            run_id,
            job_id,
            repo_root,
            timeout_seconds=timeout_seconds,
        )
        if job_log:
            return job_log, "", "ok"
        if job_error and is_log_pending_message(job_error):
            return "", job_error, "pending"
        if job_error:
            return "", job_error, "error"
        return "", log_error, "pending"

    if is_log_pending_message(log_error):
        return "", log_error, "pending"

    return "", log_error, "error"


def fetch_run_log(
    run_id: str,
    repo_root: Path,
    timeout_seconds: float = DEFAULT_COMMAND_TIMEOUT_SECONDS,
) -> tuple[str, str]:
    result = run_gh_command(
        ["run", "view", run_id, "--log"],
        cwd=repo_root,
        timeout_seconds=timeout_seconds,
    )
    if result.returncode != 0:
        error = (result.stderr or result.stdout or "").strip()
        return "", error or "gh run view failed"
    return result.stdout, ""


def fetch_job_log(
    run_id: str,
    job_id: str,
    repo_root: Path,
    timeout_seconds: float = DEFAULT_COMMAND_TIMEOUT_SECONDS,
) -> tuple[str, str]:
    result = run_gh_command(
        ["run", "view", run_id, "--job", job_id, "--log"],
        cwd=repo_root,
        timeout_seconds=timeout_seconds,
    )
    if result.returncode != 0:
        message = (result.stderr or result.stdout or "").strip()
        return "", message or "gh run view --job failed"
    return result.stdout, ""


def fetch_repo_slug(
    repo_root: Path,
    timeout_seconds: float = DEFAULT_COMMAND_TIMEOUT_SECONDS,
) -> str | None:
    result = run_gh_command(
        ["repo", "view", "--json", "nameWithOwner"],
        cwd=repo_root,
        timeout_seconds=timeout_seconds,
    )
    if result.returncode != 0:
        return None
    try:
        data = json.loads(result.stdout or "{}")
    except json.JSONDecodeError:
        return None
    name_with_owner = data.get("nameWithOwner")
    if not name_with_owner:
        return None
    return str(name_with_owner)


def normalize_field(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip().lower()


def parse_available_fields(message: str) -> list[str]:
    if "Available fields:" not in message:
        return []
    fields: list[str] = []
    collecting = False
    for line in message.splitlines():
        if "Available fields:" in line:
            collecting = True
            continue
        if not collecting:
            continue
        field = line.strip()
        if not field:
            continue
        fields.append(field)
    return fields


def is_log_pending_message(message: str) -> bool:
    lowered = message.lower()
    return any(marker in lowered for marker in PENDING_LOG_MARKERS)


def should_fetch_job_log(message: str) -> bool:
    lowered = message.lower()
    return any(marker in lowered for marker in JOB_FALLBACK_LOG_MARKERS)


def is_zip_payload(payload: bytes) -> bool:
    return payload.startswith(b"PK")


def extract_failure_snippet(log_text: str, max_lines: int, context: int) -> str:
    lines = log_text.splitlines()
    if not lines:
        return ""

    marker_index = find_failure_index(lines)
    if marker_index is None:
        return "\n".join(lines[-max_lines:])

    start = max(0, marker_index - context)
    end = min(len(lines), marker_index + context)
    window = lines[start:end]
    if len(window) > max_lines:
        window = window[-max_lines:]
    return "\n".join(window)


def find_failure_index(lines: Sequence[str]) -> int | None:
    for idx in range(len(lines) - 1, -1, -1):
        lowered = lines[idx].lower()
        if any(marker in lowered for marker in FAILURE_MARKERS):
            return idx
    return None


def tail_lines(text: str, max_lines: int) -> str:
    if max_lines <= 0:
        return ""
    lines = text.splitlines()
    return "\n".join(lines[-max_lines:])


def render_results(
    pr_number: str,
    summary: dict[str, int],
    results: Iterable[dict[str, Any]],
) -> None:
    results_list = list(results)
    if not results_list:
        print(f"PR #{pr_number}: all checks clear ({summary['passing']} passing).")
        return
    print(
        f"PR #{pr_number}: {summary['failing']} failing, {summary['pending']} pending, "
        f"{summary['passing']} passing, {summary['skipping']} skipped; "
        f"{summary['failingRuns']} failing GitHub Actions runs."
    )
    for result in results_list:
        print("-" * 60)
        print(f"Check: {result.get('name', '')}")
        if result.get("detailsUrl"):
            print(f"Details: {result['detailsUrl']}")
        run_id = result.get("runId")
        if run_id:
            print(f"Run ID: {run_id}")
        job_id = result.get("jobId")
        if job_id:
            print(f"Job ID: {job_id}")
        status = result.get("status", "unknown")
        print(f"Status: {status}")

        run_meta = result.get("run", {})
        if run_meta:
            branch = run_meta.get("headBranch", "")
            sha = (run_meta.get("headSha") or "")[:12]
            workflow = run_meta.get("workflowName") or run_meta.get("name") or ""
            conclusion = run_meta.get("conclusion") or run_meta.get("status") or ""
            print(f"Workflow: {workflow} ({conclusion})")
            if branch or sha:
                print(f"Branch/SHA: {branch} {sha}")
            if run_meta.get("url"):
                print(f"Run URL: {run_meta['url']}")

        if result.get("note"):
            print(f"Note: {result['note']}")

        if result.get("error"):
            print(f"Error fetching logs: {result['error']}")
            continue

        snippet = result.get("logSnippet") or ""
        if snippet:
            print("Failure snippet:")
            print(indent_block(snippet, prefix="  "))
        else:
            print("No snippet available.")
    print("-" * 60)


def indent_block(text: str, prefix: str = "  ") -> str:
    return "\n".join(f"{prefix}{line}" for line in text.splitlines())


if __name__ == "__main__":
    raise SystemExit(main())
