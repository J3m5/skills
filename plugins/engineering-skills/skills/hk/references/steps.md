# Steps, selection and scheduling

## Commands and tools

Use `hk builtins` and the matching definition under `_source/pkl/builtins/` to
choose a builtin. Builtins configure commands, not installations. Keep linters
with their existing mise or language package manager, including local Node bins.
Amend a builtin to retain properties you are not changing:

```pkl
["prettier"] = (Builtins.prettier) {
  glob = List("**/*.js", "**/*.ts")
  exclude = List("**/generated/**")
}
```

For a scoped commit convention, `check_conventional_commit` accepts
`allowed_scopes` from 2.12. Apply it only to an agreed list of scopes.
[Conventional commit scopes](https://github.com/jdx/hk/releases/tag/v2.12.0)

Custom check commands should report without writes; fix applies corrections.
Use strings for shell operations. Use structured Command.argv when argument
boundaries matter; standalone `"{{files}}"` expands to one argument per path.
Shell metacharacters in argv remain literal. Structured commands cannot combine
with a step's shell or a string prefix; an argv-list prefix such as
`List("mise", "x", "--")` is supported.

Strings are Tera templates; wrap literal `{{...}}` belonging to another tool in
`{% raw %}...{% endraw %}`. Conditions use expressions, not Tera:
`condition = "exec_ok('test -f .lint-enabled')"` tests exit success; exec returns
output and a nonzero exit fails evaluation. Condition evaluates per job,
step_condition once per step. Conditions may execute code. Windows strings
default to cmd.exe; check POSIX-dependent builtin definitions for portability.

## Files, profiles and monorepos

Preview the intended hook with --plan or --why. Globs, exclusions, ignore rules,
required environment, profiles and conditions can skip steps. A step without
patterns can run with no selected files. Unknown --step fails; unknown --skip-step
only warns.

A step requires all positive profiles; List("ci", "slow") needs both. Negative
profiles exclude when enabled. ci does not auto-enable itself; select profiles
through root settings/CLI/Git/environment, not a hook's child env block.

Since 2.7, `profile_condition = "profile('ci') or profile('slow')"` selects
either profile in addition to any existing filters. Run
`hk --profile ci check --plan <file>` on a matching file and confirm the step is included.

For explicit file arguments and
`--files0-from`, 2.8.2+ resolves relative paths from the invoking directory.
On older versions, run from the root with root-relative paths.
[Profiles](https://github.com/jdx/hk/releases/tag/v2.7.0) · [File selection](https://github.com/jdx/hk/releases/tag/v2.8.2)

dir sets command cwd. workspace_indicator partitions files by workspace;
workspace_files is relative to that workspace, files to the rendered command cwd.
Templated dir filters use its literal prefix; scope fully templated directories
with globs/workspace markers. In a subproject, use literal dir: 2.5.0 does not
correctly resolve templated workspace directories there.

Root subprojects loads one level and qualifies names, e.g. frontend:eslint.
Subprojects contribute steps to the same event, not every event. Put hook-wide
fix/stash/stage/report and jobs/profiles/exclude in the root; many corresponding
subproject settings are ignored with warnings. HK_MISE=1 resolves mise env per
step directory; explicit step env wins.

## Reuse successful checks (2.13+)

Use `cache = true` on a deterministic step when rerunning the same check is
costly. By default hk hashes the job's selected files. If the command reads a
wider graph or configuration, `cache_inputs` **replaces** that list. Include
the source globs, configs, lockfiles and tool version pins that affect the
result. External inputs that cannot be represented make reuse unreliable.
Fixes, interactive steps and failed checks always run. For diagnosis compare
with `HK_CACHE=0 hk check …`. [Step result caching](https://github.com/jdx/hk/releases/tag/v2.13.0)

## Coordination and efficient fixers

Read/write locks coordinate selected overlapping files, but do not choose the
last formatter or protect undeclared writes. Use depends for real ordering needs,
exclusive for broader effects, or Group as a scheduling boundary. Group children
can run together; later work waits. Child properties replace group defaults,
including lists; builtins may already define them. Prefer hk-managed stage to
git add inside commands, whose index writes need separate serialization.
allow_failure changes blocking policy; retain it only when that is intended.

For supported tools, check_diff supplies a patch; check_list_files narrows fixing
and staging. check_failed_files focuses detailed checks and requires check plus
a file-reporting command. Partial fixers may need check_after_diff to catch
remaining findings; complete formatters can keep the faster path. Verify formats
before adding optimizations. See upstream for apply_check_diff and diff utilities.

For custom commands worth testing, define step fixtures and run
`hk test --step <name>`; follow the upstream custom-linter example. Tests execute
commands, so temporary fixture paths are not a general sandbox.

- [Configuration](https://github.com/jdx/hk/blob/v2.13.0/docs/configuration.md)
- [Custom steps](https://github.com/jdx/hk/blob/v2.13.0/docs/reference/examples/custom-linters.md)
- [Monorepos](https://github.com/jdx/hk/blob/v2.13.0/docs/reference/examples/monorepo.md)
- [Schema](https://github.com/jdx/hk/blob/v2.13.0/pkl/Config.pkl)
