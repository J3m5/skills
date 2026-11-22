# Tool-provided agent skills

## Discover the active version's resources

Use `mise skills ls --json` in the relevant project to get each skill's name,
tool, version and directory. Only installed, active tools with declared skills
participate; a global tool selection may differ from the project's. The
`packslip:` backend retrieves these resources from the publisher's manifest.
Check the effective backend before proposing a migration or reinstallation.

Read the returned `SKILL.md` and relevant supporting files when the task and
host's skill-discovery policy permit it. Listing a skill through mise does not
by itself enable it in the agent's session. Follow the host's available-skill
catalog and invocation policy; an explicit request to inspect a tool's skill
can be handled without installing or activating it.

Keep local operational guidance separate from publisher-owned files in mise's
install directory. When both cover the task, compare their scope and version;
use the upstream workflow where it fits and retain useful local complements.
Do not replace an existing local skill solely because a tool now publishes one.

## Link skills for the requested scope

`mise skills sync --dir .agents/skills` creates links to active installations.
Without `--dir`, mise uses `skills.dir` under the nearest project root. If unset,
an existing `.agents/skills` wins, then an existing `.claude/skills`. If neither
exists, mise creates `.agents/skills` and a `.claude/skills` symlink to it.
An explicit setting pins the directory.

`--global` targets the home directory instead of the project root; absolute
paths are used as supplied. Choose the intended scope before syncing. These
links depend on each machine's install paths and should not be committed.
Automatic sync and manual sync without `--dir`/`--global`
select project-owned tools (and environment-selected tools) for project links;
tools declared only globally belong under the home directory. `--global`
selects global/system tools. An explicit `--dir` is a deliberate destination
choice and can include the active tool set; inspect that selection first.
Existing project links to global tools can remain until `--prune` removes them.

mise records owned links in `.mise-skills.json` and maintains a
block in `.git/info/exclude` for those links and the state file in ordinary Git
checkouts. It skips that exclusion update outside Git and in linked worktrees.
Inspect local exclusions when needed; do not add workspace-only entries to a
shared `.gitignore`.

Sync preserves user-created directories and unrelated symlinks, reporting name
collisions as skipped. Inspect a conflict rather than deleting the local skill.
Repeat sync after changing tool versions. `--prune` removes stale mise-owned
links; it does not request removal of handwritten skills.

## Fetching and automatic synchronization

`skills.fetch` defaults to true. A skill can come from the release artifact, a
signed separate asset, or the release's source commit. An exec-only source
requires `packslip.exec = true` at installation: this runs the installed tool,
so enabling it is a separate execution choice, not a prerequisite for static
skills. Missing resources are reported by ls/sync; inspect that reason before
reinstalling an otherwise working tool.

`skills.auto_sync` and `skills.prune` default to false. For requested automation,
configure them in the intended project or global scope. Auto-sync
runs after install, use and upgrade when a project root exists.
`mise use --global` instead syncs under the home directory. Changing working
directories does not trigger it. Disabling fetch does not delete already
fetched skills or existing links. Reload the host's skills if it does
not notice updated links.

After a requested change, inspect the linked targets and active versions, the
preserved local skills, and the repository status. Do not enable auto-sync or
change global discovery merely to read a skill.

- [Resources and skills](https://github.com/jdx/mise/blob/v2026.11.9/docs/dev-tools/packslip-resources.md#skills)
- [List](https://github.com/jdx/mise/blob/v2026.11.9/docs/cli/skills/ls.md)
- [Sync](https://github.com/jdx/mise/blob/v2026.11.9/docs/cli/skills/sync.md)
- [Settings](https://github.com/jdx/mise/blob/v2026.11.9/settings.toml)
- [Project/global sync scope](https://github.com/jdx/mise/blob/v2026.11.4/docs/dev-tools/packslip-resources.md)
