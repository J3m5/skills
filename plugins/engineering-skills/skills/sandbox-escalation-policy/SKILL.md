---
name: sandbox-escalation-policy
description: >-
  Resolve sandbox access blocks, escalation denials, and sudo authentication
  for local or SSH commands. Use when permissions or elevation need a decision
  or diagnosis, or when an agent-run command needs the operator to enter an
  application password through a graphical askpass prompt.
---

# Sandbox Escalation Policy

## Choose the execution path

Check the user's authorization for the operation and target, the active tool's
access rules, and any required OS identity or authentication independently.
Reuse existing authorization and grants within their scope.
Sandbox escalation leaves OS privileges unchanged, and `sudo` still runs under
the execution environment's restrictions.

Use a suitable native app or tool when its own permissions cover the work.
For shell commands, check the actual filesystem and network rules. `sudo`, GUI
use, and network use alone do not imply a sandbox exception. When the command
requires one, request it before execution if the current policy permits it.
Prefer a targeted grant when supported. For per-command escalation, submit the
exact operation with a short justification and avoid reusable prefixes that
grant a shell, interpreter, or arbitrary `sudo` commands. Leave global security
controls in place unless administering them is part of the authorized task.

- Read [Local sudo](references/sudo-local.md) to select or diagnose a local authentication channel.
- Read [Sudo over SSH](references/sudo-ssh.md) when the privileged command runs on a remote host.
- Read [Graphical askpass for applications](references/askpass.md) when the
  operator wants the agent to start an authorized operation and open a masked
  password prompt, for example to unlock a Vaultwarden vault with `bw`.

## Decide whether to retry

- **If access fails unexpectedly**, identify whether the command, OS policy, or
  sandbox blocked it. Request sandbox access only when the evidence points to
  that boundary.
- **If approval is denied**, continue with a materially safer authorized option.
  If blocked, explain the denied action and reason. Point to the interface's
  formal approval path if one applies. Do not retry through a different tool or
  wrapper to bypass the decision.
- **After a timeout, cancellation, or lost connection**, determine whether
  approval stopped or execution may have begun. Follow the current approval
  rules and check the resulting state before repeating a change that may have run.
  If the state stays unknown, retry only when the change is safe to repeat.

- [Sandbox and approval controls](https://learn.chatgpt.com/docs/sandboxing)
- [Automatic review and denials](https://learn.chatgpt.com/docs/sandboxing/auto-review)
