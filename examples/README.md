# examples/ — dev-hub, filled in

Everything else in this template starts **empty**. This folder shows what a hub looks like
after tracking one repo and finishing one task, so you can see the workflow before you run it.

**These files are reference only.** Commands never read or write `examples/`; your live state
is the empty `TASK_BOARD.md`, `TASK_LOG.md`, `log/` and `repos/` at the top of the repo. Keep
the folder as a guide, or delete it once you're comfortable.

| File | Shows | Real location in your hub |
| --- | --- | --- |
| [`TASK_BOARD.example.md`](TASK_BOARD.example.md) | Tracked Repos row, Repo Overview row, and the `EX-` task section | `TASK_BOARD.md` |
| [`example-repo/CLAUDE.md`](example-repo/CLAUDE.md) | A repo **master**, with one `## Learnings` bullet | `repos/example-repo/CLAUDE.md` |
| [`log/EX-1.md`](log/EX-1.md) | A finished task log | `log/EX-1.md` |
| [`TASK_LOG.example.md`](TASK_LOG.example.md) | The task's row in the running index | `TASK_LOG.md` |

The sample repo, `example-repo`, is an imaginary small Python to-do CLI (`todo add/list/done/rm`,
tested with `pytest`). Its task IDs use the prefix `EX-`.

---

## Walkthrough: from nothing to `EX-1` done

Each step names the command you type, what Claude does, and **which file changes**. "Commit to
`main`" means dev-hub's `main`; code always goes on a branch + PR in the target repo. The full
rules are in [`../CLAUDE.md`](../CLAUDE.md) → Task protocol and
[`../COMMANDS.md`](../COMMANDS.md).

### 1. Track the repo: `add-repo <owner>/example-repo`
- Claude detects the repo is public, derives the prefix `EX-`, and adds **one row to Tracked
  Repos** in `TASK_BOARD.md` (see the first table in
  [`TASK_BOARD.example.md`](TASK_BOARD.example.md)).
- Board maintenance is lightweight: it goes on a `chore/add-repo-example-repo-<date>` branch
  in dev-hub with a PR. **You merge that PR.** No log, no Status.

### 2. Describe it: `refresh-overview`
- Claude runs `scripts/repo_stats.sh` on every active repo and rewrites the **Repo overview**
  table (commits, last active, stack, state). Another `chore/` branch + PR; you merge it.

### 3. Find the work: `scan-repo example-repo`
- Claude clones the repo, reads its README, tests, CI and `TODO`s, and on a `chore/` branch:
  - adds a **`## example-repo — EX-` section** to `TASK_BOARD.md` with candidate tasks, all
    `Todo` (EX-1 … EX-3 in the example);
  - creates the **master** `repos/example-repo/CLAUDE.md`: what the repo is, how to install,
    build and test it, gotchas, an empty `## Learnings`, and the compact task protocol.
- You review and merge the PR. You can also add tasks yourself any time with
  `new-task example-repo`.

### 4. Start a task: `plan-task EX-1`
- Claude discusses the approach with you. When you agree, it:
  - creates **`log/EX-1.md`** from `log/TEMPLATE.md` with the **Plan**, **Checklist** and
    **Next step** filled in and `Status: WIP`;
  - adds an EX-1 row at the top of **`TASK_LOG.md`**;
  - sets EX-1 to **`WIP`** on **`TASK_BOARD.md`**;
  - commits all three **straight to dev-hub `main`** (`log: EX-1 plan`), before any code.
- Small task and you're in a hurry? Saying "pick up EX-1" skips the discussion, but the plan
  is still saved first.

### 5. Do the work (target repo)
- Claude branches **`task/EX-1-list-json`** off `example-repo`'s `main`.
- **First commit:** copies the master into the repo root as `CLAUDE.md` (the "sync
  instructions" step).
- Then the change itself, with tests, and a **draft PR** whose description follows
  [`../templates/PULL_REQUEST_TEMPLATE.md`](../templates/PULL_REQUEST_TEMPLATE.md): task ID,
  what changed and why, how it was tested, and the definition-of-done checklist.
- As it goes, Claude ticks the log's **Checklist** and keeps **Next step** current, pushing
  the log to dev-hub `main`. Anything a future task should know goes in the log as a
  **`Learning:`** line.

### 6. If it stops
- A decision Claude can't make: Status **`Blocked`**, with the question under
  `## Blocked / open questions` in the log.
- Out of usage: **`Usage-stopped`**. A run that's simply cut off stays `WIP`.
- Either way: **`pickup-task EX-1`** reads the log and the branch and continues from Next step.
  (EX-1 in the example didn't stop.)

### 7. Close it: merge, then `mark-done EX-1`
- **You** review and merge PR #12 in `example-repo`.
- Then `mark-done EX-1` checks the PR is merged and, in one commit to dev-hub `main`
  (`log: EX-1 done`):
  - sets EX-1 to **`Done`** on `TASK_BOARD.md`;
  - sets its `TASK_LOG.md` row to **`Done (merged 2026-09-19)`**;
  - finalizes **`log/EX-1.md`**: Status `Done`, PR marked merged, checklist ticked, Next step
    "None — task complete.";
  - promotes the log's `Learning:` line into the master's **`## Learnings`**. It reaches
    `example-repo` at the start of its next task.

That's the state shown in this folder. EX-2 and EX-3 are still `Todo`: `plan-task EX-2`
starts the next one, or `multi-task EX-2 EX-3` does both on one branch with one PR.

## Variations
- **Several small tasks at once:** `multi-task EX-2 EX-3` (or `multi-task example-repo` for a
  proposed batch). One branch `task/EX-2+EX-3-…`, one PR, and still one log per task. See
  `../CLAUDE.md` → Batches.
- **No push access (Claude Project, handback mode):** the same steps run against a working copy
  in the Project. At the end you get zips + `git am` patches to commit yourself, and
  `mark-done` records `Done (PR confirmed <date>)`. See `../README.md` → Claude Project
  (handback mode).
- **Overnight:** paste the kick-off prompt from [`../OVERNIGHT.md`](../OVERNIGHT.md) and name
  one S/M task (or one batch).
