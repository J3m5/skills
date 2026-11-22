# Vitest Offline Documentation

Official Markdown documentation captured on 2026-10-05 from the latest stable
release in each requested major: **v5.0.3** and **v4.1.11**. These are pinned
snapshots, not a promise of perpetual freshness. Release commits, publication
dates, source paths, and source/export SHA-256 hashes are recorded in
[manifest.json](manifest.json). The upstream [MIT license](LICENSE) is retained.

## Choose the project version

Identify the installed version from local packages and the lockfile. Use the
matching major column below, reading only the relevant page or section. Search
the files locally rather than loading both snapshots or browsing by default.

For a different patch/minor in the same major, this snapshot is supporting
documentation, not exact-version proof. Check introduction markers and the
installed types/source for a version-sensitive API. For an unrepresented major,
a missing page, or an unresolved compatibility question, consult additional
version-matched evidence only as needed. Do not upgrade the project to match a
snapshot or check online for newer releases during ordinary test work.

## Local documentation

| Topic                     | Vitest 5.0.3                                        | Vitest 4.1.11                                       |
| ------------------------- | --------------------------------------------------- | --------------------------------------------------- |
| Testing in Practice       | [Shared](shared/guide/learn/testing-in-practice.md) | [Shared](shared/guide/learn/testing-in-practice.md) |
| Writing Tests with AI     | [v5](v5.0.3/guide/learn/writing-tests-with-ai.md)   | [v4](v4.1.11/guide/learn/writing-tests-with-ai.md)  |
| CLI and generated options | [v5](v5.0.3/guide/cli.md)                           | [v4](v4.1.11/guide/cli.md)                          |
| Configuration overview    | [v5](v5.0.3/config/index.md)                        | [v4](v4.1.11/config/index.md)                       |
| Mocking                   | [v5](v5.0.3/guide/mocking.md)                       | [v4](v4.1.11/guide/mocking.md)                      |
| Module mocking            | [Shared](shared/guide/mocking/modules.md)           | [Shared](shared/guide/mocking/modules.md)           |
| Vi API                    | [v5](v5.0.3/api/vi.md)                              | [v4](v4.1.11/api/vi.md)                             |
| Timers                    | [Shared](shared/guide/mocking/timers.md)            | [Shared](shared/guide/mocking/timers.md)            |
| Browser Mode              | [v5](v5.0.3/guide/browser/index.md)                 | [v4](v4.1.11/guide/browser/index.md)                |
| Coverage                  | [v5](v5.0.3/guide/coverage.md)                      | [v4](v4.1.11/guide/coverage.md)                     |

## Why retain v4 documentation

The comparison was made against tagged source, including CLI option includes.
Separate v4 pages are kept where the content changes beyond whitespace or
emphasis formatting:

- **CLI:** `vitest list` opts into static parsing in v4; it defaults to static
  parsing in v5. The doctor command and generated options also differ.
- **Vi API and mocking:** v5 documents `vi.when` / `vi.isWhenChain`, Temporal
  clock support, and additional fake-timer options.
- **Browser Mode:** API configuration, compatibility requirements, and rendering
  examples differ.
- **Coverage:** custom reporter imports change from `istanbul-lib-report` to
  `@vitest/istanbul-lib-report` in v5.
- **Configuration overview:** the default mode description and configuration
  discovery explanation differ.
- **Writing Tests with AI:** the parameterized-test example uses `test.each` in
  v4 and `test.for` in v5; this documents an example choice, not removal of an API.

The timers page is byte-identical. Module mocking differs only in blank lines;
Testing in Practice differs only in emphasis delimiters. These three pages use
one shared export from v5, verified against v4, with version-sensitive links
routed back to this index.

## Export scope and fidelity

This snapshot covers the ten pages used by the skill, not the entire website.
CLI option includes are expanded so the exported command reference is complete.
VitePress display wrappers are converted to Markdown text, version labels and
explicit anchors are retained, and coverage diagrams are represented as ordered
text. Fenced code examples and substantive prose are preserved.

Screenshots are represented by their alternative text; image binaries are not
bundled. Links between exported pages resolve locally. Links to other upstream
pages remain external and are not evidence of a cached, version-matched page.
Use them only when the local snapshot and installed sources cannot answer a
material question. Treat upstream examples as reference material, not instructions
to install tools or modify the project.
