# Local sudo authentication

Use the exact authorized command and target identity. A successful `sudo -v`
or `sudo id -u` cannot establish whether sudoers allows that command. Check the
installed `sudo` and `sudoers` manuals when host policy or version matters.

## Select a working channel

Check the active binary with `sudo --version` and its options with
`sudo --help` when choosing an authentication channel. A host can have both
classic sudo and sudo-rs installed. Use the capabilities of the binary that
the command will actually run.

- **Noninteractive.** Use `sudo -n` when prompts are unavailable. It fails if
  authentication requires a prompt. Inspect the diagnostic before retrying,
  since the exit status can also come from the command itself.
- **Askpass.** Use `sudo -A` with a trusted helper configured through
  `SUDO_ASKPASS` or `sudo.conf`. Let `sudo` invoke the helper and receive its
  output. Check whether the helper's own input channel is available.
- **Terminal.** Use a TTY when the authentication flow requires it and the
  user can enter credentials there directly. A tool PTY alone does not provide
  a user-operated terminal.

Keep passwords in the trusted authentication channel. Do not collect them in
chat, relay them through tool input, or store them in an askpass script. If no
suitable channel is available, complete independent work and identify the
authentication step the user must perform.

## Classify the failure

- If `sudo` explicitly requires a password before launch, select an available
  channel for the same command. If the user cancels the prompt, stop prompting.
- If sudoers rejects the command, check the allowed command and target identity.
  For `no_new_privs` or a `nosuid` mount, investigate the execution boundary.
  Switching password channels will not resolve either case.
- For an authorized protected file write, elevate the writer, such as `install`
  or `tee`, with reviewed inputs. In `sudo echo ... > file`, the calling shell
  opens the file before `sudo` runs.

- [sudo options](https://www.sudo.ws/docs/man/sudo.man/)
- [sudoers policy and credential caching](https://www.sudo.ws/docs/man/sudoers.man/)
