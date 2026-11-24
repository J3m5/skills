# Scrolling

Send wheel input over the container that should scroll. Check its scroll
position or the newly visible content before repeating the action.

## Hidden tabs

Start with the normal `scroll(...)` helper. Chrome on Windows can leave a
mouse-wheel command unanswered when the attached tab is hidden. If the
scroll times out and bringing the tab forward is appropriate:

1. Call `activate_tab(current_tab())` so Chrome shows the attached tab.
2. Retry the same `scroll(...)` once.
3. Re-read the page or container scroll position before continuing.

If the task requires the tab to stay in the background and scrolling still
fails, report the exact limitation.
