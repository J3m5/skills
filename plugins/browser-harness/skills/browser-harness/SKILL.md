---
name: browser-harness
description: Control a local Chrome or Chromium browser with Browser Harness when a task needs rendered UI, browser interaction, an authenticated session, screenshots, recordings, or browser-side files. Use native web tools for ordinary public search and page retrieval.
---

# Browser Harness

Use this skill when Browser Harness is the chosen browser tool. Check for the
`browser-harness` executable and run `browser-harness --version` for version
checks. The Codex plugin supplies the skill. The CLI is a separate prerequisite.
See [Connection](references/connection.md) for setup and troubleshooting.

## Run a program

The upstream CLI reads Python on stdin and pre-imports its browser helpers:

```bash
browser-harness <<'PY'
print(page_info())
PY
```

If the installed command is the local wrapper, it also accepts
`browser-harness --code 'print(page_info())'` and `browser-harness --script FILE`.
The current environment's sandbox and approval policy controls access. If the
browser profile, runtime socket, or CDP endpoint requires access outside the
sandbox, use the supported approval mechanism for the specific operation.

## Work in the browser

- Start with `current_tab()` and `list_tabs(include_chrome=False)`. Reuse
  the tab already assigned to the task with `switch_tab(target_id)`. If no
  suitable tab exists, use `new_tab(url)` once and reuse it across invocations.
  Preserve other user tabs and their navigation.
- `switch_tab()` attaches without changing the visible tab. Use
  `activate_tab(target_id)` when the user asks to see it or when the page
  demonstrably needs visibility. Read [Tabs](references/tabs.md) and
  [Scrolling](references/interaction-skills/scrolling.md) for these cases.
- After navigation, wait for the load and verify the target URL and page
  state. To act on UI, find the element in the accessibility tree or DOM,
  use fresh bounds for coordinate input, and verify the result. Capture a
  screenshot when visual evidence matters.
- Use the intended signed-in session. Pause for passwords, MFA, consent, or
  ambiguous account selection. Confirm authorization for externally visible
  writes and verify their outcome before retrying.

For an explicitly requested recording, use `BH_RECORD=1` for the relevant
invocations and `browser-harness recordings --latest` to locate the trace.
Use the video reference before exporting or sharing a recording.

## References

Read the relevant note when an action calls for more detail.

- Browser output: [screenshots](references/interaction-skills/screenshots.md),
  [recordings and video](references/interaction-skills/make-video.md),
  [viewport](references/interaction-skills/viewport.md).
- Files: [uploads and downloads](references/files.md).
- Native alerts, confirmations, and prompts: [dialogs](references/interaction-skills/dialogs.md).
