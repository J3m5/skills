# Bitwarden CLI and Vaultwarden

Use the operator's desktop for `bw unlock` and verify that the CLI and
Bitwarden Desktop use the expected server and account. Reuse an authorized CLI
session if it is available to the runner.

Unlocking or locking can invalidate session keys for that account in the same
CLI profile, including in other terminals. If those sessions need to stay
active, use a separately configured profile or check with the operator before
proceeding. Set `BITWARDENCLI_APPDATA_DIR` for every `bw` command in the
separate profile, including cleanup.

## Set up native desktop authentication

This path was verified with Bitwarden CLI and Desktop 2026.11.0, Desktop
installed through Flatpak on Linux Mint, and Vaultwarden 1.37.5.

- **Linux Flatpak.** Install Bitwarden's official Polkit policy for the
  installed Desktop version at
  `/usr/share/polkit-1/actions/com.bitwarden.Bitwarden.policy`. Verify the
  action with `pkaction --action-id com.bitwarden.Bitwarden.unlock --verbose`
  and check that active sessions require `auth_self`. Enable **Unlock with
  system authentication** under
  **Settings → Security** in Bitwarden Desktop. Polkit can use the Linux
  account password through PAM when the system has no biometric sensor.
  If `sudo` cannot gain privileges for this authorized installation, see
  [local file administration](sudo-local.md#use-the-desktops-file-administration-service).
- **Vaultwarden.** Append `biometrics-sdk-ipc` to the comma-separated
  `EXPERIMENTAL_CLIENT_FEATURE_FLAGS` in the service's configuration.
  Apply the configuration to Vaultwarden and confirm that `GET /api/config`
  returns `featureStates["biometrics-sdk-ipc"] == true`. The clients can
  cache this response for about an hour. If Desktop still uses the old
  configuration, allow it to refresh, reopen the app and check that system
  authentication is enabled for the account.
- **Desktop proxy.** If the host CLI cannot locate the Flatpak's proxy, set
  `BITWARDEN_DESKTOP_PROXY_PATH` for the CLI process. On the tested package,
  the executable is `files/Bitwarden/desktop_proxy` relative to the location
  returned by `flatpak info --show-location com.bitwarden.desktop`. Verify
  that it is executable before using it.

- [Bitwarden Desktop biometrics on Linux](https://bitwarden.com/help/biometrics/)
- [Official Polkit policy for Desktop 2026.11.0](https://raw.githubusercontent.com/bitwarden/clients/desktop-v2026.11.0/apps/desktop/resources/com.bitwarden.desktop.policy)
- [Bitwarden CLI 2026.11.0 desktop authentication](https://github.com/bitwarden/clients/blob/cli-v2026.11.0/apps/cli/README.md#unlock-with-desktop-biometrics)
- [Vaultwarden 1.37.5 feature flag configuration](https://github.com/dani-garcia/vaultwarden/blob/1.37.5/.env.template#L2195-L2228)

## Use the session for the authorized operation

- Start `bw unlock --raw` in a runner that captures its output privately.
  Leave `BW_NOINTERACTION` unset for this attempt. Bitwarden Desktop handles
  system authentication. If the CLI falls back to a terminal password
  prompt, stop and check the Desktop setting, server flag, cache, and proxy
  before retrying. Stop prompting if the operator cancels.
- If native authentication is unavailable and the operator wants a graphical
  password helper, follow [Graphical password prompts](graphical-password-prompts.md).
  Run `bw unlock --passwordenv APP_UNLOCK_PASSWORD --raw` with the master
  password set only in the unlock process's environment.
- Keep the raw session key private. Pass `BW_SESSION` only to `bw` child
  processes that need it. Verify the session with `bw status`. For an
  authorized import, verify the expected vault record and organization.
  Extract only the required fields. For a remote import, send those fields
  directly over SSH on standard input to the verified operation on the
  expected host. Keep the password, session key, and full record on the desktop.
- Run `bw lock` in cleanup if the runner unlocked the profile for the
  operation. Confirm that the temporary session no longer unlocks the profile
  and discard the key. Report the result without printing secret-bearing output.
