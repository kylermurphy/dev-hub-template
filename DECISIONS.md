# Decisions

Why dev-hub's workflow is the way it is. One dated line per decision, newest first, with the
PR that made it. **Read this before changing a rule**; when you change one, edit `CLAUDE.md`
first, then its summaries, and add a line here.

Repo-specific decisions don't go here; they go in that repo master's `## Learnings` as
`Decision:` lines.

**Rules for this table**
- **Where** is the PR that made the decision, as a link: `[#N](https://github.com/<owner>/dev-hub/pull/N)`.
  Never write "this PR": open the PR first, then fill in its number in a follow-up commit.
  `template v0.1.0` marks decisions inherited from the dev-hub template; add your own rows
  above them.
- **Superseded decisions stay.** Add the new decision as a new row above, and end the old
  row's Decision with "*(superseded: see <date> row)*". Don't rewrite history.

| Date | Decision | Why | Where |
| --- | --- | --- | --- |
| 2026-09-25 | A claude.ai Project in handback mode is a supported surface. It keeps a working copy + ledger in Project docs, runs `mark-done` on PR confirmation, and hands back per-repo zips + `git am` patches. Its rules and its `how-to` guide live in `templates/PROJECT_INSTRUCTIONS.md`. | Lets the full workflow run from any device without push access. The instructions stay versioned in dev-hub. | template v0.1.0 |
| 2026-09-25 | The PR template stays in dev-hub (`templates/PULL_REQUEST_TEMPLATE.md`); task PRs follow it from there, and the sync step copies only `CLAUDE.md`. | One copy, no drift. Claude writes every task PR anyway; the only loss is GitHub's auto-fill for PRs opened by hand in a target repo. | template v0.1.0 |
| 2026-09-25 | Tasks on dev-hub itself (e.g. prefix `HUB-`) skip the sync step and put their bookkeeping on the task PR; `mark-done` still closes them on `main`. | dev-hub has no master, and its code and bookkeeping live in the same repo. `Done` can only follow the merge. | template v0.1.0 |
| 2026-09-25 | Model tiers everywhere: S → Haiku for read-only/mechanical work, Sonnet when it edits code or needs judgment; M → Sonnet; L → the main capable model. | One consistent rule across `README.md`, `OVERNIGHT.md` and the Subagents section. | template v0.1.0 |
| 2026-09-25 | Overnight prompts point at dev-hub's `CLAUDE.md` as the protocol's authority; a target repo's copy is a summary. Board-maintenance commands in branch-restricted sessions use the designated branch. | The repo copy only summarizes the protocol. `chore/…` branches aren't possible when a session is restricted. | template v0.1.0 |
| 2026-09-24 | The Claude desktop app with the GitHub MCP server is a supported surface for GitHub-side work (bookkeeping, branches, commits, PRs), but not for tasks that need a build or tests. Computer use isn't a route to repos. | The MCP server's write tools cover the workflow's GitHub steps, but there's no shell. Computer use can't type into terminals or IDEs. | template v0.1.0 |
| 2026-09-24 | `multi-task` batches up to 5 same-repo, non-L `Todo` tasks into one branch (`task/<ID>+<ID>+…-<slug>`) and one PR. A repo name gets a proposed batch of `Todo` S tasks. | Several simple tasks in one pass costs less review and setup than one PR each. A PR targets one repo; the cap keeps PRs reviewable. | template v0.1.0 |
| 2026-09-24 | Batches keep one log, `TASK_LOG.md` row and Status per task, linked by a `Batch:` line. Commits are prefixed with their task ID. `mark-done` closes a batch in one pass. | `mark-done`, `pickup-task`, `check-board` and Learnings keep working per task, and a single task can still be reviewed or reverted. | template v0.1.0 |
| 2026-09-24 | In a batch, a `Blocked` task is reverted and dropped; the rest ship. A usage stop pauses the whole batch. | One open question shouldn't hold up the easy wins. A budget stop affects everything left anyway. | template v0.1.0 |
| 2026-09-24 | Planning a batch uses `plan-task` with several IDs, not a new command. | One mental model: `plan-task` means "agree the plan first", whether for one task or many. | template v0.1.0 |
| 2026-09-24 | `CLAUDE.md` holds the only full task protocol; `README.md`, `COMMANDS.md` and the masters summarize it and link back. | Several full copies of the protocol drift apart. | template v0.1.0 |
| 2026-09-24 | Memory is light: `## Learnings` in each repo master (promoted from `Learning:` log lines by `mark-done`) plus this file. No full memory bank. | The masters, logs and board already cover a memory bank's ground. `CLAUDE.md` is the one file every session loads automatically. | template v0.1.0 |
| 2026-09-24 | Subagent guidance is text in `CLAUDE.md`, with no `.claude/agents/` files. | Cheap-model delegation for broad or mechanical work, without extra files to sync into every repo. | template v0.1.0 |
| 2026-09-24 | Every tracked repo has its own board section. | `scan-repo` and `check-board` assume one section per repo. | template v0.1.0 |
| 2026-09-24 | `check-board` is a written procedure (no script or CI yet). | Keeps the hub docs-only; a script can be added later. | template v0.1.0 |
| 2026-09-24 | Branch-restricted sessions put bookkeeping on the designated branch with a PR that is always open and never self-merged. `mark-done` guarantees the PR exists. | Some cloud sessions can't push to `main`; without this rule, bookkeeping can sit on a branch with no PR. | template v0.1.0 |
| 2026-09-23 | Task bookkeeping (log, `TASK_LOG.md` row, board Status) goes straight to dev-hub `main`. Code always goes branch + PR in the target repo. | Current state is always on `main` for the next session. Status updates don't wait on merges. | template v0.1.0 |
| 2026-09-23 | Statuses are `Todo` / `WIP` / `Blocked` / `Usage-stopped` / `Done`. Plans are saved to `log/<ID>.md` before heavy work. `plan-task` and `pickup-task` exist. | Unattended runs must survive stopping (decisions, usage limits) and resume without the original chat. | template v0.1.0 |
| 2026-09-23 | `mark-done` is the single Done mechanism and checks that the PR merged first (or, in handback mode, that the owner confirmed it). | One place to close a task, so board, log and `TASK_LOG.md` never disagree. | template v0.1.0 |
| 2026-09-23 | Board-maintenance commands are lightweight: a `chore/` branch + PR, no log or Status. | They maintain the board; they aren't tasks. | template v0.1.0 |
| 2026-09-23 | Repo instructions are edited in dev-hub masters (`repos/<name>/CLAUDE.md`) and copied into the repo as each task's first commit. | One source of truth that reaches every repo without a manual sync. | template v0.1.0 |
| 2026-09-23 | dev-hub is a private control repo and GitHub is the hub. Every task is self-contained: branch, PR and log, independent of any chat. | The cloud and the local machine can both reach GitHub, but not each other. | template v0.1.0 |
