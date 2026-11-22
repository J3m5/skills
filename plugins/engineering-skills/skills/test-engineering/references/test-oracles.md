# Test Oracles and Fault Detection

Use this for suspected tautologies, assertion-quality reviews, and targeted
mutation evidence. Keep the review within the requested tests and behavior.

## Establish an independent oracle

Trace the expected result to a requirement, worked example, externally defined
format, trusted reference, or domain law. A literal copied from today's output
is not independently justified merely because it is hard-coded. A helper or
reference model can be useful when it does not share the production decision
logic responsible for the risk.

Distinguish a **tautology** (the check guarantees itself without establishing the
claimed behavior), a **weak assertion** (some relevant wrong outcomes still
pass), an **uncovered scenario**, and **implementation coupling** (a harmless
internal change breaks the test). These are different diagnoses. A test may
catch useful defects while still having one of these limitations.

For a weak-assertion finding, give a realistic wrong result that satisfies the
exact matcher and the other checks in that scenario. Tie it to the test's claim;
a focused test need not establish the entire feature. Inspect helper assertions,
exception expectations, teardown checks, and runner behavior before declaring
that no assertion runs. If the contract is unavailable, identify that uncertainty
instead of inventing a requirement.

## Recognize patterns without blanket bans

| Signal                                                                                | Inspect and act                                                                                                                                                                           |
| ------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Result compared with itself, or expected value recomputed by the same tested function | Replace the circular expectation with a justified value or property. Repeated calls may legitimately test determinism, but do not establish output correctness.                           |
| Test copies production branches, algorithm, or configuration                          | Identify the shared error it would preserve. Use independent examples or a simpler reference model. A schema, protocol constant, or public configuration value may itself be contractual. |
| Assertions inspect source text, private state, or internal call order                 | Prefer the consumer-visible effect. Retain structure or ordering checks when that structure or ordering is an explicit compatibility or protocol requirement.                             |
| Snapshot recorded from current output                                                 | Inspect its contents and acceptance basis. Reviewed snapshots can preserve intended behavior or characterize legacy output; blind recording/updating does not establish correctness.      |
| Mocks repeat the implementation's call graph, or replace the subject itself           | Exercise real subject behavior. An outbound payload, forbidden write, delegation, or once-only effect can be the contract, including in a thin wrapper.                                   |
| Presence, truthiness, broad range, or partial-object check                            | Name a wrong value it permits before recommending stronger assertions. Presence/absence or a subset may be exactly the promised behavior.                                                 |
| Assertion behind a condition, empty iteration, swallowed failure, or unawaited task   | Check whether an incorrect result can bypass verification. Table-driven cases and explicit exception/no-throw contracts are not automatically defective.                                  |

For example, if an invoice rule grants 10% off from 100 units, checking only that
the total is positive admits the wrong total of 100 at the threshold. An
independently worked expectation of 90 detects changing `>= 100` to `> 100`.
The boundary case is missing coverage if no test reaches 100; a passing test at
another input is not thereby tautological.

Round-trip, idempotence, and metamorphic tests check relationships; they are not
self-comparisons merely because both sides involve production functions. State
the law and use inputs that exercise it. A round-trip may detect information
loss while missing a mutually consistent encoder/decoder format error; add
external format examples when interoperability is the claim. Likewise, a sort
property checking only order admits an implementation returning an empty list:
also preserve length and elements, including multiplicities. Generated cases
need meaningful domains and reproducible counterexamples; more inputs cannot
repair a circular oracle.

## Probe a concrete defect when useful

Start with source reasoning: name the edit, a reachable input or event sequence,
the correct observation, the changed observation, and the relevant assertion.
Check existing coverage through callers before proposing another test. Treat
an inferred survivor as a hypothesis, not an execution result.

When execution fits the requested work and resolves meaningful uncertainty:

1. Establish a passing baseline with the focused project command; confirm that
   the intended tests ran.
2. Apply one reversible fault in an isolated copy or preserve the exact current
   files before editing. Do not overwrite unrelated or concurrent work.
3. Run the relevant tests and inspect the actual failure or pass. Record the
   scope, edit, command, and observation.
4. Restore only the injected change, including after failure. When strengthening
   a test, rerun that same fault to show the new assertion detects it, then
   restore production and confirm Green.

Keep evidence levels explicit:

| Evidence                                                              | Conclusion                                                                  |
| --------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| Source inspection only                                                | Inferred detection or candidate survivor; not executed                      |
| Relevant assertion fails with the fault active                        | Observed detection for this fault and selected tests                        |
| Collected tests pass with the fault active                            | Observed survival within that scope; inspect the behavioral difference      |
| Build/setup failure, zero collected tests, unrelated error            | Inconclusive for assertion strength                                         |
| Timeout                                                               | Report separately; inspect whether the injected fault causes nontermination |
| No observable change for any reachable case under the stated contract | Equivalent; no new test required for that edit                              |

A surviving mutant can indicate missing input coverage, weak assertions, an
inadequate boundary, or equivalence; it does not establish a tautology. Preserve
a mutation tool's reported status separately from the behavioral interpretation.
Agreement on one sampled input does not establish equivalence. One detected
fault does not establish that the whole suite is adequate. Prefer
focused probes over introducing tools, exhaustive mutation runs, or score quotas.

## Decide and report

Retain a test that protects a meaningful contract, even if it has one assertion
or uses mocks. Strengthen or rewrite a demonstrated weakness when fixes are in
scope. Delete only after establishing that it adds no distinct useful protection;
preserve any needed coverage in the same change. Do not mechanically rewrite
expectations after a failure or remove tests merely for matching a pattern.

For each actionable finding, report the test location, claimed behavior, oracle
problem or missed outcome, concrete counterexample, evidence level, and smallest
useful correction. State when no actionable finding is supported.

## Sources and adaptation

Reviewed 2026-11-02. These are references, not additional skills to invoke.

- [brandhaug: remove-tautological-tests](https://github.com/brandhaug/skills/blob/master/remove-tautological-tests/SKILL.md): pattern prompts; blanket removal rules are deliberately not adopted.
- [dotnet: assertion-quality](https://github.com/dotnet/skills/blob/main/plugins/dotnet-test/skills/assertion-quality/SKILL.md): counterexample calibration; no assertion-diversity quotas or blanket round-trip classification.
- [dotnet: test-gap-analysis](https://github.com/dotnet/skills/blob/main/plugins/dotnet-test/skills/test-gap-analysis/SKILL.md): observable witnesses and inferred versus executed evidence.
- [Testing Best Practices](https://github.com/adewale/testing-best-practices/blob/main/testing-best-practices/SKILL.md): contract-driven oracles and proportional test investment.
- [WIO](https://github.com/workersio/skills/blob/main/plugins/wio/skills/wio/SKILL.md): review the value of newly generated tests before retaining them.
- [Test Smells](https://testsmells.org/pages/testsmells.html): vocabulary for distinct test problems; Java-oriented detection heuristics are not universal rules.
- [Stryker mutant states](https://stryker-mutator.io/docs/mutation-testing-elements/mutant-states-and-metrics/): execution outcomes, including timeouts and invalid mutants.
- [Stryker equivalent mutants](https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/): behaviorally inert edits and the limits of mutation scores.
