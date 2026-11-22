#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "beautifulsoup4",
#   "html2text",
#   "lxml",
# ]
# ///
"""Scrape cli.github.com/manual and refresh local markdown docs.

Usage:
  uv run /path/to/github-skill/scripts/update_cli_manual_docs.py
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import tempfile
import time
from collections import deque
from collections.abc import Iterable
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

import html2text
from bs4 import BeautifulSoup

DEFAULT_START_URL = "https://cli.github.com/manual/"
DEFAULT_OUTPUT_ROOT = Path(".agents/docs/global/platform/github")
USER_AGENT = "Mozilla/5.0 (compatible; CodexGhCliDocsUpdater/1.0)"
LATEST_RELEASE_API_URL = "https://api.github.com/repos/cli/cli/releases/latest"
STATE_FILENAME = "state.json"
STATE_VERSION = 2


@dataclass(frozen=True)
class Config:
    start_url: str
    output_root: Path
    max_pages: int | None
    delay_seconds: float
    timeout_seconds: int
    full_refresh: bool
    no_clean: bool


def parse_args() -> Config:
    parser = argparse.ArgumentParser(
        description="Refresh local markdown mirror for cli.github.com/manual pages."
    )
    parser.add_argument("--start-url", default=DEFAULT_START_URL)
    parser.add_argument(
        "--output-root",
        default=str(DEFAULT_OUTPUT_ROOT),
        help="Output directory (default: .agents/docs/global/platform/github)",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=None,
        help="Optional limit for smoke tests.",
    )
    parser.add_argument(
        "--delay-seconds",
        type=float,
        default=0.02,
        help="Delay between requests (default: 0.02).",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=30,
        help="HTTP timeout per request (default: 30).",
    )
    parser.add_argument(
        "--full-refresh",
        action="store_true",
        help="Delete existing docs and state before refresh.",
    )
    parser.add_argument(
        "--no-clean",
        action="store_true",
        help="Deprecated alias; incremental mode is now the default.",
    )
    args = parser.parse_args()
    return Config(
        start_url=args.start_url,
        output_root=Path(args.output_root),
        max_pages=args.max_pages,
        delay_seconds=args.delay_seconds,
        timeout_seconds=args.timeout_seconds,
        full_refresh=args.full_refresh,
        no_clean=args.no_clean,
    )


def normalize_manual_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        return ""
    if parsed.netloc != "cli.github.com":
        return ""
    path = parsed.path or "/"
    if not path.startswith("/manual/"):
        return ""
    if path != "/manual/" and path.endswith("/"):
        path = path[:-1]
    return f"https://cli.github.com{path}"


def output_path_for_url(output_root: Path, url: str) -> Path:
    parsed = urlparse(url)
    rel = parsed.path.lstrip("/")
    if rel in {"manual", ""} or rel.endswith("/"):
        rel = rel.rstrip("/") + "/index"
    return output_root / f"{rel}.md"


def now_utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()  # noqa: UP017 - keep Python 3.10 support


def prepare_markdown_converter() -> html2text.HTML2Text:
    converter = html2text.HTML2Text()
    converter.body_width = 0
    converter.ignore_images = True
    converter.protect_links = True
    return converter


def strip_presentation_markup(soup: BeautifulSoup) -> str:
    main = soup.find("main") or soup.find("article") or soup.body or soup

    for tag in main(["script", "style", "noscript"]):
        tag.decompose()

    # Remove line-number anchors generated for highlighted code blocks.
    for anchor in main.find_all("a"):
        attrs = dict(anchor.attrs)
        if attrs.get("aria-hidden") == "true" and str(attrs.get("href", "")).startswith(
            "#cb"
        ):
            anchor.decompose()

    # Unwrap presentational containers and keep human-visible text.
    for tag in main.find_all(["div", "span", "figure"]):
        tag.unwrap()

    return str(main)


def normalize_markdown(markdown: str) -> str:
    cleaned = markdown.strip()
    cleaned = cleaned.replace("](<", "](").replace(">)", ")")
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned + "\n"


def fetch_page(
    url: str,
    timeout_seconds: int,
    etag: str | None = None,
    last_modified: str | None = None,
) -> tuple[int, str | None, str | None, str | None]:
    headers = {"User-Agent": USER_AGENT}
    if etag:
        headers["If-None-Match"] = etag
    if last_modified:
        headers["If-Modified-Since"] = last_modified
    request = Request(url, headers=headers)
    try:
        with urlopen(request, timeout=timeout_seconds) as response:
            content_type = response.headers.get("Content-Type", "")
            raw = response.read()
            new_etag = response.headers.get("ETag")
            new_last_modified = response.headers.get("Last-Modified")
    except HTTPError as exc:
        if exc.code == 304:
            return 304, None, etag, last_modified
        raise
    if "text/html" not in content_type:
        raise ValueError(f"Non-HTML response content type: {content_type}")
    return 200, raw.decode("utf-8", errors="replace"), new_etag, new_last_modified


def fetch_latest_release_version(timeout_seconds: int) -> tuple[str | None, str | None]:
    """Return (tag_name, error_message)."""
    request = Request(
        LATEST_RELEASE_API_URL,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/vnd.github+json",
        },
    )
    try:
        with urlopen(request, timeout=timeout_seconds) as response:
            raw = response.read()
        payload = json.loads(raw.decode("utf-8", errors="replace"))
        tag_name = payload.get("tag_name")
        if isinstance(tag_name, str) and tag_name:
            return tag_name, None
        return None, "missing tag_name in latest release payload"
    except Exception as exc:  # noqa: BLE001
        return None, str(exc)


def discover_manual_links(source_url: str, soup: BeautifulSoup) -> Iterable[str]:
    for anchor in soup.find_all("a", href=True):
        href = anchor["href"].strip()
        if not href or href.startswith("#"):
            continue
        absolute = urljoin(source_url, href)
        normalized = normalize_manual_url(absolute)
        if normalized:
            yield normalized


def sanitize_page_entry(url: str, raw_entry: object) -> tuple[dict[str, object], bool]:
    """Return (normalized_entry, links_are_valid)."""
    if not isinstance(raw_entry, dict):
        return {}, False

    entry: dict[str, object] = {}
    etag = raw_entry.get("etag")
    if isinstance(etag, str) and etag:
        entry["etag"] = etag

    last_modified = raw_entry.get("last_modified")
    if isinstance(last_modified, str) and last_modified:
        entry["last_modified"] = last_modified

    output_path = raw_entry.get("output_path")
    if isinstance(output_path, str) and output_path:
        entry["output_path"] = output_path

    links_raw = raw_entry.get("links")
    links_valid = isinstance(links_raw, list)
    links: list[str] = []
    if isinstance(links_raw, list):
        for candidate in links_raw:
            if not isinstance(candidate, str):
                continue
            normalized = normalize_manual_url(urljoin(url, candidate))
            if normalized:
                links.append(normalized)
    entry["links"] = links
    entry["links_valid"] = links_valid
    return entry, links_valid


def load_state(output_root: Path) -> tuple[dict[str, dict[str, object]], list[str]]:
    state_path = output_root / STATE_FILENAME
    if not state_path.exists():
        return {}, []

    warnings: list[str] = []
    try:
        payload = json.loads(state_path.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return {}, ["state file is not valid JSON; ignoring previous state"]

    if not isinstance(payload, dict):
        return {}, ["state file payload is not an object; ignoring previous state"]

    version = payload.get("version", 1)
    if version not in {1, STATE_VERSION}:
        return {}, [f"unsupported state version {version}; ignoring previous state"]

    if version == 1:
        warnings.append("state v1 detected; migrating to v2")

    pages = payload.get("pages")
    if not isinstance(pages, dict):
        return {}, ["state pages section missing/invalid; ignoring previous state"]

    normalized_pages: dict[str, dict[str, object]] = {}
    invalid_entries = 0
    invalid_links = 0
    for url, raw_entry in pages.items():
        if not isinstance(url, str):
            invalid_entries += 1
            continue
        normalized_url = normalize_manual_url(url)
        if not normalized_url:
            invalid_entries += 1
            continue
        entry, links_valid = sanitize_page_entry(normalized_url, raw_entry)
        if not entry:
            invalid_entries += 1
            continue
        if not links_valid:
            invalid_links += 1
        normalized_pages[normalized_url] = entry

    if invalid_entries:
        warnings.append(f"dropped {invalid_entries} invalid state entries")
    if invalid_links:
        warnings.append(
            f"{invalid_links} state entries have invalid links and may be refetched"
        )
    return normalized_pages, warnings


def save_state(output_root: Path, pages: dict[str, dict[str, object]]) -> None:
    state_path = output_root / STATE_FILENAME
    state_pages: dict[str, dict[str, object]] = {}
    for url, entry in pages.items():
        state_pages[url] = {
            "etag": entry.get("etag"),
            "last_modified": entry.get("last_modified"),
            "links": entry.get("links", []),
            "output_path": entry.get("output_path"),
            "last_status": entry.get("last_status"),
            "updated_at_utc": entry.get("updated_at_utc"),
        }
    payload = {
        "version": STATE_VERSION,
        "updated_at_utc": now_utc_iso(),
        "pages": state_pages,
    }
    state_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def refresh_docs(config: Config, reported_output_root: Path | None = None) -> int:
    output_root = config.output_root
    output_root.mkdir(parents=True, exist_ok=True)

    if config.no_clean:
        print(
            "warning: --no-clean is deprecated and has no effect; incremental mode is the default",
            file=sys.stderr,
        )

    page_state, state_warnings = load_state(output_root)

    release_version, release_version_error = fetch_latest_release_version(
        timeout_seconds=config.timeout_seconds
    )

    converter = prepare_markdown_converter()
    visited: set[str] = set()
    queue: deque[str] = deque([normalize_manual_url(config.start_url)])
    written_files: list[str] = []
    not_modified_count = 0
    refetched_missing_output_count = 0
    refetched_invalid_state_count = 0
    pruned_files_count = 0
    pruned_state_entries_count = 0
    errors: list[dict[str, str]] = []

    if not queue[0]:
        raise SystemExit(f"Invalid --start-url for manual scope: {config.start_url}")

    expected_output_paths: set[Path] = set()

    while queue:
        if config.max_pages is not None and len(visited) >= config.max_pages:
            break

        url = queue.popleft()
        if url in visited:
            continue
        visited.add(url)

        state_entry = page_state.get(url, {})
        known_etag = state_entry.get("etag")
        if not isinstance(known_etag, str):
            known_etag = None
        known_last_modified = state_entry.get("last_modified")
        if not isinstance(known_last_modified, str):
            known_last_modified = None

        out_path = output_path_for_url(output_root, url)
        expected_output_paths.add(out_path.resolve())
        links_for_queue: list[str] = []
        html: str | None = None
        final_etag = known_etag
        final_last_modified = known_last_modified

        try:
            status_code, html, final_etag, final_last_modified = fetch_page(
                url,
                timeout_seconds=config.timeout_seconds,
                etag=known_etag,
                last_modified=known_last_modified,
            )
        except Exception as exc:  # noqa: BLE001
            errors.append({"url": url, "error": str(exc)})
            continue

        if status_code == 304 and not out_path.exists():
            # Existing cache says "unchanged" but output file is missing; force refetch.
            refetched_missing_output_count += 1
            try:
                status_code, html, final_etag, final_last_modified = fetch_page(
                    url,
                    timeout_seconds=config.timeout_seconds,
                )
            except Exception as exc:  # noqa: BLE001
                errors.append({"url": url, "error": str(exc)})
                continue

        links_valid_flag = state_entry.get("links_valid")
        links_known_valid = (
            bool(links_valid_flag) if isinstance(links_valid_flag, bool) else False
        )

        if status_code == 304 and not links_known_valid:
            # Cannot trust cached graph; force refetch to discover outbound links.
            refetched_invalid_state_count += 1
            try:
                status_code, html, final_etag, final_last_modified = fetch_page(
                    url,
                    timeout_seconds=config.timeout_seconds,
                )
            except Exception as exc:  # noqa: BLE001
                errors.append({"url": url, "error": str(exc)})
                continue

        if status_code == 304:
            not_modified_count += 1
            prior_links = state_entry.get("links", [])
            if isinstance(prior_links, list):
                links_for_queue = [x for x in prior_links if isinstance(x, str)]
        else:
            soup = BeautifulSoup(html or "", "lxml")
            links_for_queue = list(discover_manual_links(url, soup))
            fragment = strip_presentation_markup(soup)
            markdown = normalize_markdown(converter.handle(fragment))
            out_path.parent.mkdir(parents=True, exist_ok=True)
            header = (
                f"# Source\n\n- URL: {url}\n- Fetched (UTC): {now_utc_iso()}\n\n---\n\n"
            )
            out_path.write_text(header + markdown, encoding="utf-8")
            written_files.append(str(out_path))

        page_state[url] = {
            "etag": final_etag,
            "last_modified": final_last_modified,
            "links": links_for_queue,
            "output_path": str(out_path),
            "last_status": status_code,
            "links_valid": True,
            "updated_at_utc": now_utc_iso(),
        }
        for link in links_for_queue:
            if link not in visited:
                queue.append(link)
        time.sleep(config.delay_seconds)

    # Prune is safe only on a complete crawl of the default manual scope.
    default_scope = normalize_manual_url(config.start_url) == normalize_manual_url(
        DEFAULT_START_URL
    )
    prune_enabled = config.max_pages is None and default_scope and not errors
    if prune_enabled:
        stale_urls = [url for url in list(page_state.keys()) if url not in visited]
        for stale_url in stale_urls:
            del page_state[stale_url]
            pruned_state_entries_count += 1

        manual_dir = output_root / "manual"
        if manual_dir.exists():
            for file_path in manual_dir.rglob("*.md"):
                if file_path.resolve() not in expected_output_paths:
                    file_path.unlink()
                    pruned_files_count += 1

    save_state(output_root, page_state)

    manifest = {
        "start_url": config.start_url,
        "base": "https://cli.github.com",
        "gh_cli_release_version": release_version,
        "gh_cli_release_version_source": LATEST_RELEASE_API_URL,
        "gh_cli_release_version_error": release_version_error,
        "state_warnings": state_warnings,
        "incremental_mode": not config.full_refresh,
        "prune_enabled": prune_enabled,
        "total_visited": len(visited),
        "files_written": len(written_files),
        "not_modified_count": not_modified_count,
        "refetched_missing_output_count": refetched_missing_output_count,
        "refetched_invalid_state_count": refetched_invalid_state_count,
        "pruned_files_count": pruned_files_count,
        "pruned_state_entries_count": pruned_state_entries_count,
        "errors": errors,
        "generated_at_utc": now_utc_iso(),
        "converter": "html2text-with-wrapper-unwrapping",
    }
    (output_root / "manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )

    print(
        f"done visited={len(visited)} written={len(written_files)} "
        f"not_modified={not_modified_count} refetched_missing={refetched_missing_output_count} "
        f"refetched_invalid_state={refetched_invalid_state_count} "
        f"pruned_files={pruned_files_count} pruned_state={pruned_state_entries_count} "
        f"errors={len(errors)} "
        f"output={reported_output_root or output_root}"
    )
    for error in errors:
        print(f"error: {error['url']}: {error['error']}", file=sys.stderr)
    return 1 if errors else 0


def install_staged_output(staged_root: Path, output_root: Path) -> None:
    backup_root: Path | None = None
    if output_root.exists():
        backup_root = Path(
            tempfile.mkdtemp(
                prefix=f".{output_root.name}.backup-",
                dir=output_root.parent,
            )
        )
        backup_root.rmdir()
        output_root.rename(backup_root)

    try:
        staged_root.rename(output_root)
    except Exception:
        if backup_root is not None and backup_root.exists():
            backup_root.rename(output_root)
        raise

    if backup_root is not None:
        shutil.rmtree(backup_root)


def main() -> int:
    config = parse_args()
    if not config.full_refresh:
        return refresh_docs(config)

    output_root = config.output_root
    output_root.parent.mkdir(parents=True, exist_ok=True)
    staged_root = Path(
        tempfile.mkdtemp(
            prefix=f".{output_root.name}.staging-",
            dir=output_root.parent,
        )
    )
    try:
        gitkeep = output_root / ".gitkeep"
        if gitkeep.exists():
            shutil.copy2(gitkeep, staged_root / ".gitkeep")

        staged_config = replace(config, output_root=staged_root)
        status = refresh_docs(staged_config, reported_output_root=output_root)
        if status != 0:
            return status

        install_staged_output(staged_root, output_root)
        return 0
    finally:
        if staged_root.exists():
            shutil.rmtree(staged_root)


if __name__ == "__main__":
    raise SystemExit(main())
