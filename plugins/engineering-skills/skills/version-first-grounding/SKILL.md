---
name: version-first-grounding
description: Ground technical work in the effective software, service, API, framework, tool, or documentation version when version differences may materially change behavior, compatibility, diagnosis, implementation, or upgrade decisions. Use when the active version is uncertain, local and deployed versions may differ, version-matched evidence is needed, a compatibility issue is suspected, or the user asks whether to adapt or upgrade.
---

# Version-First Grounding

Ground only the version-sensitive part of the task. Preserve the user's explicit
target and requested action level; version grounding does not authorize an
upgrade, implementation, or documentation change by itself.

## Route By Intent

1. Identify the claim or decision that may vary by version. If version cannot
   materially affect it, continue the broader task without the full workflow.
2. Classify the intent:
   - current behavior: establish the effective version and use matching evidence
   - compatibility diagnosis: establish every relevant component version and
     support relationship
   - upgrade decision: compare the current version with viable target versions
3. Record any explicit target as a constraint and preserve it instead of
   substituting `latest`.

## Establish The Effective Version

1. Identify the version surface that governs the behavior under investigation.
2. Use the strongest available evidence, such as runtime output, deployed
   revision, image digest, resolved lockfile, installed package metadata,
   release tag, API version or date, or vendored snapshot identity.
3. Distinguish declared, resolved, installed, running, and deployed versions
   when a mismatch between them could matter.
4. If no exact identity is available, record what is known and the uncertainty.
   Continue read-only analysis when bounded uncertainty is sufficient; stop
   before a change when the missing identity could alter the implementation.

## Match Evidence To The Version

1. Prefer runtime and local artifact evidence for what is actually in use.
2. Prefer versioned primary material: official docs, tagged source, release
   notes, compatibility matrices, and migration guides matching that identity.
3. Treat `main`, latest docs, and current examples as potentially incompatible
   until their alignment with the effective version is established.
4. Compare newer releases only when it helps diagnose the issue, evaluate
   support, or answer an upgrade question.
5. Separate current-version behavior, behavior introduced later, and unsupported
   version combinations.

## Decide And Act

Before planning compatibility changes for a dependency upgrade, establish its
actual runtime, build, test, or tooling consumers. Include related type packages
and peer dependencies in the compatibility check when they govern those
consumers.

1. Adapt to the selected target when it is intentionally pinned or upgrade cost
   is outside the request.
2. Recommend an upgrade only when it is in scope and evidence shows a material
   benefit, required support path, or relevant upstream fix.
3. Report unsupported combinations. Stop before mutation only when the mismatch
   or uncertainty could change the design; otherwise continue with bounded
   conclusions.
4. Implement only when requested, against the selected target's real contract.
   Avoid workarounds based on behavior from another version line.

## Verify And Report

1. Re-check the relevant local or deployed behavior against the selected target.
2. When a claim can be checked cheaply, prefer a small empirical comparison
   across the relevant environments over argument by analogy.
3. Update version-sensitive documentation only after confirming the behavior.
4. Integrate grounding into the broader answer instead of forcing a standalone
   report. Include only the material version evidence, compatibility delta,
   decision when needed, performed or proposed action, and remaining uncertainty
   or migration risk.

## Guardrails

- Do not assume that declared, installed, deployed, and latest versions match.
- Do not mix evidence from different version lines without identifying it.
- Do not present version-specific behavior as a timeless general rule.
- Re-test defensive compatibility logic before preserving or removing it.
