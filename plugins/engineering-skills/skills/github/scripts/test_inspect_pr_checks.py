#!/usr/bin/env python3
import io
import json
import subprocess
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

import inspect_pr_checks as checks


def failing_check(run_id: str, job_id: str, name: str = "test") -> dict[str, str]:
    return {
        "name": name,
        "bucket": "fail",
        "link": f"https://github.com/openai/codex/actions/runs/{run_id}/job/{job_id}",
    }


class InspectPrChecksTests(unittest.TestCase):
    def test_summary_distinguishes_pending_from_all_clear(self) -> None:
        summary = checks.summarize_checks(
            [
                {"name": "queued", "bucket": "pending", "state": "QUEUED"},
                {"name": "passed", "bucket": "pass", "state": "SUCCESS"},
                {"name": "skipped", "bucket": "skipping", "state": "SKIPPED"},
            ]
        )

        self.assertEqual(summary["pending"], 1)
        self.assertEqual(summary["passing"], 1)
        self.assertEqual(summary["skipping"], 1)

    def test_pending_check_does_not_fetch_logs(self) -> None:
        pending = {
            "name": "queued",
            "bucket": "pending",
            "link": "https://github.com/openai/codex/actions/runs/10/job/11",
        }

        with patch.object(checks, "analyze_run") as analyze_run:
            results = checks.analyze_checks(
                [pending],
                repo_root=Path("."),
                max_lines=10,
                context=2,
                max_runs=10,
                deadline=None,
                command_timeout=1,
            )

        analyze_run.assert_not_called()
        self.assertEqual(results[0]["status"], "pending")

    def test_checks_from_one_run_are_analyzed_once(self) -> None:
        source = [
            failing_check("100", "1", "first"),
            failing_check("100", "2", "second"),
            failing_check("100", "3", "third"),
        ]

        with patch.object(
            checks,
            "analyze_run",
            return_value={"status": "ok", "logSnippet": "failure"},
        ) as analyze_run:
            results = checks.analyze_checks(
                source,
                repo_root=Path("."),
                max_lines=10,
                context=2,
                max_runs=10,
                deadline=None,
                command_timeout=1,
            )

        self.assertEqual(analyze_run.call_count, 1)
        self.assertEqual(len(results), 3)
        self.assertTrue(all(result["logSnippet"] == "failure" for result in results))

    def test_representative_job_avoids_aggregate_checks(self) -> None:
        source = [
            failing_check("100", "1", "CI required"),
            failing_check("100", "2", "Bazel test"),
        ]

        with patch.object(
            checks,
            "analyze_run",
            return_value={"status": "ok"},
        ) as analyze_run:
            checks.analyze_checks(
                source,
                repo_root=Path("."),
                max_lines=10,
                context=2,
                max_runs=10,
                deadline=None,
                command_timeout=1,
            )

        self.assertEqual(analyze_run.call_args.kwargs["job_id"], "2")

    def test_large_run_log_falls_back_to_representative_job(self) -> None:
        with (
            patch.object(
                checks,
                "fetch_run_log",
                return_value=("", "too many API requests needed to fetch logs"),
            ),
            patch.object(
                checks,
                "fetch_job_log",
                return_value=("job failed", ""),
            ) as fetch_job_log,
        ):
            log, error, status = checks.fetch_check_log(
                run_id="100",
                job_id="2",
                repo_root=Path("."),
                timeout_seconds=1,
            )

        fetch_job_log.assert_called_once_with(
            "100",
            "2",
            Path("."),
            timeout_seconds=1,
        )
        self.assertEqual((log, error, status), ("job failed", "", "ok"))

    def test_run_limit_keeps_inventory_and_marks_skipped_analysis(self) -> None:
        source = [failing_check("100", "1"), failing_check("200", "2")]

        with patch.object(
            checks,
            "analyze_run",
            return_value={"status": "ok"},
        ) as analyze_run:
            results = checks.analyze_checks(
                source,
                repo_root=Path("."),
                max_lines=10,
                context=2,
                max_runs=1,
                deadline=None,
                command_timeout=1,
            )

        self.assertEqual(analyze_run.call_count, 1)
        self.assertEqual(results[1]["status"], "analysis_skipped")
        self.assertIn("--max-runs=1", results[1]["note"])

    def test_external_check_preserves_provider_url_without_log_fetch(self) -> None:
        external = {
            "name": "external",
            "bucket": "fail",
            "link": "https://ci.example.test/build/123",
        }

        with patch.object(checks, "analyze_run") as analyze_run:
            result = checks.analyze_checks(
                [external],
                repo_root=Path("."),
                max_lines=10,
                context=2,
                max_runs=10,
                deadline=None,
                command_timeout=1,
            )[0]

        analyze_run.assert_not_called()
        self.assertEqual(result["status"], "external")
        self.assertEqual(result["detailsUrl"], external["link"])

    def test_json_pending_output_is_machine_readable(self) -> None:
        pending = {"name": "queued", "bucket": "pending", "state": "QUEUED"}
        stdout = io.StringIO()
        stderr = io.StringIO()

        with (
            patch.object(sys, "argv", ["inspect_pr_checks.py", "--json", "--pr", "7"]),
            patch.object(checks, "find_git_root", return_value=Path(".")),
            patch.object(checks, "ensure_gh_available", return_value=True),
            patch.object(checks, "resolve_pr", return_value="7"),
            patch.object(checks, "fetch_checks", return_value=[pending]),
            redirect_stdout(stdout),
            redirect_stderr(stderr),
        ):
            status = checks.main()

        payload = json.loads(stdout.getvalue())
        self.assertEqual(status, 0)
        self.assertEqual(payload["summary"]["pending"], 1)
        self.assertEqual(payload["results"][0]["status"], "pending")
        self.assertIn("1 pending", stderr.getvalue())

    def test_gh_timeout_is_reported_without_raising(self) -> None:
        with patch.object(
            checks.subprocess,
            "run",
            side_effect=subprocess.TimeoutExpired(["gh", "run", "view"], 0.1),
        ):
            result = checks.run_gh_command(
                ["run", "view", "1"],
                cwd=Path("."),
                timeout_seconds=0.1,
            )

        self.assertEqual(result.returncode, 124)
        self.assertIn("timed out", result.stderr)


if __name__ == "__main__":
    unittest.main()
