# Repository Guidelines

## Project Structure & Module Organization

This repository packages Codex skills for reuse. Published skills live under `skills/<skill-name>/`. Each skill should be self-contained and centered on a `SKILL.md`, with supporting material in `agents/`, `assets/`, and `references/` as needed.

Repository tree:

```text
.
├── AGENTS.md
├── README.md
├── mise.toml
├── .gitignore
├── skills/
│   ├── .system/
│   │   ├── skill-creator/
│   │   └── skill-installer/
│   └── report-generator/
└── backup/
```

`backup/` is intentionally local-only and ignored by Git. Do not place publishable skill content there.
Use `skills/.system/` for repository-managed system skills and `skills/<skill-name>/` for general published skills.

## Build, Test, and Development Commands

Install the documented CLI tools with:

```bash
mise install
```

Check the working tree before and after changes:

```bash
git status
```

Run skill-specific commands from the relevant skill directory when examples in `SKILL.md` use relative paths.

## Coding Style & Naming Conventions

Use Markdown for documentation and keep instructions concise, imperative, and task-focused. Prefer ASCII unless the file already uses another language or character set. Name skills with kebab-case directories such as `report-generator`. Keep supporting paths predictable: `agents/openai.yaml`, `assets/templates/`, `references/`.

When adding tooling, update `mise.toml` with `@latest`-style versions unless the repository intentionally pins otherwise.

## Testing Guidelines

This repository does not currently have an automated test suite. Validate changes by:

- checking Markdown for broken relative paths
- verifying referenced commands still match the documented toolchain
- running a minimal skill workflow when changing templates or command examples

## Commit & Pull Request Guidelines

Use the Conventional Commits spec for all new commits, for example `feat: add new skill` or `docs: add repository guidelines`. Keep commits scoped to one logical change when possible.

Pull requests should explain what changed, why it changed, and any manual verification performed. Include rendered output notes or screenshots only when changing templates or visual report assets.
