---
name: skill-review-and-auto-refactor
description: Audit and improve an existing Codex or OpenAI skill bundle or SKILL.md for clearer routing, stricter workflow instructions, and safer repeatable execution. Use only for existing skills, not for generic code review or net-new skill creation.
---

# Purpose

Audit an existing skill bundle, identify the weaknesses that most affect invocation and repeatable execution, and return a stronger grounded replacement.

Default stance:

- preserve the original business goal
- rewrite weak sections instead of only commenting on them
- reduce routing ambiguity and execution variance
- keep the revised skill directly reusable
- keep `SKILL.md` lean when detail belongs in verified companion files

# Use this skill when

Use this skill when the user asks to:

- review an existing skill
- refactor or harden a `SKILL.md`
- improve a skill's routing, workflow, or guardrails
- add missing negative cases, stop conditions, or output contracts
- make a skill more reliable for repeated Codex use

Do not use this skill when:

- the task is generic code review with no skill bundle involved
- the user wants a brand-new skill
- the request is to implement a product feature rather than improve the skill that describes it
- the target skill content cannot be inspected locally and no usable excerpt was provided

# Decide the job first

Choose the smallest grounded mode that fits the request:

- `full-refactor`: default when the user asked to improve or rewrite the skill; audit it and produce a replacement `SKILL.md`
- `audit-only`: analyze the skill and recommend concrete changes without rewriting file contents
- `trace-informed`: use only when the user explicitly asks for usage-based improvement and you have grounded local evidence from prior runs, learnings, or artifacts

Choose the output intent before editing:

- `apply-changes`: edit the target skill when the user clearly asked for refactoring or hardening
- `recommendations-only`: stop after recommendations when the request is exploratory or comparative

# Review standard

Judge the skill against these checks:

1. It has one primary job.
2. Its `name`, `description`, and display text route the right tasks to it.
3. Its workflow is ordered, imperative, and repeatable.
4. Its inputs, outputs, ambiguity handling, and stop conditions are explicit.
5. Its negative cases are strong enough to prevent common misuse.
6. It does not claim missing tools, files, scripts, or references.
7. It avoids redundant or low-signal wording.

# Workflow

## Step 1: Inspect the minimum grounded context

Read only what is needed to support the review:

- the target `SKILL.md` or `skill.md`
- `agents/openai.yaml` or nearby metadata when present
- `references/` files only when the skill points to them or they define required procedure
- `scripts/` only when the skill relies on them
- adjacent local docs only when they define the workflow the skill is supposed to encode

If the user supplied only an excerpt, combine that excerpt with any local files you can verify. Do not invent missing assets.

If the request is usage-based, inspect the smallest evidence set that can support grounded conclusions and note coverage gaps before making claims.

## Step 2: Audit the current skill

Classify issues in these buckets:

- `invocation`: weak metadata, poor routing, unclear trigger conditions
- `workflow`: vague steps, missing decisions, weak stop conditions, unclear output contract
- `content`: redundancy, contradictions, missing examples, missing negative cases
- `structure`: misleading bundle layout, unnecessary assets, missing supporting files that the workflow actually depends on

Rank issues by impact on correct invocation and repeatable execution.

## Step 3: Decide whether to rewrite or stop

Rewrite by default unless one of these cases applies:

- `audit-only` mode was requested
- `recommendations-only` output intent is the better fit
- the source is too incomplete for a safe rewrite

Stop instead of guessing when:

- the target skill cannot be found locally and no usable excerpt was provided
- the request is actually for a new skill, not a refactor
- the rewrite would require inventing missing scripts, references, or tooling behavior

If the source is incomplete but still usable, keep the rewrite narrow, mark assumptions explicitly, and avoid unsupported capabilities.

## Step 4: Rewrite the skill

When rewriting:

- keep one primary responsibility
- preserve the business goal unless the user explicitly asked to change scope
- improve metadata only when it materially improves routing
- use direct step-based instructions
- define concrete outputs
- define ambiguity handling, failure handling, and stop conditions
- add negative cases where they reduce routing risk
- remove generic advisory language
- remove duplicated instructions unless they serve distinct decisions or guardrails
- prefer full-section rewrites over line edits when a section is structurally weak
- move detail out of `SKILL.md` only when a verified companion file makes the skill clearer and cheaper to invoke
- keep the user-facing response concise after edits; summarize the rewrite instead of pasting the whole file unless the user explicitly asks for the full contents

Do not broaden scope, add speculative capabilities, or reference tools or files that are not present.

## Step 5: Verify coverage and validity

Before returning:

- check that the rewritten skill still preserves or intentionally removes each original section, output, and real guardrail
- confirm that one primary job is obvious
- confirm that use and non-use cases are explicit
- confirm that the workflow is ordered and repeatable
- confirm that the output contract is strict
- confirm that no missing assets or tools are claimed

If you edited any skill files, run this validation helper from the repository root:

```bash
python3 skills/.system/skill-creator/scripts/quick_validate.py <skill_directory>
```

If validation fails, fix the skill before returning.

## Step 6: Return the result

Return results in this order:

## 1. Audit summary

Provide 4 to 8 bullets describing the current skill.

## 2. Highest-priority issues

Provide a short ranked list of the problems that matter most.

## 3. Changelog

List the meaningful changes, the rewritten `SKILL.md` sections, the important behavioral changes, and why they improve reliability. Reference the edited file path instead of pasting the full file. Include short excerpts only when they clarify a critical change or answer a direct user request.

## 4. Optional structural recommendations

Include this section only when changes outside `SKILL.md` would materially improve reliability.

# Output style

Use concise technical prose and short bullet lists.
