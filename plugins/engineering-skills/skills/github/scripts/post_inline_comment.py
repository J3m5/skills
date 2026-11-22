#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


def read_body(args: argparse.Namespace) -> str:
    if args.body is not None:
        return args.body
    if args.body_file:
        try:
            return Path(args.body_file).read_text(encoding="utf-8")
        except OSError as exc:
            raise ValueError(f"Failed to read --body-file: {exc}") from exc
    raise ValueError("Either --body or --body-file is required for this mode")


def run_gh_api(endpoint: str, payload: dict, timeout: int) -> int:
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", suffix=".json", delete=False, encoding="utf-8"
        ) as tmp:
            json.dump(payload, tmp, ensure_ascii=False)
            tmp.flush()
            tmp_path = tmp.name

        cmd = ["gh", "api", "-X", "POST", endpoint, "--input", tmp_path]
        proc = subprocess.run(
            cmd, check=False, capture_output=True, text=True, timeout=timeout
        )

        if proc.returncode != 0:
            print(proc.stderr.strip(), file=sys.stderr)
            return proc.returncode

        print(proc.stdout.strip())
        return 0
    except FileNotFoundError:
        print("gh CLI not found. Install gh and authenticate first.", file=sys.stderr)
        return 127
    except subprocess.TimeoutExpired:
        print(f"gh api command timed out after {timeout} seconds.", file=sys.stderr)
        return 124
    finally:
        if tmp_path:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description=(
            "Post PR review comments via gh api: immediate inline comment, pending review creation, "
            "pending review submission, or reply to an existing comment thread."
        )
    )
    p.add_argument("--repo", required=True, help="owner/repo")
    p.add_argument("--pr", required=True, type=int, help="Pull request number")
    p.add_argument(
        "--mode",
        default="pending-create",
        choices=["immediate", "pending-create", "pending-submit", "reply"],
        help="Operation mode",
    )
    p.add_argument("--timeout", type=int, default=60, help="gh api timeout in seconds")

    # Body fields used by multiple modes
    g = p.add_mutually_exclusive_group()
    g.add_argument("--body", help="Body text")
    g.add_argument("--body-file", help="Path to a UTF-8 text file containing body")

    # Inline location fields (immediate and optional for pending-create single comment)
    p.add_argument("--commit", help="Head commit SHA to anchor against")
    p.add_argument("--path", help="File path in repo")
    p.add_argument("--line", type=int, help="Target line in diff")
    p.add_argument(
        "--side", default="RIGHT", choices=["RIGHT", "LEFT"], help="Diff side"
    )
    p.add_argument(
        "--start-line",
        type=int,
        default=None,
        help="Optional start line for range comment",
    )
    p.add_argument(
        "--start-side",
        choices=["RIGHT", "LEFT"],
        default=None,
        help="Optional start side",
    )

    # Pending review fields
    p.add_argument(
        "--review-body", help="Optional review-level body for pending-create"
    )
    p.add_argument(
        "--comments-file",
        help="JSON file containing comments array for pending-create (objects with path/body/line/side/optional start_line/start_side)",
    )

    # Submit pending review fields
    p.add_argument("--review-id", type=int, help="Review ID for pending-submit")
    p.add_argument(
        "--event",
        choices=["COMMENT", "APPROVE", "REQUEST_CHANGES"],
        help="Submit event for pending-submit",
    )

    # Reply fields
    p.add_argument(
        "--comment-id", type=int, help="Existing review comment ID for reply mode"
    )

    return p.parse_args()


def build_single_inline_comment(args: argparse.Namespace, comment_body: str) -> dict:
    if not args.commit:
        raise ValueError("--commit is required")
    if not args.path:
        raise ValueError("--path is required")
    if args.line is None:
        raise ValueError("--line is required")

    payload = {
        "body": comment_body,
        "commit_id": args.commit,
        "path": args.path,
        "line": args.line,
        "side": args.side,
    }
    if args.start_line is not None:
        payload["start_line"] = args.start_line
        payload["start_side"] = args.start_side or args.side

    return payload


def load_comments_array(path: str) -> list:
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except OSError as exc:
        raise ValueError(f"Failed to read --comments-file: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in --comments-file: {exc}") from exc

    if not isinstance(data, list):
        raise TypeError("--comments-file must contain a JSON array")

    for idx, item in enumerate(data):
        if not isinstance(item, dict):
            raise TypeError(f"comments[{idx}] must be an object")
        for key in ["path", "body", "line", "side"]:
            if key not in item:
                raise ValueError(f"comments[{idx}] missing required key: {key}")
        if not isinstance(item["path"], str) or not item["path"].strip():
            raise ValueError(f"comments[{idx}].path must be a non-empty string")
        if not isinstance(item["body"], str) or not item["body"].strip():
            raise ValueError(f"comments[{idx}].body must be a non-empty string")
        if not isinstance(item["line"], int) or item["line"] <= 0:
            raise ValueError(f"comments[{idx}].line must be a positive integer")
        if item["side"] not in ("RIGHT", "LEFT"):
            raise ValueError(f"comments[{idx}].side must be RIGHT or LEFT")

        if "start_line" in item:
            if not isinstance(item["start_line"], int) or item["start_line"] <= 0:
                raise ValueError(
                    f"comments[{idx}].start_line must be a positive integer"
                )
            start_side = item.get("start_side", item["side"])
            if start_side not in ("RIGHT", "LEFT"):
                raise ValueError(f"comments[{idx}].start_side must be RIGHT or LEFT")

    return data


def main() -> int:
    args = parse_args()

    try:
        if args.mode == "immediate":
            comment_body = read_body(args)
            payload = build_single_inline_comment(args, comment_body)
            endpoint = f"repos/{args.repo}/pulls/{args.pr}/comments"
            return run_gh_api(endpoint, payload, args.timeout)

        if args.mode == "pending-create":
            if not args.commit:
                raise ValueError("--commit is required for pending-create")

            comments = []
            if args.comments_file:
                comments = load_comments_array(args.comments_file)
            else:
                # Allow single-comment creation without comments-file
                comment_body = read_body(args)
                single = build_single_inline_comment(args, comment_body)
                # For create review API, inline comments should not include commit_id per item
                single.pop("commit_id", None)
                comments = [single]

            payload = {
                "commit_id": args.commit,
                "comments": comments,
            }
            if args.review_body:
                payload["body"] = args.review_body

            endpoint = f"repos/{args.repo}/pulls/{args.pr}/reviews"
            return run_gh_api(endpoint, payload, args.timeout)

        if args.mode == "pending-submit":
            if args.review_id is None:
                raise ValueError("--review-id is required for pending-submit")
            if not args.event:
                raise ValueError("--event is required for pending-submit")

            payload = {"event": args.event}
            if args.body is not None or args.body_file:
                payload["body"] = read_body(args)

            endpoint = (
                f"repos/{args.repo}/pulls/{args.pr}/reviews/{args.review_id}/events"
            )
            return run_gh_api(endpoint, payload, args.timeout)

        if args.mode == "reply":
            if args.comment_id is None:
                raise ValueError("--comment-id is required for reply")
            payload = {"body": read_body(args)}
            endpoint = (
                f"repos/{args.repo}/pulls/{args.pr}/comments/{args.comment_id}/replies"
            )
            return run_gh_api(endpoint, payload, args.timeout)

        raise ValueError(f"Unsupported mode: {args.mode}")
    except (TypeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
