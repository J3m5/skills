# Placement and Surface Guide

Use this reference when selecting the canonical documentation surface.

## Repository Ownership and Audience

Determine which repository owns the affected file and who is expected to receive it. Check relevant Git roots, tracking and ignore rules, repository conventions, and remotes. An untracked file may be intended for a future commit; a tracked file may belong only to a local workspace. Neither the name `.agents/` nor the presence or absence of a remote establishes the audience by itself.

Distinguish:

| Material                            | Owner and audience                                                        | Lifecycle                                                                                              |
| ----------------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| Shared application documentation    | Application repository; its contributors, operators, or users             | Maintained with the application's supported behavior                                                   |
| Local agent workspace documentation | Local workspace or developer; may be tracked in a separate Git repository | Durable references, supplied source documents, local setup, investigations, and coordination as needed |
| Working artifacts                   | The task or runtime that produced them                                    | Temporary unless a concrete retention need exists                                                      |

Local documentation can be canonical for workspace setup or agent coordination without being distributed with an application. Do not treat all local material as scratch, or all tracked material as a team deliverable. Conversely, keep knowledge needed by application contributors in the application's shared reference when the task requires it; a local-only note is insufficient for that audience.

### Local Parent with Independent Application Repositories

A parent repository may hold workspace configuration and documentation while excluding independent application checkouts from its tracking. These are separate ownership and commit scopes, not automatically submodules or a monorepo. Use the established layout rather than imposing it.

Keep cross-repository coordination in the owning workspace and application-facing guidance in the relevant application repository when its audience needs it. Route readers to the maintained source instead of copying specifications across both scopes.

Illustrative cases, not required files:

- **Local multi-application setup:** workspace guide for local composition, linking to each application's maintained setup instructions.
- **API contract used by several applications:** shared reference in the API repository; consumer and workspace guides link to it.
- **Cross-repository delivery sequencing:** workspace plan or issue when coordination needs a durable record.
- **One-off startup failure:** conversation or working notes; add only a reusable troubleshooting conclusion to the relevant guide.

For local-only exclusions inside an application checkout, use its established local exclusion mechanism rather than changing a shared `.gitignore` merely to accommodate the agent workspace. A workspace documentation task does not imply staging, committing, or publishing changes across its application repositories.

## Source Order

Prefer the first source that fully preserves the knowledge:

| Surface                                                         | Use for                                                                              | Avoid                                             |
| --------------------------------------------------------------- | ------------------------------------------------------------------------------------ | ------------------------------------------------- |
| Types, schemas, tests, lint, CI, generators                     | Exact enforceable contracts                                                          | Rationale that cannot be encoded                  |
| Self-explanatory code                                           | Local behavior and data flow                                                         | Cross-cutting architecture                        |
| Comments or docstrings                                          | Local rationale, invariants, compatibility constraints, public symbol contracts      | Narrating obvious code                            |
| Local README                                                    | Stable subsystem orientation, boundaries, entrypoints, local commands                | File-by-file inventories                          |
| Root README                                                     | Product introduction, installation, primary usage, contribution entrypoints, routing | Full architecture or agent-only policy            |
| Structured docs                                                 | Cross-cutting architecture, domain, security, operations, contribution workflows     | Volatile implementation inventories               |
| Generated or validated references                               | CLI, configuration, API, schemas, persistent formats                                 | Independently maintained rationale                |
| ADR                                                             | Why a consequential durable choice was made                                          | Current implementation details or progress        |
| Conversation or working notes; active plan or issue when needed | Sequence, status, provisional decisions, checkpoints                                 | Treating every operation as a durable deliverable |
| Scoped skill                                                    | Reusable agent workflows and task-specific procedures                                | Stable constraints needed on most tasks           |
| `AGENTS.md`                                                     | Frequently needed, non-inferable, high-cost agent constraints and routing            | Generic advice or repository encyclopedia         |

## Placement Questions

Consider these questions as needed:

1. Can the rule be enforced mechanically?
2. Is the knowledge reliably and cheaply inferable?
3. Must a person author, inspect, debug, or integrate with the interface?
4. What is the narrowest scope that fully owns it?
5. Who needs it?
6. When must it be loaded?
7. How volatile is it?
8. What is the consequence if it is wrong?

## Observable Interface Rule

When changing a supported interface that people author, inspect, or integrate with, preserve usable human guidance alongside its executable source. Relevant interfaces include:

- configuration files;
- persistent or serialized formats;
- CLI commands, flags, defaults, and allowed values;
- public APIs or integration contracts;
- generated indexes or manifests;
- operational procedures with exact inputs or outputs.

An existing README, CLI help, or validated example may be sufficient; a separate reference is not mandatory. For third-party tools, use their authoritative documentation rather than reproducing it locally unless a local guide is requested or needed for project-specific behavior. Internal scratch files and incidental outputs do not automatically create a supported interface.

Keep exact field validation in existing schemas or generators. Preserve the examples, semantics, defaults, limits, and failure behavior readers need, and validate changed claims against the executable source. Missing validation machinery is a finding, not an automatic expansion of the task.

## Comments

Add a comment only when removing it would materially obscure:

- rationale;
- an invariant;
- an external compatibility constraint;
- a security assumption;
- a non-obvious trade-off;
- a workaround and its removal condition;
- a public contract not expressible by types.

Refactor unclear code instead of narrating it.

## README Files

Create a local README only for a stable conceptual boundary. Include purpose, boundaries, entrypoints, validation, extension points, and links. Do not create one for every directory.

Keep the root README task-oriented and stable. Route detailed architecture and current delivery status elsewhere.

## Structured Documentation

Organize by knowledge type or user task. Give each category an index when readers would otherwise need broad searching.

Keep architecture focused on current structure and invariants. Keep security and operations explicit when the cost of omission is high.

## ADRs and Plans

Use an ADR for a consequential durable choice when the project records such decisions or future readers need its rationale. Plausible alternatives alone do not require a new decision document.

Keep multi-stage work in the conversation or working notes unless persistent coordination or the project's workflow warrants an active plan. After a persistent plan is completed:

- retain enduring rationale in the relevant existing reference, or a new decision/design document when warranted;
- update current user and contributor references;
- remove or archive transient execution detail;
- never leave the plan as the only source of final behavior.

## AGENTS.md

Apply the admission test in `SKILL.md`. Keep stable constraints concise and route to deeper sources. Commands and validation expectations belong here only when they pass that test; reusable workflows belong in scoped skills.

Nested files contain only narrower rules or overrides. Do not repeat inherited instructions.
