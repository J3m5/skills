# Graphical password prompts for applications

Use this path when the operator wants the agent to start a specific operation
and the only interaction needed is entering an application password.

1. Confirm the authorized operation and target. Request sandbox approval
   separately if needed. The password dialog only authenticates to the
   application.
2. Locate a trusted graphical password helper on the operator's active
   desktop. Use the application's own prompt if it provides one. Otherwise,
   an installed helper such as `zenity --password` can display a masked input.
   Name the application and operation in the dialog. For a headless target,
   run the prompt and local authentication on the operator's desktop if the
   approved workflow supports transferring only the required data. Check
   which host and desktop the agent can reach before promising a prompt.
3. Launch the prompt from the same runner that will authenticate to the
   application. Capture the helper's output privately in that runner and
   supply the password through the application's supported private input
   channel. Keep the password and any session token out of command-line
   arguments, chat, shell tracing, logs, and tool output. Abort before making
   changes if the operator cancels, the prompt fails, or the input is empty.
4. Perform the scoped operation, clean up any temporary session on both
   success and failure, and report only a non-sensitive result. If no trusted
   prompt is reachable, tell the operator which host lacks it and use an
   available operator-controlled authentication path.

## Example with Bitwarden CLI and Vaultwarden

- On the desktop, check that `bw` is logged in to the expected Vaultwarden
  server. Open the password dialog when a vault unlock is needed.
- Run `bw unlock --passwordenv APP_UNLOCK_PASSWORD --raw` with
  `APP_UNLOCK_PASSWORD` set only in the unlock process's environment. Capture
  the returned session key privately. Set `BW_SESSION` only for the child
  processes that need it.
- If an authorized import uses a vault record, verify the expected record and
  organization. Extract only the required fields. For a remote import, send
  those fields directly over SSH on standard input to the verified operation
  on the expected host. Keep the password, session key, and full record on the
  desktop.
- In the runner's cleanup path, lock any vault it unlocked for the operation
  with `bw lock` and discard the temporary session key. Check that the cleanup
  succeeded without printing secret-bearing command output.
