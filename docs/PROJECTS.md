# Projects

A **project** is a multi-month research initiative: the science behind the code work. Each one
is a Markdown file in [`projects/`](../projects/) holding its background, science goals,
objectives and work packages, research plans, todos, references, decisions and a research log.
Projects are mostly for you, and they're structured so agents can read them and plan from them.
The rules are in [`CLAUDE.md`](../CLAUDE.md) → Projects, and the commands in
[`COMMANDS.md`](../COMMANDS.md) → Projects.

## Three levels of work

| Level | Answers | Horizon | Lives in | Guide |
| --- | --- | --- | --- | --- |
| **Project** | why: the science question and what counts as success | months | `projects/<name>.md` | this one |
| **Feature** | what code, built as a whole on one branch | days to weeks | `FEATURE_BOARD.md` | [`FEATURES.md`](FEATURES.md) |
| **Task** | how: one self-contained change | about a session | `TASK_BOARD.md` | [`TASKS.md`](TASKS.md) |

A project's work packages link down to the tasks and features that do their code work, by board
ID (`EX-7`, `EX-FA`). The boards don't link back up, so the only place to update is the
project. Research that isn't code (reading, analysis, writing) stays in the project as work
packages and next actions.

## The files

- **`projects/INDEX.md`**: the portfolio. It has one row per project (ID, title, status,
  horizon, repos, a one-line summary, last updated), kept current by `new-project` and
  `review-projects`.
- **`projects/TEMPLATE.md`**: the template every project starts from.
- **`projects/<descriptive-name>.md`**: one per project, named for people
  (`urban-heat-islands.md`). A short uppercase ID in its metadata (`HEAT`) is how you and
  agents refer to it.

## A project file

It starts with a small **metadata block**, which GitHub shows as a table:

```yaml
---
id: HEAT                 # 2–8 capitals or digits; unique; not a repo prefix
title: Urban heat islands from satellite land-surface temperature
status: active           # idea | active | paused | done | dropped
started: 2026-09
horizon: 2027-06         # target end or next big milestone
repos: [heat_tools]      # Tracked Repos it uses, or []
updated: 2026-09-29      # change on every edit
---
```

Then come these sections, always in this order:

| Section | What goes in it |
| --- | --- |
| **Summary** | 2–3 sentences: the question, why it matters, what success looks like. It feeds the index. |
| **Background** | Context, prior work (cite references by number), the open problem, the data and tools. |
| **Science goals** | The long-term questions: `**G1** — …`. You set these; agents don't change them. |
| **Objectives and work packages** | One `### O1 — …` subheading per objective, with a `**Serves:** G1 · **Success criteria:** …` line and its own work-package table. |
| **Plans** | Research plans from `plan-project`, newest first, each dated and agreed with you. |
| **Next actions** | This project's todos, as a checklist. |
| **References** | A numbered list with DOI links. |
| **Decisions** | A `Date · Decision · Why` table. |
| **Research log** | Dated bullets, newest first: what happened, and what you learned. |

A work-package table looks like this:

```markdown
### O1 — Map summer heat-island intensity for 20 cities, 2015–2025

**Serves:** G1 · **Success criteria:** intensity maps with uncertainty for all 20 cities, validated against station data

| WP | Status | Work package | Output | Links |
| --- | --- | --- | --- | --- |
| WP1.1 | 🟢 Done | Download and cloud-mask the LST scenes | clean dataset | HT-3 |
| WP1.2 | 🟠 WIP | Build the intensity pipeline | maps + uncertainty | HT-FA |
| WP1.3 | ⏩ Todo | Validate against weather stations | validation figure | — |
```

(`HT-3` and `HT-FA` stand for a task and a feature on the boards of `heat_tools`, whose prefix
is `HT-`. A project ID can't be a repo prefix, so `HEAT` and `HT-` differ.)

**IDs** never change and are never reused: goals `G1`, objectives `O1`, work packages
`WP1.1` (objective 1, package 1). To point at another project's work, write `HEAT WP1.2`.
**Work-package statuses** are `⏩ Todo` · `🟠 WIP` · `‼️ Blocked` · `🟢 Done`.

## Working with projects

- **Start one:** `new-project "Urban heat islands from satellite data"`. Claude proposes the ID
  and file name, fills in the metadata, adds the index row, and offers to write the Summary,
  Background and goals with you. It never invents goals.
- **Plan one:** `plan-project HEAT`, `plan-project HEAT O1` or `plan-project HEAT WP1.3`.
  1. Claude drafts a research plan: the steps as a checklist, the data and methods, the risks,
     and the code work needed.
  2. It **waits for your go**, just like `plan-task`.
  3. The agreed plan goes under Plans. Code work becomes tasks or features, and their IDs go in
     the work package's Links.
- **Day to day:** just say it, e.g. "HEAT log: the cloud mask removes 40% of July scenes",
  "add a HEAT todo: email the station network", or "HEAT decision: use MODIS, not Landsat,
  for the daily series". Claude adds it to the right section and updates `updated:`. You can
  also edit the file by hand; just keep the structure.
- **Review:** `review-projects` (monthly works well) rebuilds the index and flags:
  - active projects with no update in 30 days;
  - blocked work packages;
  - todos older than 30 days;
  - work packages whose linked code work is done but the package isn't.

  It proposes updates, and you confirm them.
- **Checks:** `check-board` runs on every PR and push to `main`. It checks each project's
  metadata, sections, objectives, work packages and links, and that the index matches.

Project edits go straight to `main`: no branch, log or board status. The file is its own
record.

## Making a project easy to plan from

- Make each objective **measurable**, with success criteria you could check.
- Give each work package **one output** (a dataset, a figure, an analysis, a paper section).
- Write plans as **checklists with inputs and outputs**, so each step can become a task.
- Keep **DOIs** in the references, so agents can find the papers.
- Keep the **log** dated and short. Decisions go in Decisions, not the log.
