# Mise and project diagnostics

Choose the diagnostic surface that matches the failure. `mise doctor` checks
mise's installation and setup. `mise doctor project` runs project-defined
`[doctor.checks.NAME]` commands, for prerequisites tool versions cannot prove,
such as native-library discovery or a database accepting connections.
These are explicit, one-off diagnostics: they do not run automatically at prompts
or before tasks, continuously monitor services, or restart unhealthy daemons.

For a requested reusable prerequisite check, define a command that inspects
the intended state, with an actionable `hint`, a suitable timeout and `os`
selection when platform-specific. A hint is printed, never executed by doctor.
Keep checks with the project that needs them rather than adding global checks
for one repository. A higher-precedence same-named check replaces the entire
definition, including dir and hint. `run`, `description` and
`hint` support templates; `dir` does not.

`depends` names checks that must pass first. A failed, errored,
skipped or blocked prerequisite blocks its dependents without executing them.
Use this to report the root cause once; unknown names and cycles are config errors.

Checks run in the project's environment and installed tool PATH, from their
config root or explicit `dir`. They do not install missing tools or run task
dependencies/hooks. They are not sandboxed; config env directives still apply.
Inspect existing commands before treating a diagnostic run as read-only. For
metadata inspection of unreviewed config, use [security controls](security.md);
safe mode refuses to execute applicable checks rather than validating them.

Run `mise doctor project --json` when structured results help locate a failure.
Its document has `errors` for config-loading failures and `checks` for declared
checks; nonempty `errors` leaves `checks` empty. Check both before interpreting an
empty check list as success. This schema is separate from a task run report.
Distinguish `pass`, `fail`, execution/config `error`, `blocked` and platform
`skipped`. Failure/error makes the exit non-zero; `blocked` alone does not.
A skipped prerequisite can therefore leave a dependent blocked with exit 0.
Zero with no checks or only skipped/blocked checks does not prove the required
prerequisite exists. Diagnose the failed check and apply only the remedy needed
by the requested work.

For task definition errors, use `mise tasks validate` instead. Use daemon
`ready_*` probes to gate startup and `health_*` probes plus an intended `retry`
policy for ongoing health and recovery; see [daemons](daemons.md). A project
doctor check can inspect connectivity on demand without duplicating those
lifecycle controls or introducing a global doctor check for each daemon.

## Download failures

For an organization's TLS interception, `extra_ca_certs` can add
its approved CA certificates; do not treat disabling TLS verification as the
repair. `ipv4_only` is a targeted option for a demonstrated IPv6
connectivity problem. Inspect the actual HTTP error before changing either.
Stale netrc credentials can cause a download to fail with 401 even if the server
allows anonymous access. Inspect the authentication source without printing
credentials; do not assume every 401 has that cause.

- [Project check contracts and results](https://github.com/jdx/mise/blob/v2026.11.9/docs/configuration/project-diagnostics.md)
- [Project doctor CLI](https://github.com/jdx/mise/blob/v2026.11.9/docs/cli/doctor/project.md)
- [Mise installation doctor](https://github.com/jdx/mise/blob/v2026.11.9/docs/cli/doctor.md)
- [Check dependencies and results](https://github.com/jdx/mise/blob/v2026.11.4/docs/configuration/project-diagnostics.md)
