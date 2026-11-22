# Create initial pipeline

Paths to scripts and references below are relative to the skill directory.

Use this workflow when the user has no `.gitlab-ci.yml` (or asks for a fresh one). Follow the steps in order. Do not skip the user-confirmation step.

## 1.1 Detect the stack

Read package manifests, lockfiles, and project files to identify the language, package manager, and test runner. Common signals:

- `package.json` plus `package-lock.json`, `yarn.lock`, or `pnpm-lock.yaml` for Node.
- `pyproject.toml`, `setup.py`, `requirements.txt`, `poetry.lock`, or `uv.lock` for Python.
- `go.mod` for Go.
- `Gemfile` plus `Gemfile.lock` for Ruby.
- `Cargo.toml` plus `Cargo.lock` for Rust.
- `Dockerfile` at the repo root for Docker.

When multiple signals exist, name the dominant stack and ask the user to confirm. When no signal matches a recipe in `references/recipes.md`, say so and ask the user how to proceed.

## 1.2 Check for an existing `.gitlab-ci.yml`

If the repo already has `.gitlab-ci.yml`, switch to Workflow 2 (Add a job to an existing pipeline). Do not overwrite.

## 1.3 Search the CI/CD Catalog

For jobs that fit a standard task (SAST, container scanning, dependency scanning, secret detection, Terraform / OpenTofu, language-specific test pipelines, markdown lint), check `references/catalog.md` for a GitLab-maintained component before writing a custom job. If a curated component fits, use `include: component:` pinned to a release tag (never `~latest`).

Load `references/catalog.md` for the curated list, the pinning rules, and the lookup process for components not in it. Always fetch the current latest version via `scripts/catalog-search.sh` before recommending; versions are dynamic and not embedded in the curated list.

## 1.4 Propose the plan

Before writing YAML, output a structured proposal:

1. **Detected stack** in one line, with confidence (high / medium / low).
2. **Proposed stages**: `build`, `test`, `deploy` (deploy may be a stub).
3. **Proposed jobs**: a table:

   | Job | Stage | Purpose |
   |---|---|---|
   | (one line per proposed job) | | |

4. **`workflow:rules:` is omitted by default**. Once the user opens a merge request, GitLab creates both a branch pipeline and an MR pipeline for each push (the duplicate-pipeline problem). Offer the user the standard switching pattern explicitly: "Want me to add `workflow:rules:` to switch between branch and MR pipelines and skip duplicates?" Apply only if the user says yes.
5. **Wait for confirmation.** Do not generate YAML before the user agrees.

## 1.5 Generate `.gitlab-ci.yml`

Apply the recipe from `references/recipes.md` for the detected stack. Patterns to apply universally:

- `default:` block for shared fields (`image`, `interruptible`, `cache`, `before_script`).
- Lockfile-keyed cache when a committed lockfile is present; fall back to manifest-keyed cache otherwise (see the variants under each recipe).
- One-line comment per job explaining its purpose.
- Hidden jobs (`.base`) plus `extends:` for reuse. Not YAML anchors.
- `needs: []` on jobs that can start immediately (typically test-stage jobs independent of the build artifact).

Load `references/syntax.md` for keyword lookups and canonical-doc pointers. Load `references/images.md` and `references/caching.md` for image and cache decisions.

## 1.6 Verify and show the pipeline graph

Run `scripts/verify.sh auto`. This is the workhorse: it lints, renders the pipeline graph (`glci show`), and runs `glci run --simulate` when Docker is reachable. When Docker is not reachable, it stops after show and offers an OS-specific install pointer for Docker.

**Paste the `glci show` output verbatim as a fenced code block in your response message text** (not the Bash tool output, which auto-collapses), then present the YAML below it. The ASCII pipeline graph is usually clearer than 50 lines of YAML; treat it as the headline artifact, not as a side-effect of verification. If simulate also ran, paste its summary too.

On the first invocation in a conversation, prefix with one line of context: "Using glci (offline GitLab CI runner) to render the pipeline graph." Skip on subsequent calls.

On failure: read the error. Exit 1 means a YAML problem (surface the error, propose a fix, re-verify). Exit 2 means an environment problem (verify.sh reports what is missing). If glci is missing, verify.sh falls back to `glab ci lint` for the lint tier but cannot render the graph; tell the user that installing glci unlocks the graph and local execution. See `references/verification.md` for recovery paths.

## 1.7 Offer real execution (run tier): smoke first, full second

`auto` already covers lint, show, and simulate. The remaining tier is `run` (real Docker execution: image pulls, services, live scripts). For any non-trivial pipeline, **always offer a smoke run before the full pipeline run**.

**Step 1: offer the smoke run.** Pick one job to run end-to-end as a smoke check. Default order:

1. `build` if present (fast, validates image + dependencies + build script).
2. Otherwise the first job in the first non-`.pre` stage.
3. For matrix jobs, pick a single canonical entry (e.g., the highest Python version, not the lowest).

Phrasing:

> "Want me to run one job end-to-end first as a smoke check? I'll pick `build` (or `test [3.13]` for matrix jobs). Takes 1 to 3 minutes; confirms the image pulls, dependencies install, and the script runs cleanly. If it passes, I'll offer the full pipeline run."

If they agree, invoke `scripts/verify.sh run <job> --reuse-artifacts --confirm-docker` **via the Monitor tool** (Claude Code) so the user sees streaming output. In editors without Monitor, run `scripts/verify.sh run <job> --reuse-artifacts --confirm-docker 2>&1 | tee /tmp/run.log` and tail the log in a separate process. **Never pipe through `tail -N`**: it buffers until pipe close, hiding all progress for the duration of the run.

**Step 2: offer the full run if smoke passes.** Be honest about variance:

> "Smoke passed. Want me to run the full pipeline? Simple pipelines take a few minutes; matrix-heavy pipelines (say, 5+ Python versions plus style/typing/docs) can take 20+ minutes and stress local Docker (memory, CPU, image-pull contention). I'll stream progress live and classify any failures as `[local-timeout]`, `[oom]`, or `[real]` at the end so you can triage at a glance. GitLab.com runners will run the same matrix in parallel without these constraints."

If they agree, run `scripts/verify.sh run --confirm-docker` via Monitor (or tee + tail). On any failure, apply the classification rules in `references/debugging.md` ("Classifying failures from verify.sh run") and surface a per-job tag in your summary. Then switch to Workflow 3 (Debug) for any `[real]` failure.

## 1.8 Handle the onboarding handoff

Run `git remote -v` to detect whether a GitLab remote exists.

- If yes: tell the user the `.gitlab-ci.yml` is ready to commit and push. Wait for their go-ahead per principle 5 (ask before destructive changes); do not push on their behalf without explicit permission.
- If no: hand off to Workflow 5 (Onboarding). Load `references/onboarding.md` for the full walkthrough.
