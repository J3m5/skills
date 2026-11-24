---
name: browser-harness
description: Control a local Chrome or Chromium browser through Browser Harness for UI interaction, signed-in sessions, screenshots, and browser uploads or downloads. Use web or fetch tools for ordinary public page retrieval.
---

# Browser Harness

Send Python to the CLI on standard input. The browser helpers are preloaded.
Use a Bash here-string for a quick command.

```bash
browser-harness <<< 'print(current_tab())'
```

Use a quoted heredoc for several lines or `browser-harness < script.py` for
an existing program. The first browser call starts the daemon. If the CLI is
missing or the browser fails to connect, see [Connection](references/interaction-skills/connection.md).

## Work in the browser

1. Use `new_tab(url)` to start work on a page. The daemon remembers the
   current tab across calls. To work in a specific existing tab, find it
   with `list_tabs(include_chrome=False)` and pass the matching tab to
   `switch_tab(tab)`. See [Tabs](references/interaction-skills/tabs.md) for
   parallel tasks and visibility.
2. Verify the URL after navigation. For dynamic content, check the result of
   `wait_for_element(selector, timeout=10, visible=True)`.
3. Find the control with `js(...)` or `cdp("Accessibility.getFullAXTree")`.
   Use `fill_input(selector, text)` for text. For a coordinate click, get
   fresh viewport coordinates and call `click_at_xy(x, y)`. Verify the
   expected state before continuing or retrying an action.
4. Use the intended signed-in session. Pause for passwords, MFA, consent,
   or ambiguous account selection.

## References

- For visual evidence or input geometry, see [Screenshots](references/interaction-skills/screenshots.md),
  [Scrolling](references/interaction-skills/scrolling.md), and [Viewport](references/interaction-skills/viewport.md).
- For a native browser prompt, see [Dialogs](references/interaction-skills/dialogs.md).
- For file transfer, see [Uploads and downloads](references/files.md).
- For an explicitly requested recording or video, see [Recordings and video](references/interaction-skills/make-video.md).
