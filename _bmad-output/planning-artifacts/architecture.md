---
stepsCompleted:
  - 1
  - 2
  - 3
  - 4
  - 5
  - 6
  - 7
  - 8
lastStep: 8
status: 'complete'
completedAt: '2026-03-09'
inputDocuments:
  - _bmad-output/planning-artifacts/product-brief-vibe_visualiser-2026-03-06.md
  - _bmad-output/planning-artifacts/prd.md
  - _bmad-output/planning-artifacts/prd-validation-report.md
  - _bmad-output/planning-artifacts/ux-design-specification.md
  - docs/bmad-toad-integration-spec.md
workflowType: 'architecture'
project_name: 'mad_frog'
user_name: 'Linus'
date: '2026-03-09'
partyModeInsights:
  - 'Tool-use architecture: agent is the orchestrator, engine provides 18 tool functions'
  - 'Multi-repo model: each project is an independent Git repo, graduates to development repo'
  - 'Stateless tool: all durable state in project repos, SQLite is ephemeral, tool is independently upgradeable'
  - 'Vault detection via .obsidian/ parent walk, zero-config Obsidian integration'
  - 'Lean into Toad: subclass ToadApp, extend dont wrap, accept coupling as a feature'
  - 'Peer tool deployment: Mad Frog cloned alongside project repos, operates on sibling directories'
  - 'Method snapshot per-project: _bmad/ copied at project creation, portable provenance'
  - 'Two-tier state model: Tier 1 (Git, artifacts) durable, Tier 2 (conversation, position) rebuilt from Tier 1'
  - 'Safety nets not guardrails: auto-save, unwritten artifact detection, state rebuild — catch agent mistakes without constraining agent behaviour'
  - '~2000 lines of Python, 18 tool functions, 7 infrastructure services, 3 UI concerns, 65 tests in 2 minutes'
  - 'Decision: rename project from vibe_visualiser to mad_frog (to be applied in dedicated rename pass)'
  - 'Python 3.14 (GIL on) — Toad requires >=3.14, no-GIL deferred to post-MVP'
  - 'Single production dependency: batrachian-toad>=0.5.35 — GitPython and aiosqlite are transitive'
  - 'aiosqlite over stdlib sqlite3 — native async, no event loop blocking, zero added dependency'
  - 'uv as package manager, hatchling as build backend — matches Toad ecosystem'
  - 'Starter skeleton: 25 files, 1 dependency, complete CI and Dev Container config from day one'
  - 'Pydantic dropped: Toad uses TypedDict + dataclass everywhere, zero Pydantic in codebase or deps. Follow Toad idiom.'
  - 'Integration model: NOT a ToadApp subclass for tool exposure. Tools exposed via MCP server, UI via ToadApp subclass.'
  - 'MCP server is the extension point: session/new mcpServers parameter passes our MCP server to the AI agent'
  - 'Agent-agnostic: any ACP agent discovers our tools via standard MCP tools/list — no system prompt injection'
  - 'Three-process architecture: MadFrogApp (UI), AI Agent (Claude etc), Mad Frog MCP Server (tools + git state)'
  - 'State sync: MCP server writes state.json atomically, MadFrogApp watches via watchdog (Toad dep)'
  - 'Auto-save moved to MCP server internal timer — no AI agent round-trip, no token cost'
  - 'ToolResult is not a model: tool returns use MCP CallToolResult format directly (content + isError)'
  - 'Tool schemas are JSON Schema dicts in tools/list response — no Pydantic, no TypedDict for wire format'
  - 'Toad passes empty mcpServers[] in v0.6.8 — we override acp_new_session to inject ours'
  - 'MCP server starts projectless — two-phase lifecycle: serverless (config, list projects) → project active (services, auto-save)'
  - 'Workspace root collected via first-run modal in browser, stored in .vibe/config.yaml — no env vars for paths'
  - 'bmad_detect_changes restored (FR56-60 coverage) + bmad_report_context added = 18 tools total'
  - 'Silent context-aware pre-emptive save at 90% of context window — bmad_report_context gets real budget from agent'
  - 'state.json expanded with checkpoint_history array — sidebar reads this, not MCP tools (cross-process boundary)'
  - 'Tool handlers are free functions with signature (server, arguments) → dict — TOOL_HANDLERS registry in tools/__init__.py'
  - 'Node.js required for npx bmad init — added to Dev Container features, guarded with shutil.which() check'
  - 'bmad_get_step_prompt resolves template variables ({project-root} etc) via simple string replacement'
  - 'Credential management is Toads responsibility — no CredentialSetupScreen, just env var passthrough in devcontainer.json'
  - 'Session lock acquired in bmad_create_project/bmad_open_project, not a separate tool call — write tools assert lock held'
  - 'Replace click with argparse for CLI — preserves single production dependency principle'
  - 'Commit prefix registry: [checkpoint], [artifact], [session-auto], [context-save], [init], [bmad-update] — SQLite rebuild filters on these'
---

# Architecture Decision Document

_This document builds collaboratively through step-by-step discovery. Sections are appended as we work through each architectural decision together._

## Project Context Analysis

### What Is Mad Frog?

**Mad Frog is a Toad app that gives an LLM agent 18 tools to manage BMAD planning projects.**

The agent reads BMAD step files and facilitates guided conversations. When the agent has content ready, it calls `artifact.write()` to save it to the user's project repo with full Obsidian integration. Git provides the state engine. SQLite provides fast queries. Auto-save provides the safety net. Toad provides the UI. The entire Mad Frog codebase is under 2000 lines of Python. Everything else — the methodology, the facilitation, the adaptation — lives in the agent, where it improves for free with every model upgrade.

### Requirements Overview

**Functional Requirements:**
88 functional requirements spanning 10 domains: Project Lifecycle (FR1-8), Guided Workflow Engine (FR9-18), Solutioning & Implementation (FR19-24), Journey Map & Navigation (FR25-36), State Persistence & Recovery (FR37-45), Obsidian Integration (FR46-52), Conversation & Transcript Management (FR53-55), Bidirectional File Workspace (FR56-60), Multi-Agent Facilitation/Party Mode (FR61-68), Container & Access (FR69-88).

**Non-Functional Requirements:**
- **Performance:** Sub-500ms Journey Map rendering, 3s artifact-write-commit ceiling, 30s cold start, 512MB memory ceiling for 4-hour sessions, sub-100ms SQLite queries
- **Security:** No credential logging/display, filesystem sandboxing (tools validate paths within project root), network traffic limited to LLM provider via Toad
- **Reliability:** Zero data loss guarantee, atomic checkpoint operations, chaos test suite (5 scenarios), graceful disconnect recovery, atomic session lock
- **Accessibility:** WCAG AA contrast via Toad theme, keyboard-accessible interactions, non-colour state encoding (icons + text labels)
- **Integration:** Obsidian-native markdown validation (frontmatter, wikilinks, graph view), CommonMark compliance, platform-agnostic Docker
- **Observability:** Structured JSON logs via tool function logging decorator, error classification (recoverable/fatal)
- **Maintainability:** State format versioning with non-destructive migration, 90%+ coverage on ~2000 lines, 80%+ widget pilot coverage

**Scale & Complexity:**
- Primary domain: Full-stack Python (Textual Web + Git + SQLite)
- Complexity level: Medium-High (requirements) → Low (implementation, due to tool-use architecture)
- Total codebase: ~2000 lines Python + ~50 lines TCSS

### Core Architectural Insight

The three dependencies underneath Mad Frog — Toad, BMAD, and LLM models — are all moving targets on different timelines. A rigid orchestration engine that parses specific formats and manages complex state machines would be fighting its dependencies within 6 months.

**The solution: intelligence in the agent, infrastructure in the code.**

The agent is the most capable, most adaptable component in the system. Models are getting dramatically better at following complex instructions, generating structured content, and maintaining context. The more we hardcode into the engine, the more we prevent the agent from leveraging those improvements.

Mad Frog provides **tools** (safe, atomic, deterministic) and **safety nets** (catch agent mistakes without constraining agent behaviour). The agent provides **judgment** (when to write, what to checkpoint, how to adapt to the user). As models improve, the safety nets fire less often and the product gets better — without code changes.

### Deployment Model

**Mad Frog is a stateless peer tool, not a container for projects.**

```
~/Development/                    # User's workspace
├── mad_frog/                     # Tool (Dev Container, cloned repo)
│   ├── .vibe/                    # Tool config (bind-mounted for persistence)
│   │   └── config.yaml           # Project path registry
│   ├── _bmad/                    # Latest BMAD method (ships with tool)
│   ├── src/                      # Mad Frog source (~2000 lines)
│   └── Makefile                  # make start
│
├── surf-seer/                    # Managed project (user's repo)
│   ├── _bmad/                    # Snapshotted method version
│   ├── _bmad-output/             # Planning artifacts
│   │   └── planning-artifacts/
│   ├── src/                      # Code (Implementation phase)
│   └── .git/
│
└── new-startup-idea/             # Another managed project
    ├── _bmad/
    ├── _bmad-output/
    └── .git/
```

- **Local Docker Desktop:** Workspace root collected via first-run modal, stored in `.vibe/config.yaml`. Projects are sibling directories nominated by the user.
- **Multi-repo model:** Each project is an independent Git repo. Projects graduate to development repos at Implementation phase — the same repo that holds planning artifacts receives source code. One `git log` tells the story from idea to code.
- **Stateless tool:** All durable state lives in project repositories. Cross-project config is a lightweight path registry in `.vibe/config.yaml`. SQLite index is ephemeral — rebuilt on startup from scanning registered project repos. The tool is independently upgradeable without affecting any project.

### Architecture Overview

```
┌─────────────────────────────────────────────────┐
│                   LLM Agent                      │
│  (reads BMAD step files, facilitates convo,      │
│   calls tools, adapts to user)                   │
├─────────────────────────────────────────────────┤
│              Tool Interface (18 functions)        │
│  project.*  artifact.*  state.*  workspace.*     │
├─────────────────────────────────────────────────┤
│           Infrastructure Services                │
│  GitStateEngine  SQLiteIndex  StateOpQueue       │
│  AutoSaveService  SessionLock  VaultHealth       │
│  ArtifactValidator                               │
├─────────────────────────────────────────────────┤
│              Toad Framework                       │
│  ToadApp  ACP  Settings  Theme  Sidebar  Prompt  │
├─────────────────────────────────────────────────┤
│           UI (3 concerns)                        │
│  WelcomeScreen  BMADJourneyMap  ConversationPanel│
│  (Toad's panel + minimal ceremony enhancements)  │
└─────────────────────────────────────────────────┘
```

Five layers. Agent at top. Tools in the middle. Infrastructure below. Toad as the platform. UI as the presentation.

### Tool Interface (18 Functions)

**Project Management:**
- `project.create(name, path)` — creates directory, `git init`, copies `_bmad/` method snapshot from tool
- `project.open(path)` — loads state from Git history, rebuilds SQLite index, returns ProjectState
- `project.list()` — scans config registry, returns project summaries with health status
- `project.health_check()` — `git fsck`, bind mount check, returns status with recovery guidance

**Artifact Management:**
- `artifact.write(name, content, type)` — validates (frontmatter, wikilinks, structure), writes file, commits atomically. Detects vault-resident projects and adds vault-aware frontmatter/wikilinks.
- `artifact.read(name)` — returns artifact content from project directory
- `artifact.list()` — returns all artifacts with metadata (name, type, phase, checkpoint)
- `artifact.validate(content)` — checks frontmatter, wikilink resolution, structure. Returns issues list.

**State Management:**
- `state.checkpoint(summary, decisions)` — creates intentional Git commit with structured metadata
- `state.get_current()` — returns current phase, step, decision registry, last checkpoint summary
- `state.get_decisions()` — returns full decision registry (all decisions across all steps)
- `state.get_history()` — returns checkpoint chain for Journey Map rendering (phases, nodes, status, dates)

**Workspace:**
- `workspace.read_file(path)` — returns file content (path-sandboxed to project root)
- `workspace.list_files()` — returns project directory listing with file metadata
- `workspace.detect_changes()` — returns new/modified/deleted files since last check
- `workspace.get_agent_roster()` — returns BMAD agent manifest data for Party Mode personas

Each tool function: validates inputs, performs operation, returns structured result. Pure Python, fully testable, ~20-80 lines each. Total ~500-800 lines.

### Infrastructure Services (7)

**`GitStateEngine` (~200 lines):** Wraps GitPython. Commit, branch, read log, health check. Exposes operation boundaries (pre-commit, post-write, post-commit hooks) for chaos testing. Standard Git commands only — no extensions.

**`SQLiteCheckpointIndex` (~150 lines):** Projects table + checkpoints table. Git SHA as primary key. Insert, query by project/phase/step, rebuild from Git log. Deterministic rebuild — no auto-increment IDs, no insertion-order dependencies. Pure function of Git history across multiple repos.

**`StateOperationQueue` (~100 lines):** Async queue with priority levels. Serialises all Git-mutating operations. Intentional operations (artifact writes, checkpoints) pre-empt auto-save. Auto-save yields and retries on next timer tick. Prevents the auto-save collision problem (auto-save firing mid-artifact-write).

**`AutoSaveService` (~50 lines):** 2-minute timer. On tick: `git status` to detect changes, enqueue auto-save commit at low priority via `StateOperationQueue`. Commit message: deterministic template `[session-auto] {timestamp} | {files_changed} files | Step: {current_step}`. Also detects new workspace files and queues notification for the agent's next turn.

**`SessionLockManager` (~50 lines):** File-based lock in project directory. Atomic acquire/release. Stale lock detection (PID check). On conflict: offer read-only Journey Map view or lock takeover with original session gracefully degraded.

**`VaultHealthMonitor` (~80 lines):** Walks parent directories for `.obsidian/` folder to detect Obsidian vault. Checks bind mount is writable. Reports vault status (path, writable, last save timestamp). When vault-resident: proposes `.obsidianignore` entries for `.git/`, `src/`, `_bmad/`, etc.

**`ArtifactValidator` (~100 lines):** Parses YAML frontmatter. Checks all `[[wikilinks]]` resolve to existing files within project. Validates section structure (no orphaned headers, minimum content). Returns issues list. Integrated into `artifact.write()` — write fails if critical validation fails, warns on non-critical issues.

### UI Layer (3 Concerns)

**`MadFrogApp(ToadApp)` (~100 lines):** Overrides `compose()` to add Journey Map sidebar and Welcome Screen. Watches `.mad_frog/state.json` via watchdog for MCP server state changes. Registers `Ctrl+S` keybinding for manual checkpoint (FR33). First-run check on mount — redirects to `WorkspaceSetupScreen` if no `.vibe/config.yaml` found. Tools are exposed via a separate MCP server process (see Step 4 decisions), not registered directly on the app.

**`BMADJourneyMap(Tree)` (~150 lines):** Sidebar widget reading from `state.get_history()`. Renders phase nodes with state icons (✅ completed, 🔵 in-progress, 🔒 locked, ⚠️ stale). Temporal labels (dates, descriptions — never Git identifiers). Expand/collapse (current phase expanded by default). Click events translated to agent messages: "User wants to navigate to checkpoint X" — the agent handles confirmation and context switching conversationally.

**`WelcomeScreen` (~100 lines):** Displays project list from `project.list()` as Rich Panels with project name, phase, last-active date, and context snippet from last checkpoint. Three actions: "Start new project" (→ agent asks for name, creates via `project.create()`), "Open existing project" (→ shows sibling directories), "Resume project" (→ shows registered projects). Tiered loading: project names immediately from config cache, health status populated in background via Textual Workers.

**Ceremony/landmark TCSS (~50 lines):** Minimal styling extensions to Toad's theme. Semantic colour tokens (`--mf-completed`, `--mf-active`, `--mf-stale`, `--mf-error`, `--mf-ceremony`). Phase completion banner styling. Topic transition divider styling. All colours inherit from Toad's theme system.

**`WorkspaceSetupScreen` (~50 lines):** First-run modal asking workspace root path, saved to `.vibe/config.yaml`. Redirects to WelcomeScreen on completion.

### Core Data Structures

```
ProjectRecord:
  id: str                    # project name, unique
  path: Path                 # absolute path to project directory
  method_version: str        # tree hash of _bmad/ snapshot
  current_phase: Phase       # analysis/planning/solutioning/implementation
  current_step: str          # step file reference
  created_at: datetime
  last_active: datetime
  status: ProjectStatus      # active/archived/unhealthy

Checkpoint:
  git_sha: str               # primary key
  project_id: str
  parent_sha: str | None
  phase: Phase
  step: str
  checkpoint_type: str       # "phase_complete", "manual", "session_auto"
  summary: str               # human-readable
  decisions: list[Decision]
  timestamp: datetime

Decision:
  step: str
  topic: str
  decision: str
  rationale: str
  artifact_ref: str | None   # wikilink to affected artifact
```

### Obsidian Integration (Zero-Config)

Obsidian integration is not a separate system. It's a set of conventions activated when the project directory is inside an Obsidian vault.

- **Detection:** `VaultHealthMonitor` walks parent directories looking for `.obsidian/`. If found, project is flagged as "vault-resident."
- **Vault-resident behaviours:** Propose `.obsidianignore` entries conversationally during project setup. Generate wikilinks relative to vault root. Include vault-aware frontmatter (`aliases`, `tags`). Validate wikilink resolution against project structure.
- **Non-vault behaviours (default):** Standard Obsidian-native markdown (frontmatter + wikilinks relative to project). If the user later opens the folder as a vault, it works with zero modification.
- **Wikilink scope:** Project-directory for MVP (wikilinks between project artifacts). Optimistic vault-wide linking for references to existing vault notes. Full vault indexing deferred to post-MVP.
- **Principle:** One artifact format, two behaviour modes. Always Obsidian-native. Vault-residency enhances, doesn't change the format.

### Method Version Management

- `project.create()` copies the current `_bmad/` directory from the tool into the project repo as a snapshot
- The project always runs against its own `_bmad/` snapshot — BMAD updates to the tool don't affect existing projects
- The method snapshot travels with the project repo (portable provenance) — if pushed to GitHub, the methodology version is preserved alongside the artifacts
- `project.open()` loads step files from the project's `_bmad/` snapshot
- Tree hash of `_bmad/` recorded in project metadata for drift detection
- Explicit `bmad migrate-project` command for intentional method version upgrades (copies latest `_bmad/` from tool, summarises changes)
- Three independent update vectors: Toad framework, BMAD core method, community workflow templates — each with independent cadence, none affecting existing projects without explicit action

### Two-Tier State Model

| Tier | Contents | Persistence | Recovery |
|------|----------|-------------|----------|
| **Tier 1 (durable)** | Git commits, artifact files, decision registry, `_bmad/` snapshot | Filesystem (Git repo) | Source of truth — survives container destruction |
| **Tier 1.5 (reconstructable)** | SQLite checkpoint index | Filesystem (ephemeral) | Rebuilt from Git history on startup |
| **Tier 2 (session)** | Conversation buffer, workflow position, in-progress drafts | In-memory | Lost on restart — rebuilt from Tier 1 on resume |

- On any failure: drop Tier 2, rebuild from Tier 1
- Maximum data loss: last auto-save commit (2 min) + uncommitted conversation since then
- The agent reconstructs context on resume by calling `state.get_current()` + `state.get_decisions()` — greeted conversationally, not as a status report

### Project Onboarding (5 Paths)

When the user opens an existing directory via `project.open()`:

| Path | Detection | Behaviour |
|------|-----------|-----------|
| **Greenfield** | No `.git/`, no `_bmad/` | `git init`, copy method snapshot, start fresh |
| **Existing Git repo** | Has `.git/`, no `_bmad/` | "I see this is an existing project. Want me to set up BMAD planning?" Copy method snapshot, create initial checkpoint |
| **Mad Frog project** | Has `_bmad/` + Git checkpoints with metadata | Normal resume — load state, agent greets with context |
| **Version mismatch** | Has `_bmad/` with different method version than tool | "This project uses BMAD v6.0.4, you're running v6.1.0. Continue with project's version or migrate?" |
| **Brownfield with artifacts** | Has `_bmad-output/` artifacts but no structured Git state | "I see existing planning artifacts. Want me to validate these and pick up where you left off?" Infer phase state from artifact inspection |

The brownfield path (path 5) is the critical adoption feature — every early adopter will have existing BMAD artifacts from manual use.

### Safety Nets (Not Guardrails)

Safety nets catch agent mistakes without constraining agent behaviour. They fire less as models improve — the architecture gracefully becomes simpler over time.

1. **Auto-save:** Every 2 minutes, `AutoSaveService` commits any uncommitted changes via `StateOperationQueue`. Even if the agent forgets to checkpoint, max 2 minutes of work is at risk.

2. **Unwritten artifact detection:** If the conversation panel detects artifact-like content (structured markdown with frontmatter) but no `artifact.write()` tool call was made, it prompts: "It looks like an artifact was generated but not saved. Would you like to save it?"

3. **Wikilink validation:** `ArtifactValidator` catches broken wikilinks on every `artifact.write()`. Reports issues to the agent, which can correct and retry.

4. **State rebuild from Git:** `project.open()` reconstructs all state from Git history. Whatever was committed is recoverable. SQLite index rebuilt on every startup.

5. **Atomic operations:** `StateOperationQueue` ensures artifact write + Git commit succeed together or both roll back. No partial state, regardless of what the agent does.

### Critical Data Flows

**Flow 1: Artifact Generation (the core value loop)**

```
User types in Toad's prompt
  → Agent processes with BMAD step file context + tools
  → Agent generates artifact content
  → Agent calls artifact.write(name, content, type)
    → ArtifactValidator checks frontmatter, wikilinks, structure
    → If valid: StateOperationQueue enqueues at INTENTIONAL priority
      → File written to project/_bmad-output/
      → Git commit with checkpoint metadata
      → SQLiteCheckpointIndex updated
    → If invalid: issues returned to agent, agent can fix and retry
  → Agent calls state.checkpoint(summary, decisions)
    → Decision registry updated
    → Git commit with structured metadata
  → BMADJourneyMap refreshes from state.get_history()
  → Agent confirms to user: "Saved to your project."
```

**Flow 2: Session Resume**

```
User opens browser → MadFrogApp starts
  → Workspace config check (redirect to WorkspaceSetupScreen if no .vibe/config.yaml)
  → WelcomeScreen shows projects from project.list()
  → User clicks a project
  → project.open(path):
      → SessionLockManager.acquire() (atomic)
      → Git state loaded, SQLite index rebuilt
      → Returns ProjectState (phase, step, decisions, last checkpoint)
  → Agent receives project state via state.get_current()
  → Agent greets conversationally: "We were working on X. Want to continue?"
  → Normal conversation loop begins
```

### Architectural Principles

1. **Intelligence in the agent, infrastructure in the code.** The agent reads step files, facilitates conversations, and decides when to call tools. Our code provides tools that are safe, atomic, and fast. As models improve, the product improves — without code changes.

2. **18 tools, not 18 engines.** Every capability Mad Frog adds is a tool function the agent can call. Tools are thin wrappers around infrastructure. If a capability can be agent behaviour instead of a tool, it should be.

3. **Lean into Toad.** Subclass `ToadApp`. Use Toad's agent protocol, settings, theme, sidebar, prompt. Extend minimally. Our TCSS is under 50 lines. Accept framework coupling as a feature — it's what gives us the UI for free.

4. **Project repo is the user's deliverable.** All durable state in the project's Git repo. Commit messages are human-meaningful. Branch names are GitHub-ready. The repo is pushable as-is. The tool is stateless and independently upgradeable.

5. **Safety nets, not guardrails.** Auto-save catches uncommitted work. UI detects unwritten artifacts. Validators catch broken wikilinks. State rebuilds from Git. These nets catch agent mistakes without constraining agent behaviour. They fire less as models improve.

6. **Test tools, not intelligence.** ~65 deterministic tests in under 2 minutes. Agent quality validated through acceptance testing and improves for free with every model upgrade.

### Unresolved Decisions (for Later Architecture Steps)

1. ~~Exact Toad ACP tool registration mechanism~~ → **Resolved in Step 4: MCP server via mcpServers injection**
2. ~~Ceremony/landmark rendering approach~~ → **Resolved in Step 4: Agent markdown + sidebar state file**
3. ~~Auto-save timer implementation~~ → **Resolved in Step 4: MCP server internal asyncio timer**
4. ~~Session lock mechanism~~ → **Resolved in Step 4: File-existence lock with PID check**
5. Workspace root mount strategy details (`devcontainer.json` configuration)

### Explicit MVP Deferrals

- Conversation transcript persistence (FR53-55) — decision registry + Git metadata sufficient for MVP
- AI-generated auto-save commit messages — deterministic templates instead
- Full vault indexing for cross-vault wikilinks — optimistic linking instead
- CIS fast-track upgrade (step-skipping based on existing artifacts) — CIS outputs as reference material instead
- Smart method version compatibility checking — snapshot + drift detection instead
- Vector/semantic search over transcripts — potential FTS5 post-MVP
- Telemetry (FR85) — trivial to add later via tool call logging
- Deep workflow stack nesting — agent manages sub-workflow transitions by reading step files directly

### Build Sequence

**Week 1 — Walking Skeleton:**
- `MadFrogApp(ToadApp)` with `compose()`
- 3 core tools: `project.create()`, `artifact.write()`, `state.checkpoint()`
- `GitStateEngine` (basic commit operations)
- Acceptance test: create project → agent writes artifact → committed to Git

**Week 2 — Persistence & Navigation:**
- `SQLiteCheckpointIndex` + `state.get_history()` + full `state.*` tools
- `BMADJourneyMap` widget
- `project.open()` with state reconstruction from Git
- `AutoSaveService` + `StateOperationQueue`
- `workspace.*` tools
- Acceptance test: resume project → Journey Map shows history → auto-save running

**Week 3 — Polish & Safety:**
- `WelcomeScreen` with `project.list()` + `WorkspaceSetupScreen`
- `SessionLockManager`
- `VaultHealthMonitor` + vault-aware `artifact.write()`
- `ArtifactValidator` integrated into write pipeline
- Chaos tests (5 NFR-REL-10 scenarios)
- Acceptance test: full end-to-end — create, converse, write, resume, vault detection, chaos recovery

### Test Strategy

| Level | What | Count | Runtime |
|-------|------|-------|---------|
| Tool unit tests | Each tool function: happy path + error path | ~30 | < 30s |
| Infrastructure tests | GitStateEngine, SQLiteIndex, StateOpQueue, SessionLock | ~20 | < 30s |
| Widget pilot tests | JourneyMap, WelcomeScreen, MadFrogApp integration | ~10 | < 60s |
| Chaos tests | 5 NFR-REL-10 failure scenarios | 5 | Pre-release |
| Recorded session replay | Tool call sequence replay, end-to-end state verification | ~5 | Nightly |
| Acceptance tests | Full user journeys with real LLM | Manual | Release gate |

**Total automated: ~65 tests in under 2 minutes.** Fast feedback, zero LLM-dependent flakiness.

### Risk Register

| Risk | Status | Mitigation |
|------|--------|------------|
| Auto-save collides with intentional commit | Mitigated | `StateOperationQueue` with priority pre-emption |
| Agent doesn't call tools when it should | Mitigated | Safety nets: auto-save, unwritten artifact detection, wikilink validation |
| Toad API changes break MadFrogApp | Accepted | Pin version, full test suite on bump |
| Agent forgets earlier decisions mid-workflow | Mitigated | Decision registry persisted as Obsidian-native markdown, always available via `state.get_decisions()` |
| SQLite index corrupted | Mitigated | Ephemeral — rebuilt from Git on every startup |
| Nested Git repos (project inside existing repo) | Mitigated | Detection on `project.create()`, user warning |
| Context window exhaustion on large projects | Accepted | Agent manages own context; models are getting larger; selective tool queries |
| Community workflow breaks existing projects | Mitigated | Method snapshot per-project, `bmad validate-workflow` in CI |
| Conversation buffer lost on crash | Accepted | Tier 2 state — max 2-min loss bounded by auto-save |
| BMAD method format changes | Resilient | Agent reads step files directly — no interpreter to break. New format = agent adapts |
| LLM model improvements change behaviour | Beneficial | Tool-use architecture means model improvements flow through automatically |

## Starter Template Evaluation

### Primary Technology Domain

**Python TUI Application (Toad / Textual Web)** — single-stack Python application. Toad provides the UI, agent protocol (ACP), and web serving. No frontend/backend split.

### Verified Dependency Versions

| Dependency | Version | Source | Notes |
|-----------|---------|--------|-------|
| **Toad** (`batrachian-toad`) | 0.5.35 (PyPI) / 0.6.8 (main) | Transitive: Textual, GitPython, aiosqlite | Requires **Python >=3.14** |
| **Python** | 3.14.3 (latest stable) | Runtime | **Not 3.13** — Toad hard requirement |
| **Textual** | 8.0.2 | Via Toad | Production/Stable |
| **GitPython** | 3.1.46 | Via Toad | Already a Toad dependency — not declared separately |
| **aiosqlite** | 0.22.1 | Via Toad | Already a Toad dependency — replaces stdlib sqlite3 |
| **pytest** | 9.0.2 | Dev dependency | Native TOML config, async support |
| **ruff** | 0.15.1 | Dev dependency | Linter + formatter, Rust-fast |
| **uv** | 0.10.9 | Project/package manager | Lockfile support, Python version management |

**Critical finding:** Toad requires Python >=3.14 (not 3.13 as PRD originally specified). PRD updated accordingly.

**Decision:** Python 3.14 with standard GIL. Free-threaded (no-GIL) mode evaluated and deferred — Mad Frog's workload is I/O-bound (Git subprocess, SQLite queries, Textual event loop), gaining zero performance benefit from true parallelism. No-GIL introduces non-deterministic race condition risk with experimental ecosystem support. Revisit when free-threaded mode reaches stable status.

### Selected Approach: `uv init` + Architecture-Aligned Structure

No existing starter template matches the Mad Frog architecture (Toad subclass + Git state engine + tool-use pattern). The architecture IS the scaffold.

**Rationale:**
- `uv` is the current standard Python project manager (10x faster than pip, native lockfile)
- Our ~2000-line codebase doesn't benefit from heavy scaffolding
- Single production dependency (`batrachian-toad`) — GitPython and aiosqlite are transitive
- Dev Container config is straightforward Python 3.14 setup

### Initialization Command

```bash
uv init mad_frog --python 3.14
cd mad_frog
uv add batrachian-toad
uv add --dev pytest pytest-asyncio pytest-cov textual-dev ruff
```

### Production Dependencies

```toml
[project]
name = "mad-frog"
version = "0.1.0"
description = "A Toad app for guided BMAD planning"
requires-python = ">=3.14"
license = "MIT"
dependencies = [
    "batrachian-toad>=0.5.35",
]

[dependency-groups]
dev = [
    "pytest>=9.0",
    "pytest-asyncio>=0.25",
    "pytest-cov>=7.0",
    "textual-dev>=2.0",
    "ruff>=0.15",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"

[tool.ruff]
target-version = "py314"
line-length = 120

[tool.ruff.lint]
select = ["E", "F", "I", "UP"]

[tool.coverage.run]
source = ["src/mad_frog"]

[tool.coverage.report]
fail_under = 85
```

**One production dependency.** GitPython and aiosqlite are transitive via Toad. This is the "lean into Toad" principle taken to its logical conclusion — Toad brings the entire infrastructure stack.

### Key Technical Decisions from Starter Evaluation

**`aiosqlite` over stdlib `sqlite3`:** Toad already depends on `aiosqlite>=0.22.1`. For a Textual app where the asyncio event loop is sacred, a blocking `sqlite3` query during Journey Map render would freeze the UI. `aiosqlite` is native async, zero added dependency. `SQLiteCheckpointIndex` uses `aiosqlite` throughout.

**`uv` as package manager:** Lockfile for reproducible builds, Python version management via `.python-version` file, `uv run` ensures commands use the project virtualenv. All `Makefile` targets use `uv run`.

**`hatchling` as build backend:** Matches Toad's own build system. Consistent developer mental model.

**`ruff` for linting and formatting:** Rust-fast, zero config beyond `pyproject.toml`. Replaces flake8, isort, black in a single tool.

**PEP 735 `[dependency-groups]`:** Modern dev dependency declaration, supported in Python 3.14 and `uv`.

### Toad Integration Discovery

**Entry point:** Toad's CLI is `toad` → `toad.cli:main`. Mad Frog integrates as a custom Toad app, likely via `toad serve --app mad_frog`. Exact integration mechanism to be spiked in story one.

**ACP tool registration:** Toad uses the Agent Client Protocol (ACP). Tool functions are exposed via MCP servers passed in the `mcpServers` parameter of `session/new`. Toad v0.6.8 passes an empty list; MadFrogApp overrides `acp_new_session` to inject our MCP server. The AI agent discovers our tools via standard MCP `tools/list`. See Step 4 Decision 1 for full details.

### Complete Starter Skeleton

```
mad_frog/
├── .devcontainer/
│   └── devcontainer.json          # Python 3.14, uv sync, port 8000, API key passthrough
├── .github/
│   └── workflows/
│       └── ci.yml                 # pytest + coverage + ruff
├── agents/
│   └── claude.toml                # ACP agent config (reference implementation)
├── src/mad_frog/
│   ├── __init__.py                # empty
│   ├── py.typed                   # PEP 561 marker
│   ├── app.py                     # MadFrogApp(ToadApp) entry point (~100 lines)
│   ├── constants.py               # TOOL_ROOT, BMAD_SOURCE, DEFAULT_WORKSPACE
│   ├── models.py                  # ProjectRecord, Checkpoint, Decision, Phase enum
│   ├── mad_frog.tcss              # ~50 lines semantic colour tokens
│   ├── tools/
│   │   ├── __init__.py            # empty
│   │   ├── base.py                # @tool decorator (logging, validation, error wrapping)
│   │   ├── project.py             # project.create/open/list/health_check
│   │   ├── artifact.py            # artifact.write/read/list/validate
│   │   ├── state.py               # state.checkpoint/get_current/get_decisions/get_history
│   │   └── workspace.py           # workspace.read_file/list_files/detect_changes/get_agent_roster
│   ├── services/
│   │   ├── __init__.py            # empty
│   │   ├── git_state_engine.py    # ~200 lines, wraps GitPython
│   │   ├── sqlite_checkpoint_index.py  # ~150 lines, aiosqlite
│   │   ├── state_operation_queue.py    # ~100 lines, async priority queue
│   │   ├── auto_save_service.py        # ~50 lines, 2-min timer
│   │   ├── session_lock_manager.py     # ~50 lines, file-based lock
│   │   ├── vault_health_monitor.py     # ~80 lines, .obsidian/ detection
│   │   └── artifact_validator.py       # ~100 lines, frontmatter + wikilinks
│   └── ui/
│       ├── __init__.py            # empty
│       ├── welcome_screen.py      # ~100 lines
│       ├── journey_map.py         # BMADJourneyMap(Tree) ~150 lines
│       └── conversation_panel.py  # ~100 lines (Toad's + enhancements)
├── tests/
│   ├── conftest.py                # tmp_git_repo (with initial commit), tmp_db (aiosqlite :memory:)
│   ├── tools/                     # ~30 tool unit tests
│   ├── services/                  # ~20 infrastructure tests
│   └── ui/                        # ~10 widget pilot tests (async)
├── .gitignore                     # __pycache__, .venv, *.egg-info, dist, .coverage, .ruff_cache, *.db, .env
├── .python-version                # 3.14
├── pyproject.toml                 # single dep: batrachian-toad
├── Makefile                       # dev, start, test, lint, fmt — all via uv run
└── README.md                      # 3-line quick start
```

### Dev Container Configuration

```json
{
  "name": "Mad Frog",
  "image": "mcr.microsoft.com/devcontainers/python:3.14",
  "features": {
    "ghcr.io/devcontainers/features/git:1": {}
  },
  "postCreateCommand": "uv sync",
  "forwardPorts": [8000],
  "remoteEnv": {
    "ANTHROPIC_API_KEY": "${localEnv:ANTHROPIC_API_KEY}",
    "VIBE_WORKSPACE": "${localEnv:VIBE_WORKSPACE:-/workspaces}"
  },
  "customizations": {
    "vscode": {
      "extensions": ["charliermarsh.ruff", "ms-python.python"]
    }
  }
}
```

### Makefile

```makefile
dev:
	uv sync

start:
	uv run mad_frog

test:
	uv run pytest

lint:
	uv run ruff check src/ tests/

fmt:
	uv run ruff format src/ tests/
```

### CI Configuration

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
      - run: uv sync
      - run: uv run pytest --cov --cov-report=xml
      - run: uv run ruff check src/ tests/
```

### Architectural Decisions Established by Starter

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Python version | 3.14 (GIL on) | Toad hard requirement; no-GIL deferred |
| Package manager | uv | Fast, lockfile, Python version management |
| Build backend | hatchling | Matches Toad ecosystem |
| Production deps | batrachian-toad only | GitPython, aiosqlite transitive |
| Async database | aiosqlite | Non-blocking on Textual event loop, zero added dep |
| Linter/formatter | ruff | Single tool, Rust-fast, zero config |
| Test framework | pytest + pytest-asyncio + textual-dev | Async tests, widget pilot testing |
| Coverage floor | 85% overall | Enforced in CI from PR one |
| All `__init__.py` | Empty | Explicit imports, no barrel exports |
| Shared models | `models.py` | Prevents circular imports between tools/services/UI |

**Note:** Project initialisation using this starter skeleton should be the first implementation story. The Toad `serve --app` integration mechanism needs spiking as part of that story.

## Core Architectural Decisions

### Decision 1: Integration Model — MCP Server + ToadApp Subclass

**Context:** How does Mad Frog integrate with Toad and the AI agent?

**Evaluated options:**
1. **ACP Agent (separate process)** — register via TOML, agent-agnostic, but loses guided UI (no sidebar, no visual progress)
2. **ToadApp subclass only** — full widget control, but tool registration requires system prompt injection (fights the protocol)
3. **MCP Server + ToadApp subclass** — tools via MCP (protocol-compliant, agent-agnostic), UI via ToadApp subclass (sidebar, guided experience)

**Decision: Option 3 — MCP Server + ToadApp subclass.**

**Architecture:**

```
User runs: mad_frog ~/my-project

┌────────────────────────────────────────────────────────┐
│  MadFrogApp (ToadApp subclass)          Process 1      │
│  ┌──────────┐  ┌──────────────────────────────────┐    │
│  │ BMAD     │  │ Toad Conversation UI             │    │
│  │ Sidebar  │  │ (markdown, tool calls, diffs)    │    │
│  │          │  └──────────────┬───────────────────┘    │
│  │ watches  │                 │ ACP (JSON-RPC/stdio)   │
│  │ state    │                 │                        │
│  │ file  ◄─┼── ── ── ── ── ─┤                        │
│  └──────────┘                 │                        │
│                    ┌──────────▼──────────┐             │
│                    │  AI Agent (Claude)  │  Process 2   │
│                    │  launched by Toad   │             │
│                    └──┬──────────────┬──┘             │
│                       │              │                 │
│              ACP tools│     MCP tools│                 │
│              (fs,term)│    (bmad_*) │                 │
│                       │              │                 │
│              ┌────────▼─┐   ┌────────▼──────────┐     │
│              │  Toad     │   │  Mad Frog         │     │
│              │  built-in │   │  MCP Server       │ P3  │
│              │  RPC      │   │  (18 tools)       │     │
│              └───────────┘   │  git state,       │     │
│                              │  state file       │     │
│                              └───────────────────┘     │
└────────────────────────────────────────────────────────┘
```

**Three processes:**
1. **MadFrogApp** (Process 1) — Textual UI: sidebar navigation, welcome screen, conversation panel. Watches `state.json` for MCP server state changes via `watchdog`.
2. **AI Agent** (Process 2) — Claude or any ACP-compliant agent. Launched by Toad. Speaks ACP to Toad (file I/O, terminal) and MCP to our server (BMAD tools).
3. **Mad Frog MCP Server** (Process 3) — stdio MCP server launched by the AI agent. Exposes 18 BMAD tools via `tools/list`. Manages git state, writes state file for UI sync.

**Key data flows:**
- User clicks sidebar → synthetic prompt → AI agent responds with BMAD guidance
- AI agent calls `bmad_advance_workflow` → MCP server writes `state.json` → MadFrogApp sidebar updates
- AI agent calls `bmad_checkpoint` → MCP server does git commit → writes state
- Auto-save: MCP server internal timer (120s) → git commit → no AI agent involvement

**Rationale:**
- **Agent-agnostic:** Any ACP agent (Claude, Codex, Gemini, etc.) discovers our tools via standard MCP `tools/list`. No system prompt injection required.
- **Protocol-compliant:** Uses ACP's `mcpServers` parameter in `session/new` — the intended extension point for client-to-agent tool provisioning.
- **Guided UX preserved:** ToadApp subclass provides the sidebar, welcome screen, and visual progress tracking. The user never sees a slash command.
- **Clean separation:** UI in one process, tools in another. Each independently testable.

**Toad integration point:**

```python
class MadFrogAgent(Agent):
    async def acp_new_session(self) -> None:
        """Override to inject our MCP server into the session."""
        with self.request():
            session_new_response = api.session_new(
                str(self.project_root_path),
                [
                    {
                        "name": "mad-frog-bmad",
                        "command": "python",
                        "args": ["-m", "mad_frog.mcp_server"],
                    }
                ],
            )
        response = await session_new_response.wait()
        # ... rest follows parent pattern
```

Toad v0.6.8 passes `mcpServers: []` (empty list) in `acp_new_session`. We override to include our MCP server. The AI agent receives the MCP server config during session setup and connects automatically.

### Decision 2: Data Models — TypedDict + dataclass (stdlib)

**Context:** How do we define data contracts for tool inputs/outputs, settings, and internal state?

**Evaluated options:**
1. **Pydantic V2 BaseModel** — rich validation, JSON Schema generation, BaseSettings for env vars
2. **stdlib TypedDict + dataclass** — matches Toad's patterns exactly, zero added dependency
3. **attrs** — similar to dataclass but with more features

**Decision: TypedDict + dataclass (stdlib).**

**Rationale:**
- Toad uses `TypedDict` and `dataclass` exclusively. Zero Pydantic in Toad's codebase or dependency tree.
- MCP tool schemas are JSON Schema dicts — no Pydantic `.model_json_schema()` needed; we write schemas directly.
- Tool returns use MCP's `CallToolResult` format (`content` + `isError`) — no custom return model.
- Settings use Toad's `SchemaDict` pattern or plain `dataclass` + `os.environ`.
- `typeguard>=4.4.4` (Toad transitive dep) provides runtime type checking for TypedDicts if needed during development.
- One dependency: `batrachian-toad`. Nothing added.

**Data model patterns:**

```python
# Internal state — dataclass
@dataclass
class ProjectRecord:
    id: str
    path: Path
    method_version: str
    current_phase: str
    current_step: str
    created_at: str
    last_active: str
    status: str

# Wire format — TypedDict (matches Toad's SchemaDict pattern)
class CheckpointResult(TypedDict):
    git_sha: str
    phase: str
    step: str
    summary: str
    timestamp: str

# DB results — TypedDict + cast (matches Toad's DB pattern)
class SessionRow(TypedDict):
    id: int
    project_path: str
    current_phase: str
    artifacts_json: str
    git_ref: str
    created_at: str
    updated_at: str

# cast(SessionRow, dict(row))  # Toad's pattern exactly
```

**Settings:**

```python
# Follow Toad's Settings class pattern, not Pydantic BaseSettings
@dataclass
class MadFrogConfig:
    workspace_root: Path = field(default_factory=lambda: Path.home() / "Development")
    auto_save_interval: int = 120

    @classmethod
    def from_env(cls) -> "MadFrogConfig":
        return cls(
            workspace_root=Path(os.environ.get("VIBE_WORKSPACE", str(Path.home() / "Development"))),
            auto_save_interval=int(os.environ.get("MAD_FROG_AUTO_SAVE", "120")),
        )
```

### Decision 3: MCP Server Implementation

**Context:** How do we implement the stdio MCP server that exposes BMAD tools?

**Decision: Lightweight custom MCP server using stdio JSON-RPC.**

**MCP lifecycle:**
1. AI agent launches our server as subprocess: `python -m mad_frog.mcp_server`
2. Agent sends `initialize` → we respond with `{"capabilities": {"tools": {"listChanged": false}}}`
3. Agent sends `tools/list` → we respond with 18 tool definitions (name, description, inputSchema)
4. Agent sends `tools/call` with `name` + `arguments` → we execute and return `CallToolResult`
5. Agent closes stdin → we exit

**Transport:** stdio — newline-delimited JSON-RPC over stdin/stdout. No HTTP, no SSE. Matches ACP's McpServer transport (`command` + `args`).

**Tool definitions (18 tools):**

| Tool Name | Description | Key Parameters |
|-----------|-------------|----------------|
| `bmad_checkpoint` | Save state as git commit | `phase`, `summary` |
| `bmad_restore` | Restore from previous checkpoint | `ref` |
| `bmad_history` | List checkpoint history | `limit` |
| `bmad_advance_workflow` | Advance workflow step, update sidebar | `workflow`, `step`, `status` |
| `bmad_get_workflow_state` | Get all workflow/phase states | — |
| `bmad_get_step_prompt` | Get BMAD step file content | `workflow`, `step` |
| `bmad_write_artifact` | Write artifact to output directory | `artifact_type`, `filename`, `content` |
| `bmad_read_artifact` | Read existing artifact | `artifact_type`, `filename` |
| `bmad_list_artifacts` | List artifacts by type | `artifact_type` (optional) |
| `bmad_session_info` | Get session metadata | — |
| `bmad_lock_session` | Acquire session lock | `project_path` |
| `bmad_unlock_session` | Release session lock | — |
| `bmad_get_agent_persona` | Get BMAD agent persona data | `agent_name` |
| `bmad_list_agents` | List available BMAD agents | — |
| `bmad_auto_save_status` | Get auto-save timer status | — |
| `bmad_update_method` | Update BMAD method in project via npx bmad update | `project_path` |
| `bmad_detect_changes` | Detect new/modified/deleted files since last checkpoint | — |
| `bmad_report_context` | Report agent context window size for pre-emptive save | `context_window_tokens` |

**Tool return format (MCP CallToolResult):**

```python
# Success
{"content": [{"type": "text", "text": json.dumps(result_data)}], "isError": False}

# Error
{"content": [{"type": "text", "text": f"Error: {description}"}], "isError": True}
```

No custom `ToolResult` model. The MCP protocol IS the contract.

**Server structure:**

```python
# mad_frog/mcp_server.py
async def handle_request(request: dict) -> dict | None:
    match request.get("method"):
        case "initialize":
            return initialize_response(request["id"])
        case "notifications/initialized":
            return None  # notification, no response
        case "tools/list":
            return tools_list_response(request["id"])
        case "tools/call":
            return await dispatch_tool(request["id"], request["params"])
        case _:
            return method_not_found(request["id"], request["method"])

async def main():
    """Stdio transport: newline-delimited JSON-RPC."""
    reader = asyncio.StreamReader()
    await asyncio.get_event_loop().connect_read_pipe(
        lambda: asyncio.StreamReaderProtocol(reader), sys.stdin
    )
    while True:
        line = await reader.readline()
        if not line:
            break
        request = json.loads(line.decode())
        response = await handle_request(request)
        if response is not None:
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()
```

### Decision 4: State Synchronisation — MCP Server ↔ UI

**Context:** The MCP server (Process 3) manages BMAD state. The UI (Process 1) needs to reflect state changes in the sidebar. These are separate processes.

**Decision: Atomic state file + watchdog observer.**

**Mechanism:**
- MCP server writes `{project_root}/.mad_frog/state.json` on every state change
- Writes use atomic pattern: write to temp file, then `os.replace()` (atomic on POSIX)
- MadFrogApp watches `.mad_frog/` directory using `watchdog` (already a Toad dependency)
- On file change, MadFrogApp posts `BMADStateChanged` message → sidebar reacts

**State file format:**

```json
{
    "current_phase": "analysis",
    "workflows": {
        "create-product-brief": {"status": "in_progress", "step": "step-03"},
        "create-prd": {"status": "pending"}
    },
    "last_checkpoint": {
        "git_sha": "abc123f",
        "summary": "Product brief complete",
        "timestamp": "2026-03-09T12:00:00Z"
    },
    "checkpoint_history": [
        {"git_sha": "abc123f", "summary": "Product brief complete", "phase": "analysis", "type": "checkpoint", "timestamp": "2026-03-09T12:00:00Z"}
    ],
    "auto_save": {
        "last_save": "2026-03-09T12:02:00Z",
        "interval_seconds": 120,
        "enabled": true
    },
    "session_lock": {
        "pid": 12345,
        "acquired_at": "2026-03-09T11:00:00Z"
    },
    "updated_at": "2026-03-09T12:02:00Z"
}
```

**Rationale:**
- File-based: observable, debuggable, works across process boundaries without IPC setup
- Atomic writes: no partial reads, no corruption
- `watchdog`: already a Toad dependency, battle-tested filesystem observer
- Follows Toad's own patterns (`toad/directory_watcher.py` uses watchdog for project file monitoring)
- Simpler than Unix sockets, shared memory, or SQLite polling for MVP

### Decision 5: Auto-Save — MCP Server Internal Timer

**Context:** Auto-save every 2 minutes to bound maximum data loss.

**Decision: MCP server owns the auto-save timer. No AI agent involvement.**

Previous architecture had auto-save as `MadFrogApp.set_interval(120)` triggering the agent. This costs API tokens on every tick and interrupts conversation flow.

**Revised approach:** The MCP server is a long-running process (alive for the entire session). It runs its own `asyncio` timer alongside the stdio handler:

```python
class MadFrogMCPServer:
    async def run(self):
        asyncio.create_task(self._auto_save_loop())
        await self._stdio_loop()

    async def _auto_save_loop(self):
        while True:
            await asyncio.sleep(self.config.auto_save_interval)
            if self.git_engine.has_uncommitted_changes():
                self.git_engine.commit(
                    f"[session-auto] {datetime.now().isoformat()} | "
                    f"{self.git_engine.changed_file_count()} files | "
                    f"Step: {self.state.current_step}"
                )
                self._write_state_file()
```

**Benefits:**
- Zero token cost — no AI agent round-trip
- No conversation interruption
- Deterministic commit messages (template, not AI-generated)
- MCP server already has git access — natural home for this responsibility
- Timer managed by asyncio, not Textual — decoupled from UI lifecycle

### Decision 6: Sidebar ↔ Conversation Bridge

**Context:** User clicks a phase in the sidebar. How does this translate to an AI agent conversation?

**Decision: Synthetic user input via Textual message posting.**

When the user clicks a sidebar item, MadFrogApp composes the appropriate BMAD prompt and submits it as if the user typed it:

```python
class BMADSidebar(Widget):
    def on_click_phase(self, phase: str) -> None:
        prompt = f"I want to start the {phase} workflow."
        # Post as synthetic user input — Toad handles the rest
        self.app.post_message(UserInputSubmitted(prompt))
```

The AI agent receives this as a normal user message. Because it has access to our BMAD tools (via MCP), it can call `bmad_get_step_prompt` to load the workflow content and guide the user through the phase.

**Rationale:**
- Uses Toad's existing conversation flow — no new mechanism
- Agent-agnostic — the prompt is natural language, not a command
- Agent decides how to respond — maintains "intelligence in the agent" principle

### Decision 7: CLI Entry Point

**Context:** How does the user start Mad Frog?

**Decision: Custom `mad_frog` CLI that wraps Toad's agent resolution.**

```python
# Entry point: mad_frog
# pyproject.toml: [project.scripts] mad_frog = "mad_frog.cli:main"

import argparse

def main():
    parser = argparse.ArgumentParser(description="Mad Frog - BMAD Planning Tool")
    parser.add_argument("project_dir", nargs="?", default=".", help="Project directory")
    parser.add_argument("--agent", default="claude.com", help="AI agent identity")
    args = parser.parse_args()

    app = MadFrogApp(
        project_dir=Path(args.project_dir).resolve(),
        agent_identity=args.agent,
    )
    app.run()
```

The user runs `mad_frog ~/my-project`. They never run `toad` directly. Agent defaults to Claude but is configurable.

### Decision 8: Git Operations — GitPython subprocess wrapper

**Context:** How do we interact with Git?

**Decision: GitPython `repo.git.*` subprocess wrapper.** (Unchanged from previous evaluation.)

```python
class GitStateEngine:
    def __init__(self, repo_path: Path):
        self.repo = git.Repo(repo_path)

    def commit(self, message: str) -> str:
        self.repo.git.add(".")
        self.repo.git.commit("-m", message)
        return self.repo.head.commit.hexsha

    def has_uncommitted_changes(self) -> bool:
        return self.repo.is_dirty(untracked_files=True)

    def changed_file_count(self) -> int:
        return len(self.repo.git.status("--porcelain").splitlines())
```

Uses `repo.git.*` (subprocess calls per invocation) rather than `repo.index.*` (in-process libgit2). Stateless per-call, no resource leaks in long-running MCP server sessions.

### Decision 9: Session Lock — File-existence with PID check

**Context:** Prevent concurrent MCP server instances from modifying the same project.

**Decision: File-based lock with PID validation.** (Unchanged from previous evaluation.)

```python
class SessionLockManager:
    def __init__(self, project_path: Path):
        self.lock_file = project_path / ".mad_frog" / "session.lock"

    def acquire(self) -> bool:
        if self.lock_file.exists():
            pid = int(self.lock_file.read_text())
            if self._pid_alive(pid):
                return False  # Another session is active
            # Stale lock — previous process died
        self.lock_file.parent.mkdir(parents=True, exist_ok=True)
        self.lock_file.write_text(str(os.getpid()))
        return True

    def release(self) -> None:
        self.lock_file.unlink(missing_ok=True)
```

TOCTOU limitation documented and accepted for single-user MVP.

### Decision 10: Database — Own aiosqlite, Toad's pattern

**Context:** Persistent storage for BMAD session state beyond git commits.

**Decision: Own aiosqlite database, following Toad's exact pattern.**

```python
class BMADDatabase:
    async def open(self) -> aiosqlite.Connection:
        db = await aiosqlite.connect(self.db_path)
        db.row_factory = aiosqlite.Row
        return db

    async def create_schema(self) -> None:
        async with self.open() as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY,
                    project_path TEXT NOT NULL,
                    current_phase TEXT NOT NULL,
                    artifacts_json TEXT DEFAULT '{}',
                    git_ref TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            await db.commit()
```

No ORM. Raw SQL. `cast(SessionRow, dict(row))` for typing. Matches `toad/db.py` exactly.

### Revised Starter Skeleton

The starter skeleton from Step 3 needs updating to reflect the MCP architecture:

```
mad_frog/
├── .devcontainer/
│   └── devcontainer.json
├── .github/
│   └── workflows/
│       └── ci.yml
├── src/mad_frog/
│   ├── __init__.py
│   ├── py.typed
│   ├── cli.py                     # CLI entry point (argparse)
│   ├── app.py                     # MadFrogApp(ToadApp) — UI only
│   ├── agent.py                   # MadFrogAgent(Agent) — overrides acp_new_session
│   ├── constants.py
│   ├── models.py                  # dataclass + TypedDict definitions
│   ├── mad_frog.tcss
│   ├── mcp_server.py              # MCP server entry point (stdio JSON-RPC)
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── project.py             # bmad_create_project, bmad_open_project, etc.
│   │   ├── artifact.py            # bmad_write_artifact, bmad_read_artifact, etc.
│   │   ├── state.py               # bmad_checkpoint, bmad_restore, etc.
│   │   ├── workflow.py            # bmad_advance_workflow, bmad_get_step_prompt, etc.
│   │   └── session.py             # bmad_session_info, bmad_lock/unlock, bmad_list_agents, etc.
│   ├── services/
│   │   ├── __init__.py
│   │   ├── git_state_engine.py
│   │   ├── sqlite_index.py
│   │   ├── state_operation_queue.py
│   │   ├── auto_save_service.py
│   │   ├── session_lock_manager.py
│   │   ├── vault_health_monitor.py
│   │   ├── artifact_validator.py
│   │   └── state_file.py          # Atomic state.json read/write
│   └── ui/
│       ├── __init__.py
│       ├── welcome_screen.py
│       ├── journey_map.py
│       └── workspace_setup.py
├── tests/
│   ├── conftest.py
│   ├── test_mcp_server.py         # MCP protocol compliance tests
│   ├── tools/
│   ├── services/
│   └── ui/
├── .gitignore
├── .python-version                # 3.14
├── pyproject.toml
├── Makefile
└── README.md
```

**Key changes from Step 3 skeleton:**
- Added `mcp_server.py` — MCP server entry point
- Added `agent.py` — `MadFrogAgent(Agent)` with mcpServers injection
- Added `cli.py` — custom CLI entry point (replaces `toad serve --app`)
- Renamed `tools/base.py` → removed (no `@tool` decorator needed — MCP dispatch handles routing)
- Added `tools/workflow.py` and `tools/session.py` — split from previous groupings
- Added `services/state_file.py` — atomic state file for IPC
- Added `test_mcp_server.py` — MCP protocol compliance tests
- Removed `ui/conversation_panel.py` — Toad's conversation panel used as-is

### Revised Architecture Overview

Replaces the previous 5-layer diagram:

```
┌─────────────────────────────────────────────────┐
│              MadFrogApp (ToadApp)                │
│  BMADJourneyMap  WelcomeScreen  WorkspaceSetup   │
│  Watches state.json via watchdog                 │
├─────────────────────────────────────────────────┤
│              Toad Framework                       │
│  ToadApp  ACP  Conversation  Prompt  Terminal    │
├─────────────────────────────────────────────────┤
│         AI Agent (ACP, any provider)             │
│  Calls Toad tools (fs, terminal) via ACP         │
│  Calls BMAD tools (bmad_*) via MCP               │
├─────────────────────────────────────────────────┤
│         Mad Frog MCP Server (stdio)              │
│  18 tools: project, artifact, state, workflow    │
│  Auto-save timer, state file writer              │
├─────────────────────────────────────────────────┤
│         Infrastructure Services                  │
│  GitStateEngine  SQLiteIndex  StateOpQueue       │
│  SessionLock  VaultHealth  ArtifactValidator     │
└─────────────────────────────────────────────────┘
```

### Revised Unresolved Decisions

1. ~~Exact Toad ACP tool registration mechanism~~ → **Resolved: MCP server via mcpServers injection**
2. ~~Ceremony/landmark rendering approach~~ → **Resolved: Agent markdown via Toad's conversation panel, sidebar state via state file**
3. ~~Auto-save timer implementation~~ → **Resolved: MCP server internal asyncio timer**
4. ~~Session lock mechanism~~ → **Resolved: File-existence lock with PID check**
5. Workspace root mount strategy details (`devcontainer.json` configuration) — still open

### Revised Risk Register (Additions)

| Risk | Status | Mitigation |
|------|--------|------------|
| MCP server process dies mid-session | Mitigated | Auto-save ensures max 2-min data loss; agent gets MCP error, can report to user |
| State file race condition (write during read) | Mitigated | Atomic `os.replace()` writes; watchdog debouncing |
| AI agent doesn't call BMAD tools | Mitigated | Tool descriptions in MCP `tools/list` guide the agent; safety nets still apply |
| Toad v0.7 changes `acp_new_session` signature | Accepted | Pin `batrachian-toad>=0.5.35,<0.7`; integration test catches on bump |
| MCP protocol version mismatch | Low risk | Stable spec (2025-06-18); version negotiation in initialize handshake |

### Summary of All Step 4 Decisions

| # | Decision | Choice | Key Rationale |
|---|----------|--------|---------------|
| 1 | Integration model | MCP Server + ToadApp subclass | Agent-agnostic, protocol-compliant, guided UX preserved |
| 2 | Data models | TypedDict + dataclass (stdlib) | Matches Toad patterns, zero added deps |
| 3 | MCP server | Custom stdio JSON-RPC | 18 tools, standard MCP lifecycle, auto-save timer |
| 4 | State sync (MCP ↔ UI) | Atomic state file + watchdog | Observable, debuggable, uses existing Toad dep |
| 5 | Auto-save | MCP server internal timer | No token cost, no conversation interruption |
| 6 | Sidebar ↔ conversation | Synthetic user input | Uses Toad's existing flow, agent-agnostic |
| 7 | CLI entry point | Custom `mad_frog` CLI | User runs `mad_frog`, Toad is invisible |
| 8 | Git operations | GitPython `repo.git.*` | Subprocess wrapper, stateless, no resource leaks |
| 9 | Session lock | File-existence + PID check | ~20 lines, zero dep, sufficient for single-user MVP |
| 10 | Database | Own aiosqlite, Toad's pattern | Raw SQL, TypedDict casts, ephemeral/rebuildable |

## Implementation Patterns & Consistency Rules

### Purpose

These patterns prevent conflicts when multiple AI agents implement different parts of Mad Frog. Every pattern answers: "if two agents independently implement this, will the code be compatible?"

### The `@traced` Decorator — Applied to ALL Functions

Every function in the codebase — tools, services, UI methods, helpers — gets the `@traced` decorator. No exceptions. This provides:
- Try/catch with full traceback logging on failure
- Entry/exit logging with arguments and elapsed time
- Consistent error visibility across the entire codebase

```python
# mad_frog/services/decorators.py
import asyncio
import functools
import logging
import time
from typing import Callable, Any

logger = logging.getLogger("mad_frog")


def traced(func: Callable) -> Callable:
    """Try/catch + structured logging for all functions.

    Applied to EVERY function. Services re-raise exceptions after logging.
    Tool handlers catch and convert to MCP isError responses.
    """

    @functools.wraps(func)
    async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
        name = func.__qualname__
        logger.debug("call %s args=%s kwargs=%s", name, args, kwargs)
        start = time.perf_counter()
        try:
            result = await func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            logger.debug("ok %s elapsed=%.3fs", name, elapsed)
            return result
        except Exception:
            elapsed = time.perf_counter() - start
            logger.exception("fail %s elapsed=%.3fs", name, elapsed)
            raise

    @functools.wraps(func)
    def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
        name = func.__qualname__
        logger.debug("call %s args=%s kwargs=%s", name, args, kwargs)
        start = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            logger.debug("ok %s elapsed=%.3fs", name, elapsed)
            return result
        except Exception:
            elapsed = time.perf_counter() - start
            logger.exception("fail %s elapsed=%.3fs", name, elapsed)
            raise

    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    return sync_wrapper
```

**Enforcement rule:** If a function doesn't have `@traced`, the code review fails. No exceptions.

### Naming Patterns

| Category | Convention | Example |
|----------|-----------|---------|
| Python functions/variables | `snake_case` (PEP 8) | `get_workflow_state`, `project_path` |
| Python classes | `PascalCase` | `GitStateEngine`, `MadFrogApp` |
| Python constants | `UPPER_SNAKE_CASE` | `AUTO_SAVE_INTERVAL`, `TOOL_ROOT` |
| JSON keys (MCP responses) | `snake_case` | `{"git_sha": "abc", "current_phase": "analysis"}` |
| JSON keys (state file) | `snake_case` | `{"current_phase": ..., "last_checkpoint": ...}` |
| MCP tool names | `bmad_` prefix + `snake_case` | `bmad_checkpoint`, `bmad_write_artifact` |
| SQLite tables | `snake_case`, plural | `sessions`, `checkpoints` |
| SQLite columns | `snake_case` | `git_sha`, `project_path`, `created_at` |
| Git commit prefixes | Bracket tag | `[checkpoint]`, `[session-auto]`, `[artifact]` |
| Textual messages | `BMAD` prefix + `PascalCase` | `BMADStateChanged`, `BMADPhaseClicked` |
| File names | `snake_case.py` | `git_state_engine.py`, `state_operation_queue.py` |

### Structure Patterns

**Imports — absolute only:**

```python
# RIGHT
from mad_frog.services.git_state_engine import GitStateEngine
from mad_frog.services.decorators import traced

# WRONG
from ..services.git_state_engine import GitStateEngine
from .decorators import traced
```

**Test file structure — mirror source tree:**

```
src/mad_frog/services/git_state_engine.py  →  tests/services/test_git_state_engine.py
src/mad_frog/tools/artifact.py             →  tests/tools/test_artifact.py
src/mad_frog/mcp_server.py                 →  tests/test_mcp_server.py
```

One source file → one test file → same relative path.

**Fixtures:**
- Root `conftest.py`: shared fixtures (`tmp_git_repo`, `tmp_db`, `mcp_server`)
- Subdirectory `conftest.py`: domain-specific fixtures
- Function-scoped by default. Session-scoped only for truly expensive setup. Never module-scoped.

**Test naming:** `test_<what>_<condition>_<expected>`

```python
# RIGHT
async def test_checkpoint_no_changes_raises()
async def test_write_artifact_invalid_type_returns_error()
def test_git_engine_commit_returns_sha()

# WRONG
def test_1()
def test_checkpoint()
def test_it_works()
```

**Async tests:** Use `async def test_*` for any test touching async code. Never manually create event loops. `asyncio_mode = "auto"` in pyproject.toml handles the rest.

### Error Handling Patterns

**Two-layer contract:**

1. **Services raise exceptions.** Internal Python code uses standard exception handling.
2. **Tool handlers catch and convert to MCP `isError` responses.** The tool handler is the boundary.

```python
# Service layer — raises
class GitStateEngine:
    @traced
    def commit(self, message: str) -> str:
        if not self.has_uncommitted_changes():
            raise ValueError("Nothing to commit")
        self.repo.git.add(".")
        self.repo.git.commit("-m", message)
        return self.repo.head.commit.hexsha

# Tool handler — catches and converts
@traced
async def bmad_checkpoint(git_engine: GitStateEngine, arguments: dict) -> dict:
    try:
        phase = arguments.get("phase", "unknown")
        summary = arguments["summary"]
        sha = git_engine.commit(f"[checkpoint] {summary}")
        return {
            "content": [{"type": "text", "text": json.dumps({"git_sha": sha, "phase": phase})}],
            "isError": False,
        }
    except Exception as e:
        return {
            "content": [{"type": "text", "text": f"Error: {e}"}],
            "isError": True,
        }
```

**Validation lives in the tool handler.** Services trust their callers. The tool handler is the only layer that receives external (MCP) input and must validate `arguments` before passing to services.

### Initialisation Patterns

**Constructor injection. No module-level state.**

```python
# RIGHT: Services created in server __init__, injected into handlers
class MadFrogMCPServer:
    def __init__(self, project_path: Path):
        self.git_engine = GitStateEngine(project_path)
        self.state_queue = StateOperationQueue()
        self.auto_save = AutoSaveService(self.git_engine, self.state_queue)
        self.state_writer = StateFileWriter(project_path / ".mad_frog" / "state.json")

# WRONG: Module-level globals
git_engine = GitStateEngine(Path("."))  # Untestable, unconfigurable
```

All services created in `MadFrogMCPServer.__init__()` and passed to handlers. This makes testing trivial — inject mocks.

### State File Patterns

**All state file writes go through `StateFileWriter.write()`.** No inline file writes anywhere.

```python
class StateFileWriter:
    @traced
    def write(self, state: dict) -> None:
        """Write state.json atomically. Single point of truth."""
        tmp_path = self.state_path.with_suffix(".tmp")
        tmp_path.write_text(json.dumps(state, indent=2))
        os.replace(tmp_path, self.state_path)
```

### Logging Patterns

**stdlib `logging` module.** Matches Toad. Zero added deps.

```python
# In every module
logger = logging.getLogger(__name__)

# In CLI entry point
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
)
```

No `print()` statements. No loguru. No custom logging framework.

### Type Hint Patterns

- All function signatures get type hints (parameters and return type)
- Modern syntax: `str | None` not `Optional[str]`, `dict` not `Dict`, `list` not `List`
- `Path` objects internally, `str` at MCP boundary (JSON can't serialize `Path`)
- Google-style docstrings on tool handlers only (they're the API). Internal code: only where non-obvious.

### Async Patterns

- `async def` only where needed: I/O operations (git subprocess, SQLite queries, file reads)
- Sync for pure computation and simple data transformations
- Never `time.sleep()` in async code — always `asyncio.sleep()`

### Anti-Patterns (MUST NOT)

These are explicitly forbidden. Any agent introducing these patterns fails code review:

| Anti-Pattern | Why |
|-------------|-----|
| `from mad_frog.tools import *` | No wildcard imports, ever |
| Bare `except:` | Always catch specific exception types |
| `os.path` functions | Use `pathlib.Path` exclusively |
| `json.dumps(default=str)` | Lazy serialisation hides bugs — explicit conversion |
| Mutable default arguments | Use `field(default_factory=...)` for dataclasses |
| Module-level mutable state | All state in class instances, constructor-injected |
| `time.sleep()` in async code | Use `asyncio.sleep()` |
| SQL string formatting | Always parameterised queries: `cursor.execute("... WHERE id=?", (id,))` |
| Inline state file writes | All writes through `StateFileWriter.write()` |
| Manual event loop creation in tests | Use `async def test_*` with pytest-asyncio |
| Relative imports | Absolute imports only |
| `print()` for logging | Use `logging` module |

### Enforcement Summary

**All AI agents implementing Mad Frog MUST:**

1. Apply `@traced` to every function — no exceptions
2. Use `snake_case` for all JSON keys, SQL columns, and Python identifiers
3. Prefix MCP tool names with `bmad_` and Textual messages with `BMAD`
4. Validate MCP input in tool handlers, never in services
5. Raise exceptions in services, return `isError` in tool handlers
6. Use constructor injection — no module-level mutable state
7. Mirror source tree in test directory structure
8. Use absolute imports only
9. Use stdlib `logging` — no print, no loguru
10. Write state files only through `StateFileWriter.write()`

## Project Structure & Boundaries

### Deployment Model

Mad Frog is a **stateless tool** that operates on **sibling project directories**. Toad is a pip-installable package — we import and subclass, not copy.

```
~/Development/                         # User's workspace
├── mad_frog/                          # Tool repo (this repo)
│   ├── src/mad_frog/                  # Tool source — imports from toad package
│   ├── _bmad-output/                  # Our own planning artifacts (this doc)
│   ├── tests/
│   ├── pyproject.toml                 # deps: batrachian-toad>=0.5.35,<0.7
│   └── ...
│
├── surf-seer/                         # Managed project (sibling)
│   ├── _bmad/                         # Installed via npx bmad init
│   ├── _bmad-output/
│   └── .git/
│
└── new-idea/                          # Another managed project (sibling)
    ├── _bmad/                         # Installed via npx bmad init
    └── .git/
```

**Key principles:**
- Toad is a **runtime dependency** (`pip install batrachian-toad`). We `from toad.app import ToadApp` and subclass. No Toad source code in our repo.
- BMAD is installed into target projects via `npx bmad init`, not copied from the tool repo. Fresh version every time, from the canonical source.
- BMAD updates use `npx bmad update` — the installer handles versioning, not us.
- The tool repo may have its own `_bmad/` (for bootstrapping), but projects get independent installs.
- The MCP server receives **one path**: the project path. No tool root needed.

### BMAD Method Management

Two project lifecycle operations handle BMAD installation:

```python
# Fresh install — no _bmad/ exists in target project
bmad_create_project(path):
    mkdir(path)
    git init
    subprocess.run(["npx", "bmad", "init"], cwd=path)
    git commit "[init] Project created with BMAD"

# Update existing — _bmad/ already exists
bmad_update_method(path):
    old_hash = tree_hash(path / "_bmad")
    subprocess.run(["npx", "bmad", "update"], cwd=path)
    new_hash = tree_hash(path / "_bmad")
    if changed: git commit "[bmad-update] {old_hash} → {new_hash}"
```

The tool doesn't ship BMAD. The tool installs BMAD. Version management is the installer's problem.

### Complete Project Directory Structure

```
mad_frog/                                          # Tool repo
├── .devcontainer/
│   └── devcontainer.json                          # Python 3.14, uv sync, API key passthrough
├── .github/
│   └── workflows/
│       └── ci.yml                                 # pytest + coverage + ruff
├── src/mad_frog/
│   ├── __init__.py                                # Version string only
│   ├── __main__.py                                # from mad_frog.cli import main; main()
│   ├── py.typed                                   # PEP 561 marker
│   ├── cli.py                                     # CLI entry point (argparse) — wires MadFrogApp + MadFrogAgent
│   ├── app.py                                     # MadFrogApp(ToadApp) — compose(), watchdog, keybindings
│   ├── agent.py                                   # MadFrogAgent(Agent) — overrides acp_new_session
│   ├── constants.py                               # DEFAULT_WORKSPACE, AUTO_SAVE_INTERVAL
│   ├── models.py                                  # dataclass (no suffix) + TypedDict (*Result/*Row suffix)
│   ├── mad_frog.tcss                              # ~50 lines: --mf-completed, --mf-active, --mf-stale
│   ├── mcp_server.py                              # MadFrogMCPServer — stdio JSON-RPC, dispatch, auto-save
│   ├── tools/
│   │   ├── __init__.py                            # Empty
│   │   ├── definitions.py                         # All 18 tool schemas (name, description, inputSchema)
│   │   ├── project.py                             # bmad_create_project, bmad_open_project, bmad_list_projects,
│   │   │                                          # bmad_health_check, bmad_update_method
│   │   ├── artifact.py                            # bmad_write_artifact, bmad_read_artifact, bmad_list_artifacts
│   │   ├── state.py                               # bmad_checkpoint, bmad_restore, bmad_history
│   │   ├── workflow.py                            # bmad_advance_workflow, bmad_get_workflow_state, bmad_get_step_prompt
│   │   └── session.py                             # bmad_session_info, bmad_lock_session, bmad_unlock_session,
│   │                                              # bmad_get_agent_persona, bmad_list_agents, bmad_auto_save_status
│   ├── services/
│   │   ├── __init__.py                            # Empty
│   │   ├── decorators.py                          # @traced decorator
│   │   ├── git_state_engine.py                    # GitPython repo.git.* wrapper (~200 lines)
│   │   ├── sqlite_index.py                        # aiosqlite checkpoint index (~150 lines)
│   │   ├── state_operation_queue.py               # asyncio.PriorityQueue (~100 lines)
│   │   ├── auto_save_service.py                   # Async timer + git commit (~50 lines)
│   │   ├── session_lock_manager.py                # File lock + PID check (~50 lines)
│   │   ├── vault_health_monitor.py                # .obsidian/ detection (~80 lines)
│   │   ├── artifact_validator.py                  # Frontmatter + wikilink validation (~100 lines)
│   │   └── state_file.py                          # StateFileWriter — atomic os.replace() writes
│   └── ui/
│       ├── __init__.py                            # Empty
│       ├── welcome_screen.py                      # Project list, new/open/resume actions (~100 lines)
│       ├── journey_map.py                         # BMADJourneyMap(Tree) sidebar widget (~150 lines)
│       └── workspace_setup.py                     # First-run modal: workspace path (~50 lines)
├── tests/
│   ├── conftest.py                                # tmp_git_repo, tmp_db, tmp_project, mock_mcp_server
│   ├── test_mcp_server.py                         # MCP protocol: initialize, tools/list, tools/call
│   ├── tools/
│   │   ├── conftest.py                            # Tool-specific fixtures (mock git_engine, mock state)
│   │   ├── test_project.py
│   │   ├── test_artifact.py
│   │   ├── test_state.py
│   │   ├── test_workflow.py
│   │   └── test_session.py
│   ├── services/
│   │   ├── conftest.py                            # Service-specific fixtures
│   │   ├── test_decorators.py                     # @traced: sync, async, re-raise, log format
│   │   ├── test_git_state_engine.py
│   │   ├── test_sqlite_index.py
│   │   ├── test_state_operation_queue.py
│   │   ├── test_auto_save_service.py
│   │   ├── test_session_lock_manager.py
│   │   ├── test_vault_health_monitor.py
│   │   ├── test_artifact_validator.py
│   │   └── test_state_file.py
│   └── ui/
│       ├── conftest.py                            # Textual App pilot fixtures
│       ├── test_welcome_screen.py
│       ├── test_journey_map.py
│       └── test_workspace_setup.py
├── .gitignore                                     # __pycache__, .venv, *.egg-info, dist, .coverage,
│                                                  # .ruff_cache, *.db, .env, .mad_frog/
├── .python-version                                # 3.14
├── pyproject.toml                                 # See below
├── Makefile                                       # dev, start, test, lint, fmt
└── README.md                                      # 3-line quick start
```

### Updated pyproject.toml

```toml
[project]
name = "mad-frog"
version = "0.1.0"
description = "A Toad app for guided BMAD planning"
requires-python = ">=3.14"
license = "MIT"
dependencies = [
    "batrachian-toad>=0.5.35,<0.7",
]

[project.scripts]
mad_frog = "mad_frog.cli:main"

[dependency-groups]
dev = [
    "pytest>=9.0",
    "pytest-asyncio>=0.25",
    "pytest-cov>=7.0",
    "textual-dev>=2.0",
    "ruff>=0.15",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"

[tool.ruff]
target-version = "py314"
line-length = 120

[tool.ruff.lint]
select = ["E", "F", "I", "UP"]

[tool.coverage.run]
source = ["src/mad_frog"]

[tool.coverage.report]
fail_under = 85
```

### Architectural Boundaries

#### Process Boundaries (3 processes)

| Process | Entry Point | Responsibility | Communicates With |
|---------|-------------|----------------|-------------------|
| MadFrogApp | `mad_frog` CLI → `app.py` | UI: sidebar, welcome, workspace setup, watchdog | AI Agent (ACP via Toad) |
| AI Agent | Launched by Toad | Conversation, BMAD facilitation | Toad (ACP), MCP Server (MCP) |
| MCP Server | `python -m mad_frog.mcp_server` | 18 tools, git state, auto-save | AI Agent (MCP stdio) |

#### MCP Server Internal Boundaries

```
mcp_server.py (JSON-RPC dispatch only — no business logic)
    ↓ routes to
tools/*.py (validate MCP args, call services, catch exceptions, return CallToolResult)
    ↓ delegates to
services/*.py (pure business logic, typed Python args, raises exceptions, no MCP knowledge)
```

#### UI Internal Boundaries

```
cli.py (wires MadFrogApp + MadFrogAgent, argparse argument parsing)
    ↓ creates
app.py (MadFrogApp — Textual lifecycle, compose, keybindings, watchdog)
    ↓ composes
ui/*.py (self-contained widgets, communicate via Textual messages)
    ↓ watches
.mad_frog/state.json (written atomically by MCP server, read by watchdog)
```

**No direct imports between `ui/` and `tools/` or `services/`.** They're in different processes.

#### Toad Integration Points

```python
# app.py — UI extension
from toad.app import ToadApp

class MadFrogApp(ToadApp):
    CSS_PATH = [*ToadApp.CSS_PATH, "mad_frog.tcss"]

    def compose(self) -> ComposeResult:
        yield BMADSidebar()
        yield from super().compose()

# agent.py — ACP extension
from toad.acp.agent import Agent
from toad.acp import api, protocol

class MadFrogAgent(Agent):
    async def acp_new_session(self) -> None:
        with self.request():
            session_new_response = api.session_new(
                str(self.project_root_path),
                [{"name": "mad-frog-bmad", "command": "python",
                  "args": ["-m", "mad_frog.mcp_server"]}],
            )
        response = await session_new_response.wait()
        self.session_id = response["sessionId"]
        # ... rest follows parent pattern

# cli.py — wires them together
from toad.agents import resolve_agent  # or equivalent

class MadFrogApp creates MadFrogAgent, not default Agent
```

### Requirements to Structure Mapping

| FR Domain | Files | Key Tool/Service |
|-----------|-------|------------------|
| Project Lifecycle (FR1-8) | `tools/project.py`, `services/git_state_engine.py` | `bmad_create_project`, `bmad_open_project`, `bmad_update_method` |
| Guided Workflow (FR9-18) | `tools/workflow.py`, `mcp_server.py` | `bmad_advance_workflow`, `bmad_get_step_prompt` |
| Solutioning (FR19-24) | `tools/artifact.py`, `services/artifact_validator.py` | `bmad_write_artifact` |
| Journey Map (FR25-36) | `ui/journey_map.py`, `services/state_file.py` | `BMADJourneyMap`, watchdog |
| State Persistence (FR37-45) | `tools/state.py`, `services/git_state_engine.py`, `services/state_operation_queue.py`, `services/auto_save_service.py` | `bmad_checkpoint`, auto-save |
| Obsidian Integration (FR46-52) | `services/vault_health_monitor.py`, `services/artifact_validator.py` | Vault detection, wikilinks |
| Conversation (FR53-55) | Toad built-in (conversation panel) | Deferred to post-MVP |
| File Workspace (FR56-60) | `tools/project.py` | `bmad_detect_changes`, Toad ACP `fs_read`/`fs_list` |
| Party Mode (FR61-68) | `tools/session.py` | `bmad_get_agent_persona`, `bmad_list_agents` |
| Container & Access (FR69-88) | `.devcontainer/`, `cli.py`, `ui/workspace_setup.py` | Dev Container config |

### Data Flow

```
User clicks sidebar phase
  → BMADPhaseClicked message (Textual)
  → MadFrogApp composes synthetic prompt
  → Toad sends prompt to AI Agent via ACP
  → AI Agent calls bmad_get_step_prompt via MCP
  → MCP Server reads project's _bmad/ step file, returns content
  → AI Agent facilitates conversation with user
  → AI Agent calls bmad_write_artifact via MCP
  → MCP Server: ArtifactValidator checks → file written → git commit
  → MCP Server: StateFileWriter.write() updates state.json (atomic)
  → watchdog detects change → BMADStateChanged message
  → BMADJourneyMap sidebar updates
```

### Test Structure (~71 tests)

| Test File | What | Est. Count |
|-----------|------|-----------|
| `test_mcp_server.py` | MCP protocol compliance (init, list, call, errors) | 5 |
| `tools/test_project.py` | create, open, list, health_check, update_method | 7 |
| `tools/test_artifact.py` | write, read, list + validation errors | 6 |
| `tools/test_state.py` | checkpoint, restore, history | 5 |
| `tools/test_workflow.py` | advance, get_state, get_step_prompt | 5 |
| `tools/test_session.py` | info, lock/unlock, agents, auto_save_status | 5 |
| `services/test_decorators.py` | sync, async, re-raise, log format, elapsed | 4 |
| `services/test_git_state_engine.py` | commit, dirty check, tree_hash, log | 5 |
| `services/test_sqlite_index.py` | create, query, rebuild | 4 |
| `services/test_state_operation_queue.py` | priority ordering, pre-emption | 3 |
| `services/test_auto_save_service.py` | timer fires, skip when clean | 3 |
| `services/test_session_lock_manager.py` | acquire, release, stale detection | 4 |
| `services/test_vault_health_monitor.py` | detect, no vault, nested | 3 |
| `services/test_artifact_validator.py` | frontmatter, wikilinks, structure | 4 |
| `services/test_state_file.py` | atomic write, concurrent read | 3 |
| `ui/test_welcome_screen.py` | render, project list, actions | 3 |
| `ui/test_journey_map.py` | render, state update, click events | 3 |
| `ui/test_workspace_setup.py` | render, setup flow | 2 |
| **Total** | | **~71** |

### constants.py

```python
from pathlib import Path
import os

DEFAULT_WORKSPACE = Path(os.environ.get("VIBE_WORKSPACE", "/workspaces"))
AUTO_SAVE_INTERVAL = int(os.environ.get("MAD_FROG_AUTO_SAVE", "120"))
```

No `BMAD_SOURCE` — BMAD is installed via `npx bmad init`, not copied from the tool.

## Architecture Validation Results

### Coherence Validation ✅

**Decision Compatibility:** All 10 core decisions are mutually compatible. MCP server + TypedDict + stdio JSON-RPC require no bridging layers. State sync (atomic file + watchdog) and auto-save (MCP timer) coexist via StateOperationQueue priority arbitration. Python 3.14, uv, hatchling, ruff — all version-compatible with Toad ecosystem.

**Pattern Consistency:** `@traced` decorator, two-layer error contract, snake_case naming, absolute imports, and constructor injection are applied uniformly across all layers. No conflicting conventions detected.

**Structure Alignment:** Three-process architecture cleanly maps to directory structure. No cross-boundary imports between ui/ and tools/services/. Test structure mirrors source 1:1.

### Requirements Coverage Validation ✅

**Functional Requirements (88 FRs across 10 domains):** All FR domains have architectural support. FR53-55 (Conversation & Transcript Management) explicitly deferred to post-MVP with documented rationale. FR56-60 (Bidirectional File Workspace) now covered by restored `bmad_detect_changes` tool.

**Non-Functional Requirements (8 categories):** All addressed — performance (sub-500ms sidebar, 3s artifact ceiling), security (path sandboxing, no credential logging), reliability (auto-save, atomic ops, chaos tests, context-save), accessibility (Toad theme WCAG AA), integration (Obsidian-native), observability (@traced + structured logging), maintainability (85% coverage, state versioning).

### Implementation Readiness Validation ✅

**Decision Completeness:** All decisions include version numbers, rationale, and implementation code. @traced decorator is copy-pasteable. MCP server spec covers full lifecycle. Tool handler signature pattern documented.

**Structure Completeness:** ~40 source files annotated with purpose and line estimates. pyproject.toml, devcontainer.json, CI, Makefile all provided. Test fixture hierarchy documented.

**Pattern Completeness:** 12 anti-patterns forbidden. 10 enforcement rules. Naming table covers all identifier types. Tool dispatch registry pattern specified.

### Validation Audit Findings (26 Items)

The following items were identified through comprehensive Party Mode validation audit. Items are grouped by type. All items are refinements — no architectural redesign required, though item 23 is a critical lifecycle correction.

#### Architecture Corrections (Critical)

**Item 23 — MCP Server Starts Projectless (Two-Phase Lifecycle):**

The MCP server is injected into the ACP session at startup via `mcpServers`, before the user has selected a project. Therefore `MadFrogMCPServer.__init__()` cannot take `project_path` as an argument.

**Corrected lifecycle:**

- **Phase 1 (serverless):** MCP server starts with no active project. Reads `.vibe/config.yaml` for workspace root on first `bmad_list_projects` call. Handles `initialize`, `tools/list`, and projectless tools (`bmad_list_projects`, `bmad_report_context`, `bmad_session_info`).
- **Phase 2 (project active):** `bmad_create_project` or `bmad_open_project` creates `ProjectContext` — bundles `GitStateEngine`, `SessionLockManager`, `StateFileWriter`, `StateOperationQueue`, `AutoSaveService`. Auto-save timer starts. All project-scoped tools become available.

```python
class MadFrogMCPServer:
    def __init__(self):
        self.project: ProjectContext | None = None
        self.context_window = DEFAULT_CONTEXT_WINDOW
        self.session_tokens = 0

    def _require_project(self) -> ProjectContext:
        if self.project is None:
            raise NoProjectOpen("Call bmad_create_project or bmad_open_project first.")
        return self.project
```

**Ripple effects:**
- Constructor injection pattern moves from `__init__()` to `bmad_open_project`/`bmad_create_project`
- CLI entry point: MCP server takes zero args (`python -m mad_frog.mcp_server`)
- Workspace root derived from `.vibe/config.yaml`, not CLI arg or env var
- Auto-save timer starts on project open, not server start
- Crash recovery: `__init__()` is idempotent — stale `.mad_frog/session.lock` from crashed instance detected and force-acquired on project open

#### Tool Additions & Corrections

**Item 7 — Restore `bmad_detect_changes`:**

FR56-60 (Bidirectional File Workspace) requires detecting files dropped into the project since last checkpoint. Toad's built-in ACP `fs_read`/`fs_list` handle file reading but don't know about our git state. `bmad_detect_changes` compares current filesystem against last git commit via `git status --porcelain`. Added to `tools/project.py`.

**Item 16 — Add `bmad_report_context` (Context-Aware Pre-emptive Save):**

New tool allowing the AI agent to report its context window size in tokens. Called once at session start. MCP server uses this to calculate the 90% threshold for silent pre-emptive save.

```python
{
    "name": "bmad_report_context",
    "description": "Report your context window size in tokens. Call this once at the start of every session.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "context_window_tokens": {"type": "integer", "description": "Your total context window size in tokens"}
        },
        "required": ["context_window_tokens"]
    }
}
```

**Fallback:** If agent never calls the tool, `DEFAULT_CONTEXT_WINDOW` from env var (200,000) is used.

**Silent pre-emptive save at 90%:** MCP server tracks cumulative tool I/O tokens (`len(text) // 4` estimate). At 90% of context window: silent `[context-save]` git commit via StateOperationQueue. No warnings, no UI, no user notification. Just a safety net.

```python
CONTEXT_SAVE_RATIO = 0.90

if self.session_tokens > self.context_save_at and not self._context_saved:
    await self.state_queue.enqueue_and_wait(
        priority=Priority.INTENTIONAL,
        operation=lambda: self.git_engine.commit(
            f"[context-save] ~{self.session_tokens} tokens"
        ),
    )
    self._context_saved = True
```

**Item 1 — Updated Tool Count: 18 Tools**

| Category | Tools |
|----------|-------|
| Project (6) | `bmad_create_project`, `bmad_open_project`, `bmad_list_projects`, `bmad_health_check`, `bmad_update_method`, `bmad_detect_changes` |
| Artifact (3) | `bmad_write_artifact`, `bmad_read_artifact`, `bmad_list_artifacts` |
| State (3) | `bmad_checkpoint`, `bmad_restore`, `bmad_history` |
| Workflow (3) | `bmad_advance_workflow`, `bmad_get_workflow_state`, `bmad_get_step_prompt` |
| Session (7) | `bmad_session_info`, `bmad_lock_session`, `bmad_unlock_session`, `bmad_get_agent_persona`, `bmad_list_agents`, `bmad_auto_save_status`, `bmad_report_context` |

Note: Session category has 7 tools but 4 are lightweight metadata queries.

#### Design Updates

**Item 13 — Expanded `state.json` with `checkpoint_history`:**

The sidebar (Process 1) cannot call MCP tools (Process 3). It reads `state.json` via watchdog. The original state file format lacked checkpoint history needed for Journey Map rendering.

Expanded format:

```json
{
    "current_phase": "analysis",
    "workflows": { "...": "..." },
    "last_checkpoint": { "git_sha": "abc123", "summary": "...", "timestamp": "..." },
    "checkpoint_history": [
        {"git_sha": "abc123", "summary": "Product brief complete", "phase": "analysis", "type": "checkpoint", "timestamp": "..."},
        {"git_sha": "def456", "summary": "PRD draft saved", "phase": "planning", "type": "artifact", "timestamp": "..."}
    ],
    "auto_save": { "last_save": "...", "interval_seconds": 120, "enabled": true },
    "session_lock": { "pid": 12345, "acquired_at": "..." },
    "updated_at": "..."
}
```

MCP server appends to `checkpoint_history` on every `bmad_checkpoint` and `bmad_write_artifact` call. Sidebar renders the tree from this array.

**Item 22 — Session Lock Acquired in open/create, Not Separate Tool Call:**

Write tools assert the lock is held via `_require_project()` (which implies lock). Lock acquired internally by `bmad_create_project` and `bmad_open_project`. Released on MCP server shutdown. `bmad_lock_session` and `bmad_unlock_session` remain for explicit lock management (takeover scenarios) but are not required for normal flow.

**Item 24 — Awaitable Queue Operations:**

`StateOperationQueue.enqueue_and_wait()` returns an awaitable result, allowing tool handlers to detect git commit failures and report them via `isError`. Uses `asyncio.Event` per enqueued operation. ~10 lines added to queue implementation.

**Item 26 — First-Run Workspace Modal (Replaces CredentialSetupScreen):**

Credential management is Toad's responsibility. `CredentialSetupScreen` removed entirely. Replaced with `WorkspaceSetupScreen` — a single modal shown on first launch asking "Where are your projects?" Path saved to `.vibe/config.yaml`.

Updated `ui/` directory:

```
ui/
├── __init__.py
├── welcome_screen.py          # Project list, new/open/resume (~100 lines)
├── journey_map.py             # BMADJourneyMap(Tree) sidebar (~150 lines)
├── workspace_setup.py         # First-run modal: workspace path (~50 lines)
```

App lifecycle:
1. Start → `.vibe/config.yaml` exists? → No → show workspace modal → save → Welcome Screen
2. Start → config exists? → Yes → straight to Welcome Screen

#### Decision Updates

**Item 3 — Replace `click` with `argparse` (Decision 7 correction):**

`click` is not a Toad transitive dependency. Using it would add a second production dependency, breaking the single-dep principle. `argparse` (stdlib) handles the CLI's one argument (`project_dir`) and one option (`--agent`) in 8 lines.

**Item 5 — Decision #5 Fully Resolved: Local Docker Desktop Only:**

Workspace path collected via first-run modal, stored in `.vibe/config.yaml`. No env vars needed for paths. Codespaces support dropped from scope — if someone uses Codespaces, they set `workspace_root` manually in config. Docker always runs Linux containers, so all paths are POSIX — no cross-platform path issues.

`devcontainer.json` retains `ANTHROPIC_API_KEY` passthrough (forwarding, not managing).

#### Pattern Additions

**Item 12 — Tool Schema Example + Description Quality Pattern:**

Tool descriptions are the UX for the AI agent. Quality standard:
- Start with action verb: "Save", "List", "Read", "Advance", "Get"
- Include when to use it: "Save current project state as a git checkpoint"
- Include key context: "with phase and summary metadata"
- Under 100 characters

Example schema:

```python
TOOL_DEFINITIONS = [
    {
        "name": "bmad_checkpoint",
        "description": "Save current project state as a git checkpoint with phase and summary metadata.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "phase": {"type": "string", "description": "Current BMAD phase"},
                "summary": {"type": "string", "description": "Human-readable checkpoint summary"},
            },
            "required": ["summary"],
        },
    },
]
```

**Item 15 — StateOperationQueue Boundary Clarification:**

The queue serialises **git-mutating operations only**. File writes (e.g., writing an artifact to disk) happen outside the queue. Only the subsequent `git commit` is enqueued. This prevents unnecessary serialisation of all tool operations.

**Item 18 — `bmad_get_step_prompt` Resolves Template Variables:**

BMAD step files contain template variables (`{project-root}`, `{planning_artifacts}`, etc.). The tool resolves these via simple string replacement before returning content to the agent:

```python
@traced
def resolve_step_content(raw: str, config: dict, project_path: Path) -> str:
    replacements = {
        "{project-root}": str(project_path),
        "{planning_artifacts}": str(project_path / "_bmad-output" / "planning-artifacts"),
        "{implementation_artifacts}": str(project_path / "_bmad-output" / "implementation-artifacts"),
        "{communication_language}": config.get("communication_language", "English"),
        "{project_knowledge}": str(project_path / "docs"),
    }
    result = raw
    for token, value in replacements.items():
        result = result.replace(token, value)
    return result
```

Config values loaded once from project's `_bmad/bmm/config.yaml` (or `_bmad/core/config.yaml`) at project open.

**Item 19 — Config Loading Pattern:**

Project config loaded in `ProjectContext.__init__()` from the project's BMAD config YAML. Stored as a plain dict. Accessed by tools that need template resolution or project metadata. Single load, shared reference.

**Item 21 — Tool Dispatch Registry Pattern:**

```python
# tools/__init__.py
from mad_frog.tools.project import bmad_create_project, bmad_open_project, ...
from mad_frog.tools.artifact import bmad_write_artifact, bmad_read_artifact, ...

TOOL_HANDLERS: dict[str, Callable] = {
    "bmad_create_project": bmad_create_project,
    "bmad_open_project": bmad_open_project,
    # ... all 18
}
```

Tool handler signature (all tools follow this exactly):

```python
@traced
async def bmad_<tool_name>(server: "MadFrogMCPServer", arguments: dict) -> dict:
    """Docstring matches MCP schema description exactly."""
    # 1. _require_project() if project-scoped
    # 2. Validate arguments
    # 3. Call services via server.project.<service>
    # 4. Return CallToolResult dict
```

Consistency test:

```python
def test_all_tools_have_handlers():
    from mad_frog.tools import TOOL_HANDLERS
    from mad_frog.tools.definitions import TOOL_DEFINITIONS
    assert {t["name"] for t in TOOL_DEFINITIONS} == set(TOOL_HANDLERS.keys())
```

**Item 25 — Commit Prefix Registry + SQLite Rebuild Filtering:**

| Prefix | Source | Indexed | Journey Map |
|--------|--------|---------|-------------|
| `[checkpoint]` | `bmad_checkpoint` | Yes | Yes |
| `[artifact]` | `bmad_write_artifact` | Yes | Yes |
| `[session-auto]` | Auto-save timer | Yes | No (background) |
| `[context-save]` | Context threshold | Yes | No (background) |
| `[init]` | `bmad_create_project` | Yes | Yes |
| `[bmad-update]` | `bmad_update_method` | Yes | Yes |
| No prefix | Manual user commits | No | No |

`SQLiteCheckpointIndex.rebuild()` only indexes commits with recognised prefixes. `BMADJourneyMap` only renders commits with user-visible types (`checkpoint`, `artifact`, `init`, `bmad-update`).

#### Dependency & Infrastructure

**Item 17 — Node.js in Dev Container + `npx` Guard:**

`npx bmad init` requires Node.js. Added to Dev Container config:

```json
"features": {
    "ghcr.io/devcontainers/features/git:1": {},
    "ghcr.io/devcontainers/features/node:1": {}
}
```

Guard in tool handler:

```python
if not shutil.which("npx"):
    return {"content": [{"type": "text", "text": "Error: npx not found. Node.js required for BMAD installation."}], "isError": True}
```

Applied to both `bmad_create_project` and `bmad_update_method`.

#### Spike Items (Story 1 Verification)

**Item 6 — `acp_new_session` Parent Pattern:**

The `MadFrogAgent.acp_new_session` override shows the mcpServers injection but uses `# ... rest follows parent pattern` for post-session-ID setup. The parent method's exact behaviour (attributes set, messages posted) must be verified by reading Toad source during story 1 spike.

**Item 8 — App ↔ Agent Wiring:**

How `MadFrogApp` tells Toad to use `MadFrogAgent` instead of the default `Agent` class is undetermined. Possible mechanisms: class attribute override, constructor parameter, agent resolution config. To be spiked in story 1.

**Item 9 — Speculative Toad Imports:**

- `from toad.agents import resolve_agent` — unverified, may not exist
- `ToadApp.CSS_PATH` — expected via Textual inheritance but unverified on ToadApp specifically

Both verified or corrected during story 1 spike.

#### Doc Fixes

**Item 2 — Method Version Management section** references "copies the current `_bmad/` directory from the tool." Should read "runs `npx bmad init`." Similarly "copies latest `_bmad/` from tool" → "runs `npx bmad update`."

**Item 11 — MCP Server Crash Recovery:** `__init__()` is idempotent. On project open, detect stale `.mad_frog/session.lock` from crashed previous instance, force-acquire, rebuild state from git.

#### Updated constants.py

```python
import os

AUTO_SAVE_INTERVAL = int(os.environ.get("MAD_FROG_AUTO_SAVE", "120"))
DEFAULT_CONTEXT_WINDOW = int(os.environ.get("MAD_FROG_CONTEXT_WINDOW", "200000"))
CONTEXT_SAVE_RATIO = 0.90
```

No path constants. Workspace root from `.vibe/config.yaml`. Tool root from `__file__`.

#### Updated Test Count (~90 Tests)

| Test File | What | Count |
|-----------|------|-------|
| `test_mcp_server.py` | Protocol compliance + integration + tool registry sync | 9 |
| `tools/test_project.py` | create, open, list, health_check, update_method, detect_changes + npx guard | 9 |
| `tools/test_artifact.py` | write, read, list + validation errors + commit failure | 7 |
| `tools/test_state.py` | checkpoint, restore, history | 5 |
| `tools/test_workflow.py` | advance, get_state, get_step_prompt + template resolution | 6 |
| `tools/test_session.py` | info, lock/unlock, agents, auto_save_status, report_context | 6 |
| `services/test_decorators.py` | sync, async, re-raise, log format | 4 |
| `services/test_git_state_engine.py` | commit, dirty check, tree_hash, log | 5 |
| `services/test_sqlite_index.py` | create, query, rebuild, prefix filtering | 6 |
| `services/test_state_operation_queue.py` | priority ordering, pre-emption, awaitable result | 4 |
| `services/test_auto_save_service.py` | timer fires, skip when clean | 3 |
| `services/test_session_lock_manager.py` | acquire, release, stale detection, crash recovery | 5 |
| `services/test_vault_health_monitor.py` | detect, no vault, nested | 3 |
| `services/test_artifact_validator.py` | frontmatter, wikilinks, structure | 4 |
| `services/test_state_file.py` | atomic write, concurrent read, checkpoint_history | 4 |
| `services/test_context_save.py` | threshold fire, fires once, uses queue, default fallback | 4 |
| `ui/test_welcome_screen.py` | render, project list, actions | 3 |
| `ui/test_journey_map.py` | render, state update, click events, excludes auto-saves | 4 |
| `ui/test_workspace_setup.py` | saves config, rejects invalid path, skips when exists | 3 |
| **Total** | | **~90** |

#### Updated Build Sequence

**Story 1 — Validation Spike:**

Spike only. Verify Toad integration assumptions:
- `MadFrogApp(ToadApp)` launches with `compose()` override
- `MadFrogAgent(Agent)` overrides `acp_new_session` with mcpServers injection
- MCP server starts, agent connects, `tools/list` returns tools, `tools/call` executes one tool
- Verify `CSS_PATH`, agent wiring mechanism, `acp_new_session` parent behaviour

Acceptance test: `MadFrogApp` runs → agent session starts → MCP server receives `initialize` → agent calls one tool → response received.

Architecture assumptions marked "spike verification" are confirmed or corrected in this story.

**Week 1 — Walking Skeleton (post-spike):**
- 3 core tools: `bmad_create_project`, `bmad_write_artifact`, `bmad_checkpoint`
- `GitStateEngine`, `StateOperationQueue`, `StateFileWriter`
- `WorkspaceSetupScreen` modal
- Acceptance test: workspace setup → create project → agent writes artifact → committed to Git

**Week 2 — Persistence & Navigation:**
- Remaining tools (18 total)
- `SQLiteCheckpointIndex` + rebuild from git
- `BMADJourneyMap` sidebar reading `state.json` checkpoint_history
- `AutoSaveService` + context-save
- `bmad_report_context` + token tracking

**Week 3 — Polish & Safety:**
- `WelcomeScreen` with `bmad_list_projects`
- `VaultHealthMonitor` + vault-aware `bmad_write_artifact`
- `ArtifactValidator` integrated into write pipeline
- `SessionLockManager` crash recovery
- Chaos tests (5 scenarios)
- Template variable resolution in `bmad_get_step_prompt`

### Architecture Completeness Checklist

**✅ Requirements Analysis**

- [x] Project context thoroughly analyzed
- [x] Scale and complexity assessed (Medium-High requirements → Low implementation)
- [x] Technical constraints identified (Python 3.14, Toad coupling, single dep)
- [x] Cross-cutting concerns mapped (Obsidian integration, state sync, auto-save, context-save)

**✅ Architectural Decisions**

- [x] 10 core decisions documented with versions and rationale
- [x] Technology stack fully specified (single production dep + Node.js for npx)
- [x] Integration patterns defined (MCP server + ToadApp subclass + MadFrogAgent override)
- [x] Performance considerations addressed (async I/O, atomic state file, SQLite cache)

**✅ Implementation Patterns**

- [x] Naming conventions established (snake_case, bmad_ prefix, BMAD prefix)
- [x] Structure patterns defined (absolute imports, constructor injection, tool handler signature)
- [x] Communication patterns specified (MCP JSON-RPC, Textual messages, state file + watchdog)
- [x] Process patterns documented (@traced, two-layer error handling, atomic writes, commit prefix registry)

**✅ Project Structure**

- [x] Complete directory structure defined (~40 files with annotations)
- [x] Component boundaries established (3 processes, no cross-boundary imports)
- [x] Integration points mapped (Toad: 3 imports, MCP: stdio, state: file + watchdog)
- [x] Requirements to structure mapping complete (10 FR domains → specific files)

**✅ Validation & Audit**

- [x] 26 audit items identified and documented
- [x] 1 critical lifecycle correction (projectless MCP server)
- [x] 2 tool additions (bmad_detect_changes, bmad_report_context)
- [x] All logic paths traced end-to-end
- [x] Race conditions analyzed (StateOperationQueue, atomic writes, watchdog)
- [x] Failure modes documented (MCP crash recovery, git commit failure, npx missing)

### Architecture Readiness Assessment

**Overall Status:** READY FOR IMPLEMENTATION

**Confidence Level:** HIGH — all critical decisions made, patterns concrete with code examples, audit findings documented. Story 1 spike will verify 3 Toad integration assumptions before full build begins.

**Key Strengths:**
- Single production dependency minimises supply chain risk
- Three-process architecture provides clean separation and independent testability
- MCP-based tool exposure is agent-agnostic and protocol-compliant
- Silent context-save safety net closes the last data-loss risk
- Two-phase server lifecycle cleanly separates config from project state
- 90 tests mapped to specific files — test plan is implementation-ready
- 26 audit items documented — implementing agents have answers before they have questions

**Spike Verification Items (Story 1):**
- `ToadApp.CSS_PATH` class attribute inheritance
- `MadFrogApp` → `MadFrogAgent` wiring mechanism
- `acp_new_session` parent method post-session-ID behaviour
- `toad.agents.resolve_agent` import existence

**Areas for Future Enhancement:**
- Conversation transcript persistence (FR53-55) — post-MVP
- Full vault indexing for cross-vault wikilinks — optimistic linking for now
- No-GIL Python evaluation when ecosystem matures
- Telemetry (FR85) — trivial addition via tool call logging
- Dynamic context window detection from ACP session metadata (currently via tool call)

### Implementation Handoff

**AI Agent Guidelines:**

- Follow all architectural decisions exactly as documented
- Apply `@traced` to every function — no exceptions
- Use implementation patterns consistently: absolute imports, constructor injection, snake_case JSON keys
- Respect process boundaries: no imports between ui/ and tools/services/
- All git-mutating operations through StateOperationQueue — no exceptions
- Tool handlers follow exact signature: `async def bmad_*(server, arguments) -> dict`
- Refer to this document for all architectural questions
- Check the 26 audit items for edge cases and clarifications

**First Implementation Priority:**

Story 1: Validation spike — verify Toad integration assumptions (`CSS_PATH`, agent wiring, `acp_new_session` parent behaviour). Minimal code, maximum learning. Architecture assumptions confirmed or corrected before full build begins.
