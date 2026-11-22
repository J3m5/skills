# CI and coding agents

## Tool-provided skills

hk releases may expose `hk-configure` for adding or changing checks and
`hk-debug` for failures, skipped steps and staged-file diagnosis. With a mise
packslip installation, `mise skills ls --json` discovers the skills of the hk
version active in the project and returns their paths. Their presence on disk
does not establish availability in the host's skill catalog; follow its
invocation policy or an explicit request to inspect them.

Read the relevant upstream skill when available. Keep this local skill for
additional configuration, hook-installation, Pkl, CI/MCP and recovery details;
check the installed CLI and pinned schema when versions differ. Do not edit the
publisher's installed files or synchronize skills merely to run a check.
For requested mise discovery or synchronization setup, see
[tool-provided skills](../../mise/references/tool-skills.md).

## Choose execution scope

CI can invoke hk validate and `hk check --check --all` without installing hooks.
Install declared tools and language dependencies. Call `hk` directly if the job's PATH selects it, or run the project's existing check task. Use `mise exec -- hk …` when the job has mise but lacks the configured tool environment.
Keep executable versions and Pkl imports consistent with repository policy.
Inspect custom check effects and report commands; --check cannot prevent writes.

For branch checks use --from-ref <base> --to-ref HEAD with fetched references and
enough history. --pr detects the default branch. These select paths and run on
the current checkout, not historical contents; shared config/dependency changes
may justify a full check.

From 2.13, steps can consume `{{from_ref}}` / `{{to_ref}}` or
`HK_FROM_REF` / `HK_TO_REF`. They hold the supplied refs, which can be empty
outside a range. A downstream comparison must compute the merge base if it
needs the same starting point as hk. [Ref range](https://github.com/jdx/hk/releases/tag/v2.13.0)

For agent edits use explicit files or --unstaged, which excludes staged files.
--files0-from <path> (or - for stdin where allowed) preserves exact filenames.
Preview with --plan --json or --why; these can evaluate Pkl and executable
conditions. Choose fix/staging behavior from the task, then review the diff.

## Declared effects and output

--safe refuses unknown/destructive effects before executing a run. Declare a
supported actual effect with CommandSpec, for example:

```pkl
check = new CommandSpec {
  command = new Command { argv = List("my-linter", "{{files}}") }
  effect = "read"
}
```

Plain strings, Scripts and Commands have unknown effects; builtins commonly
supply declarations. The gate covers fallback/recheck commands and, in tested
2.5.0, hook report. The tag's security page incorrectly says report is unchecked;
its schema, agents guide and runtime agree it is checked. Recheck on other versions.

Effects are assertions, not a sandbox or permission grant. hk does not constrain
filesystem, network or environment, and the gate does not restrict Pkl evaluation.
Do not relabel an unknown/destructive command merely to pass the gate.

--format json reports results; jsonl emits execution events. Parse final status
and failure/cancellation. Since 2.11, many builtins parse their tool's native output automatically.
For a custom step, choose a parser matching its output. Empty diagnostics do
not prove success. Read raw output/parser warnings;
retained output can be capped. --sarif exports supported diagnostics; --junit-xml
exports step results. --no-fail-fast collects failures when that suits the workflow.

## Requested host integration

hk agent instructions/hooks/mcp --target codex emit snippets to stdout. Review
and merge only the requested integration; generators do not install it. Do not
change host config or add stop hooks merely to run project checks. Since 2.6,
the agent stop hook passes when there is no config or check hook. A config
that fails to load still blocks.

hk mcp --root <project> is a STDIO server with startup-fixed roots. start_check
does not pass the effect gate; start_safe_check/start_safe_fix do. Scope defaults
to all; choose changed/unstaged/staged when appropriate. Changed disables stashing;
staged still reads worktree contents; HK_STASH_UNTRACKED=0 can omit untracked files.
Dashboard support depends on the host; structured CLI works without enabling MCP.

- [CI](https://github.com/jdx/hk/blob/v2.13.0/docs/ci.md)
- [Agents](https://github.com/jdx/hk/blob/v2.13.0/docs/agents.md)
- [Security model](https://github.com/jdx/hk/blob/v2.13.0/docs/security.md)
