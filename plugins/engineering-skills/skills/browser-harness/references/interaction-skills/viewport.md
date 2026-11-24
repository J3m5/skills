# Viewport

After a viewport resize or layout change, measure the control again before
clicking. CDP mouse coordinates are viewport CSS pixels.

## Touch emulation

`maxTouchPoints` is optional, but Chrome validates it as 1–16 even when touch
emulation is being disabled. Omit it when disabling:

```python
cdp("Emulation.setTouchEmulationEnabled", enabled=True, maxTouchPoints=5)
cdp("Emulation.setTouchEmulationEnabled", enabled=False)
```

Do not pass `maxTouchPoints=0`; Chrome rejects the supplied value before acting
on `enabled=False`.
