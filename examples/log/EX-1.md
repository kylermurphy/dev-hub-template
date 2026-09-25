# EX-1 — Add a `--json` flag to `todo list`

> **Example only.** A finished task log, as `mark-done EX-1` leaves it. Real logs live in
> [`../../log/`](../../log/), created from [`../../log/TEMPLATE.md`](../../log/TEMPLATE.md).

- **Repo:** example-repo
- **Branch:** `task/EX-1-list-json`
- **Batch:** none
- **PR / patch:** [<owner>/example-repo#12](https://github.com/<owner>/example-repo/pull/12) (merged 2026-09-19)
- **Status:** Done
- **Started:** 2026-09-18 · **Updated:** 2026-09-19
- **Surface / model:** claude.ai/code · Sonnet

## Definition of done
`todo list --json` prints a JSON array of items (id, text, done); covered by a test; `--help`
documents it.

## Plan
Add a `--json` flag to the `list` sub-command in `cli.py`. When set, serialize the items that
`store.load()` returns with `json.dumps` (sorted by id) instead of the table output. Add a
test in `tests/test_cli.py` using the `tmp_todo_home` fixture, and describe the flag in its
`help=` string. Risk: the table formatter mutates items; serialize before formatting.

## Checklist
- [x] Branch `task/EX-1-list-json` off `main`; first commit syncs `CLAUDE.md` from the master
- [x] Add `--json` to `todo list` in `cli.py`
- [x] Test: `todo list --json` output parses and matches the stored items
- [x] `--help` text for the flag
- [x] `pytest` and `ruff check .` pass; draft PR opened
- [x] PR merged; `mark-done EX-1`

## Next step
None — task complete.

## Blocked / open questions

## What was done
- `cli.py`: new `--json` flag on `list`; prints `json.dumps(items, indent=2)` sorted by id.
- `tests/test_cli.py`: `test_list_json` adds two items, runs `todo list --json`, and checks the
  parsed output.
- Draft PR #12 opened with the PR template (ID, what/why, how tested, DoD checklist).

## How it was tested
- `pytest` → 14 passed (13 existing + 1 new).
- `ruff check .` → no issues.
- Manual: `TODO_HOME=$(mktemp -d) todo add "buy milk" && todo list --json`.

## Notes / follow-ups
- Learning: tests must set `TODO_HOME` to a temporary directory (the `tmp_todo_home` fixture
  does this); otherwise they read and overwrite the real `~/.todo`.
- Follow-up already on the board: EX-2 (CI) would have caught the missing lint run earlier.
