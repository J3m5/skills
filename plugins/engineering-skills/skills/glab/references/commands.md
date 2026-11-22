## Quick reference

```shell
# Issues
glab issue view <iid>
glab issue list --label "bug,priority::1"
glab issue create --title "title" --description-file /tmp/desc.md
glab issue note <iid> -m "comment text"

# Merge requests
glab mr create --push --title "fix: title" --description-file /tmp/desc.md
glab mr view <iid>
glab mr list --assignee <user>
glab mr update <iid> --description-file /tmp/desc.md
glab mr note create <iid> -m "comment text"

# CI/CD
glab ci status
glab ci status --output json
glab ci list
glab ci get --merge-request <iid> --with-job-details
glab ci get --pipeline-id <id> --output json
glab ci retry <job-id>
glab api projects/:id/jobs/<job-id>/trace

# Machine-readable output
glab mr list --output json | jq '.[].title'
```

**Templates:** Check `.gitlab/merge_request_templates/` and
`.gitlab/issue_templates/` for project-specific templates.

**References:** Always use full URLs in note/comment bodies (e.g.
`https://gitlab.com/org/project/-/issues/123`) instead of short references
(`#123`, `!456`). This applies to issues, merge requests, epics, and so on.
Short refs resolve against project context and render as literal text on
group-level items (epics, group work items); full URLs expand everywhere.
