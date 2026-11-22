---
name: report-generator
description: Generate or update a structured report from source material, then publish HTML/PDF deliverables. Use when the user asks to review a report file, analyze source inputs, write a structured report, or regenerate a styled PDF report with Pandoc and WeasyPrint.
---

# Report Generator

## Overview

Produce a final structured report from source material, then generate the HTML and PDF deliverables. Follow the current workflow used in this repository: source review, report writing, styling, and PDF export. Prefer `pandoc + weasyprint` for PDF generation. Keep `chromium` as a fallback when a browser-print rendering is specifically needed. When the user wants an industrialized or reusable rendering pipeline, use the generic Pandoc assets in `assets/templates/`.

## Workflow

1. Identify the report inputs.
   Determine the report source file and whether the relevant material is already documented locally or must be gathered from external sources.

2. Gather and review the source material.
   Read the local Markdown file, notes, or structured data first. If information must be collected from elsewhere, gather only what is needed for the report.

3. Investigate supporting material as needed.
   Validate reported problems, claims, or requirements against the available source material and codebases when the report depends on technical confirmation.

4. Write or update the base report.
   Read [references/base-report-writing.md](./references/base-report-writing.md).
   Keep the report final-form: no drafting history, no references to previous report versions, and no speculative attribution unless clearly marked as such.

5. Generate deliverables.
   Read [references/pdf-generation-html-css-pandoc-weasyprint.md](./references/pdf-generation-html-css-pandoc-weasyprint.md).
   Regenerate the HTML and PDF after content or CSS changes.

6. Review the rendered output.
   Inspect the generated PDF before considering the task complete. Use the HTML as an inspection artifact only when layout debugging is needed. Check the first page, title/subtitle area, section hierarchy, page breaks, and any synthesis block or repeated section layout. Once a first render has been reviewed and validated, do not repeat a full render review on every regeneration unless the template or the input data changed in a major way that could alter the layout.

7. Use the generic template assets when the user wants reusable rendering.
   Use `assets/templates/report-template.html` and `assets/templates/report-template.css` with a metadata model based on `sections`.
   Use `assets/templates/report-example.md` as the example input shape.

## Report Rules

- Prefer current code evidence over ticket commentary or historical notes.
- Separate source attribution clearly: `Front-end`, `API`, `Mixte`, or `Contrat front/API non aligné`.
- State causes as final conclusions only when supported by code.
- Keep unresolved points narrow and explicit.
- When reviewing an existing report, fix outdated conclusions instead of appending historical commentary.
- For synthesis sections, make the source of the problem immediately identifiable and visually separate from the explanation.

## Repository Pattern

In this repository family, the usual pattern is:

- report source in a Markdown file such as `report.md`
- optional related repositories such as a front-end worktree or sibling API repository
- deliverables regenerated as:
  - `<report>.md`
  - `<report>.html`
  - `<report>.pdf`

## PDF Engine Policy

- Default to `pandoc + weasyprint` for report PDFs.
- Install `weasyprint` with `mise use -g pipx:weasyprint` when needed.
- `mise` documents Python CLIs through the `pipx` backend; if `uv` is installed on the machine, that backend can use `uv` internally.
- Keep `chromium` as a fallback for browser-print parity or when a rendering discrepancy must be compared against a real browser engine.

## Hardening Rules

- Never launch HTML generation and PDF export in parallel. Generate the HTML first, then export the PDF.
- When using `chromium`, always pass `--no-pdf-header-footer` to avoid leaking the local `file://` path, browser title, date, and default page counter into the PDF.
- After any Chromium export, verify that the PDF is not just a browser error page such as `ERR_FILE_NOT_FOUND`.
- Treat `subtitle` as intentional report content. Do not inject a generic workflow subtitle unless the user asked for one.
- Prefer explicit binary discovery for `weasyprint` with `mise which weasyprint` when `pandoc` cannot find it on `PATH`.
- When the user asks for reusable rendering, keep the data model generic (`sections`) and avoid report-specific names in the template contract.
- Do not treat file generation as sufficient verification. A render review is a required step of the workflow.
- After an initial validated render, a lighter verification pass is enough for minor content-only regenerations. Repeat a full render review only after major template, CSS, metadata, or repeated-structure changes.

## Generic Templating Mode

Use the generic assets when the user wants to industrialize the rendering instead of hand-authoring every section in Markdown.

The reusable data model should be based on `sections`, not `issues`.
Each section can contain:

- `title`
- `summary_title`
- `summary_source`
- `summary_text`
- `blocks`

Each `blocks` item can contain:

- `heading`
- `body`
- `items`

This keeps the template reusable for audit reports, analysis reports, migration reports, status reports, or any document split into repeated sections.

## References

- Base report writing:
  [references/base-report-writing.md](./references/base-report-writing.md)
- HTML/CSS/PDF generation:
  [references/pdf-generation-html-css-pandoc-weasyprint.md](./references/pdf-generation-html-css-pandoc-weasyprint.md)

## Assets

- Generic Pandoc HTML template:
  [assets/templates/report-template.html](./assets/templates/report-template.html)
- Generic report stylesheet:
  [assets/templates/report-template.css](./assets/templates/report-template.css)
- Example structured Markdown input:
  [assets/templates/report-example.md](./assets/templates/report-example.md)
