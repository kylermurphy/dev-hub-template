# CLAUDE.md — example-repo

Instructions for Claude Code **and** claude.ai/code (cloud) sessions working in this repo.
Both read this file. Edit it in dev-hub (`repos/example-repo/CLAUDE.md`), not
here: this copy is replaced from the master at the start of each task.

> **Example only.** This is what a master looks like after `scan-repo example-repo` and one
> finished task (EX-1). In a real hub it lives at `repos/example-repo/CLAUDE.md`.

## What this is
`todo`, a small command-line to-do list written in Python. Items are stored as JSON in a data
directory (`~/.todo` by default). Commands: `todo add`, `todo list`, `todo done`, `todo rm`.

## Environment & install
- Python **>= 3.10**.
- Install with dev extras: `pip install -e ".[dev]"` (installs `pytest` and `ruff`).
- Entry point: `todo` (defined in `pyproject.toml` → `[project.scripts]`).

## Commands
- Tests: `pytest`
- Lint: `ruff check .`
- CI: none yet (task **EX-2**).

## Layout (`src/todo/`)
- `cli.py`: argument parsing and the sub-commands
- `store.py`: reads and writes the JSON data file
- `tests/`: pytest suite; `conftest.py` provides a temporary data directory

## Conventions & gotchas
- The data directory comes from `TODO_HOME` if set, otherwise `~/.todo`.
- Keep `store.py` free of printing; all output goes through `cli.py`.

## Learnings

Durable facts from past tasks, promoted from `log/<ID>.md` by `mark-done` (max ~15).

- Tests must set `TODO_HOME` to a temporary directory (the `tmp_todo_home` fixture does this);
  otherwise they read and overwrite the real `~/.todo`. (EX-1)

## Task protocol (dev-hub tasks)

Tasks come from **dev-hub** (`<owner>/dev-hub`). Its `CLAUDE.md` → **Task protocol** is the
full, authoritative version; this is the summary. Each task is self-contained: start from its
board row alone.

- **Branch** `task/<ID>-<slug>` off the default branch; never commit to `main`.
- **First commit:** sync this file from its dev-hub master
  (`repos/example-repo/CLAUDE.md`). Edit instructions in the master, never here.
- **Plan** saved to dev-hub `log/<ID>.md` before heavy work (`plan-task <ID>`); a `plan <ID>`
  dry run saves nothing. **Draft PR** following dev-hub's `templates/PULL_REQUEST_TEMPLATE.md`
  (not copied here): ID, what, why, how tested, DoD check.
- **Bookkeeping** (`log/<ID>.md`, `TASK_LOG.md` row, board Status → `WIP`) goes straight to
  dev-hub `main`. In a branch-restricted session it goes to the designated branch with an
  open PR instead (say so in chat; never merge it yourself). Only `mark-done <ID>` sets `Done`.
- **Stop states:** `Blocked` (fill `## Blocked / open questions`) or `Usage-stopped`; keep
  `Next step` current and resume with `pickup-task <ID>`.
- **Batches** (`multi-task`, or `plan-task` with several IDs): one branch
  `task/<ID>+<ID>+…-<slug>` and one PR for up to 5 simple tasks; each keeps its own log, and
  commits are prefixed with their ID. A `Blocked` task is dropped from the batch; the rest
  ship. Rules: dev-hub `CLAUDE.md` → Batches.
- **Learnings:** mark lasting findings as `Learning:` lines in the log; `mark-done` promotes
  them into `## Learnings` above (via the master).
- **Subagents:** delegate only broad/mechanical work to cheaper models, per dev-hub
  `CLAUDE.md` → Subagents; the main session does all commits and pushes.
- Run `pytest` and `ruff check .` before opening the PR.
- Definition of done = the task's row on dev-hub `TASK_BOARD.md`.

## Task board
This repo's backlog IDs use the **`EX-`** prefix.
