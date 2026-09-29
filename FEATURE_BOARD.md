# Feature Board

Larger work in one repo that lives on its own branch until it's finished as a whole, one
section per repo. Small, self-contained work goes on [`TASK_BOARD.md`](TASK_BOARD.md) instead;
[`docs/FEATURES.md`](docs/FEATURES.md) explains which to use. Rules: `CLAUDE.md` → Features.

## How to use this board

- **Add a feature:** `new-feature <repo>`, or describe it and Claude adds it. It gets the
  repo's next letter (`EX-FA`, `EX-FB`, …), and its subtasks are numbered inside it
  (`EX-FA1`, `EX-FA2`, …).
- **Read a feature:** the **Description** says what it builds and why; the table lists the
  subtasks. Agents read the Description before the table.
- **Start it:** `plan-task <feature ID>` agrees the plan, makes the `feature/<ID>-<slug>`
  branch and opens one draft PR.
- **Work it:** `pickup-task <subtask ID>`, or the feature ID for the next subtask. Subtasks are
  committed straight onto the feature branch, each commit prefixed with the subtask ID. They
  get no PR of their own.
- **Finish it:** review and merge the feature PR, then run `mark-done <feature ID>`.

Status key: the same as the task board: ⏩ `Todo` · 🟠 `WIP` · ‼️ `Blocked` ·
🛑 `Usage-stopped` · 🟢 `Done`. A subtask is `Done` once its commits are on the feature branch
and the checks pass. The feature is `Done` only after its PR merges (`mark-done`).

<!-- Feature sections go below, one per repo that has features: `## <repo> — `<PREFIX>-``, created
by `new-feature <repo>`. See examples/FEATURE_BOARD.example.md for a filled-in feature. -->
