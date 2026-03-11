# Agentic Iteration Sprint Runner Specification

## Overview

The Agentic Iteration Sprint Runner (`sprint_runner.py`) is an autonomous Python orchestrator that drives agile stories through a full software development lifecycle. By combining the **BMad Method** (for agile processes and structured implementation) and **Desloppify** (for rigorous, blind, multi-agent code quality remediation), it establishes a complete **Agentic Iteration Process**.

This specification outlines a full Python rebuild of the runner to support robust, parallel, and asynchronous operations, taking full advantage of the BMad and Desloppify ecosystems.

## Pipeline & States

The lifecycle consists of gates. The orchestrator is the state machine, and agents are the transition functions.
`backlog → create-story → ready-for-dev → dev-story → review → code-review → quality-check → desloppify-triage → desloppify-review → desloppify-remediate → done → merge + next`

---

## 1. Story Generation (BMad `create-story`)

**Purpose:** Translate backlog items into actionable developer requirements using BMad Method's Scrum Master agent.
**Status Transition:** `backlog` → `ready-for-dev`
**Process:**
- Orchestrator detects `backlog` status in `sprint-status.yaml`.
- Checks out `feature/{story-key}` from `dev`.
- Spawns: `claude -p "/bmad-agent-bmm-sm CS"` isolated via `--no-session-persistence`.
- **Pre-flight (Restart Recovery):** Checks if the `_bmad-output/implementation-artifacts/{story-key}.md` file exists or if the `feat({story-key}): create-story completed` commit is present in git history. If either is true, skips the agent execution entirely to avoid repeating work after a restart.
- **Gate Check:** Verification of the story `.md` file creation.
**Commits:**
- **Work Commit:** After the agent successfully generates the story file, the orchestrator stages the new `.md` file (`git add -A`) and commits: `feat({story-key}): create-story completed`. The commit body will document the specific story file added.
- **Status Commit:** Updates the status to `ready-for-dev` in `sprint-status.yaml`, stages it, and commits: `chore({story-key}): status update to ready-for-dev`.

## 2. Implementation (BMad `dev-story`)

**Purpose:** Autonomously write the source code, tests, and configuration.
**Status Transition:** `ready-for-dev` → `review`
**Process:**
- Spawns: `claude -p "/bmad-agent-bmm-dev DS"` to read the generated spec and write code.
- **Pre-flight (Restart Recovery):** Checks git history for the `feat({story-key}): dev-story completed` commit, or checks for uncommitted/staged code changes compared to `dev`. If changes or the completed commit exist, skips the agent execution to avoid overwriting or repeating work.
- **Gate Check:** Verifies Git diff detects changes (committed, staged, unstaged) in `src/` or `tests/`.
**Commits:**
- **Work Commit:** After the agent completes implementation, the orchestrator stages all changes (`git add -A`) and commits: `feat({story-key}): dev-story completed`. The orchestrator extracts a summary of additions, modifications, and deletions from `git status` or `git diff --stat` to populate the commit body, providing well-documented descriptions of the changes.
- **Status Commit:** Updates the status to `review` in `sprint-status.yaml`, stages it, and commits: `chore({story-key}): status update to review`.

## 3. Initial Code Review (BMad `code-review`)

**Purpose:** Baseline review and immediate auto-fixing of obvious implementation issues.
**Status Transition:** `review` → `quality-check`
**Process:**
- Spawns: `claude -p "/bmad-agent-bmm-dev CR"` with an explicit system prompt to **ALWAYS** choose "Fix them automatically" without human interaction.
- **Pre-flight (Restart Recovery):** Checks git history for the `fix({story-key}): code-review auto-fixes completed` or `chore({story-key}): status update to quality-check` commit. If found, skips the agent execution to prevent repeating the code review process.
- **Gate Check:** Verifies agent exited successfully and status is updated.
**Commits:**
- **Work Commit:** *Always* run this commit step even if no files changed. If the agent made changes, stage them and commit: `fix({story-key}): code-review auto-fixes completed` (including diff stats). If no changes were made, commit an empty marker: `chore({story-key}): code-review completed (no changes)`. This ensures the idempotency pre-flight check has a reliable marker.
- **Status Commit:** Updates the status to `quality-check` in `sprint-status.yaml`, stages it, and commits: `chore({story-key}): status update to quality-check`.

---

## 4. Agentic Iteration Process (Desloppify)

This section details the rebuild of the runner to fully integrate the `desloppify` CLI for continuous, agentic code remediation.

### Phase 1: Desloppify Triage (`desloppify-triage`)
**Purpose:** Map the system architecture, boundaries, and current state.
**Status Transition:** `quality-check` → `desloppify-review` (internal state transition)
**Process:**
- **Pre-flight (Restart Recovery):** Checks git history for the `chore({story-key}): desloppify-triage completed` commit. If found, bypasses the triage phase entirely.
- Orchestrator installs/updates `desloppify[full]`.
- Runs sequential isolated subagents for the 4 triage stages:
  1. **Observe:** `desloppify plan triage --stage-prompt observe` → Run Agent → `desloppify plan triage --confirm observe`
  2. **Reflect:** `desloppify plan triage --stage-prompt reflect` → Run Agent → `desloppify plan triage --confirm reflect`
  3. **Organize:** `desloppify plan triage --stage-prompt organize` → Run Agent → `desloppify plan triage --confirm organize`
  4. **Enrich:** `desloppify plan triage --stage-prompt enrich` → Run Agent → `desloppify plan triage --confirm enrich`
- **Completion:** Orchestrator executes `desloppify plan triage --complete`.
**Commits:**
- **Work Commit:** Stages any Desloppify metadata/configuration changes (`.desloppify/` directory if untracked/modified) and commits: `chore({story-key}): desloppify-triage completed`. The commit body will document the generation of the triage plan and the files tracked.

### Phase 2: Parallel Blind Review (`desloppify-review`)
**Purpose:** Remove agent bias by performing blind, parallel scoring on multiple quality dimensions.
**Status Transition:** `desloppify-review` → `desloppify-remediate` (internal state transition)
**Python Architecture Requirement:** Must use `asyncio.create_subprocess_exec` to run agents concurrently.
**Process:**
- **Pre-flight (Restart Recovery):** Checks git history for the `chore({story-key}): desloppify-review completed` commit. If found, bypasses the parallel review phase.
- Orchestrator runs `desloppify review batch --prepare` (or `desloppify review --prepare`) to generate `review_packet_blind.json`.
- Orchestrator spawns parallel `claude` agents using `asyncio.gather` with a **Concurrency Semaphore (Max 2)** to prevent API Rate Limits (429 Too Many Requests). Each agent is isolated and evaluates a distinct set of dimensions.
- Agents output independent JSON files.
- Orchestrator runs `desloppify review batch --merge` (or custom merge script) to combine into `merged.json`.
- Orchestrator imports results: `desloppify review --import merged.json --scan-after-import`.
**Commits:**
- **Work Commit:** Stages the generated `merged.json` and any resulting review artifacts, then commits: `chore({story-key}): desloppify-review completed`. The commit body will detail the dimensions evaluated and the score artifacts imported.

### Phase 3: Remediation Loop (`desloppify-remediate`)
**Purpose:** Iteratively resolve all identified code issues.
**Status Transition:** `desloppify-remediate` → `done`
**Process:**
- **Pre-flight (Restart Recovery):** Natively idempotent via `desloppify next`, which only surfaces unresolved items. Additionally, verifies if the `chore({story-key}): status update to done` commit is present, and if so, skips this phase entirely.
- **Full Pass:** Orchestrator loops `desloppify next`. Spawns an agent with prompt: *"Run desloppify next. Fix the issue. Run the resolve command. Repeat."* Continues until `next` reports no issues.
- **Targeted Pass:** Orchestrator scopes scan to changed directories (`git diff --name-only dev..HEAD`) *using deeper ruleset thresholds or explicit targeted flags if applicable* to find localized issues missed by the full scan, enforcing a strict time cap (e.g., 600 seconds).
- **Follow-up:** If the targeted pass times out, orchestrator runs `desloppify next`, logs the output to `_bmad-output/implementation-artifacts/{story-key}-quality-followup.md`, and creates a new `backlog` entry in `sprint-status.yaml`.
**Commits:**
- **Iteration Commits:** After *each successful fix iteration* in the loop, the orchestrator stages the specific code changes (`git add -A`) and commits: `fix({story-key}): desloppify-run{n}-iter{x} completed`. The commit body includes a well-documented description of the specific issue resolved and the files added, modified, or deleted based on `git diff --stat`.
- **Follow-up Commit:** If a follow-up is created, stages the new `.md` file and `sprint-status.yaml` and commits: `chore({story-key}): desloppify-followup-backlog created`. The commit body will detail the remaining issues transferred to the backlog.
- **Status Commit:** Finally, updates the status to `done` in `sprint-status.yaml`, stages it, and commits: `chore({story-key}): status update to done`.

---

## 5. Delivery & Continuity

**Purpose:** Merge completed work and orchestrate the next cycle.
**Process:**
- Orchestrator detects `done` status.
- **Pre-flight (Restart Recovery):** Checks if the branch `feature/{story-key}` has already been merged into `dev` (e.g., checking `git branch --merged dev` or checking if `sprint-status.yaml` still marks it as actionable). If merged, bypasses the merge.
- Executes `git merge --no-ff feature/{story-key}` into `dev`. 
- **Conflict Handling:** If `git merge` exits with a non-zero status (conflict), the orchestrator **must** execute `git merge --abort`, log a fatal error alerting the operator, and halt. Under no circumstances should conflict markers be committed.
- Looks ahead in `sprint-status.yaml` for the next actionable story.
- Creates `feature/{next-story-key}` branch and loops.
**Commits:**
- **Merge Commit:** The `git merge --no-ff` command inherently creates a merge commit on the `dev` branch: `Merge branch 'feature/{story-key}' into dev`. This encapsulates all the individual, well-documented work and status commits made during the story's lifecycle.

---

## Python Architecture Specifications

### Component Architecture (Class Structure)
To manage the complexity of asynchronous orchestration, state recovery, and git manipulation, the application **must be broken down into distinct modules/classes** rather than a single monolithic script.

**Recommended Structure:**
- `sprint_runner.py` (Entrypoint)
- `orchestrator/`
  - `__init__.py`
  - `runner.py` (`SprintOrchestrator`: Main state machine loop, lifecycle routing)
  - `state.py` (`StateManager`: Reads/writes `sprint-status.yaml`)
- `agents/`
  - `__init__.py`
  - `base.py` (`BaseAgentRunner`: Async subprocess management, concurrency limits)
  - `bmad.py` (`BMadAgentRunner`: Specializes in `/bmad-agent-*` invocations)
  - `desloppify.py` (`DesloppifyRunner`: Specific logic for Triage, Review, and Remediate loops)
- `vcs/`
  - `__init__.py`
  - `git_manager.py` (`GitManager`: Async git operations, commit formatting, conflict abortion, git history parsing for idempotency checks)
- `utils/`
  - `logger.py` (Structured logging setup for `stderr` and specific log files)

### Async Orchestration
The orchestrator must be built using `asyncio` to natively handle parallel processes (especially for Desloppify Phase 2). Sync blocks (like file writes or Git operations) should be wrapped appropriately, but all agent (`claude`) subprocesses must be asynchronous.

### Subprocess Management
- All `claude` invocations must use: `--dangerously-skip-permissions`, `--model opus`, `--output-format json`, `--no-session-persistence`.
- The orchestrator strips `CLAUDECODE` from the environment before spawning subprocesses to allow nested CLI usage.

### Git Operation Encapsulation
To support the rigorous commit requirements, the `GitManager` class will need robust asynchronous wrappers for Git operations (`git add -A`, `git diff --stat`, `git commit -m`) to generate the detailed commit bodies required for each phase. It must also handle the stateful branching, commit message formatting, and safe abort logic for merge conflicts.

### Idempotency & Restart Recovery
- The state in `sprint-status.yaml` combined with the git commit history represents the ultimate source of truth.
- If the runner crashes mid-process or after a successful stage but before a status update, upon restart it will:
  1. Read the current status from `sprint-status.yaml` via `StateManager`.
  2. Evaluate the **Pre-flight (Restart Recovery)** checks utilizing `GitManager` to inspect commit history (`git log --grep`) or file existence checks.
  3. Resume precisely where it left off, advancing to the next logical gate without repeating expensive agent executions.

### Logging Architecture
- **Console (`stderr`):** High-level orchestrator progress (INFO level).
- **`sprint_runner.log`:** Full debug trace, subprocess commands, and Git operations (rotated 5MB).
- **`desloppify_run.log`:** Append-only detailed output of all Desloppify operations, iteration loops, and parallel review scores.