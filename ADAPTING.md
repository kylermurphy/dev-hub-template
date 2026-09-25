# Adapting dev-hub to other agents / ecosystems

> ⚠️ **Untested.** These notes haven't been tried with any agent other than Claude. Treat them
> as a starting map, not a verified recipe, and expect to adjust. If you port dev-hub, please
> note what broke (a `CHANGELOG.md` entry or an issue on the template repo helps others).

dev-hub is written **Claude-specific by default**. It names Claude Code and the claude.ai
surfaces, and its access and usage-limit notes describe Claude's model. That's deliberate: it
works out of the box for Claude users. Everything here is plain markdown and plain-language
prompts, though, so porting it to another agent is mostly find-and-replace plus the notes
below. The three spots marked **(Claude-specific)** in the docs link to the matching section
here.

## Surface mapping

| dev-hub says | Means, generally | Your equivalent |
| --- | --- | --- |
| **Claude Code** | a local coding agent that uses your own git credentials and can push to private repos | your local coding agent |
| **claude.ai/code** | a cloud coding agent, with access to the repos you attach, that can push and open PRs while you're away | your hosted/background coding agent |
| **Claude Project (handback mode)** | a chat assistant that can read the hub (synced read-only) but can't push; it hands back patches for you to commit | any assistant with read access and file output |
| **Claude desktop app + GitHub MCP server** | an assistant that writes through the GitHub API but has no shell (no builds or tests) | any agent with a GitHub API integration |
| **CLAUDE.md** | the per-repo instruction file an agent reads | `AGENTS.md`, `.cursorrules`, etc. |
| **Haiku / Sonnet / Opus / Fable** | cheap-fast / mid / most-capable model tiers | your provider's model line-up |
| **subagent (Agent/Task tool)** | a helper agent the main session can hand work to, on a cheaper model | your agent's delegation feature, if any |

## What to change

### 1. Instruction-file name
Agents look for different filenames. The template ships `AGENTS.md` as a one-line pointer to
`CLAUDE.md`, so tools that read `AGENTS.md` still find the hub's instructions. If your tool
reads only its own file:
- rename the masters (`repos/<name>/CLAUDE.md`) and the hub's `CLAUDE.md`;
- update the task protocol's **Sync instructions first** step (`CLAUDE.md`, step 2) and every
  mention of `CLAUDE.md` in `README.md`, `COMMANDS.md`, `OVERNIGHT.md` and
  `templates/PROJECT_INSTRUCTIONS.md`.

### 2. Private-repo access
The workflow assumes public repos clone anywhere, and a private repo (including dev-hub
itself) can be pushed to only from an agent that holds real git credentials for it. How that
authorization happens is tool-specific: wire up whatever your agent uses (an SSH key, a
personal access token, an app install) and keep the rule **"if it can't push, hand back a
patch."** Two Claude-only mechanisms may have no equivalent:
- **Branch-restricted sessions** (`CLAUDE.md` → Branch-restricted sessions): a cloud session
  pinned to one branch. If your agent has no such mode, the section is simply never used.
- **Claude Project handback mode** (`templates/PROJECT_INSTRUCTIONS.md`): relies on claude.ai
  Project docs as a working copy. Another tool needs its own place to keep that state.

### 3. Usage limits (`OVERNIGHT.md`)
The 5-hour session window and weekly cap are Claude subscription specifics. Replace them with
your plan's limits, or with your API spend caps if you pay per token. The *design* is
tool-agnostic: cheap model for routine work, S/M tasks only unattended, one task (or one
batch) per run, persist the plan first, resume from the log.

### 4. Model tiers
Model names appear in `CLAUDE.md` (Subagents), `README.md` (Defaults) and `OVERNIGHT.md`.
Map "fast / mid / most-capable" to your provider's line-up; the effort → tier rule stays.

## What stays the same

The board (`TASK_BOARD.md`), Tracked Repos, the task protocol (branch → sync instructions →
persist the plan → PR → log), the statuses, batches (`multi-task`), the commands, the
resumability/plan-persistence contract, `DECISIONS.md`, and the logging are all agent-neutral.
They're conventions, not code.

**GitHub is assumed throughout**, though: PRs, the PR template, `git am` patches, GitHub
Desktop in the handback steps, and GitHub Actions for CI. Moving to another forge (GitLab,
Gitea, …) is a larger change than switching agents: rename "PR" to your merge-request
equivalent and revisit every GitHub-specific step.
