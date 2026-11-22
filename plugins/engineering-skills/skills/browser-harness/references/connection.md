# Connection and troubleshooting

- Install the Browser Harness CLI using the [upstream project](https://github.com/browser-use/browser-harness). In a mise-managed environment, use the configured tool and wrapper.
- Run `browser-harness --doctor` when the daemon cannot connect. For an
  explicitly selected CDP endpoint, use `BU_CDP_URL` or `BU_CDP_WS`.
- If local Chrome or Chromium is running and remote debugging is disabled,
  have the user enable it at `chrome://inspect/#remote-debugging`. If the
  browser shows a permission popup, wait for the user to click Allow before
  retrying. Repeated attach attempts can produce repeated popups.
- Chrome can expose internal pages or the omnibox popup as CDP targets.
  Inspect the tab list and use `switch_tab()` to attach to the intended
  page. Use `ensure_real_tab()` to recover from an internal or invisible
  target when an existing real tab is suitable for the task.
- In a local wrapper configuration, `BH_CHROME_PATH` can select a specific
  Chrome or Chromium executable. Use the active desktop's window controls
  when the user explicitly needs the browser window brought to the front.
