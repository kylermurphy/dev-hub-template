# Commands

Named, on-demand operations. Trigger one by naming it in any session, e.g. "add-repo
owner/name", "run refresh-overview", "scan-repo example-repo", "plan-task EX-2",
"multi-task EX-3 EX-4", "mark-done EX-2".

**Cheat-sheet.** *Board maintenance:* `add-repo <repo>` · `refresh-overview` ·
`scan-repo <name>` · `new-task <repo>` · `check-board` — *Task lifecycle:*
`plan-task <ID>…` · `multi-task <ID>… | <repo>` · `pickup-task <ID>` · `mark-done <ID>…`.
Prefix any of them with `plan` for a dry run.

There are two kinds of command:

- **Board maintenance** (`add-repo`, `refresh-overview`, `scan-repo`, `new-task`,
  `check-board`) is **lightweight**. Each run makes a `chore/…` branch on dev-hub and opens a
  PR with a short note. It does **not** create a `log/<ID>.md`, a `TASK_LOG.md` row or a board
  Status, because these commands maintain the board rather than doing a task. They never commit
  to `main`. **Branch-restricted session?** Use the designated branch instead of a `chore/…`
  one, with the same PR rules (always open, never self-merged; see *Branch-restricted
  sessions* under Task lifecycle).
- **Task lifecycle** (`plan-task`, `multi-task`, `pickup-task`, `mark-done`) operates on
  **one task**, or on a **batch** of simple tasks sharing one PR, and follows the full task
  protocol (`CLAUDE.md` → Task protocol). Code goes on a
  `task/<ID>-<slug>` branch + PR in the **target repo**. The task's dev-hub bookkeeping
  (`log/<ID>.md`, its `TASK_LOG.md` row, its board Status) is committed **straight to dev-hub
  `main`**, so the current state is always on `main` for the next session to read. That
  bookkeeping is the only thing ever committed to `main`. **Branch-restricted session?**
  Then it goes on the designated branch with a PR into `main` instead (see *Branch-restricted
  sessions* under Task lifecycle). **`HUB-` tasks** (dev-hub itself) put it on their task PR
  (`CLAUDE.md` → dev-hub's own tasks).

Board maintenance commands read the **Tracked Repos** table in `TASK_BOARD.md`, the single
list of repos available to work on. `add-repo` appends to it, and you can also edit it by
hand. Set a row's **Tracking** to `paused` to skip it. `new-task` just needs the repo name.

Onboarding a repo end to end: `add-repo <repo>` → `refresh-overview` → `scan-repo <name>`.
A task end to end: `plan-task <ID>` → implement → PR merges → `mark-done <ID>`
(`pickup-task <ID>` to resume a stopped one). A batch: `multi-task <ID> <ID> …` (or
`plan-task <ID> <ID> …` to agree a plan first) → one PR merges → `mark-done <ID> <ID> …`.

**Where they run** (details: `README.md` → Surfaces and access). Reading and analysis work
from any session: public repos clone anywhere and `repo_stats.sh` runs in the cloud. Pushing
to a **private** repo, including dev-hub itself (every command here writes to dev-hub), needs
a session that can reach it:

- **claude.ai/code with the repo attached**: the reliable in-browser path.
- **Claude Code** on the machine, or a computer linked to an app chat: uses the owner's own git
  credentials.
- **The Claude desktop app with the GitHub MCP server**: reads and writes through the GitHub
  API, so every command's dev-hub commits and PRs work. It has no shell, so
  `refresh-overview`'s `repo_stats.sh` can't run; take the facts from the GitHub API instead
  (commits, dates, files).
- **A claude.ai Project in handback mode**: reads dev-hub read-only (synced from `main`) and
  can't push. Commands run against a working copy in the Project's docs and come back as
  per-repo zips + patches for the owner to commit, following `templates/PROJECT_INSTRUCTIONS.md`.

## Plan first (dry run)

Any command or task can be **previewed before it runs**. Prefix it with `plan`, e.g.
"plan scan-repo example-repo" or "plan EX-2". Claude does only the read-only part (clone, inspect,
propose the changes or an implementation approach, with open questions) and makes **no
branch, commit, or PR**. The preview is ephemeral; nothing is saved. Review and adjust, then
say "run" / "go" to execute for real. Plan-first is the natural mode when you're present;
unattended runs skip it and **go to a draft**.

Not the same as **`plan-task <ID>`**, which *saves* the finalized plan to `log/<ID>.md` and
starts the task (see Task lifecycle).

---

## Board maintenance

### add-repo &lt;repo&gt;

Add a repo to the **Tracked Repos** table — the first step in onboarding a repo. It only
touches Tracked Repos; run `refresh-overview` then `scan-repo <name>` afterward to fill the
overview and build the task table.

Input: a repo URL, `owner/name`, or bare name (defaults to `github.com/<owner>/<name>`, where
`<owner>` is the `DEVHUB_OWNER` environment variable or the owner of this hub; ask if unsure).

**Steps**
1. Branch `chore/add-repo-<name>-<date>` on dev-hub.
2. If the repo is already in Tracked Repos, stop (or update its row) — never add a duplicate.
3. Fill the row:
   - **Repo** = the repo name; **URL** = the full GitHub URL.
   - **Visibility** = `public` or `private` — detect by trying an anonymous clone; if that
     fails but an authenticated one succeeds, it's `private`. Ask if it can't be determined.
   - **Prefix** = a short, UPPERCASE task-ID prefix ending in `-`, **unique** across Tracked
     Repos (derive from the name, e.g. `example-repo` → `EX-`; on a clash, pick a distinct variant
     and confirm).
   - **Tracking** = `active`.
   - **Notes** = a short one-line description (from the owner, or inferred).
4. Append the row to Tracked Repos.
5. Open a PR: `chore: track <name>`.

**Then:** run `refresh-overview` (fills its Overview row) and `scan-repo <name>` (builds its
task table + `CLAUDE.md` master).

---

### refresh-overview

Fill/refresh the **Repo Overview** table from Tracked Repos. Overview only — it does not touch
task tables or any `CLAUDE.md`.

**Steps**
1. Branch `chore/refresh-overview-<date>` on dev-hub.
2. For each `active` repo in Tracked Repos, run `scripts/repo_stats.sh <url>` (clones it and
   prints commits, first/last dates, extensions, CI/tests/packaging).
3. Rewrite the Repo Overview table — one row per active repo: Purpose (from its README /
   judgment), Commits, Last active (e.g. "May 2026"), Stack, State (e.g.
   "Alpha · no tests · no CI"). Order by commit count, descending.
4. Update the "last refreshed <date>" line under the heading.
5. Open a PR: `chore: refresh Repo Overview (<date>)`.

**Notes**
- A repo whose clone fails (private, no GitHub access) keeps a row with State
  "unreachable — needs GitHub access" rather than being dropped.
- `paused` repos are skipped; leave any existing row and mark its State "paused".

---

### scan-repo &lt;name&gt;

Identify candidate tasks for **one** repo and update its task table. **Append & preserve** —
existing rows, IDs, and Status are kept; only genuinely new candidates are added.

**Steps**
1. Branch `chore/scan-<name>-<date>` on dev-hub.
2. Clone the repo; read its README, structure, tests, CI, dependencies, and in-code
   `TODO`/`FIXME` markers. `scripts/repo_stats.sh <name>` gives the mechanical facts.
3. If the repo has no `## <name> — <PREFIX>-` section yet, create one (using the **Prefix**
   from its Tracked Repos row), placed by commit count among the other sections, and seed its
   `repos/<name>/CLAUDE.md` master from an existing one (in a fresh hub, from
   `examples/example-repo/CLAUDE.md`, dropping its "Example only" note and its Learnings):
   same sections, an empty `## Learnings`, and the compact task protocol. Otherwise read the
   existing table. Every repo gets its own section; there's no shared table.
4. Propose candidate tasks. For each **new** one, append a row with the next ID in the repo's
   series, Status `Todo`, plus Type, Effort (S/M/L), and a concrete Definition of done.
   **Do not** modify, reorder, or renumber existing rows, and never reuse an ID.
5. Refresh the repo's `CLAUDE.md` master with anything the scan learned (build/test commands,
   gotchas). The master is the source of truth. Also **prune `## Learnings`**: drop items that
   are no longer true, and move settled ones into the proper section (Commands, Conventions &
   gotchas) so the list stays short (~15 max).
6. Open a PR: `chore: scan <name> — N new tasks (<date>)`, listing the new IDs.

**Notes**
- Keep each Definition of done testable — the row is the task's acceptance test.
- If unsure whether a candidate is worth adding, add it as `Todo` with a short note rather
  than dropping it; you can prune on review.

---

### new-task &lt;repo&gt;

Add a single, hand-specified task to a repo's table — a convenience wrapper around editing the
table yourself.

**Steps**
1. Branch `chore/new-task-<repo>-<date>` on dev-hub.
2. Take the task description the owner provides. Assign the **next ID** in the repo's series (never
   reuse one), Status `Todo`, and infer Type and Effort (S/M/L).
3. Write a concrete, testable **Definition of done** (ask if the intent is ambiguous).
4. Append the row to that repo's table — don't touch other rows.
5. Open a PR: `chore: add <ID> to <repo> (<date>)`.

**Or just edit the table:** add a row with the next ID, Status `Todo`, and the columns
`| ID | Status | Task | Type | Effort | Definition of done |`. The command only saves you the
ID lookup, formatting, and PR.

---

### check-board

A lightweight consistency check of the board. It changes nothing except what's needed to open
the report PR.

**Steps**
1. Branch `chore/check-board-<date>` on dev-hub.
2. Check, against **Tracked Repos** as the source of truth:
   - every `active` repo has its own `## <name> — <PREFIX>-` section and a
     `repos/<name>/CLAUDE.md` master (except `dev-hub`, whose instructions are its root
     `CLAUDE.md`);
   - no **orphans**: no task section or `repos/<name>/` master for a repo that isn't in
     Tracked Repos;
   - `TASK_LOG.md` rows are newest first;
   - **Prefixes** in Tracked Repos are unique, and every task ID uses its repo's prefix;
   - **task IDs** are unique across the whole board;
   - every **Status** is one of `Todo`, `WIP`, `Blocked`, `Usage-stopped`, `Done`
     (`TASK_LOG.md` may record `Done (merged <date>)` or, from handback mode,
     `Done (PR confirmed <date>)`);
   - every `WIP` / `Blocked` / `Usage-stopped` / `Done` task has a `log/<ID>.md` and a
     `TASK_LOG.md` row, and each log's `Status` matches the board;
   - **batches** agree: every ID on a log's `Batch:` line lists the others back, and all
     (except ones marked "dropped from batch") share the same branch and PR.
3. Open a PR `chore: check-board (<date>)` with the findings in the PR body: one line each,
   or "no issues found". If the board itself needs no change, commit the report as
   `log/check-board-<date>.md` so the PR has something to carry.

**Notes**
- Report only. Fix findings with the normal commands (or by hand) after review, never inside
  `check-board`.


---

## Task lifecycle

These operate on **one task** (or, for `multi-task` and a multi-ID `plan-task`, a **batch**:
see `CLAUDE.md` → Batches) and follow the full task protocol: a `task/<ID>-<slug>` branch +
PR in the target repo, the target repo's `CLAUDE.md` synced from its dev-hub master as that
branch's first commit, a PR description that follows dev-hub's
`templates/PULL_REQUEST_TEMPLATE.md`, and `log/<ID>.md` + `TASK_LOG.md` + board Status kept
current on dev-hub `main`.

**`HUB-` tasks** (dev-hub itself; `CLAUDE.md` → dev-hub's own tasks): the branch is in
dev-hub, the sync step is skipped, and every bookkeeping step below commits to the **task
branch** instead of `main`, so it lands when the task PR merges. `mark-done` still commits
`Done` straight to `main` after that merge.

**Branch-restricted sessions.** If the session is pinned to one designated dev-hub branch, every
bookkeeping step below commits to that branch instead of `main`, following `CLAUDE.md` →
**Branch-restricted sessions**:
- merge `origin/main` into the branch first; if its previous PR already merged, restart the
  branch from `origin/main` and open a new PR;
- after pushing, make sure a PR from the branch into `main` is **open**: open it, or update
  the open one's title/body to cover every task on it. **Never merge it yourself**;
- say so in chat the first time it happens for a task: the task isn't fully closed out until
  that PR merges;
- if another bookkeeping PR merged first and this one conflicts, merge `main` in and keep both
  sides.

Statuses: `Todo` not started · `WIP` in progress (branch/PR open) · `Blocked` waiting on a
decision · `Usage-stopped` paused by usage limits · `Done` merged. Only `mark-done` sets
`Done`.

### plan-task &lt;ID&gt; [&lt;ID&gt; …]

Produce a plan for a task and **persist** it, so the plan survives the session. **With several
IDs** it's the planned version of `multi-task`: agree one plan for the whole set in chat,
then save each task's part to its own log and run the set as a batch (see *Several IDs*
below).

**Steps**
1. Look up `<ID>` on `TASK_BOARD.md`; read the repo's `repos/<name>/CLAUDE.md` master and
   clone the repo. If `log/<ID>.md` or a `task/<ID>-…` branch already exists, use
   `pickup-task <ID>` instead.
2. **Discuss and refine** the plan in chat: approach, sub-steps, risks, open questions.
   (Unattended: draft the plan yourself and go straight on.)
3. **On finalize:**
   - Create `task/<ID>-<slug>` off the target repo's default branch and make its first commit
     the instructions sync (`CLAUDE.md` from its master; protocol step 2; skipped for `HUB-`).
   - In dev-hub, create `log/<ID>.md` from `log/TEMPLATE.md` with **`## Plan`** (the
     finalized plan), **`## Checklist`** (its steps) and **`## Next step`** filled in, and
     `Status: WIP`. Add the task's `TASK_LOG.md` row (at the top) and set its board
     Status → `WIP`.
     Commit `log: <ID> plan` and push to dev-hub `main`. This is the task's first dev-hub
     commit, made before any heavy work. (Branch-restricted: push to the designated branch
     and open/update its bookkeeping PR, as above. `HUB-`: commit it to the task branch.)
4. Then **implement** per the plan (a draft PR in the target repo, log kept current as you
   go), or **stop here** if only planning was asked. `Next step` then says "implement step 1"
   and `pickup-task <ID>` continues from it.

**Several IDs.** Check the batch rules first (same repo, all `Todo`, no **L**, ≤ 5; see
`multi-task`). Step 2 discusses the set as a whole: order, shared changes, risks. On finalize,
do `multi-task` steps 2–4 with the agreed plan written into each task's `## Plan` instead of
the short one. Then implement (`multi-task` steps 5–6), or stop after saving if only planning
was asked (every task stays `WIP`, and `pickup-task` on any of the IDs continues the batch).

`plan-task` saves the plan and starts the task. The `plan <anything>` prefix is an ephemeral
preview that saves nothing.

### multi-task &lt;ID&gt; &lt;ID&gt; … | &lt;repo&gt;

Do several simple tasks **in one pass: one branch, one PR**. This is the quick path, with a
short plan per task. For a batch that needs discussion first, use `plan-task <ID> <ID> …`.
Rules: `CLAUDE.md` → **Batches**.

**Steps**
1. **Pick the batch.**
   - IDs given → check them: all in the **same repo**, all `Todo`, no **L**, **at most 5**. If
     any fails, stop and say which, e.g. "EX-6 is L" or "split into one batch per repo".
   - Repo given → propose up to 5 of its `Todo` **S** tasks and confirm with the owner
     (unattended: take the proposal).
   - Order the tasks so dependencies come first.
2. **Branch** `task/<ID>+<ID>+…-<slug>` off the target repo's default branch, e.g.
   `task/EX-3+EX-4+EX-5-cleanup`. The first commit is the instructions sync, once.
3. **Bookkeeping (one commit, `log: <ID>, <ID>, … batch start`).** For each task:
   - `log/<ID>.md` from the template, with a short **Plan** (a few lines), Checklist, Next
     step, `Status: WIP` and a **`Batch:`** line (`<sibling IDs> · <branch> · <PR once open>`);
   - a `TASK_LOG.md` row at the top (all rows share the branch, then the PR);
   - board Status → `WIP`.

   Push to dev-hub `main` (branch-restricted: the designated branch + its bookkeeping PR;
   `HUB-`: the task branch).
4. **Open the draft PR early** (after the first task's commits), titled
   `<ID>, <ID>, …: <summary>`, and add its link to every log and `TASK_LOG.md` row.
5. **Work task by task, in order.** Commits are prefixed with the task ID (`EX-3: …`). Run
   the repo's checks after each task. Tick that task's checklist and update the `Next step`
   of the remaining tasks (e.g. "batch: EX-5 next").
   - **A task hits a decision you can't make** → `git revert` its commits on the branch, set
     it `Blocked` with its question under `## Blocked / open questions`, mark its `Batch:`
     line "dropped from batch", and carry on with the rest. It resumes later on its own.
   - **Stopping for budget** → every unfinished task becomes `Usage-stopped` (the finished
     ones stay `WIP`). `pickup-task` on any ID resumes the batch.
6. **Finish the PR body** per dev-hub's PR template: every ID under Task, then **one section per
   task** (what changed and why, how tested, its definition-of-done checklist), and any
   dropped task with its reason. Update the bookkeeping (Next step → "awaiting review/merge").

After merge: `mark-done <ID> <ID> …` (or `mark-done` on any one ID and accept closing the
batch).

### pickup-task &lt;ID&gt;

Resume an unfinished task: `Blocked`, `Usage-stopped`, or any `WIP` with an existing task
branch (`task/<ID>-…`, or a batch branch `task/…+<ID>+…`). **A batch member resumes the
whole batch**: read every sibling log on its `Batch:` line and continue with the unfinished
ones (a task "dropped from batch" resumes on its own, on a new `task/<ID>-…` branch).

**Steps**
1. Read `log/<ID>.md` on dev-hub `main`, or from its open bookkeeping PR's branch if an
   earlier branch-restricted session left changes unmerged (`HUB-`: from the task branch)
   (**Plan**, **Checklist**, **Next step**, **Blocked / open questions**) and check out the
   task's branch in the target repo (`git log` shows what's committed). If the branch has
   commits the log doesn't mention, trust the branch and update the log.
2. If it was **`Blocked`**, confirm the blocker is resolved (the owner's answer in chat, or a
   recorded decision) **before proceeding**. If it isn't, stop and leave it `Blocked`.
3. Set Status → `WIP` (log + board, pushed to dev-hub `main`, or to the designated branch +
   bookkeeping PR if branch-restricted, or to the task branch for `HUB-`), clear the resolved
   items from `## Blocked / open questions`, and **continue from Next step** to a draft/PR,
   keeping the log current as you go.
4. If it stops again, use the protocol's stop states (`Blocked` / `Usage-stopped`) with a
   current `Next step`.

### mark-done &lt;ID&gt; [&lt;ID&gt; …]

Close out a finished task. This is the **single Done mechanism**: nothing else sets `Done`.
Run it right after the task's PR merges. It pushes directly to dev-hub `main` (no branch, no
PR). **In a branch-restricted session** it commits to the designated branch instead and must
**guarantee a PR into `main` is open** before it finishes (step 6).

Input: one or more task IDs, e.g. `EX-1` or `EX-3 EX-4 EX-5`. For a `HUB-` task, its
WIP bookkeeping arrived on `main` with the merged task PR; `mark-done` then works as below.
**Batches:** if a given ID's log has a `Batch:` line, offer to close the whole batch (all
siblings not "dropped from batch"). Then run the steps once for the set: one merge check (they
share the PR), every task updated in step 4 (learnings promoted per task), and **one** commit
`log: <ID>, <ID>, … done`.

**Steps**
1. Sync: check out dev-hub `main` and pull the latest (`git pull origin main`).
   **Branch-restricted:** check out the designated branch and merge `origin/main` into it. If
   the branch's previous PR has already merged, restart it from `origin/main` (same name).
   Read the task's log from this branch, or from another open bookkeeping PR's branch if
   its WIP commit hasn't merged yet.
2. Find the ID's row in its repo's section of `TASK_BOARD.md`. If there
   is no such row, stop and say so. If it's already `Done`, report that and make no commit.
   Under the fallback, still do step 6 if the `Done` commit is sitting on a branch with no
   open PR.
3. **Merge check.** Read the PR link from `log/<ID>.md` (or the `TASK_LOG.md` row) and check
   that the PR is merged.
   - Merged → continue, using its merge date.
   - Open / closed unmerged, or no PR (patch handback) → stop and ask; proceed only on
     "mark-done &lt;ID&gt; anyway", using today's date.
   - **Claude Project (handback mode):** the owner's confirmation of the PR replaces the merge
     check, since they open and merge it themselves. Record `Done (PR confirmed <date>)` in
     `TASK_LOG.md` and `(PR confirmed <date>)` on the log's PR line
     (`templates/PROJECT_INSTRUCTIONS.md`).
4. Update:
   - **`TASK_BOARD.md`**: the row's Status → `Done`. Touch nothing else in the row.
   - **`TASK_LOG.md`**: the task's row Status → `Done (merged <date>)`. If there's no row,
     add one at the top (newest first) with what's known.
   - **`log/<ID>.md`**: `Status: Done`, PR line marked `(merged <date>)`, `Updated: <date>`,
     remaining checklist items ticked, `## Blocked / open questions` emptied, **Next step** →
     `None — task complete.` If the log doesn't exist, create a minimal one from
     `log/TEMPLATE.md` and note that it was back-filled.
   - **Promote learnings** into `repos/<name>/CLAUDE.md` → `## Learnings` (for `HUB-`
     tasks, add workflow decisions to `DECISIONS.md` instead):
     - add each `Learning:` line from the log's `## Notes / follow-ups`, tagged `(<ID>)`;
     - skip anything already covered in the master, and fix or remove any bullet this task
       made untrue;
     - keep it to ~15 bullets. If there's nothing durable, skip this step and say so.

     The change reaches the target repo at its next task's sync step; nothing is pushed to
     the target repo now.
5. Commit `log: <ID> done` and `git push origin main`.
   **Branch-restricted:** push to the designated branch instead
   (`git push -u origin <branch>`).
6. **Branch-restricted only: guarantee the PR.** Look for an open PR from the designated
   branch into `main`.
   - **None open** → open one. Title: `Log <ID>: bookkeeping (<from> → Done)`. Body:
     - **dev-hub bookkeeping only, no code changes**;
     - why it's on a branch (the session is branch-restricted);
     - what each commit on the branch changed and why (usually the earlier WIP commit plus
       this `mark-done` commit);
     - "How it was tested: N/A";
     - that the definition of done was verified in the target-repo PR (link);
     - that **merging this PR is what lands the change on `main`**.
   - **Already open** (e.g. from an earlier task in this session) → update its title to
     cover every task on it (`Log EX-1, EX-2: bookkeeping`) and add this task's section
     to the body.
   - **Never merge it yourself.** Tell the owner in chat: the PR link, and that the task isn't fully
     closed out until it merges. `mark-done` isn't finished until this PR exists.

**Notes**
- Only the fields above change (plus the master's `## Learnings`). Never edit a task's
  description or Definition of done here.
