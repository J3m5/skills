# Observable Contract Patterns

Use this reference before replacing human-readable interface documentation with code or schemas. Apply the relevant interface pattern within the requested scope. Prefer existing validation and generation mechanisms; treat a missing mechanism as a finding unless implementing it is part of the authorized work.

## Principle

Implementation and human-readable references serve different purposes.

The executable source establishes implemented acceptance rules and behavior; validated requirements and decisions establish the intended contract. Report discrepancies without treating implementation as proof that a requirement is wrong. The human reference lets a person discover the interface, understand its semantics, author valid input, inspect stored output, and diagnose failures.

Avoid independent copies of the same exact specification. Use existing validation or generation mechanisms when relevant; otherwise review against available sources and state verification limits. A missing mechanism does not by itself require adding tooling or removing useful guidance.

Apply these patterns to supported interfaces within the task's scope. The lists below guide relevant coverage; using a file or command during a task does not require creating its documentation and validation machinery.

## Configuration and Recipe Formats

Provide:

- format version;
- complete minimal or representative example;
- required and optional fields;
- allowed values;
- ordering semantics;
- defaults and omission behavior;
- parser limits and rejected syntax;
- extension strategy.

Validate changed examples with the real parser or schema when available. When adding regression coverage is warranted, read the example from Markdown rather than maintaining another copy in a test.

Keep resolution algorithms and architectural rationale in design documentation; link rather than duplicate them.

## Persistent Formats

Document supported durable formats in the existing reference where possible; version it when the compatibility policy requires it. Internal checkpoints and ad hoc reports do not automatically need a published format contract.

Document:

- path and lifecycle;
- field names in the actual serialized representation;
- mutability;
- identity and hashing semantics;
- canonical ordering and encoding;
- size limits;
- compatibility and unknown-version behavior.

Validate changed JSON examples with the existing executable schema or parser when available and relevant. Check serialization when the representation is contractual. Use realistic but clearly illustrative identifiers.

## CLI Interfaces

Use command definitions as the canonical source for the arguments, flags, values, defaults, descriptions, and environment variables the CLI defines. For variables interpreted by a library or runtime, explain their effect on the command and link to that component’s documentation for their semantics.

CLI help can suffice as the human reference; generate a separate reference when readers or an established workflow need it. Preserve important constraints enforced elsewhere, such as runtime schemas, in the relevant help or reference.

Check rendered help or generated-reference freshness when those surfaces change. Separate current commands from planned commands.

## Public APIs

Generate signatures and field inventories when tooling can do so reliably. Keep examples, stability guarantees, lifecycle, errors, and integration guidance in a curated reference.

Do not copy internal module inventories into architecture documents.

## Test Strategy Documentation

Document testing policy, levels, fixtures, boundaries, and required gates. Do not maintain an exhaustive prose inventory of individual test cases when the test suite is the authoritative source.

Retain named threat-model requirements, compatibility matrices, or acceptance criteria when they provide traceability beyond the test implementation.

## Safe Consolidation Examples

Prefer:

- design document explains invariants;
- versioned reference shows exact observable form;
- existing schemas or generators enforce exact constraints when available;
- documented examples are checked with existing tooling or reviewed with explicit verification limits;
- index routes to both design and reference.

Reject:

- design document with a manually copied full schema;
- schema source as the only documentation for users;
- unverified examples presented as validated;
- generated output edited manually;
- future fields mixed into current format references.
