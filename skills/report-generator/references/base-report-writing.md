# Base Report Writing

Use this reference when writing or updating the Markdown report.

## Goal

Produce a final report, not an audit trail of how the report evolved.

## Structure

Recommended structure:

- frontmatter with `title` and `subtitle`
- `## Synthèse`
- one `## ...` section per major topic, finding, workstream, or chapter
- within each section, use only the blocks that fit the document:
  - `### Problème`
  - `### Conclusion`
  - `### Constats`
  - `### Analyse`
  - `### Recommandation`

## Writing Rules

- Write in French unless the user asks otherwise.
- State conclusions directly and cleanly.
- Do not mention previous report versions, draft states, or historical phrasing.
- Do not narrate the investigation process inside the report.
- Keep the report readable for a human reviewer who only sees the final document.

## Evidence Rules

- Base each conclusion on current code evidence.
- If the code proves a cause, say so plainly.
- If the code proves only part of the problem, keep the unresolved part narrow.
- Avoid hedging when the cause is directly visible in code.

## Synthesis Rules

The synthesis must be faster to scan than the detailed sections.

For each synthesis entry:

- show the section title
- show the source of the problem or observation clearly when relevant
- put the explanation on a separate line

Good source labels:

- `Front-end`
- `API`
- `Mixte`
- `Contrat front/API non aligné`

## Tone

- factual
- concise
- decisive when evidence exists
- no historical commentary about the report itself
