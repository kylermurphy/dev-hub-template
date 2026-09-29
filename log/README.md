# log/

One markdown file per dev-hub task, named `<TASK-ID>.md` (e.g. `EX-1.md`), created from
`TEMPLATE.md`. This is dev-hub's **own, independent** record of what each task did — it does
not depend on a GitHub PR staying open, or on any chat or Claude Code session history.

Each log carries the task's **Status** (`WIP` · `Blocked` · `Usage-stopped` · `Done`,
mirroring the board, which adds an icon to each), its **Plan** (saved by `plan-task` before
heavy work), Checklist, **Next step** (what `pickup-task` resumes from), **Blocked / open
questions**, and notes
(`Learning:` lines are promoted into the repo master's `## Learnings` by `mark-done`). Task
bookkeeping here is committed straight to `main`, or to a PR from the designated branch in a
branch-restricted session (see `../CLAUDE.md` → Branch-restricted sessions). Only `mark-done`
sets `Done`.

Tasks done together by `multi-task` (a **batch**) keep one log each; their `Batch:` lines
name each other, the shared branch and the shared PR.

A **feature** (`../FEATURE_BOARD.md`) has one log, `<feature ID>.md` (e.g. `EX-FA.md`), with a
checklist item per subtask; subtasks have no logs of their own.

`../TASK_LOG.md` is the running index across all tasks and features.
