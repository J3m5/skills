# QA/product handoffs

Use this guide for a requested QA/product comment or handoff. Do not create one
automatically while drafting an MR description or completing implementation.

- Describe what QA can observe: visible labels, available or disabled controls,
  values during a connection loss, and behavior as the system recovers.
- When posting on the ticket or issue, do not simply repeat changes or acceptance
  criteria already described there. Add useful verification details, findings,
  or remaining limitations instead.
- Preserve useful expected states, transitions, and failure cases when shortening
  the message. Do not reduce it to a vague request to test the feature. Bullets
  or a checklist help when there are several independent scenarios.
- Omit protocol names, subscription failures, and request races unless QA needs
  them to reproduce or diagnose behavior. Explain their visible consequences.
- Explain a remaining failure through its verified trigger and observable
  consequence, including a stopping threshold when it matters to QA. Separate
  that mechanism from an unconfirmed cause of the original incident.
- Say which part of the ticket is fixed and which remains open. Do not present
  an "il faut…" workaround as the solution to an unresolved acceptance criterion.

Apply the shared publication rules in `SKILL.md`. Authorization to draft a
handoff alone does not authorize publishing it on the ticket.
