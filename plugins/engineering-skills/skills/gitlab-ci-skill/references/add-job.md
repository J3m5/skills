# Add a job to an existing pipeline

Paths to scripts and references below are relative to the skill directory.

Use this workflow when the repo already has `.gitlab-ci.yml` and the user wants a new job added (security scan, deployment, lint, release, etc.). Do not rewrite the file. Add a focused change that matches the project's existing conventions.

## 2.1 Read the existing config

Read `.gitlab-ci.yml` at the repo root. Then follow every `include:` directive:

- `include: local:` paths: read the referenced files in the repo (typically under `.gitlab/ci/`).
- `include: component:` references: note the component is in use but do not fetch its source. The user's overrides live in their own YAML.
- `include: template:` or `include: remote:`: note for context; you cannot modify them.
- `include: project:`: skip; cross-project includes are outside the local file system.

Build a mental model of the full pipeline by combining the root file and the local includes.

## 2.2 Analyze the project's conventions

Before adding anything, identify how the project already does things. The new job must look like the existing ones.

- **Hidden base jobs** (job names starting with `.`): if `.docker-job`, `.test-base`, or similar exist, the new job almost certainly should `extends:` one of them. Pick the closest match.
- **Stage layout**: read the `stages:` array. Place the new job in an existing stage. Only propose extending `stages:` if no existing stage fits, and call that out as a separate change.
- **Conditional execution style**: if existing jobs use `rules:`, the new job uses `rules:`. If they use `only:` / `except:` (deprecated but still seen), match the existing style for consistency; mention the deprecation as an aside, not a blocker.
- **Default block**: if `default:` covers `image`, `before_script`, `cache`, or `tags`, the new job inherits them automatically. Do not duplicate fields the default already provides.
- **Reuse pattern**: prefer the project's pattern. If the project uses hidden jobs + `extends:`, do that. If the project uses YAML anchors (rarer, less idiomatic), match the anchor style and note the option to migrate later.
- **DAG / `needs:`**: if other jobs declare `needs:`, the new job should too. If the project relies purely on stage ordering, do not introduce `needs:` unless it materially helps.
- **Artifact flow**: see which jobs produce artifacts and which consume them. If the new job needs an upstream artifact, wire `needs: [{ job: <name>, artifacts: true }]` per the project's existing pattern.
- **Naming conventions**: match the existing style (`build`, `build-image`, `test ruby 1/3`, etc.). Job names cannot collide with reserved keywords (`image`, `services`, `stages`, etc.).
- **`workflow:rules:`**: if the project gates pipeline creation, the new job inherits that gating. Do not add `workflow:` here unless the user asks.

## 2.3 Check the CI/CD Catalog

If the new job is a standard task (SAST, container scanning, dependency scanning, secret detection, Terraform / OpenTofu, markdown lint), consult `references/catalog.md` and prefer a GitLab-maintained component. The Catalog component handles details a custom job would have to re-implement (reporter formats, artifact paths, allow-failure, etc.).

If a component fits, add it via `include: component:` pinned to a release tag obtained via `scripts/catalog-search.sh`. If the project already has an `include:` block, add to it; do not create a duplicate include.

## 2.4 Propose the change

Output the change as a diff-style addition, not a full file rewrite:

1. **Summary**: one line stating what the new job does and where it goes (stage, base, rules).
2. **The added YAML**: the new job (and any required `include:` entry or `stages:` extension) as a fenced code block with `+` markers on every added line, mimicking unified diff output. The user can read added lines at a glance.
3. **Wait for confirmation.** Do not write to disk before the user agrees.

Example proposal format:

```diff
  stages:
    - build
    - test
    - deploy
+   - security

+ include:
+   - component: gitlab.com/components/secret-detection/secret-detection@<version>

+ secret-detection:
+   stage: security
```

## 2.5 Apply, show, and verify

When the user approves, write the change to `.gitlab-ci.yml` (or the appropriate included file, per step 2.1). Then run `scripts/verify.sh -f <file> show` and **paste the output verbatim** into your response. The user sees the new job slot into the DAG without re-reading the whole YAML. This paste is mandatory even when the output contains warnings (e.g., `glci: skipping component include ... no GitLab token configured`). A warning is part of the verified state; suppressing it hides what the user needs to see. Paste the full output, then explain what each warning means in one line. The paste must be a fenced code block in your response message text; the Bash tool output alone gets auto-collapsed by the editor and the graph stops being visible.

If verification fails: surface the error, propose a fix to the addition only, re-verify. Do not modify unrelated parts of the file.

After show passes, offer to confirm just the changed piece end-to-end. This is the smoke run for Workflow 2: a single-job execution that catches image/dependency/script issues without paying for a full pipeline replay.

> "I can run only the new job locally to confirm it works: `scripts/verify.sh run <new-job> --reuse-artifacts --confirm-docker`. Reuses cached upstream artifacts; usually 1 to 3 minutes depending on image size and what the new job does."

If Docker is reachable and the user agrees, invoke **via the Monitor tool** (Claude Code) so the user sees streaming output; in editors without Monitor, use `2>&1 | tee /tmp/run.log` and tail the log. Never `| tail -N`, it buffers. If a failure surfaces, apply the classification rules in `references/debugging.md` to label it `[local-timeout]`, `[oom]`, or `[real]` before recommending next steps.

If Docker is not reachable, tell the user what they'd get from the run (and surface the install pointer from verify.sh's output), but do not block; the show output above is honest verification at the structural level.

## 2.6 Ask for commit approval

Show `git diff` of the change and ask before staging. Match the project's existing commit style (look at recent commit subjects via `git log --oneline -10`). Do not push without explicit per-action permission per principle 5.
