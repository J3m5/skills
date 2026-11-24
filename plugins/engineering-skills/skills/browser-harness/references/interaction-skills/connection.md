# Connection

Check the installed CLI with `browser-harness --version`. When mise manages
the tool, use `mise exec -- browser-harness` if the CLI is missing from PATH.
For installation, see the [Browser Harness package](https://pypi.org/project/browser-harness/).

Run a browser command first. The daemon starts on demand. Use
`browser-harness --doctor` if the command fails. To check an existing daemon
without starting it, run `browser-harness doctor --json --require-existing-daemon`.

- If Chrome requests remote debugging permission, keep the original command
  running and wait for the user to click **Allow**. If debugging is disabled,
  direct the user to `chrome://inspect/#remote-debugging`. Repeated attach
  attempts may produce additional prompts.
- On macOS, `browser-harness mac-approve` can handle the local Chrome debugging
  prompt while the original call waits. Use the same `BU_NAME` if the original
  call used a named daemon. If it reports `accessibility-required`, the user
  must grant the app Accessibility access before retrying the helper.
- `BH_CHROME_PATH` can select the Chrome or Chromium executable used at launch.
  Use `BU_CDP_URL` or `BU_CDP_WS` before starting a daemon when the task
  specifies a DevTools endpoint. Choose a fresh daemon name if another daemon
  already serves a different endpoint.
- If a daemon dedicated to the task stays unresponsive, run
  `browser-harness --reload` with the original daemon name, then reconnect.
  Restart a shared daemon only when its other users can reconnect safely.
  The CLI manages its runtime socket and PID files.
- If the attachment reports an internal page or the omnibox, use the
  [tab workflow](tabs.md) to select the intended target.
