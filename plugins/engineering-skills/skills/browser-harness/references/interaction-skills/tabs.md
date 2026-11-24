# Tabs

`new_tab(url)` opens a background tab for the task or reuses its blank tab.
Use `current_tab()` to identify the tab you're driving. List existing pages
with `list_tabs(include_chrome=False)`. When selecting a specific existing
tab, pass its full entry to `switch_tab(tab)` so the CLI can detect a URL
change since inspection.

For parallel tasks in the same profile, set a distinct `BH_OWNER` for each
task and reuse it on every invocation. They share the local daemon.
`list_tabs()` reports ownership. If a tab is `taken`, use a tab you own.
If a tab closes or changes, inspect the available tabs again.

Close tabs you opened for the task when they are no longer needed. Keep tabs
the user needs to inspect or use. The target order comes from CDP. Use the
visible browser UI when the user identifies a tab by its position.

If the user asks to see a tab, use `activate_tab(target_id)`. If a screenshot
or scroll stalls while a tab is hidden, visibility can affect rendering.
Activate it and retry once when bringing it forward is appropriate.
