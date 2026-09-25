# Changelog

All notable changes to the dev-hub template. Versions follow [semver](https://semver.org/);
the current version is in [`VERSION`](VERSION).

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
