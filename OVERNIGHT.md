# Running tasks while away / overnight

Setup assumed: a Claude **subscription** (Pro/Max), runs **kicked off manually before bed**,
leaning on the **cheapest model that works**. This guide keeps overnight runs from (a) losing
work if the budget runs out and (b) eating into the next workday's allowance.

## Two limits to respect (subscription)

These numbers are **(Claude-specific)**: a Claude subscription's limits. On another plan or
agent, substitute your own (see [`ADAPTING.md` → Usage
limits](ADAPTING.md#3-usage-limits-overnightmd)).

- **5-hour session window** — resets ~5 hours after it starts. This is your daytime
  protection: finish overnight runs a few hours before you start work and the window refills
  on its own.
- **Weekly limit** — resets on a fixed day/time. This is the one heavy overnight work can
  erode across several nights; the guardrails below protect it.

Usage is driven by model, effort level, conversation length, and features like extended
thinking and web search (see Sources).

## Guardrails for an overnight run

- **Model:** cheapest that works — a fast model (Haiku/Sonnet-class), not Opus. Reserve
  Opus/Fable for L / design tasks done while you're present.
- **Effort:** lower the effort level for routine tasks; turn off extended thinking and web
  search when the task doesn't need them.
- **Scope:** only **S / M** tasks overnight. L tasks need a decision from you — don't queue them.
- **One task per run, or one `multi-task` batch** of up to 5 **S** tasks in the same repo
  (one branch, one PR). Don't let one session try to clear the whole board; that's how a
  marathon session blows the weekly cap. An S/M **feature subtask** counts as one task
  (`pickup-task <subtask ID>`); planning a feature (`plan-task <feature ID>`) needs you there.
- **Finish early:** aim to wrap a few hours before your workday so the session window resets.
- **Stop cleanly:** if you stop for budget, set Status `Usage-stopped` with a current
  `Next step`; on a **When to stop and ask** rule (dev-hub `CLAUDE.md`), set `Blocked` with the
  question. Either way `pickup-task` resumes it.
- **Where to run:** claude.ai/code with the target repo **and** dev-hub attached (both are
  written to), or Claude Code. A Claude Project (handback mode) can't push and stops for your
  PR confirmation before `mark-done`, so it doesn't suit unattended runs. The
  Claude desktop app with the GitHub MCP server can push, but it has no shell (no builds or
  tests) and needs the machine on, so it's a poor fit for overnight runs.
- **Branch-restricted session?** Then the dev-hub bookkeeping lands in a PR from the
  session's designated branch, not on `main`. In the morning, look for that dev-hub PR (and
  the target-repo PR) and merge it to close the task out (`CLAUDE.md` → Branch-restricted
  sessions).

## Model tier by effort

| Effort | Lean | Examples |
| --- | --- | --- |
| S | Fast (Haiku/Sonnet) | hygiene, docs, dep bumps, add CI, move files |
| M | Mid (Sonnet) | test suite, refactor, packaging |
| L | Capable (Opus/Fable), **while present** | calibration module, validation study, design calls |

## Kick-off prompt (paste before bed)

> Work on dev-hub task **<ID>** only: `run-task <ID>` (plan it yourself; don't wait for me).
> Follow the task protocol in dev-hub's `CLAUDE.md`. The target repo's `CLAUDE.md` is a copy of
> its dev-hub master with a short summary; if the copy is missing or out of date, use dev-hub's.
> Branch `task/<ID>-<slug>`, and **persist the plan to `log/<ID>.md` before doing heavy work**,
> naming who does each step. Commit and push as you go, and keep `log/<ID>.md` updated with
> **Status** and a **Next step** after each step. If a `task/<ID>` branch or `log/<ID>.md`
> already exists, use `pickup-task <ID>` and resume from Next step instead of restarting. If
> you hit a **When to stop and ask** rule (dev-hub `CLAUDE.md`), set Status `Blocked` and
> record the question under `## Blocked / open questions`. **If you stop for budget, set Status
> `Usage-stopped`.** Use the cheapest model that can do this reliably.

**Batch variant** (several S tasks, one PR):

> Run `multi-task <ID> <ID> …` (dev-hub, unattended). Follow dev-hub's `CLAUDE.md` → Batches
> (the target repo's `CLAUDE.md` is only a copied summary; if it's missing or out of date, use
> dev-hub's): one branch `task/<ID>+<ID>+…-<slug>` and one draft PR, a short plan per task
> saved to each `log/<ID>.md` before the work, and commits prefixed with their task ID. If one
> task hits a **When to stop and ask** rule (dev-hub `CLAUDE.md`), revert it, set it `Blocked`
> with the question, and finish the rest. If you stop for budget, set the unfinished tasks `Usage-stopped`. Use the
> cheapest model that can do this reliably.

(With a repo name instead of IDs, `multi-task <repo>` takes Claude's proposed batch
unattended.)

## Resume next morning

> `pickup-task <ID>`: read `log/<ID>.md` and the `task/<ID>` branch, continue from **Next
> step**, and finish per the definition of done.

If the task is `Blocked`, answer the open question in the same message so `pickup-task` can
proceed. For a batch, `pickup-task` on any of its IDs resumes the whole batch; a
task dropped from it as `Blocked` resumes on its own.

## If a run stops mid-task

Nothing is lost: the branch holds the commits and `log/<ID>.md` holds the Plan, Status and
Next step. A run that stopped cleanly shows `Blocked` or `Usage-stopped`. One cut off abruptly
may still say `WIP`, which is fine: a `WIP` task with a `task/<ID>` branch is resumable. Start
a fresh run with `pickup-task <ID>` (the resume prompt above). `TASK_BOARD.md` and
`TASK_LOG.md` show what's in flight.

## Sources
- [What is the Max plan?](https://support.claude.com/en/articles/11049741-what-is-the-max-plan)
- [Usage limit best practices](https://support.claude.com/en/articles/9797557-usage-limit-best-practices)
- [What is a limit reset?](https://support.claude.com/en/articles/17007452-what-is-a-limit-reset)
- [How do usage and length limits work?](https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work)
