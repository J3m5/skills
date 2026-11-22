# Vitest Reference

Use this with the generic test-design guidance, without assuming React, Angular,
Vue, or another application framework. This is a decision guide, not a copy of
the Vitest manual or a dependency pin.

## Effective version and execution

Inspect the lockfile and installed package as well as the manifest's version
range. Read the existing Vitest/Vite configuration, test projects, setup files,
plugins, and scripts. Select the matching major from the
[local official documentation index](../assets/vitest/index.md): v5.0.3 or
v4.1.11. Shared pages have been compared across both versions. Read only the
relevant page or section, using local search for API details.

For other patch/minor versions, check introduction markers and installed
types/source before relying on a version-sensitive API. The snapshot is not
exact-version proof for those versions. Use web research only when a material
question remains unresolved locally; do not check for newer releases routinely
or upgrade Vitest merely to use an example from this reference.

Use the project's runner and documented scripts, keeping required environment
and setup intact. A direct invocation means the already installed local binary,
not an unpinned package download. For agent execution, use one-shot mode
(`vitest run` or the project's equivalent), rather than an indefinite watch.
Filter by the relevant file and, when useful, test name (`-t`). Preserve required
test-project selection. Check that tests were actually collected; zero tests is
not success. Follow with the required suite and checks.

## Assertions and asynchronous tests

When several cases exercise the same behavior with different inputs or expected
results, prefer the installed runner’s parameterized-test API to a custom loop
that registers tests. Keep each case’s name and expected outcome explicit.
Retain separate tests when their setup or behavior materially differs.

Follow existing explicit imports or configured globals. Use Vitest's `vi` APIs,
not Jest APIs inferred from similar syntax. Select assertions for the actual
contract: equality for values, structural equality for objects, error assertions
for failure semantics, and interaction assertions for contractual effects.

Await the action and promise assertions, including `resolves` and `rejects`.
Return or await work started by a test so failures cannot escape its lifetime.
Use the project's existing async utilities. When available in the installed
version, `vi.waitFor` or `expect.poll` can observe eventual conditions; keep their
callbacks free of repeated business actions and use bounded waits. A helper that
flushes promises does not by itself prove lifecycle behavior.

## Mocks, module boundaries, and cleanup

Use `vi.fn` for a controlled collaborator or `vi.spyOn` for an observable effect.
Derive mock signatures from real functions with `vi.fn<typeof actualFunction>()`;
check native partial-mock semantics in the installed version before adding
custom type wrappers.

Avoid replacing the module whose behavior is being tested. Module mocking has
hoisting and caching semantics: `vi.mock` factories cannot freely capture later
top-level values. Prefer the project's established pattern and consult the
locally exported [module mocking guide](../assets/vitest/shared/guide/mocking/modules.md)
before using `vi.hoisted`, dynamic imports, or cache resets. Mocking an export
does not replace a direct call to it from inside the same module.

Choose cleanup for the state changed, accounting for setup/configured hooks:

| Operation                                      | Intended use                                                                                                        |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| `vi.clearAllMocks()`                           | Clear call history while keeping implementations                                                                    |
| `vi.resetAllMocks()`                           | Clear history and reset mock implementations; consult the installed version's reset semantics                       |
| `vi.restoreAllMocks()`                         | Restore original object properties replaced by `vi.spyOn`; do not assume it clears standalone mocks or module mocks |
| `vi.unstubAllGlobals()` / `vi.unstubAllEnvs()` | Restore values changed through Vitest's corresponding stub APIs                                                     |

Recreate restored spies where needed. Restore direct mutations separately;
Vitest's unstub APIs do not track arbitrary assignments. Avoid a blanket
combination of reset, restore, and module-cache clearing in every test.

## Timers and lifecycle

Use `vi.useFakeTimers()` when timer policy is the behavior under test. Advance
the required interval deliberately; use supported async timer advancement when
callbacks schedule promise work. Avoid draining every timer in an unbounded
polling loop. `vi.setSystemTime()` changes clock readings; it does not itself
execute due timers.

Dispose components and subscriptions before clearing or switching the clock that
owns their timers, accounting for local and global hook order. If fake timers
were installed, complete pending callbacks required by the library's cleanup
protocol, then discard residual timers and restore real time, including after
failed assertions.
Enabling fake timers during teardown does not capture timers already scheduled
on the real clock. Do not combine fake time and a waiting helper without checking
their interaction in the installed version.

## Environment and coverage limits

Keep the configured environment unless the scenario needs another boundary.
Node tests cannot establish DOM behavior; DOM emulators do not establish layout,
browser API fidelity, or a real user flow. Use an existing Browser Mode or E2E
setup when those contracts require a browser. Browser Mode's module spying and
mocking rules differ from Node mode; consult its guide before copying a pattern.
Do not install a browser provider as a routine consequence of using this skill.

Use the configured coverage provider and compatible package versions. Inspect
relevant uncovered branches and exclusions without treating a percentage as an
acceptance verdict. Review snapshot changes against requirements before updating
them; bulk updates must not silently bless a regression.

## Optional assertion and mutation tooling

For oracle analysis and interpretation of mutation results, use
[test-oracles.md](test-oracles.md). Reuse installed tooling and check its effective
version before changing configuration; these tools are not prerequisites.

### Static checks with ESLint or Oxlint

Use the project's existing linter. The [Vitest ESLint plugin](https://github.com/vitest-dev/eslint-plugin-vitest)
and Oxlint provide these checks; respect configured ESLint plugin aliases.

| Rule (Oxlint documentation)                                                                                 | Purpose                                    | Oxlint category |
| ----------------------------------------------------------------------------------------------------------- | ------------------------------------------ | --------------- |
| [vitest/expect-expect](https://oxc.rs/docs/guide/usage/linter/rules/vitest/expect-expect)                   | Recognized assertion present               | `correctness`   |
| [vitest/no-conditional-expect](https://oxc.rs/docs/guide/usage/linter/rules/vitest/no-conditional-expect)   | Flag conditional assertions                | `correctness`   |
| [vitest/valid-expect](https://oxc.rs/docs/guide/usage/linter/rules/vitest/valid-expect)                     | Valid syntax and async usage               | `correctness`   |
| [vitest/no-standalone-expect](https://oxc.rs/docs/guide/usage/linter/rules/vitest/no-standalone-expect)     | Assertions inside tests or allowed helpers | `correctness`   |
| [vitest/no-restricted-matchers](https://oxc.rs/docs/guide/usage/linter/rules/vitest/no-restricted-matchers) | Explicit matcher/modifier restrictions     | `style`         |
| [no-self-compare](https://oxc.rs/docs/guide/usage/linter/rules/eslint/no-self-compare) (ESLint core)        | Self-comparisons such as `x === x`         | `pedantic`      |

Oxlint enables `correctness` by default, but its [built-in `vitest` plugin](https://oxc.rs/docs/guide/usage/linter/plugins)
is opt-in. Enabling it activates the four correctness rules unless configuration
overrides them; no ESLint plugin installation is needed. Preserve existing
plugins when editing `plugins`, which replaces the default set. Enable the other
two rules individually when useful; enabling their whole categories is optional.
`no-restricted-matchers` has no effect without configured restrictions.

Check effective versions, test-file scope, options, and assertion helpers;
matching names do not guarantee identical defaults. Oxlint's Vitest
`expect-expect` recognizes `expect`, `expectTypeOf`, `assert`, and `assertType`;
the ESLint plugin documents a `typecheck` setting for type tests.

These rules do not establish oracle independence: `no-self-compare` checks
operators, not `expect(result).toEqual(result)`. Restrict matchers only for
justified project policy, not a blanket ban on presence or partial assertions.

### Targeted mutation checks

For an existing [StrykerJS Vitest runner](https://stryker-mutator.io/docs/stryker-js/vitest-runner/),
check compatibility with the installed Vitest and Stryker packages and limit
mutation scope to the question. Its related-test selection can miss integration
tests that reach code without importing it; verify selection before interpreting
survival. Per-test mutation coverage is not proof of meaningful assertions.

[Incremental mode](https://stryker-mutator.io/docs/stryker-js/incremental/)
reuses previous outcomes, but changes to dependencies, configuration, external
snapshots, or other untracked inputs can invalidate them. Force fresh results for
the affected scope when necessary, using the installed version's options and
the project's command. Distinguish reused results from newly executed probes.

## Local official documentation

Use the [versioned index](../assets/vitest/index.md#local-documentation) to choose
the appropriate page. The exports include Testing in Practice, Writing Tests
with AI, CLI and generated options, configuration overview, mocking, module
mocking, Vi API, timers, Browser Mode, and coverage.

Release identities, source and export hashes, transformations, and deduplication
decisions are in [manifest.json](../assets/vitest/manifest.json). Read its
provenance when needed; it is not required context for every test task.
