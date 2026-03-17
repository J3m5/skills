---
name: codex-usage-report
description: Gather a Codex usage-consumption report from the local machine and draft a GitHub issue comment using documented current defaults plus local config checks. Use when the user reports Codex usage limits draining too fast, wants to fill a setup template for openai/codex issues, or needs a reproducible workflow for collecting Codex setup details and comparing them against the currently documented defaults.
---

# Codex Usage Report

## Overview

Collect the local Codex setup first, then compare it against the documented defaults in this skill rather than inferring behavior from a single CLI output.

Prefer verified local facts for machine-state fields and ask the user directly for subjective or behavioral fields.

## Workflow

### 1. Collect local machine facts

Ask the user for the subjective fields first, then run the helper script with those answers:

```bash
python3 ~/.codex/skills/codex-usage-report/scripts/collect_local_setup.py \
  --workspace "$PWD" \
  --format markdown \
  --status-line "[short status line]" \
  --review-often "[yes/no]" \
  --plan-mode-often "[yes/no]" \
  --long-sessions "[yes/no]" \
  --frequent-compactions "[yes/no]" \
  --skills-usage "[short answer]" \
  --affected-models "[short answer]" \
  --new-vs-baseline "[yes/no]" \
  --additional-context "[short paragraph]"
```

This gathers:

- Operating system and kernel
- Installed Codex CLI version
- Local `~/.codex/config.toml` model and reasoning defaults
- Whether `service_tier`, `model_context_window`, or explicit `features.*` overrides are present
- Matching project entry from the main config file for the current workspace
- Auth mode and plan type from `~/.codex/auth.json`
- Available skill count from local skill directories
- `AGENTS.md` size for the provided workspace
- Recent session context-window and compaction signals from `~/.codex/sessions`
- A ready-to-paste Markdown report when the user answers are provided as script arguments

If the helper output is not enough, inspect these files directly:

- `~/.codex/config.toml`
- `~/.codex/version.json`
- `~/.codex/auth.json`
- `~/.codex/sessions/.../rollout-*.jsonl`

### 2. Use the documented defaults

As of **2026-03-17**, use these defaults unless the user explicitly asks you to refresh them:

- Fast mode: **Disabled**
- 1M context window: **Disabled**
- Sub-agents: **Enabled**
- Other experimental features: **No**

These defaults are for report drafting. They should be compared against local config and explicit user behavior.

### 3. Apply the default-value rules

Use these rules when filling the report:

- `fast mode`
  Check local config for `service_tier`.
  If `service_tier` is unset and the user did not explicitly enable fast mode, report `Disabled (default)`.
  If `service_tier` is set to a fast tier or the user explicitly enabled fast mode, do not mark it as default.

- `1M context window`
  Check local config for `model_context_window`.
  If `model_context_window` is unset locally, report `Disabled (default)`.
  If it is explicitly set, report it as enabled or custom rather than default.

- `sub-agents`
  Check local config for explicit `features.multi_agent` overrides when present.
  If there is no explicit override, report `Enabled (default)`.
  If the issue comment is really asking about habitual usage rather than availability, ask the user directly before over-claiming.

- `other experimental features`
  Confirm from local config whether under-development or experimental flags are explicitly set.
  If none are explicitly enabled, report `No (default)`.

### 4. Ask for user-reported behavior before generating the report

Ask the user directly for fields that are not reliably derivable or that are expensive to infer. Do this before generating the final Markdown so you can pass the answers as script parameters:

- Do you use `/review` often?
- Do you use plan mode often?
- Are your sessions long?
- Do repeated compactions happen often?
- Does this affect one model or multiple models?
- Is this new relative to the normal baseline?
- Do you use many skills or MCPs in practice?
- Optional short status line for the top of the comment
- Optional additional context paragraph

If local logs suggest an answer but do not prove it, present the signal and ask the user to confirm.

### 5. Generate the comment

Prefer the helper script for the final Markdown when the user answers are available. Use hand-written drafting only if the user wants custom wording that the script cannot express.

The generated comment should contain:

- A one-sentence status line at the top if the issue now appears resolved or changed
- `###` section headers for readability
- Questions as bullets
- Answers in bold for visual separation
- `(default)` appended only when you verified that the current local value matches the documented defaults in this skill

Do not leave lines like `If yes, which ones?` when the answer is no.

## Guardrails

- Never say `fast mode` is enabled just because `codex features list` shows `fast_mode true`.
- Never say `1M context window` is enabled just because the model has a large normal context window.
- Treat documented defaults in this skill as dated snapshots. Refresh them only when the user explicitly asks or when you have reason to think they changed.
- Base the report on local config checks plus user confirmation for behavioral questions.

## Output Shape

Use this structure unless the user asks for something else:

```markdown
[short status line about whether the issue is still present, improved, or resolved]

### Setup

- Operating system: **[value]**
- Codex version: **[value]**
- ...

### Usage Pattern

- Do you use /review often? **[value]**
- ...

### Additional Context

[short paragraph describing any workaround, reset, or observation]
```
