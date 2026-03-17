#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import glob
import json
import os
import platform
import subprocess
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore


HOME = Path.home()
CODEX_HOME = HOME / ".codex"

DOCUMENTED_DEFAULT_DATE = "2026-03-17"
DOCUMENTED_FEATURE_STAGES = {
    "apply_patch_freeform": "under_development",
    "apps": "experimental",
    "artifact": "under_development",
    "child_agents_md": "under_development",
    "code_mode": "under_development",
    "code_mode_only": "under_development",
    "codex_git_commit": "under_development",
    "codex_hooks": "under_development",
    "default_mode_request_user_input": "under_development",
    "enable_fanout": "under_development",
    "enable_request_compression": "stable",
    "exec_permission_approvals": "under_development",
    "fast_mode": "stable",
    "guardian_approval": "experimental",
    "image_detail_original": "under_development",
    "image_generation": "under_development",
    "js_repl": "experimental",
    "js_repl_tools_only": "under_development",
    "memories": "under_development",
    "multi_agent": "stable",
    "personality": "stable",
    "plugins": "under_development",
    "powershell_utf8": "under_development",
    "prevent_idle_sleep": "experimental",
    "realtime_conversation": "under_development",
    "request_permissions_tool": "under_development",
    "responses_websockets": "under_development",
    "responses_websockets_v2": "under_development",
    "runtime_metrics": "under_development",
    "shell_snapshot": "stable",
    "shell_tool": "stable",
    "shell_zsh_fork": "under_development",
    "skill_env_var_dependency_prompt": "under_development",
    "skill_mcp_dependency_install": "stable",
    "tool_call_mcp_elicitation": "under_development",
    "tool_suggest": "under_development",
    "undo": "stable",
    "unified_exec": "stable",
    "use_legacy_landlock": "stable",
    "voice_transcription": "under_development",
}


def read_toml(path: Path) -> dict:
    if not path.exists():
        return {}
    return tomllib.loads(path.read_text())


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def run(cmd: list[str]) -> str:
    try:
        return subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT).strip()
    except Exception as exc:
        return f"<error: {exc}>"


def detect_os_info() -> dict:
    system = platform.system()
    release = platform.release()
    machine = platform.machine()
    platform_str = platform.platform()

    pretty_name = system
    if system == "Linux":
        os_release = Path("/etc/os-release")
        if os_release.exists():
            data: dict[str, str] = {}
            for line in os_release.read_text(errors="ignore").splitlines():
                if "=" not in line:
                    continue
                key, value = line.split("=", 1)
                data[key] = value.strip().strip('"')
            pretty_name = data.get("PRETTY_NAME") or data.get("NAME") or "Linux"
    elif system == "Darwin":
        product = run(["sw_vers", "-productName"])
        version = run(["sw_vers", "-productVersion"])
        build = run(["sw_vers", "-buildVersion"])
        pretty_name = " ".join(
            part
            for part in [product, version]
            if part and not part.startswith("<error:")
        )
        return {
            "platform": platform_str,
            "system": "Darwin",
            "release": release,
            "machine": machine,
            "pretty_name": pretty_name or "macOS",
            "build": None if build.startswith("<error:") else build,
        }
    elif system == "Windows":
        version = platform.version()
        pretty_name = f"Windows {release}".strip()
        return {
            "platform": platform_str,
            "system": "Windows",
            "release": release,
            "machine": machine,
            "pretty_name": pretty_name,
            "build": version,
        }

    return {
        "platform": platform_str,
        "system": system,
        "release": release,
        "machine": machine,
        "pretty_name": pretty_name,
        "build": None,
    }


def parse_auth_plan(auth: dict) -> tuple[str | None, str | None]:
    token = ((auth.get("tokens") or {}).get("id_token")) or ""
    if not token or "." not in token:
        return auth.get("auth_mode"), None
    try:
        payload = token.split(".")[1]
        payload += "=" * (-len(payload) % 4)
        claims = json.loads(base64.urlsafe_b64decode(payload))
        auth_claims = claims.get("https://api.openai.com/auth", {})
        return auth.get("auth_mode"), auth_claims.get("chatgpt_plan_type")
    except Exception:
        return auth.get("auth_mode"), None


def find_project_entry(config: dict, workspace: Path) -> tuple[str | None, dict | None]:
    projects = config.get("projects") or {}
    if not isinstance(projects, dict):
        return None, None
    workspace_str = str(workspace)
    matches: list[tuple[str, dict]] = []
    for key, value in projects.items():
        if not isinstance(key, str) or not isinstance(value, dict):
            continue
        if workspace_str == key or workspace_str.startswith(key.rstrip("/") + "/"):
            matches.append((key, value))
    if not matches:
        return None, None
    matches.sort(key=lambda item: len(item[0]), reverse=True)
    return matches[0]


def count_available_skills() -> int:
    roots = [HOME / ".codex" / "skills", HOME / ".agents" / "skills"]
    count = 0
    seen: set[Path] = set()
    for root in roots:
        if not root.exists():
            continue
        for skill_md in root.glob("**/SKILL.md"):
            if skill_md.parent not in seen:
                seen.add(skill_md.parent)
                count += 1
    return count


def count_enabled_mcps(config: dict) -> int:
    servers = config.get("mcp_servers") or {}
    if not isinstance(servers, dict):
        return 0
    count = 0
    for value in servers.values():
        if not isinstance(value, dict):
            continue
        if bool(value.get("enabled", True)):
            count += 1
    return count


def find_agents_size(workspace: Path) -> tuple[Path | None, int | None]:
    candidates = sorted(
        list(workspace.rglob("AGENTS.md")) + list(workspace.rglob("agents.md")),
        key=lambda p: (len(p.parts), str(p)),
    )
    if not candidates:
        return None, None
    target = candidates[0]
    return target, target.stat().st_size


def summarize_recent_sessions() -> dict:
    result = {
        "recent_context_windows": [],
        "recent_compaction_mentions": 0,
    }
    paths = sorted(
        glob.glob(str(CODEX_HOME / "sessions" / "*" / "*" / "*" / "rollout-*.jsonl"))
    )[-8:]
    context_windows: list[int] = []
    compactions = 0
    for path in paths:
        try:
            with open(path, encoding="utf-8", errors="ignore") as handle:
                for line in handle:
                    if "compaction" in line.lower() or "compacted" in line.lower():
                        compactions += 1
                    try:
                        row = json.loads(line)
                    except Exception:
                        continue
                    if (
                        row.get("type") == "event_msg"
                        and row.get("payload", {}).get("type") == "token_count"
                    ):
                        value = (
                            row.get("payload", {})
                            .get("info", {})
                            .get("model_context_window")
                        )
                        if isinstance(value, int):
                            context_windows.append(value)
        except OSError:
            continue
    result["recent_context_windows"] = sorted(set(context_windows))
    result["recent_compaction_mentions"] = compactions
    return result


def kb_string(num_bytes: int | None) -> str | None:
    if num_bytes is None:
        return None
    return f"{num_bytes / 1000:.1f} KB"


def default_fast_mode(service_tier: str | None) -> tuple[str, bool]:
    if service_tier:
        return "Enabled", False
    return "Disabled", True


def default_context_window(
    model_context_window_override: int | None,
) -> tuple[str, bool]:
    if model_context_window_override is None:
        return "Disabled", True
    return "Enabled", False


def default_subagents(explicit_features: dict) -> tuple[str, bool]:
    value = explicit_features.get("multi_agent")
    if value is None:
        return "Enabled", True
    return ("Enabled" if bool(value) else "Disabled"), False


def default_other_experimental(explicit_features: dict) -> tuple[str, bool]:
    experimental_enabled = []
    for key, value in explicit_features.items():
        stage = DOCUMENTED_FEATURE_STAGES.get(key)
        if stage in {"experimental", "under_development"} and bool(value):
            experimental_enabled.append(key)
    if experimental_enabled:
        return "Yes", False
    return "No", True


def fmt_default(value: str, is_default: bool) -> str:
    return f"**{value}**" + (" (default)" if is_default else "")


def render_markdown(data: dict, args: argparse.Namespace) -> str:
    explicit_features = data["explicit_feature_overrides"]
    fast_mode, fast_default = default_fast_mode(data["service_tier"])
    context_window, context_default = default_context_window(
        data["model_context_window_override"]
    )
    subagents, subagents_default = default_subagents(explicit_features)
    other_experimental, experimental_default = default_other_experimental(
        explicit_features
    )

    lines: list[str] = []
    if args.status_line:
        lines.append(args.status_line.strip())
        lines.append("")

    os_line = data["os"]["pretty_name"]
    extra_os_parts = []
    if data["os"].get("release"):
        extra_os_parts.append(f"kernel/release {data['os']['release']}")
    if data["os"].get("build"):
        extra_os_parts.append(f"build {data['os']['build']}")
    if data["os"].get("machine"):
        extra_os_parts.append(data["os"]["machine"])

    lines.append("### Setup")
    lines.append("")
    lines.append(
        f"- Operating system: **{os_line}**"
        + (f" ({', '.join(extra_os_parts)})" if extra_os_parts else "")
    )
    lines.append(
        f"- Codex version: **{data['codex_version'].replace('codex-cli', 'Codex-CLI')}**"
    )
    lines.append("- Client used: **CLI**")
    if data.get("model"):
        lines.append(f"- Selected model: **{data['model'].upper()}**")
    if data.get("model_reasoning_effort"):
        lines.append(
            f"- Selected reasoning level: **{str(data['model_reasoning_effort']).capitalize()}**"
        )
    if args.plan_mode_often:
        lines.append(
            f"- Do you use plan mode often? **{args.plan_mode_often.strip().capitalize()}**"
        )
    lines.append(f"- Fast mode: {fmt_default(fast_mode, fast_default)}")
    lines.append(f"- 1M context window: {fmt_default(context_window, context_default)}")
    lines.append(f"- Sub-agents: {fmt_default(subagents, subagents_default)}")
    lines.append(
        f"- Other experimental features enabled: {fmt_default(other_experimental, experimental_default)}"
    )
    lines.append("")
    lines.append("### Usage Pattern")
    lines.append("")
    if args.review_often:
        lines.append(
            f"- Do you use /review often? **{args.review_often.strip().capitalize()}**"
        )
    if args.long_sessions:
        lines.append(
            f"- Are your sessions long? **{args.long_sessions.strip().capitalize()}**"
        )
    if args.frequent_compactions:
        lines.append(
            f"- Do repeated compactions happen often? **{args.frequent_compactions.strip().capitalize()}**"
        )
    if data.get("agents_md_bytes") is not None:
        lines.append(
            f"- Do you have a long AGENTS.md? **Yes**, about **{kb_string(data['agents_md_bytes'])}**"
        )
    if args.skills_usage:
        lines.append(
            f"- Do you use many MCPs or skills? **{args.skills_usage.strip()}**"
        )
    lines.append(f"- Number of available skills: **{data['available_skill_count']}**")
    lines.append(f"- Number of enabled MCPs: **{data['enabled_mcp_count']}**")
    if args.affected_models:
        lines.append(
            f"- Does this affect gpt-5.3-codex, gpt-5.4, or both? **{args.affected_models.strip()}**"
        )
    if args.new_vs_baseline:
        lines.append(
            f"- Is this new in the last few days compared with your normal baseline? **{args.new_vs_baseline.strip().capitalize()}**"
        )
    lines.append("")
    lines.append("### Additional Context")
    lines.append("")
    if args.additional_context:
        lines.append(args.additional_context.strip())
    else:
        lines.append("No additional context provided.")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", default=os.getcwd())
    parser.add_argument(
        "--format", choices=["json", "markdown", "both"], default="json"
    )
    parser.add_argument("--status-line")
    parser.add_argument("--review-often")
    parser.add_argument("--plan-mode-often")
    parser.add_argument("--long-sessions")
    parser.add_argument("--frequent-compactions")
    parser.add_argument("--skills-usage")
    parser.add_argument("--affected-models")
    parser.add_argument("--new-vs-baseline")
    parser.add_argument("--additional-context")
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    config = read_toml(CODEX_HOME / "config.toml")
    auth = read_json(CODEX_HOME / "auth.json")

    auth_mode, plan_type = parse_auth_plan(auth)
    agents_path, agents_size = find_agents_size(workspace)
    sessions = summarize_recent_sessions()
    project_key, project_entry = find_project_entry(config, workspace)
    explicit_features = config.get("features") or {}
    if not isinstance(explicit_features, dict):
        explicit_features = {}

    data = {
        "workspace": str(workspace),
        "os": detect_os_info(),
        "codex_version": run(["codex", "--version"]).splitlines()[-1],
        "model": config.get("model"),
        "model_reasoning_effort": config.get("model_reasoning_effort"),
        "service_tier": config.get("service_tier"),
        "model_context_window_override": config.get("model_context_window"),
        "explicit_feature_overrides": {
            k: explicit_features[k] for k in sorted(explicit_features.keys())
        },
        "matching_project_key": project_key,
        "matching_project_entry": project_entry,
        "auth_mode": auth_mode,
        "plan_type": plan_type,
        "available_skill_count": count_available_skills(),
        "enabled_mcp_count": count_enabled_mcps(config),
        "agents_md_path": str(agents_path) if agents_path else None,
        "agents_md_bytes": agents_size,
        "recent_context_windows": sessions["recent_context_windows"],
        "recent_compaction_mentions": sessions["recent_compaction_mentions"],
        "documented_default_date": DOCUMENTED_DEFAULT_DATE,
    }

    if args.format == "json":
        print(json.dumps(data, indent=2))
    elif args.format == "markdown":
        print(render_markdown(data, args))
    else:
        print(json.dumps(data, indent=2))
        print()
        print(render_markdown(data, args))


if __name__ == "__main__":
    main()
