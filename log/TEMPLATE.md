# <TASK-ID> — <short title>

- **Repo:** <target repo>
- **Branch:** `task/<ID>-<slug>` (batch: `task/<ID>+<ID>+…-<slug>`)
- **Batch:** <none, or sibling IDs · branch · PR. Mark "dropped from batch" if this task was
  pulled out as Blocked>
- **PR / patch:** <PR link, or "patch delivered <date>">
- **Status:** WIP | Blocked | Usage-stopped | Done   <!-- mirrors the board; only mark-done sets Done -->
- **Started:** <date> · **Updated:** <date>
- **Surface / model:** claude.ai/code | claude code | desktop app + GitHub MCP | app · <model used>

## Definition of done
<paste the task's row/acceptance criteria from TASK_BOARD.md>

## Plan
<the finalized plan: approach, sub-steps, risks. Written by `plan-task` (or before heavy work
on any non-trivial/unattended task) and committed to dev-hub `main` as the task's first log
commit, or to the designated branch + PR if the session is branch-restricted>

## Checklist
- [ ] <sub-step 1>
- [ ] <sub-step 2>
- [ ] <sub-step 3>

## Next step
<the single next action to take if resuming — keep this line current at all times>

## Blocked / open questions
<what's needed to unblock: the decision or input required, and options considered. Empty
when not Blocked>

## What was done
<running summary of changes; append as you go, don't wait until the end>

## How it was tested
<commands run and their results>

## Notes / follow-ups
<open items; new tasks to add to TASK_BOARD.md. Prefix anything a future task in this repo
should know with `Learning:` (e.g. "Learning: tests need `TODO_HOME` set"). `mark-done` promotes
those lines into the master's `## Learnings`>
