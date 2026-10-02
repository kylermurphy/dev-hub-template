# CLAUDE.md — dev-hub (control repo)

Instructions for Claude Code, claude.ai/code (cloud) sessions, and Claude desktop-app sessions
(which load it through a Project) working in this hub repo.
This file holds the **only full version of the task protocol**; everything else (`README.md`,
the repo masters) summarizes it and points here.

## What this repo is
The private control/planning hub for the owner's development work. It holds the backlog
(`TASK_BOARD.md` for tasks, `FEATURE_BOARD.md` for larger features), the task records
(`TASK_LOG.md`, `log/`), the commands (`COMMANDS.md`) and their helpers (`scripts/`, with
`check-board` run in CI on every PR), the overnight guide (`OVERNIGHT.md`), the workflow
decisions (`DECISIONS.md`), master copies of each target repo's instruction file
(`repos/<name>/CLAUDE.md`), and the PR template every task PR follows (`templates/`).
`projects/` holds the research layer above the boards: one file per multi-month research
project, plus a portfolio index. `README.md` is the human overview (the levels of work,
commands, setup); `docs/` holds the guides (`docs/TASKS.md`, `docs/FEATURES.md`,
`docs/PROJECTS.md`, and `docs/SURFACES.md` for where dev-hub runs, including handback mode).
`examples/` holds a filled-in sample for reference only (never edit it as live state);
`AGENTS.md` points other agents here; `ADAPTING.md` covers porting to other agents. It
contains **no application code**; it's planning and instructions only.

## Target repos

The canonical list of target repos and their task-ID prefixes is `TASK_BOARD.md` →
**Tracked Repos**. Each repo's master instructions live at `repos/<name>/CLAUDE.md`. No
duplicate list is kept here, so nothing can drift from the board. dev-hub can track itself too
(add it to Tracked Repos, e.g. with prefix `HUB-`); its instructions are this file, so it has
no `repos/dev-hub/` master.
Each repo's name in Tracked Repos links to its task section on the board (`scan-repo` adds the
link when it creates the section). A repo's features, if it has any, are in its section of
`FEATURE_BOARD.md`.

## Task protocol (mandatory)

Every task started from dev-hub is a **self-contained unit of work, independent of any
other chat or Claude Code session**. Start it from its board row alone (assume no prior
context) and always:

1. **New branch.** Create `task/<ID>-<short-slug>` off the target repo's default branch (a
   batch uses one branch for all its tasks; see **Batches** below).
   Never commit to the target repo's `main`.
2. **Sync instructions first.** As the first commit on the branch, make sure the target repo's
   root `CLAUDE.md` matches dev-hub's `repos/<name>/CLAUDE.md`; if it's missing or out of
   date, copy the master in and commit before doing anything else. The dev-hub master is the
   source of truth. It's edited here and reaches the repo this way; never hand-edit the
   repo's copy. (The PR template is **not** copied; see step 4.) The instruction-file name
   `CLAUDE.md` is **(Claude-specific)**; other agents read other names (see `ADAPTING.md` →
   Instruction-file name).
3. **Persist the plan.** Every task gets a written plan in `log/<ID>.md`, committed to dev-hub
   **before heavy work**. It has three parts:
   - `## Plan`: the approach, the sub-steps, the risks, and **who does each sub-step** (the
     main model, or a subagent: see Subagents);
   - `## Checklist`;
   - `## Next step`.

   There are two ways to get it:
   - **`plan-task <ID>` plans with the owner.** Post the plan in chat, discuss it, and **wait
     for their explicit go** before saving or starting anything. Answers to open questions,
     earlier discussion, or "plan and do" aren't a go.
   - **`run-task <ID>` plans on its own.** Write the plan, save it and carry on, stopping only
     under **When to stop and ask** (below). It's for S/M tasks with a clear definition of
     done. L tasks, rows that need a decision, and features go through `plan-task`. Naming a
     task ID on its own ("do EX-3") means `run-task`.

   An interactive `plan <ID>` dry run stays ephemeral, since the owner is present.
4. **PR.** Open a draft PR for that branch (a patch/diff only when the session can't push;
   see `docs/SURFACES.md`). The description follows dev-hub's
   `templates/PULL_REQUEST_TEMPLATE.md` (read it from dev-hub; it isn't copied into target
   repos): the task **ID**, what changed, why, how it was tested, and the definition-of-done
   check.
5. **Log in dev-hub.** `log/<ID>.md` (from `log/TEMPLATE.md`) with the same summary and the PR
   link, a row at the top of `TASK_LOG.md`, and the task's **Status** on `TASK_BOARD.md` →
   `WIP`. This bookkeeping is committed **straight to dev-hub `main`** (the one exception to
   "never commit to `main`"), unless the session is branch-restricted (see below), in which
   case it goes to the designated branch + a PR; `HUB-` tasks put it on their task PR (see
   below). When the PR merges, **`mark-done <ID>`** sets `Done`. It's the only way a task
   becomes `Done`. The log is dev-hub's own record and must stand on its own even if the PR
   or the session is gone.
6. **Learnings.** Mark anything a future task in that repo should know (a build quirk, a
   gotcha, a repo-level decision) as a `Learning:` line in the log's `## Notes / follow-ups`.
   `mark-done` promotes those into the master's `## Learnings` (see Memory, below).
7. **Stop states; resume, don't restart.** Commit/push incrementally and keep `log/<ID>.md`'s
   `Status`/`Next step` current.
   - Hit a **When to stop and ask** rule (below) → ask the owner if they're present; otherwise
     Status **`Blocked`**, and fill `## Blocked / open questions` with what's needed.
   - Stopping for budget → Status **`Usage-stopped`** if you're able to.
   - Either way keep `Next step` current so **`pickup-task <ID>`** can resume. A run cut off
     abruptly may not set a status. That's fine: a `WIP` task with a `task/<ID>` branch is
     still resumable.
   - If a `task/<ID>` branch or log already exists, continue from `Next step`
     (`pickup-task`) rather than restarting.
8. **Definition of done** = the task's row on `TASK_BOARD.md`.

### When to stop and ask

Whatever runs without waiting for the owner (`run-task`, `multi-task`, `pickup-task`, an overnight
run) stops for them when:
1. the definition of done is ambiguous, or can't be tested as written;
2. a design choice with more than one reasonable answer would change something visible, such
   as an API, the file layout, names users see, or a data format, and nothing settles it:
   not the row, the repo's master, `DECISIONS.md`, or the repo's existing conventions;
3. a step is irreversible or reaches outside the task's branch and PR: deleting data,
   force-pushing, publishing, touching another repo, changing secrets or CI permissions;
4. the work turns out bigger than the row's effort, or needs changes the row doesn't cover;
5. checks fail for reasons outside the task, or the same fix fails twice.

**Owner present:** ask in chat (the question, the options, your recommendation) and wait.
**Away** (an overnight run, or no answer this session): set the task `Blocked` with the
question under `## Blocked / open questions` and stop it. A batch drops it and finishes the
rest. Anything the rules don't catch, decide it and record the choice in the log and the PR,
so the owner can review it afterwards.

### dev-hub's own tasks (`HUB-`)

A `HUB-` task changes dev-hub itself, so the code and its bookkeeping live in the same repo:

- **Branch** `task/HUB-<n>-<slug>` in dev-hub. **Skip the sync step**: dev-hub's `CLAUDE.md`
  is its own master (there's no `repos/dev-hub/`).
- **Bookkeeping goes on the task PR**, not straight to `main`: the plan and `log/HUB-<n>.md`,
  its `TASK_LOG.md` row and the board Status → `WIP` are commits on the task branch. `main`
  shows the task as `Todo` until that PR merges.
- **Closing:** after the PR merges, `mark-done HUB-<n>` commits `Done` straight to `main` as
  usual (it can't be in the task PR, since `Done` means merged). Learnings go to
  `DECISIONS.md`, not a master.

### Branch-restricted sessions (bookkeeping fallback)

Some cloud sessions are launched pinned to **one designated dev-hub branch** and may not push
anywhere else without explicit permission. There, committing bookkeeping straight to `main` is
impossible, so:

- **Where it goes.** Bookkeeping commits (`plan-task`'s WIP commit, status/`Next step` updates,
  `mark-done`) go on the **designated branch**. They reach `main` only when that branch's PR
  merges, so **the task isn't fully closed out until that dev-hub PR merges too**.
- **Say so, once per task.** The first time the fallback applies to a task, say it in chat,
  e.g. *"This session is branch-restricted, so EX-2's bookkeeping is going to a PR on
  `<branch>` instead of straight to `main`. Merge that PR to finish closing out the task."*
- **Always leave a PR open.** Never leave bookkeeping commits on a branch with no PR. After
  each bookkeeping push, open a PR from the designated branch into `main` if none is open,
  or update the open one's title/body. **Never merge it yourself.** `mark-done` must
  *guarantee* the PR exists before it finishes.
- **Sync first.** Before committing, merge `origin/main` into the designated branch so the PR
  is conflict-free when opened or updated. If that branch's previous PR has **already
  merged**, restart the branch from `origin/main` (same name) and open a **new** PR; never
  stack new commits onto merged history.
- **Several tasks, one session.** They share the designated branch, so they share one PR.
  Retitle it to cover every task (e.g. `Log EX-1, EX-2: bookkeeping`) and give each task
  its own section in the body.
- **Several sessions, several PRs.** Each touches its own `log/<ID>.md`, but `TASK_LOG.md`
  (rows added at the same spot) and adjacent `TASK_BOARD.md` rows can conflict once another
  PR merges. Resolve by merging `main` into the branch and **keeping both sides**: every
  `TASK_LOG.md` row (newest first), and each board row's Status from its own task. Each
  commit only touches its own task's rows, so merge order never undoes another task.
- **Reading state.** While a task's bookkeeping PR is open, its latest log is on that branch,
  not `main`. `pickup-task` and `mark-done` read it from there.
- **PR format.** Title: `Log <ID>: bookkeeping (<from> →
  <to>)`, e.g. `(WIP → Done)`. Body:
  - it's **dev-hub bookkeeping only, no code changes**;
  - why it's on a branch (the session is branch-restricted);
  - what each commit changed and why (usually a WIP commit plus the `mark-done` commit);
  - "How it was tested: N/A";
  - that the task's definition of done was verified in the target-repo PR (link);
  - that **merging this PR is what lands the change on `main`**.

### Batches (several tasks, one PR)

`multi-task <ID> <ID> …` (or `plan-task` with several IDs) runs simple tasks together on one
branch with one PR. Everything above still applies **per task**, with these differences:

- **Eligible:** every task in the **same repo** (a PR targets one repo), all `Todo`, no **L**
  tasks, **at most 5**. Given a repo name instead of IDs, propose a batch of its `Todo` **S**
  tasks and confirm it (unattended: take the proposal). Order the tasks so dependencies come
  first.
- **One branch:** `task/<ID>+<ID>+…-<slug>` (e.g. `task/EX-3+EX-4+EX-5-cleanup`), with
  the instructions sync as its first commit, done once for the batch.
- **Per-task records:** each task keeps its own `log/<ID>.md` (with its own Plan), its own
  `TASK_LOG.md` row and board Status. Each log's **`Batch:`** line names the sibling IDs, the
  branch and the PR. The batch's initial bookkeeping is one commit.
- **Commits per task:** prefix each commit with its task ID (`EX-3: …`) so a task can be
  reviewed or reverted on its own. Run the repo's checks after each task, and keep each log's
  checklist and `Next step` current.
- **One draft PR:** title `<ID>, <ID>, …: <summary>`. Body per the template, with a What
  changed section and a definition-of-done checklist **per task**.
- **Blocked task → drop it, finish the rest.** Revert that task's commits from the branch, set
  it `Blocked` with its question, and mark its `Batch:` line "dropped from batch". It resumes
  later on its own (`pickup-task <ID>`, new `task/<ID>-…` branch). The PR body lists it as
  dropped.
- **Usage-stopped → the whole batch.** Every unfinished task becomes `Usage-stopped`.
  `pickup-task` on any batch ID resumes the batch from its logs.
- **Closing:** after merge, `mark-done` closes the whole batch in one pass: one merge check,
  one bookkeeping commit, learnings promoted per task. Dropped tasks are skipped.

### Features (long-lived feature branches)

A **feature** is larger work in one repo that stays on its own branch until it's finished as a
whole: several related steps that shouldn't reach `main` one at a time. Features live on
`FEATURE_BOARD.md`, one `## <name> — <PREFIX>-` section per repo that has any. Use one for
three or more related steps that belong together; otherwise use tasks or a batch
(`docs/FEATURES.md` → Task or feature?). Everything above applies to a feature as it does to a
task, with these differences:

- **IDs.** A feature is `<PREFIX>F<letter>` (`EX-FA`, `EX-FB`, …, the next free letter in that
  repo); its subtasks are `<feature ID><n>` (`EX-FA1`, `EX-FA2`), numbered inside the feature.
  IDs are never reused, and neither form can be mistaken for a task ID (`EX-7`).
- **The block.** A `### <ID> — <title>` heading, then a
  `**Status** … · **Branch** … · **PR** … · **Log** …` line (`—` until they exist), a
  **Description.** paragraph (2–4 sentences: what the feature builds and why; read it before the
  table), a **Done when.** line (the feature's definition of done), and the subtask table
  `| ID | Status | Subtask | Type | Effort | Definition of done |`. Keep subtasks S or M; an L
  one is split when the feature is planned.
- **Starting** (`plan-task <feature ID>`): branch `feature/<ID>-<slug>` off the default branch,
  with the instructions sync as its first commit; the plan (design, subtask order) in
  `log/<ID>.md`; one `TASK_LOG.md` row; the feature's Status → `WIP`. Open a **draft PR into
  the default branch** early: it's the feature's single review, and CI runs on every push.
- **Subtasks have no PR, log or `TASK_LOG.md` row of their own.** To work one
  (`pickup-task <subtask ID>`, or the feature ID for the next one):
  - first merge the default branch into the feature branch, so it doesn't drift;
  - commit straight onto the feature branch, each commit prefixed with the subtask ID
    (`EX-FA2: …`), so a subtask can be reviewed or reverted on its own;
  - run the repo's checks. Set the subtask `WIP` when you start it and `Done` once its commits
    are pushed and the checks pass. This is the one `Done` that `mark-done` doesn't set.
  - The feature's log keeps a checklist item per subtask, and its Next step names the next one.
- **Stop states** apply to the feature (log + board). A subtask that needs a decision is
  `Blocked` in the table, with its question in the feature log; other subtasks can carry on.
- **Closing** (`mark-done <feature ID>`): after the feature PR merges, and only if every
  subtask is `Done`. To drop a subtask, remove its row and say why in the feature log (its ID
  isn't reused). `mark-done` then closes the feature like a task.
- `multi-task` doesn't take features or subtasks. A `HUB-` feature follows the `HUB-` rules:
  its bookkeeping rides on the feature PR.

Statuses: `Todo` not started · `WIP` in progress (branch/PR open) · `Blocked` waiting on a
decision · `Usage-stopped` paused by usage limits · `Done` merged.
**On `TASK_BOARD.md` and `FEATURE_BOARD.md`** each Status is written as its icon + word,
exactly: `⏩ Todo` · `🟠 WIP` · `‼️ Blocked` · `🛑 Usage-stopped` · `🟢 Done`. Copy them from
here (`‼️` is two code points). The word is the Status, so "set `WIP`" anywhere means writing
`🟠 WIP` on the board. `TASK_LOG.md` and `log/<ID>.md` use the word alone.

For unattended/overnight runs (model choice, guardrails, kick-off/resume prompts) see
`OVERNIGHT.md`. Default lean: the cheapest model that reliably does the task; **S/M** tasks
only when unattended.

## Projects (research layer)

`projects/` is the strategic layer above the boards. It has one Markdown file per multi-month
research project, holding its goals, objectives, plans, todos and research log. It's mostly
for the owner, and structured so agents can read it and plan from it. Guide: `docs/PROJECTS.md`.
Commands: `new-project`, `plan-project`, `review-projects` (`COMMANDS.md`).

- **Files.** Each project is `projects/<descriptive-name>.md` (lowercase with hyphens, e.g.
  `urban-heat-islands.md`), made from `projects/TEMPLATE.md`. `projects/INDEX.md` is the
  portfolio, with one row per project.
- **IDs.**
  - Each project has a short uppercase ID in its metadata (`id: HEAT`): 2–8 capital letters or
    digits, unique, and never a tracked repo's prefix without its hyphen.
  - Inside a project: goals `G1`, objectives `O1`, work packages `WP1.1` (objective 1,
    package 1).
  - IDs never change and are never reused. Refer to another project's work as `HEAT WP1.2`.
- **The structure is fixed.** The metadata block and the `##` sections stay in the template's
  order, with one `### O<n> — …` subheading and one work-package table per objective.
  `check-board` checks this. Work-package statuses are `⏩ Todo` · `🟠 WIP` · `‼️ Blocked` ·
  `🟢 Done`.
- **Edits go straight to `main`** (in a branch-restricted session: the designated branch and
  its PR), or the owner edits by hand.
  - Update `updated:` on every change, and the project's `INDEX.md` row when its status,
    horizon or updated date changes.
  - Projects aren't tasks: they have no log, `TASK_LOG.md` row or board Status. The file is
    its own record.
- **Agents propose; the owner decides goals and objectives.** Never add, remove or reword them
  without asking them. Plans come from `plan-project`, which discusses the plan and waits for
  their go, like `plan-task`. The agreed plan goes under `## Plans`, newest first.
- **Code work** that a plan needs becomes tasks or features (`new-task`, `new-feature`), and
  their board IDs go in the work package's **Links** column. Links point one way only: board
  rows don't point back.
- **Private.** Project files are never copied to the public template; only `TEMPLATE.md` and a
  made-up example are.

## Subagents (delegating to cheaper models)

Claude Code and claude.ai/code can hand work to a **subagent** (the Agent/Task tool) and pick
its model per call. The main session keeps the plan, every judgment call, and **all commits,
pushes, PRs and bookkeeping**. Delegate only when it's cheaper than doing it yourself:

| Delegate | Model |
| --- | --- |
| Broad read-only search: find usages, locate config, survey a codebase | Haiku |
| Mechanical fan-out: `repo_stats.sh` over Tracked Repos (`refresh-overview`), one identical edit across all `repos/*/CLAUDE.md` | Haiku (Sonnet if the edit needs care) |
| Run tests / lint / a build and summarize the failures | Haiku |
| Draft tests or docs from a clear, written spec | Sonnet |

- **Every plan names its subagents.** Each sub-step of a `plan-task` or `run-task` plan says
  who does it: the main model, or a Haiku or Sonnet subagent. Delegation is decided up front
  and visible in the log.
- **Don't delegate** the plan, design decisions, anything that could be `Blocked`, **L** tasks,
  or small jobs. A subagent starts cold, so the handoff costs more than a quick edit.
- **Model by effort**, the same tiers as `OVERNIGHT.md` and `README.md`: **S** → Haiku for
  read-only or mechanical work, Sonnet when it edits code or needs judgment; **M** → Sonnet;
  **L** / design → stay on the main (capable) model while the owner is present.
- **Brief it fully:** paths, goal, what to return, and "don't commit or push". Run independent
  subagents in parallel.
- **Verify before using:** read the diff or re-run the check yourself before committing
  anything a subagent produced.
- **Unattended runs:** use few subagents; each one draws on the same usage budget.

## Memory

- **Per repo: `## Learnings`** in each master `repos/<name>/CLAUDE.md`. These are durable,
  repo-specific facts (build quirks, gotchas, repo-level `Decision:` lines). Written at
  `mark-done` from the log's `Learning:` lines. They reach the repo through the protocol's
  sync step at the start of its next task. Keep ~15 bullets at most; `scan-repo` prunes them.
- **Workflow: `DECISIONS.md`** in dev-hub. Dated one-liners recording why the workflow is the
  way it is. Add a line whenever the workflow changes, and read it before changing a rule.
- **Per task:** `log/<ID>.md` (Plan, Next step, notes) and its `TASK_LOG.md` row.

## Working rules here
- When asked to start a task, look it up in `TASK_BOARD.md`, then work in the **target
  repo** (clone it), not in this hub, but write the log entry back here.
- A repo's instructions are edited in its **dev-hub master** (`repos/<name>/CLAUDE.md`); the
  protocol's sync step propagates them into the repo. Don't hand-edit a repo's root copy.
- Keep `TASK_BOARD.md` and `TASK_LOG.md` current as tasks land. `python3 scripts/check_board.py`
  checks they agree with `log/`; CI runs it on every PR and push to `main`. A `check-board`
  rule lives in `COMMANDS.md` and in the script: change both together.
- **Commands** are defined in `COMMANDS.md`; run them when named.
  - **Board maintenance** (`add-repo <repo>`, `refresh-overview`, `scan-repo <name>`,
    `new-task <repo>`, `new-feature <repo>`, `check-board`) is driven by the **Tracked Repos**
    table. It's lightweight: branch + PR on dev-hub, no log or board Status.
  - **Projects** (`new-project`, `plan-project <ID>`, `review-projects`) work on `projects/`;
    see Projects above.
  - **Task lifecycle** (`plan-task <ID>…`, `run-task <ID>`, `multi-task <ID>…`,
    `pickup-task <ID>`, `mark-done <ID>…`) follows the task protocol above (batches: see
    Batches; features: see Features, where they also take feature and subtask IDs). Its
    bookkeeping goes straight to dev-hub `main`, or to the designated branch + a PR in a
    branch-restricted session (`HUB-` tasks: on the task PR).
- **Where it runs:** private repos, including dev-hub, are reachable from **claude.ai/code
  with the repo attached** (the reliable in-browser path), from **Claude Code**, or from a
  linked computer. The **Claude desktop app with the GitHub MCP server** can also read and
  write them through the GitHub API (bookkeeping, branches, commits, PRs), but it has no
  shell. So it can't clone, build or run tests: say so in the PR's "How it was tested", and
  leave tasks whose definition of done needs a build or tests to a surface with a shell. A
  **claude.ai Project in handback mode** reads dev-hub read-only (synced from `main`) and hands
  back zips + patches, following `templates/PROJECT_INSTRUCTIONS.md` (which also defines its
  `how-to` command). It runs tasks, batches, board maintenance and projects, but **not
  features**: a patch can't carry the merges a feature branch needs. Computer use can't type
  into terminals or IDEs, so it isn't a way to run git (see `docs/SURFACES.md`).
- **Plan first when present:** if asked to "plan &lt;command or ID&gt;", do the read-only part and
  propose the changes in chat with no commits; execute only on "go"/"run". That preview is
  ephemeral. `plan-task <ID>` also discusses first and always waits for the owner's go, but it
  saves the agreed plan to `log/<ID>.md` and starts the task. `run-task <ID>` is the path
  that doesn't wait: it writes its own plan, saves it, and goes to a draft PR (protocol step
  3).
- **Changing the workflow:** edit this file first, then the summaries (`README.md`, the
  guides in `docs/`, `COMMANDS.md`, the masters' compact protocol), and add a line to
  `DECISIONS.md` (its Where
  column is the PR's number and link; see the rules at its top).
- This repo is **private**. Do not add secrets or credentials regardless.
