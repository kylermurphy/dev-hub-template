# repos/

One folder per tracked repo, each holding that repo's **master** instruction file:
`repos/<name>/CLAUDE.md`. `scan-repo <name>` creates it the first time; after that you (or
`scan-repo` / `mark-done`) edit it here, and the task protocol copies it into the target
repo's root as each task's first commit. Never hand-edit the copy inside the target repo.

Empty in a fresh hub. For a filled-in master, see
[`../examples/example-repo/CLAUDE.md`](../examples/example-repo/CLAUDE.md).
