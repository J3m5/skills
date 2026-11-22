# Manage GitHub CLI Skills

Use this reference when the task is to work with agent skills through `gh
skill`. The command set is preview; re-check `gh skill --help` after CLI
upgrades or before fragile operations.

## Ownership Boundary

Follow the host's skill-library guidance when evaluating a source, checking
duplicate names, and selecting an installation destination.

Use this reference when the selected method is explicitly `gh skill`, or when
the task is to inspect, update, or troubleshoot an existing `gh skill`
installation. Do not run both installation mechanisms for the same skill.

## Output Contract

- the scope, agent host, and directory used
- the selected source repository or local directory
- the skill names, versions, pins, and paths affected
- whether the action was read-only or changed the local skill installation

## Primary Workflow

1. Use `gh skill list` for inventory and current state.
2. Use `gh skill install OWNER/REPO` without a skill name or `--all` to
   discover available skills non-interactively before selecting one.
3. Use explicit `--agent` and `--scope`, or use `--dir` as a direct placement
   override when the destination matters.
4. Install or update only when requested. Publishing is a separate external action.

## Daily Commands

Inventory installed skills:

```bash
gh skill list --json skillName,sourceURL,scope,version,pinned,path
gh skill list --agent codex --scope user --json skillName,sourceURL,scope,version,pinned,path
gh skill list --dir .agents/skills --json skillName,sourceURL,scope,version,pinned,path
```

Discover skills available in a repository without installing:

```bash
gh skill install OWNER/REPO
gh skill install OWNER/REPO | rg REVIEW_OR_DOMAIN_TERM
```

Install one skill:

```bash
gh skill install OWNER/REPO SKILL --agent codex --scope user
gh skill install OWNER/REPO SKILL --agent universal --scope user
gh skill install OWNER/REPO SKILL --dir ~/.agents/skills
```

Install all discovered skills from a repository:

```bash
gh skill install OWNER/REPO --all --agent codex --scope user
```

Install from a local directory:

```bash
gh skill install ./my-skills-repo SKILL --from-local --agent codex --scope user
```

Update installed skills:

```bash
gh skill update SKILL
gh skill update --all
```

## Guardrails

- Treat install, update, publish, and force overwrite as local writes.
- Treat `gh skill install OWNER/REPO` without a skill name or `--all` as
  read-only discovery in non-interactive contexts; adding a skill name, `--all`,
  or `--force` changes local installation state.
- In `gh` 2.96.0 and newer, `--agent universal --scope user` installs to
  `~/.agents/skills`.
- Treat `--dir` as overriding `--agent` and `--scope`; in `gh` 2.96.0 and
  newer it also skips the target-agent prompt.
- Do not use `--force`, `--all`, or `--scope user` unless the user asked for
  that breadth or the repo workflow requires it.
- Prefer an exact skill path for large repositories to avoid full discovery.
- Use `--pin` when reproducibility matters.
