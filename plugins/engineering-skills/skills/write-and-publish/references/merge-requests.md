# PR/MR descriptions

Write for reviewers who have not read the conversation. Explain the concrete
problem, resulting behavior, useful validation, and remaining uncertainty.
Use section headings and lists to make those points easy to scan. Scale each
section to the change rather than filling a long fixed template.

## Section order

For French descriptions, use this order. Adapt the language or a required
repository template while keeping associated links immediately after context.

1. **Contexte**: explain the trigger or problem and the resulting behavior in
   one short paragraph. A concrete before/after example helps when needed.
2. **Liens associés**: list the primary ticket or issue, relevant related
   tickets, and PRs/MRs as bullets with clickable full URLs, regardless of the
   tracking tool. Briefly explain each link's relationship to this change.
   Include verified dependencies, complementary changes (including in other
   repositories), and PRs/MRs this change completes or replaces, even when the
   ticket does not reference them. Select links useful to the review rather
   than automatically copying every reference from the ticket. Do not invent
   relationships or link the PR/MR being described. Omit the section when no
   relevant ticket, issue, or PR/MR is associated.
3. **Changements**: use bullets for parallel changes, each explaining observable
   behavior or a meaningful implementation choice. Avoid a file-by-file diff
   summary and generic claims such as "improved robustness".
4. **Validation**: summarize useful results in one short sentence or a few
   bullets. Focus on the changed behavior and representative scenarios. Group
   routine lint, type and formatting checks rather than listing each command.
   Omit test file inventories, logs, counts and coverage percentages unless they
   help assess the changed behavior or a material risk, or the user requests
   that detail. State the scope only when it changes how the reviewer should
   interpret the result.
5. **Points restant à valider**: include this section only for material pending
   checks or unresolved uncertainty. Use `- [ ]` for concrete remaining checks.
   Describe known limitations directly when they are not checklist tasks.

Keep a blank line between headings and their content. Use prose or ordinary
bullets for completed validation. Reserve checklists for concrete follow-up
checks or a required repository template. Report success only when supported
by evidence, not because it is expected or another environment passed. Omit
validation that only repeats the PR/MR UI, and do not invent pending tasks.

## Evidence suited to the change

Include evidence that helps reviewers judge the affected behavior without
repeating the author's investigation. Scale it to the change and place it next
to the claim it supports, within the existing sections.

- For visual changes, use comparable screenshots (same element, viewport and
  crop), or a short video when interaction matters. Follow repository requirements.
  For a user-flow capture, retain the relevant application layout and show the
  states needed to judge the changed behavior. Refresh affected captures after the
  final UI or copy changes, so the evidence matches the submitted revision.
- For a bug or CLI change, show a representative input or command and its actual
  result. For an API or feature, an example of how to use it may be more useful.
- Support performance claims with measurements, relevant conditions and variation
  across runs. Distinguish measured results from estimates.
- For before/after evidence, identify the compared revisions or environments when
  needed to interpret the result. Use an authentic baseline and account for other
  differences that could affect the comparison.
- A test passing after a fix does not establish that it failed before. State
  whether that failure was observed when claiming regression evidence.
- Inspect each capture and verify attachment links before publication. Use demo
  or sanitised data and remove sensitive content from captures and output.
- For an MR with a single screenshot, show it directly in the screenshots section
  without a table or a `<details>` block.
- For an MR with multiple screenshots, put one Markdown table in that section.
  Wrap the whole table in a single collapsed `<details>` block with a descriptive
  `<summary>`. Leave a blank line before and after the table so GitLab renders it.
  Use one row per view or state and place desktop and mobile captures side by
  side when applicable. Leave a cell empty if that capture is unavailable.

## Content boundaries

- Describe the final change. Rewrite stale titles or descriptions when the user
  requests an update after scope changes. Omit abandoned approaches unless they
  explain a tradeoff reviewers need to assess.
- Do not repeat information already available in the PR/MR UI, such as CI status.
  Include only validation details or limitations that add useful review context.

- Do not mention AI involvement unless the author explicitly requests it.
- Keep local delivery tooling, agent coordination, review counts, and temporary
  artifact paths out of the description unless they materially affect the review.
- This format guides drafting. An already approved body remains authoritative:
  do not reformat it at publication time without a requested edit or approval
  of the revised text. Apply the shared publication rules in `SKILL.md`.
