---
name: test-engineering
description: Design, implement, and audit automated tests for observable behavior, including representative bug regressions, tautological or weak assertions, faithful test doubles, and deterministic asynchronous scenarios. Use when test design or quality is part of the task; adapt to the project's existing runner, with a Vitest reference available.
---

# Test Engineering

Produce tests that detect meaningful behavioral failures, remain useful through
refactoring, and provide fast feedback. Apply to libraries, services, APIs, and
applications without assuming a language or UI framework.

## Ground the task

Read repository instructions, the relevant behavior and its consumers, existing
tests, and test configuration. Identify the installed runner and effective version,
environment, fixtures, setup and teardown, and documented commands. Preserve
existing conventions unless they prevent a representative test.

Derive expected outcomes from requirements and contracts, not from the current
implementation alone. Surface an ambiguity that changes the expected result.
Do not introduce a runner, dependency, environment, or production abstraction
solely to follow this skill; justify changes when the requested tests need them.

## Select the relevant guidance

- For scenario selection, regression design, test doubles, asynchronous behavior,
  or a test-quality audit, read [test-design.md](references/test-design.md).
- For suspected tautologies, oracle quality, or mutation evidence, also read
  [test-oracles.md](references/test-oracles.md).
- When the project uses Vitest, also read [vitest.md](references/vitest.md).
  Select version-matched pages from the [local documentation](assets/vitest/index.md)
  for API details; prefer these snapshots and installed sources to web research.
- For another runner, retain the generic guidance and consult that runner's
  official documentation as needed. Do not translate Vitest APIs mechanically.

Framework references describe mechanics; the generic contract describes what
must be demonstrated. Load only the relevant references.

## Work efficiently

Select the smallest test boundary that exposes the risk; add integration or
end-to-end evidence where a narrower test cannot exercise the relevant contract.
Reuse meaningful existing coverage. Avoid a fixed test count or coverage target.

Before keeping a new or changed test, identify the contract it protects, the
source of its expected result, and a plausible violation its assertions detect.
An oracle is the basis for deciding correctness; it must not simply reproduce
the result under test. Judge assertions by their contract, not matcher counts
or syntax. Review requests alone do not authorize deleting or rewriting tests.

For bug fixes, reproduce the reported behavior and observe failure for the
intended reason before correcting production code. For new behavior, use targeted
**Test-Driven Development (TDD) / Red–Green–Refactor** where it drives the design;
complete other tests during implementation. Missing symbols or broken setup
alone do not demonstrate a behavioral regression.

Run focused tests first, then the checks and suites required by the project.
Repeat or broaden only for new changes, failures, or unresolved risks. Avoid
repeated full-suite, coverage, or mutation runs without a concrete question.

## Report evidence

Summarize the behavior covered, meaningful scenarios, actual commands and results,
and remaining limits. Distinguish designed, executed, skipped, and blocked tests;
identify the tested revision when it matters. A green mock-based test does not
prove a real integration, browser, or hardware contract.

When used within a delivery workflow, contribute test design and evidence to its
existing acceptance matrix and handoff. Leave delegation, review budgets, and
delivery approvals to that workflow; do not create duplicate tracking artifacts.
