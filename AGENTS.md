# Repository Guidelines

## Project Structure & Module Organization

This repository packages Codex skills for reuse. Published skills live under `skills/<skill-name>/`. Each skill should be self-contained and centered on a `SKILL.md`, with supporting material in `agents/`, `assets/`, and `references/` as needed.

Repository tree:

```text
.
├── AGENTS.md
├── README.md
├── mise.toml
├── .oxfmtrc.json
├── .gitignore
├── skills/
│   ├── .system/
│   │   ├── skill-creator/
│   │   └── skill-installer/
│   └── report-generator/
├── docs/
│   └── agentsskills/   # local upstream reference clone, ignored by Git
└── backup/
```

`backup/` is intentionally local-only and ignored by Git. Do not place publishable skill content there.
Use `skills/.system/` for repository-managed system skills and `skills/<skill-name>/` for general published skills.

## Build, Test, and Development Commands

Install the documented CLI tools with:

```bash
mise install
```

Run the main repo checks with:

```bash
mise run --raw check
```

Apply repo formatting and auto-fixes with:

```bash
mise run --raw fix
```

Check the working tree before and after changes:

```bash
git status
```

Always run `mise` tasks with `mise run --raw <task>` in this repository. Do not use plain `mise run <task>`, because it can leave lingering background terminals in this environment.

Run skill-specific commands from the relevant skill directory when examples in `SKILL.md` use relative paths.

## Coding Style & Naming Conventions

Use Markdown for documentation and keep instructions concise, imperative, and task-focused. Prefer ASCII unless the file already uses another language or character set. Name skills with kebab-case directories such as `report-generator`. Keep supporting paths predictable: `agents/openai.yaml`, `assets/templates/`, `references/`.

Repository formatting is managed by `oxfmt` and Python formatting by `ruff format`. When adding tooling, declare it in `mise.toml`; use `node = "lts"` and `pnpm = "latest"` for npm-backed `mise` tools, and prefer `latest` unless the repository intentionally pins otherwise.
Keep this `AGENTS.md` in sync with the actual repository state and with durable user preferences, recommendations, and workflow instructions that should continue to guide future work in this repo.

## Testing Guidelines

This repository does not currently have a conventional automated test suite. Validate changes by:

- running `mise run --raw check`
- checking Markdown for broken relative paths when editing docs or skills
- verifying referenced commands still match the documented toolchain
- running a minimal skill workflow when changing templates or command examples
- running skill validation helpers when available, for example `python3 skills/.system/skill-creator/scripts/quick_validate.py`

## Commit & Pull Request Guidelines

Use the Conventional Commits spec for all new commits, for example `feat: add new skill` or `docs: add repository guidelines`. Keep commits scoped to one logical change when possible.

Pull requests should explain what changed, why it changed, and any manual verification performed. Include rendered output notes or screenshots only when changing templates or visual report assets.
