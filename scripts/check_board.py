#!/usr/bin/env python3
"""check_board.py — run dev-hub's `check-board` consistency checks.

Usage: python3 scripts/check_board.py [ROOT]
ROOT defaults to the dev-hub checkout this script sits in; pass a copy to test against it.
Prints one line per finding, then a summary. Exit status: 0 no findings, 1 findings,
2 the board couldn't be parsed.

The checks are specified in COMMANDS.md → check-board. Change the spec and this script
together; CI runs this on every dev-hub PR and push to `main`.
"""
import html
import re
import sys
import unicodedata
from pathlib import Path

# The board's Status strings. Must match CLAUDE.md → Statuses ("‼️" is U+203C U+FE0F).
BOARD_STATUS = {
    "⏩ Todo": "Todo",
    "\U0001f7e0 WIP": "WIP",
    "‼️ Blocked": "Blocked",
    "\U0001f6d1 Usage-stopped": "Usage-stopped",
    "\U0001f7e2 Done": "Done",
}
WORDS = set(BOARD_STATUS.values())
STARTED = WORDS - {"Todo"}  # these need a log and a TASK_LOG.md row
NO_MASTER = {"dev-hub"}  # its instructions are its root CLAUDE.md
TASK_LOG_DONE = re.compile(r"^Done \((merged|PR confirmed) \d{4}-\d{2}-\d{2}\)$")

ID_RE = re.compile(r"^[A-Z]+-\d+$")
LOG_ID_RE = re.compile(r"^[A-Z]+-(\d+|F[A-Z]+)$")  # a task's or a feature's log
FEATURE_HEAD_RE = re.compile(r"^### (\S+) — (.+)$")
FEATURE_STATUS_RE = re.compile(r"^\*\*Status\*\* (.+?) · \*\*Branch\*\*")

# projects/ (CLAUDE.md → Projects): the template's metadata keys and ## sections, in order.
PROJECT_KEYS = ("id", "title", "status", "started", "horizon", "repos", "updated")
PROJECT_STATUS = ("idea", "active", "paused", "done", "dropped")
PROJECT_SECTIONS = ("Summary", "Background", "Science goals", "Objectives and work packages",
                    "Plans", "Next actions", "References", "Decisions", "Research log")
PROJECT_NOT_PROJECTS = ("TEMPLATE.md", "INDEX.md")
PROJECT_ID_RE = re.compile(r"^[A-Z0-9]{2,8}$")
MONTH_RE = re.compile(r"^\d{4}-\d{2}$")
OBJECTIVE_RE = re.compile(r"^### O(\d+) — \S")
BOARD_REF_RE = re.compile(r"\b[A-Z]+-(?:\d+|F[A-Z]+\d*)\b")  # EX-7, EX-FA, EX-FA2
WP_STATUS = tuple(k for k, v in BOARD_STATUS.items() if v != "Usage-stopped")
SECTION_RE = re.compile(r"^## (\S+) — `([A-Z]+-)`\s*$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
LINK_CELL_RE = re.compile(r"^\[([^\]]+)\]\(#([^)\s]+)\)$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
LOG_FIELD_RE = re.compile(r"^- \*\*(Status|Batch|Branch|PR / patch):\*\*\s*(.*)$")


class BoardError(Exception):
    """The board is missing something the checks can't run without."""


def cells(line):
    """Split a Markdown table row into stripped cells (escaped pipes stay in the cell)."""
    parts = re.split(r"(?<!\\)\|", line.strip())
    return [c.strip() for c in parts[1:-1]]


def tables(text):
    """Yield (level-2 heading, header cells, [(line number, cells), ...]) for each table."""
    lines = text.splitlines()
    heading, fenced, i = None, False, 0
    while i < len(lines):
        line = lines[i]
        if line.lstrip().startswith("```"):
            fenced = not fenced
        elif not fenced and line.startswith("## "):
            heading = line
        elif (not fenced and line.startswith("|") and i + 1 < len(lines)
              and re.match(r"^\|\s*:?-{3,}", lines[i + 1])):
            header, rows, i = cells(line), [], i + 2
            while i < len(lines) and lines[i].startswith("|"):
                rows.append((i + 1, cells(lines[i])))
                i += 1
            yield heading, header, rows
            continue
        i += 1


def slug(text):
    """GitHub's heading anchor for `text` (the github-slugger rule), before de-duplication."""
    text = html.unescape(text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)  # links render as their text
    text = text.replace("`", "").replace("*", "").lower()
    keep = (c for c in text
            if c in " -" or unicodedata.category(c)[0] in "LMN" or unicodedata.category(c) == "Pc")
    return "".join(keep).replace(" ", "-")


def anchors(text):
    """Every heading anchor in a Markdown file, with GitHub's -1, -2… suffixes on repeats."""
    seen, out, fenced = {}, {}, False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        m = None if fenced else HEADING_RE.match(line)
        if not m:
            continue
        base = result = slug(m.group(2))
        while result in seen:
            seen[base] += 1
            result = f"{base}-{seen[base]}"
        seen[result] = 0
        out[result] = line
    return out


def column(header, name, where):
    try:
        return header.index(name)
    except ValueError:
        raise BoardError(f"{where}: no '{name}' column in {header}")


def read_log(path):
    fields = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        m = LOG_FIELD_RE.match(line)
        if m and m.group(1) not in fields:
            fields[m.group(1)] = m.group(2).strip()
    return fields


def feature_blocks(text):
    """Yield (repo section match or None, first line number, lines) per `### ` block."""
    section, block, start, fenced = None, None, 0, False
    for n, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("```"):
            fenced = not fenced
        if not fenced and (line.startswith("## ") or line.startswith("### ")):
            if block is not None:
                yield section, start, block
                block = None
            if line.startswith("## "):
                section = SECTION_RE.match(line)
            else:
                block, start = [line], n
        elif block is not None:
            block.append(line)
    if block is not None:
        yield section, start, block


def strip_comments(text):
    """Blank out HTML comments, keeping line numbers."""
    return re.sub(r"<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)


def read_metadata(lines):
    """The `key: value` lines of a leading --- block, and the line number of its end."""
    if not lines or lines[0].strip() != "---":
        return None, 0
    meta = {}
    for n, line in enumerate(lines[1:], 2):
        if line.strip() == "---":
            return meta, n
        key, sep, value = line.partition(":")
        if sep:
            meta[key.strip()] = value.strip()
    return None, 0


def batch_ids(batch):
    """The IDs named before the first "·" of a Batch: line (none → empty)."""
    return set(re.findall(r"\b[A-Z]+-\d+\b", batch.split("·")[0]))


def first(pattern, text):
    m = re.search(pattern, text or "")
    return m.group(1) if m else None


def check(root):
    findings = []

    def add(check_name, message):
        findings.append(f"[{check_name}] {message}")

    board_path = root / "TASK_BOARD.md"
    if not board_path.is_file():
        raise BoardError(f"{board_path} not found")
    board = board_path.read_text(encoding="utf-8")

    # --- Parse the board -------------------------------------------------------------
    tracked = {}  # name -> {prefix, tracking, link, line}
    sections = {}  # name -> prefix, from "## <name> — `<PREFIX>-`"
    section_anchor = {}  # name -> GitHub anchor of that heading
    tasks = []  # (id, status cell, section name or None, line)
    board_anchors = anchors(board)
    for a, line in board_anchors.items():
        m = SECTION_RE.match(line)
        if m:
            sections[m.group(1)] = m.group(2)
            section_anchor[m.group(1)] = a

    tracked_table = False  # an empty table is fine (a fresh hub); a missing one isn't
    for heading, header, rows in tables(board):
        if heading == "## Tracked Repos":
            tracked_table = True
            ci = {n: column(header, n, "Tracked Repos") for n in ("Repo", "Prefix", "Tracking")}
            for lineno, row in rows:
                if len(row) != len(header):
                    raise BoardError(f"TASK_BOARD.md:{lineno}: {len(row)} cells, the table has "
                                     f"{len(header)}")
                cell = row[ci["Repo"]]
                m = LINK_CELL_RE.match(cell)
                name = m.group(1) if m else cell
                tracked[name] = {
                    "prefix": row[ci["Prefix"]].strip("`"),
                    "tracking": row[ci["Tracking"]],
                    "link": m.group(2) if m else None,
                    "line": lineno,
                }
            continue
        if header[:1] != ["ID"]:
            continue  # not a task table
        section = SECTION_RE.match(heading or "")
        status_col = column(header, "Status", heading)
        for lineno, row in rows:
            if len(row) != len(header):
                raise BoardError(f"TASK_BOARD.md:{lineno}: {len(row)} cells, the table has "
                                 f"{len(header)}")
            tasks.append((row[0], row[status_col], section.group(1) if section else None,
                          lineno))
    if not tracked_table:
        raise BoardError("TASK_BOARD.md has no Tracked Repos table")

    # --- 1. every active repo has a section and a master -----------------------------
    for name, repo in tracked.items():
        if repo["tracking"] != "active":
            continue
        if name not in sections:
            add("sections", f"active repo {name} has no '## {name} — `{repo['prefix']}`' section")
        if name not in NO_MASTER and not (root / "repos" / name / "CLAUDE.md").is_file():
            add("sections", f"active repo {name} has no repos/{name}/CLAUDE.md master")

    # --- 2. Tracked Repos names link to their sections --------------------------------
    for name, repo in tracked.items():
        link, where = repo["link"], f"TASK_BOARD.md:{repo['line']}"
        if name in sections and link is None:
            add("links", f"{where}: {name} isn't linked to its section "
                         f"(#{section_anchor[name]})")
        elif name in sections and link != section_anchor[name]:
            add("links", f"{where}: {name} links to #{link}, but its section is "
                         f"#{section_anchor[name]}")
        elif name not in sections and link is not None:
            add("links", f"{where}: {name} links to #{link}, but it has no section")

    # --- 3. no orphans ----------------------------------------------------------------
    for name in sections:
        if name not in tracked:
            add("orphans", f"section '## {name}' is for a repo not in Tracked Repos")
    repos_dir = root / "repos"
    if repos_dir.is_dir():
        for d in sorted(p for p in repos_dir.iterdir() if p.is_dir()):
            if d.name not in tracked:
                add("orphans", f"repos/{d.name}/ is for a repo not in Tracked Repos")

    # --- 5. prefixes unique; task IDs use their repo's prefix -------------------------
    by_prefix = {}
    for name, repo in tracked.items():
        by_prefix.setdefault(repo["prefix"], []).append(name)
    for prefix, names in by_prefix.items():
        if len(names) > 1:
            add("prefixes", f"prefix {prefix} is used by {', '.join(names)}")
    for name, prefix in sections.items():
        if name in tracked and tracked[name]["prefix"] != prefix:
            add("prefixes", f"section {name} uses {prefix}, Tracked Repos says "
                            f"{tracked[name]['prefix']}")
    for tid, _, section, lineno in tasks:
        where = f"TASK_BOARD.md:{lineno}"
        if not ID_RE.match(tid):
            add("prefixes", f"{where}: '{tid}' isn't a task ID")
        elif section is None:
            add("prefixes", f"{where}: {tid} is outside a repo section")
        elif not re.fullmatch(re.escape(sections[section]) + r"\d+", tid):
            add("prefixes", f"{where}: {tid} doesn't use {section}'s prefix "
                            f"{sections[section]}")

    # --- 6. task IDs unique -----------------------------------------------------------
    seen = {}
    for tid, _, _, lineno in tasks:
        if tid in seen:
            add("ids", f"{tid} appears twice (TASK_BOARD.md:{seen[tid]} and :{lineno})")
        else:
            seen[tid] = lineno

    # --- TASK_LOG.md and logs ---------------------------------------------------------
    task_log = {}  # id -> [(date, status, line)]
    log_rows = []
    task_log_path = root / "TASK_LOG.md"
    if task_log_path.is_file():
        for _, header, rows in tables(task_log_path.read_text(encoding="utf-8")):
            if "Task" not in header:
                continue
            d, t, s = (column(header, n, "TASK_LOG.md") for n in ("Date", "Task", "Status"))
            for lineno, row in rows:
                if len(row) != len(header):
                    raise BoardError(f"TASK_LOG.md:{lineno}: {len(row)} cells, the table has "
                                     f"{len(header)}")
                log_rows.append((row[d], row[t], row[s], lineno))
                task_log.setdefault(row[t], []).append((row[d], row[s], lineno))
    else:
        add("task-log", "TASK_LOG.md not found")

    logs = {}
    log_dir = root / "log"
    if log_dir.is_dir():
        for p in sorted(log_dir.glob("*.md")):
            if LOG_ID_RE.match(p.stem):
                logs[p.stem] = read_log(p)

    # --- 4. TASK_LOG.md newest first --------------------------------------------------
    previous = None
    for date, tid, _, lineno in log_rows:
        if not DATE_RE.match(date):
            add("task-log", f"TASK_LOG.md:{lineno}: {tid} has date '{date}', not YYYY-MM-DD")
            continue
        if previous and date > previous:
            add("task-log", f"TASK_LOG.md:{lineno}: {tid} ({date}) is below an older row "
                            f"({previous}); rows go newest first")
        previous = date

    # --- 7. Status values -------------------------------------------------------------
    board_word = {}
    for tid, status, _, lineno in tasks:
        if status in BOARD_STATUS:
            board_word[tid] = BOARD_STATUS[status]
        else:
            add("status", f"TASK_BOARD.md:{lineno}: {tid} Status '{status}' isn't one of "
                          f"{', '.join(BOARD_STATUS)}")
    for tid, fields in logs.items():
        status = fields.get("Status")
        if status is None:
            add("status", f"log/{tid}.md has no '- **Status:**' line")
        elif status not in WORDS:
            add("status", f"log/{tid}.md Status '{status}' isn't one of {', '.join(sorted(WORDS))}")
    for date, tid, status, lineno in log_rows:
        if status not in WORDS and not TASK_LOG_DONE.match(status):
            add("status", f"TASK_LOG.md:{lineno}: {tid} Status '{status}' isn't a Status word, "
                          "'Done (merged <date>)' or 'Done (PR confirmed <date>)'")

    # --- 10. the feature board --------------------------------------------------------
    feature_path = root / "FEATURE_BOARD.md"
    features = {}  # id -> line
    subtasks = {}  # id -> line
    feature_text = feature_path.read_text(encoding="utf-8") if feature_path.is_file() else ""
    for m in re.finditer(r"^## (.+)$", feature_text, flags=re.M):
        sm = SECTION_RE.match(m.group(0))
        if not sm:
            continue
        name, prefix = sm.groups()
        if name not in tracked:
            add("features", f"FEATURE_BOARD.md section '## {name}' is for a repo not in "
                            "Tracked Repos")
        elif tracked[name]["prefix"] != prefix:
            add("features", f"FEATURE_BOARD.md section {name} uses {prefix}, Tracked Repos says "
                            f"{tracked[name]['prefix']}")
    for section, start, block in feature_blocks(feature_text):
        where = f"FEATURE_BOARD.md:{start}"
        head = FEATURE_HEAD_RE.match(block[0])
        if section is None:
            add("features", f"{where}: '{block[0]}' isn't inside a repo section")
            continue
        prefix = section.group(2)
        if not head or not re.fullmatch(re.escape(prefix) + r"F[A-Z]+", head.group(1)):
            add("features", f"{where}: '{block[0]}' isn't '### {prefix}F<letter> — <title>'")
            continue
        fid = head.group(1)
        if fid in features:
            add("features", f"{fid} appears twice (FEATURE_BOARD.md:{features[fid]} and "
                            f":{start})")
        features[fid] = start
        status_line = next((l for l in block if l.startswith("**Status**")), "")
        sm = FEATURE_STATUS_RE.match(status_line)
        if not sm:
            add("features", f"{where}: {fid} has no '**Status** … · **Branch** …' line")
        elif sm.group(1) not in BOARD_STATUS:
            add("status", f"{where}: {fid} Status '{sm.group(1)}' isn't one of "
                          f"{', '.join(BOARD_STATUS)}")
        else:
            board_word[fid] = BOARD_STATUS[sm.group(1)]
        for label in ("Description.", "Done when."):
            text = next((l for l in block if l.startswith(f"**{label}**")), None)
            if text is None or not text[len(label) + 4:].strip():
                add("features", f"{where}: {fid} has no **{label}** text")
        sub_words = []
        table = next(((h, rows) for _, h, rows in tables("\n".join(block)) if h[:1] == ["ID"]),
                     None)
        if table is None or not table[1]:
            add("features", f"{where}: {fid} has no subtask table")
            continue
        header, rows = table
        status_col = column(header, "Status", fid)
        for offset, row in rows:
            lineno = start + offset - 1
            if len(row) != len(header):
                raise BoardError(f"FEATURE_BOARD.md:{lineno}: {len(row)} cells, the table has "
                                 f"{len(header)}")
            sid, status = row[0], row[status_col]
            if not re.fullmatch(re.escape(fid) + r"\d+", sid):
                add("features", f"FEATURE_BOARD.md:{lineno}: subtask '{sid}' isn't {fid}<n>")
            elif sid in subtasks:
                add("ids", f"{sid} appears twice (FEATURE_BOARD.md:{subtasks[sid]} and "
                           f":{lineno})")
            subtasks.setdefault(sid, lineno)
            if status in BOARD_STATUS:
                sub_words.append(BOARD_STATUS[status])
            else:
                add("status", f"FEATURE_BOARD.md:{lineno}: {sid} Status '{status}' isn't one "
                              f"of {', '.join(BOARD_STATUS)}")
        word = board_word.get(fid)
        if word == "Todo" and any(w != "Todo" for w in sub_words):
            add("features", f"{fid} is Todo but some of its subtasks have started")
        if word == "Done" and any(w != "Done" for w in sub_words):
            add("features", f"{fid} is Done but not all of its subtasks are")

    # --- 11. projects -----------------------------------------------------------------
    board_ids = {t[0] for t in tasks} | set(features) | set(subtasks)
    repo_prefixes = {repo["prefix"].rstrip("-") for repo in tracked.values()}
    projects = {}  # id -> (file name, metadata)
    project_dir = root / "projects"
    project_files = (sorted(p for p in project_dir.glob("*.md")
                            if p.name not in PROJECT_NOT_PROJECTS)
                     if project_dir.is_dir() else [])
    for path in project_files:
        where = f"projects/{path.name}"
        lines = strip_comments(path.read_text(encoding="utf-8")).splitlines()
        meta, end = read_metadata(lines)
        if meta is None:
            add("projects", f"{where} doesn't start with a --- metadata block")
            continue
        for key in PROJECT_KEYS:
            if not meta.get(key):
                add("projects", f"{where}: metadata has no '{key}'")
        pid = meta.get("id", "")
        if pid and not PROJECT_ID_RE.match(pid):
            add("projects", f"{where}: id '{pid}' isn't 2–8 capital letters or digits")
        if pid in repo_prefixes:
            add("projects", f"{where}: id '{pid}' is a tracked repo's prefix")
        if pid in projects:
            add("projects", f"{where}: id {pid} is also used by projects/{projects[pid][0]}")
        elif pid:
            projects[pid] = (path.name, meta)
        checks = (("status", lambda v: v in PROJECT_STATUS, " | ".join(PROJECT_STATUS)),
                  ("started", MONTH_RE.match, "YYYY-MM"), ("horizon", MONTH_RE.match, "YYYY-MM"),
                  ("updated", DATE_RE.match, "YYYY-MM-DD"))
        for key, ok, form in checks:
            if meta.get(key) and not ok(meta[key]):
                add("projects", f"{where}: {key} '{meta[key]}' isn't {form}")
        repos = re.fullmatch(r"\[(.*)\]", meta.get("repos", ""))
        if meta.get("repos") and not repos:
            add("projects", f"{where}: repos '{meta['repos']}' isn't [name, name] or []")
        for name in (r.strip() for r in (repos.group(1).split(",") if repos else [])):
            if name and name not in tracked:
                add("projects", f"{where}: repos names '{name}', which isn't in Tracked Repos")
        heads = [(n, line[3:].strip()) for n, line in enumerate(lines, 1)
                 if n > end and line.startswith("## ")]
        names = [h for _, h in heads]
        pos = -1
        for section in PROJECT_SECTIONS:
            found = [i for i, h in enumerate(names) if h == section and i > pos]
            if not found:
                where_else = " in the template's order" if section in names else ""
                add("projects", f"{where}: no '## {section}' section{where_else}")
                continue
            pos = found[0]
        if "Objectives and work packages" not in names:
            continue
        obj_line = heads[names.index("Objectives and work packages")][0]
        last = next((n for n, _ in heads if n > obj_line), len(lines) + 1)
        block_starts = [n for n in range(obj_line + 1, last) if lines[n - 1].startswith("### ")]
        objectives, wps = set(), set()
        for i, start in enumerate(block_starts):
            stop = block_starts[i + 1] if i + 1 < len(block_starts) else last
            head = lines[start - 1]
            om = OBJECTIVE_RE.match(head)
            if not om:
                add("projects", f"{where}:{start}: '{head}' isn't '### O<n> — <objective>'")
                continue
            onum = om.group(1)
            if onum in objectives:
                add("projects", f"{where}:{start}: O{onum} appears twice")
            objectives.add(onum)
            table = next(((h, rows) for _, h, rows in tables("\n".join(lines[start - 1:stop - 1]))
                          if h[:1] == ["WP"]), None)
            if table is None:
                add("projects", f"{where}:{start}: O{onum} has no work-package table")
                continue
            header, rows = table
            status_col = column(header, "Status", f"{where} O{onum}")
            links_col = header.index("Links") if "Links" in header else None
            for offset, row in rows:
                lineno = start + offset - 1
                if len(row) != len(header):
                    raise BoardError(f"{where}:{lineno}: {len(row)} cells, the table has "
                                     f"{len(header)}")
                wp = row[0]
                if not re.fullmatch(rf"WP{onum}\.\d+", wp):
                    add("projects", f"{where}:{lineno}: '{wp}' isn't WP{onum}.<m>")
                elif wp in wps:
                    add("projects", f"{where}:{lineno}: {wp} appears twice")
                wps.add(wp)
                if row[status_col] not in WP_STATUS:
                    add("projects", f"{where}:{lineno}: {wp} Status '{row[status_col]}' isn't one "
                                    f"of {', '.join(WP_STATUS)}")
                for ref in BOARD_REF_RE.findall(row[links_col] if links_col is not None else ""):
                    if ref not in board_ids:
                        add("projects", f"{where}:{lineno}: {wp} links {ref}, which isn't on "
                                        "either board")
    index_path = project_dir / "INDEX.md"
    if projects and not index_path.is_file():
        add("projects", "projects/INDEX.md not found")
    elif index_path.is_file():
        seen = set()
        for _, header, rows in tables(index_path.read_text(encoding="utf-8")):
            if header[:1] != ["ID"]:
                continue
            col = {n: column(header, n, "projects/INDEX.md")
                   for n in ("ID", "Project", "Status", "Horizon", "Updated")}
            for lineno, row in rows:
                where = f"projects/INDEX.md:{lineno}"
                if len(row) != len(header):
                    raise BoardError(f"{where}: {len(row)} cells, the table has {len(header)}")
                pid = row[col["ID"]]
                if pid not in projects:
                    add("projects", f"{where}: {pid} has no project file")
                    continue
                if pid in seen:
                    add("projects", f"{where}: {pid} has two rows")
                    continue
                seen.add(pid)
                fname, meta = projects[pid]
                link = re.search(r"\]\(([^)#\s]+)\)", row[col["Project"]])
                if not link or link.group(1) != fname:
                    add("projects", f"{where}: {pid}'s Project cell doesn't link {fname}")
                for name in ("Status", "Horizon", "Updated"):
                    if row[col[name]] != meta.get(name.lower()):
                        add("projects", f"{where}: {pid} {name} is '{row[col[name]]}' but "
                                        f"{fname} says '{meta.get(name.lower())}'")
        for pid, (fname, _) in sorted(projects.items()):
            if pid not in seen:
                add("projects", f"{pid} (projects/{fname}) has no row in projects/INDEX.md")

    # --- 8. started tasks and features have a log and a TASK_LOG.md row that agree ----
    for tid, word in board_word.items():
        if word not in STARTED:
            continue
        if tid not in logs:
            add("records", f"{tid} is {word} but has no log/{tid}.md")
        elif logs[tid].get("Status") in WORDS and logs[tid]["Status"] != word:
            add("records", f"{tid} is {word} on the board but {logs[tid]['Status']} in "
                           f"log/{tid}.md")
        if tid not in task_log:
            add("records", f"{tid} is {word} but has no TASK_LOG.md row")

    # --- 9. batches agree -------------------------------------------------------------
    for tid, fields in sorted(logs.items()):
        siblings = batch_ids(fields.get("Batch", "")) - {tid}
        for sib in sorted(siblings):
            if sib not in logs:
                add("batches", f"log/{tid}.md names batch member {sib}, which has no log")
            elif tid not in batch_ids(logs[sib].get("Batch", "")):
                add("batches", f"log/{tid}.md names {sib} in its batch, but log/{sib}.md "
                               f"doesn't name {tid}")
        if "dropped from batch" in fields.get("Batch", ""):
            continue
        branch = first(r"`([^`]+)`", fields.get("Branch"))
        pr = first(r"(https?://[^\s)\]>]+)", fields.get("PR / patch"))
        for sib in sorted(siblings):
            other = logs.get(sib)
            if not other or "dropped from batch" in other.get("Batch", "") or sib < tid:
                continue  # missing (reported above), dropped, or pair already compared
            if first(r"`([^`]+)`", other.get("Branch")) != branch:
                add("batches", f"{tid} and {sib} are one batch but name different branches")
            if first(r"(https?://[^\s)\]>]+)", other.get("PR / patch")) != pr:
                add("batches", f"{tid} and {sib} are one batch but name different PRs")

    return findings


def main(argv):
    root = Path(argv[1]) if len(argv) > 1 else Path(__file__).resolve().parent.parent
    try:
        findings = check(root)
    except BoardError as e:
        print(f"check-board: can't check the board: {e}")
        return 2
    for f in findings:
        print(f)
    if findings:
        print(f"check-board: {len(findings)} issue(s) found")
        return 1
    print("check-board: no issues found")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
