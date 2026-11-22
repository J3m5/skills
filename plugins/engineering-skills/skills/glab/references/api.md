## API calls

`glab api` auto-prepends `/api/v4/`. Use relative paths:

```shell
glab api user                              # NOT /api/v4/user
glab api projects/:id/merge_requests
glab api projects/:id/issues | jq '.[0]'
```

### Placeholders

`glab api` expands these built-in tokens in a path, a field value, or inline JSON:

`:branch` `:fullpath` `:group` `:id` `:namespace` `:repo` `:user` `:username`

`:user` and `:username` work anywhere. The rest are read from the current
repository, so they need a Git checkout with a GitLab remote. Outside one, or to
target a different project, supply the value instead:

```shell
glab api projects/:id/issues                    # inside a checkout
glab api projects/:id/issues -R group/project   # any project; placeholder still expands
glab api projects/group%2Fproject/issues        # literal path -- %2F is required
glab api projects/1234/issues                   # numeric project ID
```

To insert any other value, define your own placeholder with
`--placeholder <name>=<value>`. In the path, glab encodes the value as a single
segment, so you don't need to write `%2F` by hand. In `-F` values it is sent
unchanged. For a query string value, pass it as a field with `-X GET -F` rather
than in the path:

```shell
glab api projects/:fullpath/repository/branches/:target --placeholder target=feature/login
glab api projects/:id/issues -X GET -F search=:term --placeholder term='a&b'
```

Anything else beginning with a colon is **not** a placeholder. glab sends it to
the API verbatim, so the request fails at the server rather than in glab.

### Content-type guidance

When using `-f` for PUT/POST, pass simple `key=value` pairs. Array bracket
syntax like `ids[]=1` is not supported:

```shell
# -f / --raw-field — literal string value
glab api projects/:id/merge_requests/42 -X PUT -f "assignee_id=1"
glab api projects/:id/issues/42/notes -f body="comment text"

# -F / --field — reads @file as a string. The leading @ means "read this
# file", so only pass a real path here. A literal body that starts with @
# (e.g. "@user thanks") must NOT go through -F — it would be read as a
# filename. Use -f for literal inline text, or write the body to a file and
# point -F at the file (recommended for rich/markdown bodies).
glab api projects/:id/issues/42/notes -F body=@/tmp/comment.md

# --input — raw request body from a file (or '-' for stdin). Does NOT set
# Content-Type. Without the header, JSON endpoints return HTTP 415.
glab api projects/:id/issues/42/notes \
  --input /tmp/body.json \
  -H "Content-Type: application/json"

# --form — multipart/form-data. Required for endpoints that take a real file
# upload, such as project or group uploads and wiki attachments. -F does not
# do this: it reads the file into a text field, and the endpoint rejects the
# request with HTTP 400.
#
# IMPORTANT: --form is mutually exclusive with -f, -F, and --input. Every
# field in a multipart request must use --form
glab api projects/:id/uploads --method POST --form "file=@screenshot.png"

# Wiki attachment — both fields must use --form
glab api projects/:fullpath/wikis/attachments --method POST \
  --form "file=@screenshot.png" --form "branch=main"
```

### Arrays and nested objects

`-F` / `--field` parses a value that starts with `[` or `{` as JSON, so arrays
and nested objects go inline without a file. Placeholders are expanded inside
the JSON. Invalid JSON returns an error rather than being sent as a string.

```shell
# Array of strings
glab api -X PUT projects/:id -F 'topics=["my-topic","GitLab"]'

# Nested object, with a placeholder expanded inside it
glab api projects/:id/merge_requests/42/discussions -X POST \
  -F body="looks good" \
  -F 'position={"position_type":"text","new_path":"main.go","new_line":42}'

# Empty array clears a field
glab api -X PUT projects/:id -F 'topics=[]'
```

`-f` / `--raw-field` never parses JSON: a bracketed value like
`-f 'scopes=[api,read_api]'` is sent as the literal string. Use `-F` with real
JSON for arrays. On GET and DELETE requests, and whenever `--input` is used,
`-F` arrays are serialized as repeated `key[]=` query parameters.
