# dev-hub

> **This is the dev-hub template (v0.3.0).** Click **Use this template** on GitHub to make your
> own private `dev-hub`, then follow [Setup](#setup). Everything starts empty.
> **New here?** See [`examples/`](examples/) for a filled-in board, repo master and task log,
> with a step-by-step walkthrough of one task. **Not using Claude?** See
> [`ADAPTING.md`](ADAPTING.md). Originally built by [Kyle Murphy](https://github.com/kylermurphy);
> MIT licensed ([`LICENSE`](LICENSE)). **The story behind it**, in four blog posts:
> [dev-hub](https://kylermurphy.github.io/posts/2026/09/post-10/) · [handback mode](https://kylermurphy.github.io/posts/2026/09/post-11/) ·
> [features](https://kylermurphy.github.io/posts/2026/09/post-12/) · [projects](https://kylermurphy.github.io/posts/2026/10/post-13/).

| [Task board](TASK_BOARD.md) | [Feature board](FEATURE_BOARD.md) | [Project portfolio](projects/INDEX.md) |
| :---: | :---: | :---: |
| tasks, grouped by repo | features, grouped by repo | research projects |

dev-hub is a private, docs-only repo that turns Claude into a development/management team for
your projects and GitHub repos. With it you can:

- track your repos and have Claude identify work in them and then work on its own or with you
  to complete the work;
- hand off tasks from your phone or laptop and get a PR back to review;
- build larger features on one branch, a subtask at a time;
- track multi-month research projects providing work plans and linking them to the code that
  serves them;
- run work while you're away, and resume anything from its log.

**`dev-hub` holds a log of tasks, features and projects, the rules every Claude session follows,
and a record of completed work (small memory bank), so any session on any surface can pick up
the work.**

## Three levels of work: use what fits

Tasks and features are grouped by repo: each board has one section per tracked repo. A project
isn't tied to one repo; its work packages can link to tasks and features in any of them.

| Level | Use it for | Lives in | Guide |
| --- | --- | --- | --- |
| **Task** | One self-contained change in one repo: a fix, a test suite, a docs pass. One branch and one PR, merged when it's done. | [`TASK_BOARD.md`](TASK_BOARD.md) | [`docs/TASKS.md`](docs/TASKS.md) |
| **Feature** | Several related steps in one repo that should reach `main` together, e.g. a new module. One branch for days or weeks, and one PR at the end. | [`FEATURE_BOARD.md`](FEATURE_BOARD.md) | [`docs/FEATURES.md`](docs/FEATURES.md), which starts with "Task or feature?" |
| **Project** | A multi-month research effort: goals, objectives, work packages, plans and a research log, linked to the tasks and features that do its code work. | [`projects/`](projects/), with the portfolio in [`projects/INDEX.md`](projects/INDEX.md) | [`docs/PROJECTS.md`](docs/PROJECTS.md) |

The levels work together, but none needs the others. Use the ones that suit how you work, and
add the rest later. An empty board or an empty `projects/` is fine, and `check-board` passes
either way. For example:
- **Tasks only:** track your repos and hand off work. This is the simplest place to start.
- **Tasks and features:** add a feature when several steps have to land together.
- **Projects with tasks and features:** a project's work packages link to the board IDs doing
  their code work, so the research and the code stay connected.
- **Projects only:** a structured research notebook (goals, plans, todos, references, a log)
  with no tracked repos. Set the project's `repos: []`.

## How tasks and features run

Tasks and features follow the same loop, **Plan → Launch → Track → Land**. The rules are in
[`CLAUDE.md`](CLAUDE.md) → Task protocol and → Features, and the guides have diagrams.

- **Plan.** `plan-task <ID>` drafts a plan with you and **waits for your go**. `run-task <ID>`
  has Claude plan a small (S/M) task itself and carry on. Either way, the plan is saved to the
  log before any heavy work. Features always start with `plan-task`.
- **Launch.** Claude branches in the target repo (`task/<ID>-<slug>`, or
  `feature/<ID>-<slug>`), copies in the repo's `CLAUDE.md`, does the work and opens a draft PR.
  `multi-task` runs a few small tasks on one branch. A feature's subtasks are committed onto its
  branch one `pickup-task` at a time.
- **Track.** The log's checklist and Next step, and the board Status, stay current. A stopped
  task or feature is `Blocked` (waiting on your decision) or `Usage-stopped`, and `pickup-task`
  resumes it from any session.
- **Land.** You review and merge the PR. `mark-done` sets `Done`, finishes the log and saves
  what the work learned into the repo's instructions.

Projects have their own cycle: `plan-project` agrees a research plan with you, the project file
is updated as work happens, and `review-projects` checks in on every project.

## Commands

Commands are words you type in a Claude session. Each is specified in
[`COMMANDS.md`](COMMANDS.md).

| Command | What it does |
| --- | --- |
| ***Repos and boards*** | *Track your repos and keep the task and feature boards current.* |
| `add-repo <repo>` | Starts tracking a repo and gives it a task-ID prefix (`example-repo` → `EX-`). |
| `refresh-overview` | Rebuilds the Repo Overview table: commits, last activity, stack, state. |
| `scan-repo <name>` | Reads a repo (README, tests, CI, TODOs), proposes tasks, and writes or refreshes its master `CLAUDE.md`. |
| `new-task <repo>` | Adds a task you describe, with the next free ID and a definition of done. |
| `new-feature <repo>` | Adds a feature you describe, with a description and proposed subtasks. |
| `check-board` | Checks that the boards, logs and projects agree. It also runs in CI on every PR. |
| ***Tasks and features*** | *Plan and implement tasks and features.* |
| `plan-task <ID> …` | Plans a task, a batch or a feature with you, waits for your go, then starts the work. |
| `run-task <ID>` | Claude plans a small task itself and works it through to a draft PR, stopping only to ask when it must. |
| `multi-task <ID> <ID> …` | Up to five small tasks from one repo on one branch, with one PR. |
| `pickup-task <ID>` | Resumes a stopped task or batch, or works a feature's next subtask. |
| `mark-done <ID> …` | After the merge: sets `Done`, finishes the log, and saves the learnings. |
| ***Projects*** | *Plan and track research projects.* |
| `new-project "<title>"` | Starts a project file from the template and adds it to the portfolio. |
| `plan-project <ID> [O<n> \| WP<n.m>]` | Drafts a research plan for a project, objective or work package with you, and waits for your go. |
| `review-projects` | Rebuilds the portfolio and flags stale projects, blocked work and old todos. |
| ***Any command*** | *Preview it before it runs.* |
| `plan <command>` | A dry run: Claude does the read-only part and proposes the changes. Nothing is committed until you say "go". |

## Where it runs

**GitHub is the hub.** Every surface can reach GitHub, so all state lives there: dev-hub holds the
boards, rules and logs, and work on the appropriate repo lands as branches and PRs you review.

| Surface | Good for | Verified (upstream) |
| --- | --- | --- |
| **Claude Code on the web or in the Claude app** ([claude.ai/code](https://claude.ai/code)) | Everything, from any device: it clones, builds, tests, pushes and opens PRs. | ✅ |
| **Claude Code on your computer** | Everything, with your local git credentials, while the machine is on. | ✅ |
| **Claude Project (handback mode)** | Tasks, batches and projects without Claude Code. It can't push, so work comes back as patches for you to commit. Not features. | ✅ for tasks |
| **Claude desktop app + GitHub MCP server** | Bookkeeping, board commands and PRs through the GitHub API. No shell, so no builds or tests. | not yet verified |
| **Claude desktop app with computer use** | Not a route to repos on its own. | not yet verified |

Access, setup and caveats for each surface, including handback mode in full, are in
[`docs/SURFACES.md`](docs/SURFACES.md).

## Setup

0. **Create your hub from this template.** On GitHub, click **Use this template** → **Create a
   new repository**, name it `dev-hub`, and make it **private**. Replace `<owner>` in the docs
   with your GitHub user or org (it appears in a few example commands and links), and set
   `DEVHUB_OWNER=<owner>` in your shell or environment so `scripts/repo_stats.sh` and
   `add-repo` can expand bare repo names.
1. **GitHub access.** Connect GitHub in claude.ai (**Settings → Connectors**) and install the
   [Claude GitHub App](https://github.com/apps/claude) on dev-hub and every repo you track.
   Without it, cloud sessions can't push or open PRs.
2. **Pick a surface.** Start a claude.ai/code session with dev-hub and the target repo
   attached, or clone dev-hub next to your project checkouts for Claude Code
   (`git clone git@github.com:<owner>/dev-hub.git`). A Claude Project or the desktop app
   needs extra setup: see [`docs/SURFACES.md`](docs/SURFACES.md).
3. **Add a repo:** `add-repo <owner/name>`, then `refresh-overview`, then `scan-repo <name>`.
   That adds the repo to Tracked Repos and builds its task table and master `CLAUDE.md`. The
   master reaches the repo at its first task, so there's nothing to seed by hand.
4. **Start working:** `run-task <ID>` on a small task, or `plan-task <ID>` to plan it with
   Claude. The walkthrough in [`examples/`](examples/) shows one task end to end. For research, `new-project "<title>"`. Unattended runs are in
   [`OVERNIGHT.md`](OVERNIGHT.md).

## Instructions and memory

| What | Where | Read by |
| --- | --- | --- |
| Rules for working in dev-hub, including the full task protocol | [`CLAUDE.md`](CLAUDE.md) | every session in dev-hub |
| A repo's rules (build, test, layout, gotchas) and its `## Learnings` | the repo's root `CLAUDE.md`, copied from its master `repos/<name>/CLAUDE.md` | sessions working in that repo |
| A task's or feature's record: plan, checklist, Next step, what was done | `log/<ID>.md`, plus its row in `TASK_LOG.md` | `pickup-task`, `mark-done`, you |
| A project's record: plans, decisions, research log | the project file, `projects/<name>.md` | `plan-project`, `review-projects`, you |
| Why the workflow is the way it is | [`DECISIONS.md`](DECISIONS.md) | anyone changing the workflow |
| Personal preferences | the claude.ai app's own memory | the app only; not for repo specifics |

- **A feature is logged like a task.** It has one log file, `log/<feature ID>.md`, with a
  checklist item per subtask, and one row in `TASK_LOG.md`. Its subtasks have no log or row of
  their own.
- **Tasks and features share a repo's memory.** Anything lasting goes in the log as a
  `Learning:` line, and `mark-done` promotes it into the repo master's `## Learnings` (about 15
  at most; `scan-repo` prunes them). The repo's next task or feature starts with them.
- **Edit a repo's instructions in its master**, never in the repo's root copy. The copy is
  replaced at the start of each task or feature, which is also how edits reach the repo.
- **Changing the workflow:** edit `CLAUDE.md` first, then its summaries (this README, the
  guides in `docs/`, `COMMANDS.md`, the masters' compact protocol), and add a line to
  `DECISIONS.md`.

## Contents

| Path | What it is |
| --- | --- |
| [`README.md`](README.md) | This overview. |
| [`docs/`](docs/) | The guides: [`TASKS.md`](docs/TASKS.md), [`FEATURES.md`](docs/FEATURES.md), [`PROJECTS.md`](docs/PROJECTS.md) and [`SURFACES.md`](docs/SURFACES.md) (where dev-hub runs, including handback mode). |
| [`CLAUDE.md`](CLAUDE.md) | Instructions for Claude in this hub: the **full task protocol** (the only full copy), features, projects, subagents and memory. |
| [`COMMANDS.md`](COMMANDS.md) | The spec for every command, plus the `plan` dry-run prefix. |
| [`TASK_BOARD.md`](TASK_BOARD.md) | The tasks: **Tracked Repos** (the list of repos), the Repo Overview, and one task table per repo. |
| [`FEATURE_BOARD.md`](FEATURE_BOARD.md) | The features: one section per repo, each feature with a description and a subtask table. |
| [`projects/`](projects/) | Research projects: one file per project from [`TEMPLATE.md`](projects/TEMPLATE.md), and the portfolio in [`INDEX.md`](projects/INDEX.md). |
| [`TASK_LOG.md`](TASK_LOG.md) | The index of tasks and features, in flight and done, newest first. |
| [`log/`](log/) | One record per task or feature (`<ID>.md`), from `log/TEMPLATE.md`. |
| [`repos/<name>/CLAUDE.md`](repos/) | The **master** instruction file for each target repo, including its `## Learnings`. Empty until `scan-repo` creates the first one. |
| [`OVERNIGHT.md`](OVERNIGHT.md) | Running work while you're away: usage limits, guardrails, kick-off and resume prompts. |
| [`DECISIONS.md`](DECISIONS.md) | Why the workflow is the way it is: dated decisions. |
| [`templates/`](templates/) | The PR template every task PR follows (Claude reads it from here; it isn't copied into target repos), and `PROJECT_INSTRUCTIONS.md` for a Claude Project in handback mode. |
| [`scripts/`](scripts/) | Helper scripts: `repo_stats.sh` (for `refresh-overview` and `scan-repo`) and `check_board.py` (every `check-board` check). |
| [`.github/workflows/`](.github/workflows/) | CI: `check-board.yml` runs `scripts/check_board.py` on every PR and push to `main`. |
| [`examples/`](examples/) | A filled-in sample (`example-repo` with tasks `EX-1`…`EX-3` and feature `EX-FA`, plus a sample research project) and a step-by-step walkthrough. Read-only reference: your working files are the empty ones above. |
| [`AGENTS.md`](AGENTS.md) | A one-line pointer to `CLAUDE.md` for other agents. |
| [`ADAPTING.md`](ADAPTING.md) | How to adapt dev-hub to another agent or ecosystem (untested). |
| [`CHANGELOG.md`](CHANGELOG.md), [`VERSION`](VERSION) | Template version history; current version. |
| [`LICENSE`](LICENSE) | MIT. |

---

This repo is **private**. Keep it private, and never commit secrets or credentials.
