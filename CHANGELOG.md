# Changelog

All notable changes to the dev-hub template. Versions follow [semver](https://semver.org/);
the current version is in [`VERSION`](VERSION).

## [0.3.0] — 2026-10-02

A reworked README, a guide to where dev-hub runs, workflow diagrams, and projects in handback
mode.

### Added
- **`docs/SURFACES.md`**, a fourth guide: what each Claude surface can reach, how to set it up,
  and its caveats, including handback mode (a Claude Project) in full. It moved out of the
  README.
- **Diagrams**: the task lifecycle in `docs/TASKS.md`, and the feature lifecycle and a feature
  branch (`feature/EX-FA-calendar-sync`, with `main` merged in) in `docs/FEATURES.md`. Each box
  says whether that step happens in dev-hub or the target repo.
- **Projects in handback mode**: `new-project`, `plan-project`, `review-projects` and everyday
  project edits run in a Claude Project and come back as a dev-hub patch.
- Links to the four blog posts about dev-hub (dev-hub, handback mode, features, projects) at
  the top of the README.

### Changed
- The README is a short overview: links to the three boards, what dev-hub does, the three
  levels of work and how to combine them (each works on its own), the Plan → Launch → Track →
  Land loop for tasks and features, a command table, a summary of where it runs, setup, and
  memory (a feature has one log and one `TASK_LOG.md` row, and shares the repo's learnings with
  tasks).
- Handback mode says what runs there: tasks, batches, board maintenance and projects, but
  **not features**, since a patch can't carry a feature branch's merges. `plan-task` and
  `plan-project` wait for the owner's go there too; naming a task means `run-task`.
- `docs/TASKS.md` groups tasks by repo and points to the README's command table;
  `docs/PROJECTS.md` covers projects with no tracked repos, and where project edits go in a
  branch-restricted session or handback mode.
- Pointers to the old README sections (`CLAUDE.md`, `COMMANDS.md`, `ADAPTING.md`,
  `examples/README.md`) now go to `docs/SURFACES.md` or `docs/TASKS.md`.
- `DECISIONS.md`: two new rows (the README and guides, and handback mode's scope).

Synced from dev-hub `4d21ce3`.

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
