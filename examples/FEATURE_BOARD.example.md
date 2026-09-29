# Example: `FEATURE_BOARD.md` with one feature

> **Example only.** This is a feature as `new-feature example-repo` writes it, before
> `plan-task EX-FA` starts it. Your real feature board is
> [`../FEATURE_BOARD.md`](../FEATURE_BOARD.md), which starts empty. The walkthrough in
> [`README.md`](README.md) and the guide [`../docs/FEATURES.md`](../docs/FEATURES.md) explain
> each part.

## example-repo — `EX-`

*Created by `new-feature example-repo`: "calendar sync, so to-dos can be exported to and
imported from iCalendar files." Nothing has started yet, so every Status is `⏩ Todo` and
Branch, PR and Log read `—`.*

### EX-FA — Calendar sync: export and import to-dos as iCalendar

**Status** ⏩ Todo · **Branch** — · **PR** — · **Log** —

**Description.** Lets `todo` share due dates with any calendar app. It adds optional due dates,
with time zones, to to-do items, a `todo export --ics` command that writes the list as
iCalendar to-dos, and a `todo import` command that reads them back. Export and import share
one date model, so they stay on one branch and reach `main` together.

**Done when.** Every subtask is done: `todo export --ics` and `todo import` round-trip a list
without loss, due dates and time zones included; the README documents due dates, export and
import; and CI passes on the feature PR.

| ID | Status | Subtask | Type | Effort | Definition of done |
| --- | --- | --- | --- | --- | --- |
| EX-FA1 | ⏩ Todo | Add a shared due-date model with time zones (`todo add --due`) | Refactor | M | Items store an optional due date with a time zone; data files without due dates still load; covered by tests |
| EX-FA2 | ⏩ Todo | `todo export --ics` writes the list as iCalendar to-dos | Feature | M | Output is valid iCalendar and keeps each item's text, done state and due date; covered by a test |
| EX-FA3 | ⏩ Todo | `todo import <file>` reads iCalendar to-dos into the list | Feature | M | Importing `export` output gives the same list; duplicates are skipped; a bad file gives a clear error; tests |
| EX-FA4 | ⏩ Todo | Document due dates, export and import in the README | Docs | S | README has an example for `--due`, `export --ics` and `import`, matching `todo --help` (do after EX-FA3) |
