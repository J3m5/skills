## Common mistakes

- **`-m` or piped stdin is required on `note` commands** — with neither,
  `glab mr note create`, `glab issue note`, and `glab incident note` open
  `$EDITOR` on a TTY, which hangs in non-interactive environments.
- **Use `glab mr note create`, not `glab mr note -m`** — the `--message`,
  `--unique`, `--resolve`, and `--unresolve` flags on the root `glab mr note`
  command are deprecated. Use the `create`, `resolve`, and `reopen`
  subcommands instead.
- **Editor-opening flags are unsafe in agent environments** — avoid
  `--description "-"` on `issue create` / `mr create` / `mr update` and
  avoid omitting `-m` on `note` commands. Pass an explicit value or pipe
  from stdin instead.
- **`glab issue note` and `glab incident note` only post root-level
  comments** — use `glab mr note create --reply` for MRs, or
  `glab api .../discussions/<id>/notes` for issues/incidents (write the body
  to a file and pass `-F body=@file` for anything non-trivial).
- **A note with only an attachment needs `</dev/null` in scripts** — when
  stdin is not a terminal, `note` commands read it as the body and wait until
  it closes. Run `glab mr note create <iid> --attach ./shot.png </dev/null`
  so glab neither waits on an open pipe nor consumes a loop's input.
- **`--attach -` uses stdin for the file** — the body must then come from
  `-m`, for example `pngpaste - | glab mr note create <iid> -m "Repro" --attach -`.
- **`-F` does not upload files** — `-F file=@x.png` sends the file contents as
  a string field, and upload endpoints reject it with HTTP 400. Use `--form
  file=@x.png` for multipart uploads. `-F` reads a file only to fill a *text*
  field, such as a note body. Also, `--form` is mutually exclusive with `-f`,
  `-F`, and `--input` — every field in a multipart request must use `--form`
  (e.g. `--form "file=@x.png" --form "branch=main"`).
- **`--input` requires an explicit `Content-Type` header** — `glab api
  --input file.json` sends raw bytes without setting Content-Type, causing
  HTTP 415. Add `-H "Content-Type: application/json"` or use `-f` / `-F`
  instead.
- **`glab ci retry` takes a job ID, not a pipeline ID** — to retry an
  entire pipeline, use `glab api projects/:id/pipelines/<id>/retry -X POST`.
- **`glab ci trace` streams** — it blocks until the job finishes. For
  agents, use `glab ci get` for pipeline state or
  `glab api projects/:id/jobs/<job-id>/trace` to fetch a finished log.
- **`glab ci view` is interactive** — terminal UI that blocks. Use
  `glab ci status` or `glab ci get` for pipeline state instead.
- **Always `--push` on `glab mr create`** — without it the remote branch
  may not exist and MR creation fails.
- **No `--state` on `mr list`** — use `--all`, `--merged`, or `--closed`.
- **No `--body` flag** — `--body` is a `gh` flag. `glab` uses `--description`.
- **Labels** — `--label` to add, `--unlabel` to remove. Scoped labels like
  `status::doing` auto-replace within their scope.
