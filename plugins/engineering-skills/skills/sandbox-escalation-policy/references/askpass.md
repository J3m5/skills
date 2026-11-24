# Graphical password prompts for applications

Use this path when the operator wants the agent to start a specific operation
and the only interaction needed is entering an application password.

1. Confirm the authorized operation and target. Request sandbox approval
   separately if needed. The password dialog only authenticates to the
   application.
2. Check which host and operator desktop the agent can reach. For a headless
   target, authenticate on the operator's desktop when the approved workflow
   supports sending only the data the target needs. If no trusted prompt is
   reachable, use an available operator-controlled authentication path or
   stop and explain which access is missing.
3. Use the application's own prompt when available. Start the authorized
   operation and observe the application's reported result. The application
   receives the password directly. Stop on cancellation or authentication
   failure, and check the operation's state if it may already have run.
4. If the application needs a separate helper, use a trusted one such as
   `zenity --password`. Name the application and operation in the dialog.
   Launch the helper from the runner that authenticates to the application.
   Capture its output privately and pass the password through the application's
   supported input channel. Keep passwords and session tokens out of
   command-line arguments, chat, shell tracing, logs, and tool output.
   Stop before running the authorized operation if the helper is cancelled,
   fails, or returns empty input.
5. After successful authentication, carry out the authorized operation or
   verify its outcome if the application has already run it. Clean up any
   temporary session the workflow created on success or failure, and report
   only a non-sensitive result.

## Example with Bitwarden CLI and Vaultwarden

- On the desktop, verify the expected Vaultwarden server and CLI account.
  Use an existing authorized session if it is available to the runner.
  Unlocking or locking can invalidate session keys for the same account in
  the same CLI profile, including in other terminals. If those sessions
  need to stay active, use a separately configured profile or check with the
  operator before proceeding. When using a separate profile, set
  `BITWARDENCLI_APPDATA_DIR` for every `bw` command, including cleanup.
- If an unlock is needed, open the password dialog and run
  `bw unlock --passwordenv APP_UNLOCK_PASSWORD --raw` with
  `APP_UNLOCK_PASSWORD` set only in the unlock process's environment.
  Capture the returned session key privately. Whether reusing or creating a
  session, pass `BW_SESSION` only to `bw` processes that need it.
- If an authorized import uses a vault record, verify the expected record and
  organization. Extract only the required fields. For a remote import, send
  those fields directly over SSH on standard input to the verified operation
  on the expected host. Keep the password, session key, and full record on the
  desktop.
- Run `bw lock` in the runner's cleanup path if the runner unlocked that
  profile for this operation. Discard the temporary session key and check
  cleanup without printing secret-bearing command output.
