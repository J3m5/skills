# Sudo over SSH

Local sandbox access, SSH login, and remote `sudo` are separate checks.
`SSH_ASKPASS` handles SSH authentication. Remote `sudo` looks for its helper in
the destination's environment and configuration.

## Establish the destination and channel

Use the authorized host, remote account, target identity and command. Preserve
host-key verification and the existing trusted connection setup. Avoid adding
agent forwarding as an authentication fallback. Quote command arguments for
the remote shell as well as the local invocation.

For a noninteractive operation, `ssh -o BatchMode=yes` and remote `sudo -n`
disable prompts at their respective layers. Inspect diagnostics to distinguish
an SSH error, a remote sudo rejection, and a failure after command launch.

For interactive remote sudo, use a trusted session the user can interact with
directly. Request the remote TTY separately from any local PTY using SSH's
`-t` when authentication requires it. If no such channel is available, identify
the exact authentication step the user must perform.

## Headless hosts and remote askpass

Check `sudo --version` and `sudo --help` on the destination before choosing
an authentication path. The remote host may use classic sudo or sudo-rs.
Package presence and the local machine's sudo version do not establish which
options the remote command supports.

If the destination supports `sudo -A` and already has a trusted askpass
helper, check its configuration in the session that will run sudo. A helper
configured through `SUDO_ASKPASS` must be available and executable on the
destination. Shell startup settings can differ between interactive and
noninteractive SSH sessions.

- **TTY-backed helper.** If the helper reads `/dev/tty`, run it through
  `sudo -A` in a remote TTY the user can interact with. From a user-operated
  terminal, `ssh -t <host>` can allocate that channel. A tool-owned PTY
  alone cannot collect the user's password.
- **Graphical helper.** A configured GUI helper needs an accessible
  graphical session. On a headless host, use the existing TTY-backed helper
  or a user-operated terminal with ordinary interactive sudo, according to
  the destination's configuration.

## Keep passwords off the command input stream

Do not pipe a local password helper into `ssh` and `sudo -S`. Both sides of the
pipeline start independently. SSH can still run the command if the helper is
cancelled and remote sudo needs no password. `pipefail` reports a pipeline
failure after the fact. With cached authentication or `NOPASSWD`, password
bytes may reach the child command as ordinary stdin.

A separate `sudo -v` invocation may leave no usable cache for a later SSH
session. Sudo timestamps can be scoped to a TTY or parent process. After a
disconnect, check remote state before retrying any potentially applied change.

- [Local authentication options](sudo-local.md)
- [sudo stdin authentication](https://www.sudo.ws/docs/man/sudo.man/)
- [SSH terminal options](https://man.openbsd.org/ssh)
- [SSH BatchMode](https://man.openbsd.org/ssh_config#BatchMode)
