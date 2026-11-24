---
name: modern-web-guidance
description: Consult the Modern Web Guidance catalog for modern HTML, CSS, and browser API patterns, including accessibility, performance, and browser fallbacks. Use when explicitly invoked for frontend implementation, review, or modernization.
---

# Modern Web Guidance

Use the upstream CLI with Node.js 22 or newer. Set `DISABLE_TELEMETRY=1` on
every invocation.

Search for the specific web capability in a short English phrase. Retrieve
the relevant guide IDs from the results.

```sh
DISABLE_TELEMETRY=1 npx --yes modern-web-guidance@latest search "confirmation modal dialog"
DISABLE_TELEMETRY=1 npx --yes modern-web-guidance@latest retrieve dialog
```

Apply the guidance within the project's browser support policy and existing
design. Keep relevant fallbacks for browsers the project supports. Verify the
result against the guide and the requested behavior.

For a requested codebase-wide modernization audit, run the scanner from the
project root. Check the findings against their guide and the code's context
before proposing or making changes.

```sh
DISABLE_TELEMETRY=1 npx --yes modern-web-guidance@latest legacy-scan . --json
```
