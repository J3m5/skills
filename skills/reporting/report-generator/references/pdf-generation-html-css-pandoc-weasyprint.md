# PDF Generation With HTML CSS Pandoc WeasyPrint

Use this reference when regenerating the styled report deliverables.

## Goal

Generate a clean HTML intermediate and a final PDF from a Markdown report.

## Files

Typical files:

- report source: `report.md`
- stylesheet: `report.css`
- generated HTML: `report.html`
- generated PDF: `report.pdf`

## Process

1. Update the Markdown report.

2. Update the CSS when layout or readability changes are required.

3. Format the repository if required by local instructions.
   In this repository, run:

```bash
npm run format
```

4. Generate HTML with Pandoc.

```bash
pandoc report.md -s -c report.css -o report.html
```

5. Generate PDF with Pandoc and WeasyPrint.

```bash
pandoc report.md \
  --standalone \
  --css=report.css \
  --pdf-engine=/ABSOLUTE/PATH/TO/weasyprint \
  -o report.pdf
```

Run these steps sequentially. Do not start PDF generation before HTML generation has completed when you are also producing an intermediate `.html` file for inspection.

6. Review the rendered output.

- Review the generated PDF before delivery.
- Open or inspect the generated HTML only when the layout is being adjusted or when debugging a rendering issue.
- Check at minimum the first page, title/subtitle block, section headings, page breaks, summary layout, and any repeated section rendering.
- If the user reported a layout issue, inspect exactly the affected page instead of relying only on file timestamps.
- Once a first render has been reviewed and validated, do not redo a full visual review for every minor regeneration. Repeat the full review only if the template, CSS, metadata, or structured input changed in a way that could alter the layout.

Recommended installation with `mise`:

```bash
mise use -g pipx:weasyprint
```

`mise` documents Python CLIs through the `pipx` backend. If `uv` is installed on the machine, that backend may use `uv` internally.

Use `mise which weasyprint` to get the exact binary path if `pandoc` does not see it on `PATH`.

Example:

```bash
pandoc report.md \
  --standalone \
  --css=report.css \
  --pdf-engine="$(mise which weasyprint)" \
  -o report.pdf
```

Then review the output:

```bash
pdftotext report.pdf - | sed -n '1,40p'
```

## Generic Template Mode

For reusable rendering pipelines, use the bundled assets:

- `assets/templates/report-template.html`
- `assets/templates/report-template.css`
- `assets/templates/report-example.md`

The template is driven by a generic `sections` variable.

Example:

```bash
pandoc assets/templates/report-example.md \
  --template=assets/templates/report-template.html \
  --css=assets/templates/report-template.css \
  -o report.html
```

Then:

```bash
pandoc assets/templates/report-example.md \
  --standalone \
  --template=assets/templates/report-template.html \
  --css=assets/templates/report-template.css \
  --pdf-engine=/ABSOLUTE/PATH/TO/weasyprint \
  -o report.pdf
```

You can still generate the intermediate HTML separately when you want to inspect or tweak the layout before exporting the PDF.

Review both artifacts after generation:

```bash
pdftotext report.pdf - | sed -n '1,40p'
```

## Chromium Fallback

Use Chromium only when you need browser-print parity or when comparing a rendering issue against a real browser engine.

```bash
chromium --headless --disable-gpu \
  --no-pdf-header-footer \
  --print-to-pdf=report.pdf \
  file:///ABSOLUTE/PATH/report.html
```

Important:

- Do not run the Chromium export in parallel with the Pandoc HTML generation.
- Always use `--no-pdf-header-footer`.
- Always use an absolute `file://` URL.
- If the generated PDF is unexpectedly tiny or only one page long, inspect it for a browser error page before trusting it.

## Structured Data Model

Use `sections` as the repeated top-level collection.

Typical shape:

```yaml
---
title: Rapport
subtitle: Exemple
sections:
  - title: Contexte
    summary_title: Besoin principal
    summary_source: Dossier source
    summary_text: Le projet vise une refonte progressive avec contraintes d'intégration et d'accessibilité.
    blocks:
      - heading: Synthèse
        body: Le périmètre prioritaire doit être clarifié avant la phase de livraison.
      - heading: Points clés
        items:
          - Le besoin couvre plusieurs canaux de diffusion.
          - La contrainte de compatibilité est structurante.
---
```

## Layout Guidance

- Keep the synthesis easy to scan.
- Make issue source labels visually distinct.
- Prefer short section titles and stable typographic hierarchy.
- Fix line breaks in Markdown first, then in CSS.
- When Pandoc list layout is unstable, use small HTML wrappers inside Markdown for predictable blocks.
- Prefer the generic `sections` template when repeated report blocks must stay structurally uniform across many reports.

## Verification

After generation:

- confirm HTML was rewritten
- confirm the PDF file was rewritten
- perform a render review of the PDF, not only a file existence check
- if Chromium was used, extract text from the PDF and confirm it does not contain `ERR_FILE_NOT_FOUND`, a `file:///` path, or browser header/footer text
- verify the subtitle is intentional and not a leftover generation note
- inspect the first page or screenshot if the user reports layout problems

When a previous render has already been reviewed and approved:

- keep a lighter verification pass for minor content-only updates
- repeat a full render review only after major changes to the template, CSS, metadata, section structure, or other data that may affect layout

Useful verification command:

```bash
pdftotext report.pdf - | sed -n '1,40p'
```

Common failure modes seen in practice:

- Chromium export started before the HTML file existed, producing a PDF that only contains `ERR_FILE_NOT_FOUND`.
- Chromium exported browser chrome into the PDF because `--no-pdf-header-footer` was omitted.
- A generic subtitle such as a workflow note was injected through Pandoc metadata and appeared in the final deliverable.
- `pandoc` could not find `weasyprint` on `PATH`, while `mise which weasyprint` returned a valid binary path.
