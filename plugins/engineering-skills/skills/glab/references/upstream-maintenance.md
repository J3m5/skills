## Contributing improvements

This skill ships inside `glab`. Its front matter records where it is
maintained: `metadata.source-project` and `metadata.source-path`.

If any guidance here is inaccurate or outdated, such as a command that no
longer works, a wrong flag, or incorrect API behavior:

1. Use `glab api` to read the file `<source-path>/SKILL.md` in
   `source-project` on `main`. If the issue is already fixed there, use that
   guidance instead of opening another merge request.
2. After a release with the fix, upgrade `glab`. Refresh your copy:
   - `glab skills get glab`: the upgraded binary already has it.
   - Installed with `glab skills install` (project or user): a copy is
     glab-installed only if its front matter has `source-project` set to
     `gitlab-org/cli`. If every `glab/` in both locations is glab-installed,
     run `glab skills update glab` from the project. It replaces all of them.
     Otherwise, refresh only the glab-installed ones with
     `glab skills install glab --force` from that project (add `--global`
     for the user location). Ask the user about any copy without
     `source-project`.
   - Installed with `--path`: run
     `glab skills install glab --path <parent-dir> --force`.
   - Third-party copy: refresh it at its source.
3. If the problem is still present on `main`, confirm with the user, then open
   a merge request against `source-project` with the fix. Keep changes
   focused: one fix per merge request, with a Conventional Commits message.
