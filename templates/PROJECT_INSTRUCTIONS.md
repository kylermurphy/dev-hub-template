# dev-hub in this Project (handback mode)

Chats in this Project can't push to GitHub. dev-hub (private) is synced read-only into
Project knowledge from `main`. Target repos must be public: they're cloned fresh each time
(a private target repo can't be worked on here). dev-hub's `CLAUDE.md` and `COMMANDS.md`
still govern every command, with the substitutions below.

## Work without asking
Carry every command straight through: checks, work, bookkeeping, `wc/` writes and handbacks.
Don't ask whether to proceed, offer options, or wait for "go". Stop only for:
- the PR confirmation before `mark-done` (see Finishing);
- a decision the task can't make (it becomes `Blocked`);
- another chat having the same repo `in progress`;
- a sync-check mismatch that needs the user.

## Working copy (Project docs, shared by every chat in this Project)
- `wc/dev-hub/<path>` is this mode's dev-hub `main`. Copy-on-write: a file enters `wc/` the
  first time it changes. Read `wc/` first, the synced copy otherwise. Re-read a `wc/` doc
  right before writing it, since another chat may have changed it.
- The synced copy can only be read in fragments, so a file's first `wc/` copy is rebuilt from
  them. Say so in the handback for any file copied for the first time.
- A target-repo branch lives in `wc/<repo>/<branch>/` as patches + `PR.md`. Rebuild it by
  cloning the repo and applying the patches.
- `wc/LEDGER.md` has two sections:
  - **Sync snapshot**: from the last sync check, the date, the Project's knowledge size, and
    each synced dev-hub file's document ID.
  - **Log**: one row per action, with date · command/ID · repo(s) · files · status.
    Statuses: `in progress` · `stopped` · `awaiting confirmation` (the three **unfinished**
    ones) · `handed back` · `synced`.

## Starting any dev-hub work (every time, in this order)
**1. Unfinished work.** 🚩 List every unfinished ledger row under a red-flag warning that
unfinished tasks can leave the repos and the board inconsistent. If another chat has the same
repo `in progress`, ask the user before touching it.

**2. Has dev-hub been synced since the last snapshot?** Compare the snapshot's document IDs
with the current ones: a changed ID means that file's content changed; also note files added
or removed. **The IDs decide.** Knowledge size is only a hint, because the `wc/` docs count
toward it too.
- Nothing changed → say "dev-hub unchanged since <snapshot date>" in one line and go on.
- No snapshot yet (first run) → record one and go on.

**3. If anything changed, check that everything agrees** before running anything. Report
what changed, then each mismatch with how to fix it:
- **Handbacks.** `handed back` work now in the synced copy → delete its `wc/` files and set
  the rows to `synced`. Still missing → the user commits it and re-syncs.
- **Outside edits.** A changed file that also has pending `wc/` edits → merge and show the
  result. Anything that can't be merged cleanly waits for the user's decision.
- **Rule changes.** If `CLAUDE.md`, `COMMANDS.md`, `templates/` or a `repos/*/CLAUDE.md`
  master changed, summarize the new rules. Flag pending `wc/` work or handbacks that no longer
  follow them, and any line of these Project instructions they contradict (the user updates
  the instructions).
- **Board consistency.** Run the `check-board` checks on the synced board, merged with `wc/`.
- **Confirmed PRs.** A task marked `Done (PR confirmed …)` whose target-repo `main` still
  lacks the change → the user merges the PR, or reopens the task (`pickup-task`) if the PR
  changed or was closed.

**4. Record a new snapshot**, then run the command (or wait, if a fix needs the user).

## Substitutions
- Bookkeeping "straight to dev-hub `main`" → write to `wc/dev-hub/`.
- Target-repo branch + draft PR → patches + `PR.md` in `wc/<repo>/<branch>/`. The user opens
  the PR after the handback.
- Board maintenance `chore/` branch + PR → `wc/dev-hub/` + PR text (with the branch name).
- `mark-done` merge check → the user's confirmation of the PR. Record it as
  `Done (PR confirmed <date>)` in `TASK_LOG.md` and as `(PR confirmed <date>)` on the log's
  PR line. The board Status is `Done`.

## Finishing a task or maintenance command
1. Show the changes and the `PR.md` / PR text. Ask the user to confirm the PR looks good.
2. On confirmation, say "Running `mark-done <ID>`" and run it in `wc/` (tasks only).
3. Hand back **one zip per repository**. Each zip holds:
   - the changed files at their repo paths;
   - a `.patch`;
   - the PR text and branch name (target repos, board maintenance), or the commit message
     (dev-hub task bookkeeping, which goes straight to `main`);
   - a list of files to delete, if any.

   Also send each `.patch` **as its own file**, named `<repo>-<ID or command>.patch`, so it
   can be grabbed without the zip.
4. Give simple instructions: which repo and branch each batch goes to, and what happens next.
   **Print the steps from "Applying a patch" below, in full**, for every repo, both in chat
   and in each zip's `README.md`. Use the real branch name and patch filename.
5. Set the ledger rows to `handed back`. The next sync check that finds them in dev-hub
   closes them out.

## Unfinished work
- Only finished work is handed back: a task is finished once its PR is confirmed and
  `mark-done` has run. If a task stops (`Blocked`, `Usage-stopped`, cut off), say so in chat at
  once and resolve it here: answer the question, then `pickup-task`.

## `how-to` (command)
When the user says `how-to`, print the guide below as written. It isn't dev-hub work, so skip
the checks.

> **How this Project works (handback mode)**
> Claude runs dev-hub tasks here but can't push to GitHub. Claude does the work; you commit it.
>
> **The loop**
> 1. Name a task or command: `do task EX-4`, `plan-task EX-4`,
>    `multi-task EX-4 EX-5`, `scan-repo example-repo`.
> 2. Claude checks for unfinished work (🚩) and whether dev-hub changed since the last run.
> 3. Claude clones the repo, does the work, keeps the bookkeeping in the Project's working
>    copy (`wc/`), and shows you the PR.
> 4. You reply "looks good". Claude runs `mark-done` and hands back one zip + one `.patch`
>    per repo.
> 5. You apply the patches, push, open the PR, and re-sync the Project's dev-hub source.
>
> **Example**
> - You: `do task EX-4`
> - Claude: "No unfinished work · dev-hub unchanged since <date>." … "Here's the PR for
>   `example-repo`. Look good?"
> - You: `looks good`
> - Claude: "Running `mark-done EX-4`." Handback: `example-repo-EX-4.patch`, `dev-hub-EX-4.patch`
>   (plus a zip for each).
>
> **Applying a patch is one command.** In GitHub Desktop: open the repo, pull `main`, then
> create the PR's branch (target repo) or stay on `main` (dev-hub). Then Repository →
> **Open in Command Prompt**:
> ```
> git am path_to_patch/example-repo-EX-4.patch
> ```
> Push, and you're done: the patch recreates the commits with their messages. If it fails,
> run `git am --abort` and upload the zip's files instead.
>
> **Good to know**
> - Keep each chat to one repo. For several tasks in one repo, use `multi-task`.
> - Only finished work is handed back. Anything unfinished is flagged 🚩 at the start of
>   every chat.
> - Re-sync the Project after committing; the next chat checks that it landed.
> - If a build or test can't run here, its checks are left in the PR for you.

## Applying a patch (user; printed with every handback)
1. **Open the repo in GitHub Desktop.** Pull `main`, then switch to the right branch:
   - target repo: create the branch named in `PR.md`, from `main`;
   - dev-hub task bookkeeping: stay on `main`;
   - board maintenance: create the `chore/` branch named in the PR text, from `main`.
2. **Open a command line there:** Repository → **Open in Command Prompt**.
3. **Apply the patch**, one command on its own line, with the full path to the downloaded file:
   ```
   git am path_to_patch/<repo>-<ID or command>.patch
   ```
4. **Push** in GitHub Desktop, and open the PR if there is one.

If it fails with "previous rebase directory … still exists", an earlier attempt stopped partway.
Clear it, then repeat step 3:
```
git am --abort
```
If a patch doesn't apply (dev-hub `main` moved, or a first-copy file differs slightly), run
`git am --abort` and upload the files from the zip instead. Do the same on the GitHub website.
