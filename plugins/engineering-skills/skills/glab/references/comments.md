## Comments and discussions

Use the `mr note` subcommands (`create`, `resolve`, `reopen`); flags on the
root `glab mr note` command are deprecated.

### Short, inline bodies — pass `-m`

```shell
glab issue note        <iid> -m "comment text"
glab mr note create    <iid> -m "comment text"
glab incident note     <iid> -m "comment text"

# Cross-project
glab mr note create <iid> -m "..." --repo group/project
```

### Long or Markdown bodies — pipe to stdin

`glab mr note create`, `glab mr note update`, `glab mr note draft create`,
`glab mr note draft update`, `glab issue note`, and `glab incident note` read
the body from stdin when `-m` is omitted and the input is a pipe. This avoids
shell-quoting pitfalls (backticks, `$`, backslashes, apostrophes) and is the
safest pattern for non-interactive use. A piped body also works with
`--attach <file>`: the attachment links are added after the body.

```shell
# From a file
glab mr note create <iid> < /tmp/body.md

# Inline literal multi-line body — quoted heredoc, no shell expansion inside
glab mr note create <iid> << 'EOF'
Your **markdown** comment.
Code blocks and `inline code`, $variables, and \backslashes are all literal.
EOF

glab issue note <iid> << 'EOF'
It's the same for issues and incidents.
EOF

# Body from a file, with a screenshot attached after it
glab mr note create <iid> --attach ./screenshot.png < /tmp/body.md
```

For descriptions on `glab issue create` / `glab issue update` /
`glab mr create` / `glab mr update` / `glab work-items create` /
`glab work-items update`, pass `--description-file`. A path of `-` reads
from stdin, so a quoted heredoc works directly:

```shell
glab mr create --push --title "fix: title" --description-file - << 'EOF'
## What does this MR do?

It's a fix for `foo`.
EOF

glab mr update <iid> --description-file /tmp/desc.md
```

Do not nest a heredoc inside command substitution, such as
`--description "$(cat << 'EOF' ... EOF)"` or `-m "$(cat << 'EOF' ... EOF)"`.
The default `/bin/bash` on macOS is bash 3.2, which fails with
`unexpected EOF while looking for matching ''` when the body contains an
apostrophe. Feed the heredoc to `--description-file -` or to stdin instead.

### Threaded replies on merge requests

`glab mr note create` supports `--reply <discussion-id>` for replying inside
an MR thread. The value can be the full discussion ID or a unique prefix of
at least 8 characters.

Diff comments accept a single line (`--line 42`), a range (`--line 10:15`),
a removed line (`--old-line 7`), or no line for a file-level comment.

```shell
glab mr note create  <iid> --reply <discussion-id> -m "I agree!"
glab mr note create  <iid> --file main.go --line 42 -m "Needs refactoring"
glab mr note create  <iid> --file main.go --line 10:15 -m "Extract this block"
glab mr note create  <iid> --file main.go --old-line 7 -m "Why was this removed?"
glab mr note create  <iid> --file main.go -m "General comment on this file"
glab mr note create  <iid> -m "LGTM" --unique    # idempotent: skip if same body exists
```

`glab mr note resolve` / `reopen` take the MR identifier followed by the
discussion identifier. The identifier can be a discussion ID (full 40-char
hex or 8+ char prefix) or a note ID (integer; the parent discussion is
looked up automatically):

```shell
glab mr note resolve <iid> <discussion-id>
glab mr note resolve <iid> <note-id>           # integer note ID also works
glab mr note reopen  <iid> <discussion-id>
```

### Threaded replies on issues, incidents, and work items

The CLI does not wrap threaded replies for these, so you fall back to
`glab api`. **For any non-trivial body, write it to a file and post the file**
rather than inlining rich Markdown — inlined backticks, `$`, newlines, and a
leading `@` all break (see [Content-type guidance](api.md#content-type-guidance)):

```shell
# Discover the discussion ID
glab api projects/:id/issues/<iid>/discussions \
  | jq '.[] | {id, body: .notes[0].body}'

# Build the body in a file, then post it with -F body=@file
cat > /tmp/reply.md << 'EOF'
@user — here's the result, with `code`, a $variable, and an emoji ✅.
EOF
glab api projects/:id/issues/<iid>/discussions/<discussion-id>/notes \
  -F body=@/tmp/reply.md
```

For a short, plain reply you can still inline it with `-f body="reply text"`.
