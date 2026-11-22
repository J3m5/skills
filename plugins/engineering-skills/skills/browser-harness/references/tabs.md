# Tab selection and visibility

```python
print(current_tab())
for tab in list_tabs(include_chrome=False):
    print(tab["targetId"], tab.get("url"))
```

- `switch_tab(target_id)` attaches to an existing tab in the background.
  The daemon keeps the attachment across CLI calls. Use `goto_url(url)`
  to navigate within the task's tab.
- `new_tab(url)` can reuse an attached blank tab. To preserve that blank
  tab, call `new_tab()` and then `goto_url(url)` on the new target.
- Screenshots and ordinary CDP input work on the attached background tab.
  `activate_tab(target_id)` makes that tab visible. When a scroll times
  out because the page is hidden, see [Scrolling](interaction-skills/scrolling.md).
- CDP lists targets in its own order. If the user refers to an ordinal
  position in the visible tab strip, inspect the browser UI before choosing
  a target.
- Close tabs only when they were opened for the task or the user authorized
  closing them.
