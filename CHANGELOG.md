# Changelog

All notable changes to the dev-hub template. Versions follow [semver](https://semver.org/);
the current version is in [`VERSION`](VERSION).

## [0.2.0] — 2026-09-29

Features, research projects, `run-task`, and a scripted, CI-checked board.

### Added
- **Features** for larger work that stays on one branch until it's finished:
  `FEATURE_BOARD.md`, IDs `<PREFIX>FA` with subtasks `<PREFIX>FA1`, …, one
  `feature/<ID>-<slug>` branch and one draft PR per feature. New command `new-feature`; the
  lifecycle commands take feature and subtask IDs. Rules in `CLAUDE.md` → Features.
- **Projects**, a research layer above the boards: one Markdown file per multi-month project
  in `projects/` (from `projects/TEMPLATE.md`, with goals, objectives, work packages, plans,
  todos, references, decisions and a research log) and a portfolio in `projects/INDEX.md`. New
  commands `new-project`, `plan-project` and `review-projects`. Rules in `CLAUDE.md` →
  Projects.
- **`run-task <ID>`**: Claude writes and saves its own plan and goes to a draft PR, for S/M
  tasks with a clear definition of done. Naming a task ID on its own means `run-task`.
- **`scripts/check_board.py`**, the `check-board` spec as a script (Python standard library
  only), and a GitHub Actions workflow running it on every PR and push to `main`.
- **Guides** in `docs/`: `TASKS.md`, `FEATURES.md` and `PROJECTS.md`.
- **Examples**: a feature (`examples/FEATURE_BOARD.example.md`), a made-up research project
  with its index row (`examples/projects/`), and walkthrough steps for both.

### Changed
- `plan-task` always plans, discusses and **waits for the owner's explicit go**; answers to its
  questions aren't a go.
- One **"When to stop and ask"** list in `CLAUDE.md` governs everything that runs without
  waiting (`run-task`, `multi-task`, `pickup-task`, overnight runs).
- Every plan names who does each step: the main model, or a subagent.
- `TASK_BOARD.md` statuses show an icon with the word (`⏩ Todo` · `🟠 WIP` · `‼️ Blocked` ·
  `🛑 Usage-stopped` · `🟢 Done`), and each Tracked Repos name links to its task section.
- The README is now an overview; how each way of working runs moved to the `docs/` guides.
- `scripts/repo_stats.sh` is executable and the commands call it with `bash`.
- `DECISIONS.md`: six new rows; the "check-board is a written procedure" row is superseded.
- The examples use the status icons, and the example master and log follow the new plan rules.

Synced from dev-hub `486acbe`.

## [0.1.0] — 2026-09-25

First public release of the template, genericized from a working dev-hub.

### Added
- The hub files, empty and ready to use: `TASK_BOARD.md` (Tracked Repos, Repo Overview),
  `TASK_LOG.md`, `log/` (`README.md`, `TEMPLATE.md`), `repos/` (masters are created by
  `scan-repo`).
- `CLAUDE.md` with the full task protocol: sync instructions, persisted plans, stop states
  (`Blocked`, `Usage-stopped`), branch-restricted sessions, batches, subagents, memory.
- `COMMANDS.md`: board maintenance (`add-repo`, `refresh-overview`, `scan-repo`, `new-task`,
  `check-board`) and task lifecycle (`plan-task`, `multi-task`, `pickup-task`, `mark-done`),
  plus the `plan` dry-run prefix.
- `OVERNIGHT.md` (unattended runs), `DECISIONS.md` (design rationale),
  `templates/PULL_REQUEST_TEMPLATE.md`, `templates/PROJECT_INSTRUCTIONS.md` (Claude Project
  handback mode), `scripts/repo_stats.sh`.
- `examples/`: a filled-in `example-repo` (master, board, log, task-log row) with a
  step-by-step walkthrough.
- `AGENTS.md` pointer, `ADAPTING.md` (porting notes, untested), `LICENSE` (MIT), `VERSION`.
