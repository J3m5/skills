# Behavioral Test Design and Quality

## Risk-Based Testing and test boundaries

Choose scenarios for their ability to reveal a plausible failure. Use an
acceptance criterion or public contract as the oracle: expected outputs,
persisted state, observable effects, errors, or forbidden effects.

| Boundary         | Useful evidence                                              | Limitation to account for                                          |
| ---------------- | ------------------------------------------------------------ | ------------------------------------------------------------------ |
| Unit             | A domain rule, calculation, or state transition in isolation | Replaced collaborators may hide integration defects                |
| Integration      | Real collaboration across relevant modules or infrastructure | A simulated transport or database proves only its modeled contract |
| Contract         | Consumer/provider agreement on schemas and semantics         | A hand-written fixture alone does not verify provider conformance  |
| End-to-end (E2E) | A critical flow through the assembled system                 | Higher setup cost and more potential sources of nondeterminism     |

Use the test pyramid as a feedback-cost heuristic, not a mandatory distribution.
For a schema or wiring defect, select a boundary that actually crosses the faulty
connection rather than multiplying unit mocks.

Apply **Equivalence Partitioning** and **Boundary Value Analysis** to input ranges.
Use decision tables for interacting rules or state-transition scenarios for
lifecycle behavior when they improve coverage. Consider empty or invalid inputs,
failures, recovery, repeated actions, and forbidden effects only where callers can
reach them. Add property-based tests for broad invariants when the risk and
available tooling justify them; retain a reproducible counterexample.

## Arrange–Act–Assert (AAA) / Given–When–Then

Give each test a behavioral name and a focused scenario. Several assertions may
be needed to establish one outcome; there is no one-assertion rule. Keep the
action and expected result visible. Extract fixture builders for distracting
setup, but avoid shared helpers that conceal the scenario or compute the oracle
with the production algorithm.

Prefer stable public observations to private fields, extracted helpers, or an
exact internal call order. Assert interactions when the interaction is itself
the contract, such as sending a request once or preventing a write after disposal.
Assert the values and errors required by the contract. A presence check or
no-throw assertion can suffice when it expresses the scenario's complete contract.
Review snapshots as specifications; use focused assertions when a large snapshot
would bury the behavior under irrelevant changes.

After structural UI changes, query the currently rendered interface. A saved DOM
node can remain readable after unmount and no longer represent a control
available to the user.

## Representative regression / Red–Green–Refactor

Reconstruct the trigger, relevant dependency behavior, and externally visible
failure. Keep the system under test real. A simplified reproducer is useful only
if it retains the mechanism responsible for the defect.

Run the new test against the uncorrected behavior and inspect the failure. Setup,
import, or timeout errors unrelated to the defect are not the intended Red.
Then make the correction and observe Green; refactor while retaining coverage.
If the fix is already present, use a safe local comparison or a reversible
reintroduction of the specific defect when permitted, preserving existing work.
Otherwise report that Red was not observed rather than claiming it was.

Do not weaken an assertion, broaden a fixture, or replace the system under test
just to obtain Green. A demonstrably incorrect test may be corrected against the
contract, with the reason stated. Characterization tests can preserve existing
behavior during refactoring; known defects must not become accepted requirements.

## Test doubles and integration fidelity

Use real collaborators when they are fast and controllable. Stub external inputs,
use a small fake for useful stateful behavior, or spy on a contractual effect.
Replace only the boundary needed for control. Preserve relevant return shapes,
error channels, scheduling, cancellation, and subscription semantics.

For consumer tests, model the external responses needed by the scenario rather
than recreating the provider’s full validation engine. Exercise provider
admission rules in provider or integration tests. Client-side parsing and input
assistance remain legitimate behavior to test; they do not prove that the
provider will accept the operation.

Reconsider the mocked boundary before adding recursive partial types or repeated
casts. Keep valid fixtures aligned with the real contract; isolate intentionally
malformed results without weakening production types. Type compatibility alone
does not establish behavioral fidelity.

Share repeated boundary setup with explicit ownership and reset of mutable mock
or cache state. Keep scenario-specific responses, actions, and expectations
visible in the test.

A double must not manufacture the success being asserted. For example, emitting
only success cannot validate reconnection after an error; a single immediately
resolved request cannot validate overlapping requests or late responses. Keep a
real consumer or producer in the test where their agreement is the risk, and
state any provider, browser, or hardware validation still missing.

## Determinism, isolation, and asynchronous lifecycle

Give each test fresh owned state. Control time, randomness, identifiers, and
external resources when they affect the result. Release resources, subscriptions,
listeners, temporary state, and overrides even after failure. Respect existing
parallelism; serializing the suite is not a substitute for isolation.

Drive asynchronous sequences explicitly: start work, hold a response or event,
change state, release it, and assert the final public outcome. Include out-of-order
completion or cancellation when relevant. Await actions and assertions. Use
controlled clocks for timer policy and bounded condition-based waits for genuine
eventual observations; avoid arbitrary sleeps and repeated side effects inside
retry callbacks. Separate timer scheduling from promise/event completion.

Do not hide a timing defect with retries or larger timeouts. First distinguish a
product race, a faulty test double, and an environment failure.

Immediate rendering in a library's test mode does not prove its scheduled work
is disabled. When animation timing is outside the scenario, prefer supported
test or reduced-motion options over mocking controls; verify that callbacks and
scheduled work also follow that mode in the installed version.

## Test-quality audit

Independently inspect the contract, production path, fixture, and assertions.
Ask which realistic faulty behavior would fail this test and which violation of
its stated claim could still pass. Evaluate all assertions, including helpers
and framework-managed checks, before judging a test. Look for mocked-out
behavior, unreachable scenarios, unawaited promises, leaked state, and unsupported
integration claims. For circular oracles, weak assertions, snapshots, property
tests, or mutation probes, use [test-oracles.md](test-oracles.md).

Use coverage to locate unexplored branches; exercised lines do not establish
correctness. Use the oracle guidance to distinguish an inferred gap from an
executed mutation result. When a new guard rejects unexpected traffic, a scoped
unhandled request can verify that the scenario fails rather than merely logging
an error. Report concrete missing scenarios and their consequences; do not
require tests for trivial implementation details or documentation edits.

Check runner diagnostics and process status as well as assertions: a run can
report passing test cases and still fail on unhandled asynchronous errors.
