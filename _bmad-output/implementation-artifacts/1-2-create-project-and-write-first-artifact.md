# Story 1.2: Create Project & Write First Artifact

Status: ready-for-dev

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a user,
I want to create a new BMAD project in my chosen workspace directory and write my first planning artifact,
so that I can begin the guided planning process with all work safely committed to Git.

## Acceptance Criteria

### AC 1.2.1 — First-Run Workspace Configuration
- Given the application launches and no workspace path has been configured
- When `WorkspaceSetupScreen` is displayed as a modal
- Then I can browse to or type an absolute directory path
- And the path is validated to be writable and on a local filesystem (not a network mount)
- And the chosen path is persisted for future launches
- And the modal cannot be dismissed without selecting a valid path

### AC 1.2.2 — Welcome Screen with New Project Action
- Given the workspace path is configured
- When `WelcomeScreen` renders
- Then a "Start new project" button is prominently displayed
- And the screen renders within 1 second of launch (PERF-02)

### AC 1.2.3 — Duplicate Project Name Prevention (FR2)
- Given a project named "my-project" already exists
- When I attempt to create a new project with the name "my-project"
- Then the system rejects the name with a clear message explaining the conflict
- And I am guided to choose a unique name before proceeding

### AC 1.2.4 — Project Creation via bmad_create_project
- Given I click "Start new project" and provide a project name
- When `bmad_create_project` is invoked
- Then a new directory is created under the workspace path
- And `git init` initializes a repository in that directory
- And `npx bmad init` scaffolds the BMAD method files into `_bmad/`
- And a branch-prefix namespace is established for this project (e.g., `project-name/main`)
- And a `ProjectRecord` is persisted in the SQLite index via `SQLiteCheckpointIndex`
- And `GitStateEngine` is initialized for the new repository

### AC 1.2.5 — First Artifact Write via bmad_write_artifact
- Given a project has been created and the agent is in the Analysis phase
- When `bmad_write_artifact` is called with artifact content
- Then the artifact file is written atomically (write-to-temp then rename)
- And the file includes valid Obsidian frontmatter (title, type, date, phase)
- And YAML frontmatter passes validation against the expected schema
- And a Git commit is created with the artifact content
- And the commit message follows the convention `[artifact] <type>: <title>`

### AC 1.2.6 — Sensitive File Protection (SEC-01)
- Given a project has been created
- When I inspect the project directory
- Then `.env` is listed in `.gitignore`
- And no files matching `*.secret`, `*.key`, or `credentials.*` are tracked by Git

### AC 1.2.7 — Crash Recovery of Partial Write (REL-01, REL-02)
- Given an artifact write is in progress
- When the process is killed mid-write
- Then on next launch, no partial artifact file exists in the working tree
- And Git history contains only complete, valid commits

## Tasks / Subtasks

- [ ] Task 1: MCP Server Two-Phase Lifecycle (AC: 1.2.4, foundation for all)
  - [ ] 1.1 Refactor `mcp_server.py` to class-based `MadFrogMCPServer` with `self.project: ProjectContext | None = None`
  - [ ] 1.2 Add `_require_project()` guard that raises `NoProjectOpen` if no project active
  - [ ] 1.3 Update `_dispatch()` to pass `server` instance to tool handlers
  - [ ] 1.4 Update tool handler signature to `async def handler(server, arguments) -> dict`
  - [ ] 1.5 Update existing `handle_bmad_ping` to match new signature (receives server, arguments)
  - [ ] 1.6 Move TOOL_HANDLERS registry to `tools/__init__.py` with imports from all tool modules
  - [ ] 1.7 Add `tools/definitions.py` with all tool schemas for this story (bmad_ping, bmad_create_project, bmad_write_artifact)

- [ ] Task 2: GitStateEngine service (AC: 1.2.4, 1.2.5, 1.2.7)
  - [ ] 2.1 Create `services/git_state_engine.py` — wraps GitPython (`import git`) for commit, init, status, tree_hash
  - [ ] 2.2 Implement `init(path)` — `git.Repo.init(path)`, create initial `.gitignore`, initial commit `[init] Project created`
  - [ ] 2.3 Implement `commit(message, paths=None)` — stage specified files (or all), commit with message
  - [ ] 2.4 Implement `is_dirty()` — returns bool via `repo.is_dirty(untracked_files=True)`
  - [ ] 2.5 Implement `tree_hash(path)` — returns `repo.git.rev_parse("HEAD:_bmad")` for method version tracking
  - [ ] 2.6 CRITICAL: GitPython is a transitive dependency via Toad — do NOT add to pyproject.toml

- [ ] Task 3: StateFileWriter service (AC: 1.2.4, 1.2.5)
  - [ ] 3.1 Create `services/state_file.py` — atomic `state.json` writes via `os.replace()` (write temp, rename)
  - [ ] 3.2 Implement `write(state_dict)` — serializes to JSON, writes to temp file, `os.replace()` to `state.json`
  - [ ] 3.3 Implement `read()` — loads and returns state dict from `state.json`
  - [ ] 3.4 State format: `{"current_phase": "...", "workflows": {}, "last_checkpoint": {}, "checkpoint_history": [], "auto_save": {}, "session_lock": {}, "updated_at": "..."}`

- [ ] Task 4: StateOperationQueue service (AC: 1.2.5, 1.2.7)
  - [ ] 4.1 Create `services/state_operation_queue.py` — async priority queue serializing git-mutating operations
  - [ ] 4.2 Implement `Priority` enum: `INTENTIONAL = 0`, `AUTO_SAVE = 10` (lower = higher priority)
  - [ ] 4.3 Implement `enqueue_and_wait(priority, operation)` — enqueue, await result via `asyncio.Event`
  - [ ] 4.4 Implement `_worker()` — asyncio task that processes queue items sequentially
  - [ ] 4.5 IMPORTANT: Only git-mutating operations go through the queue; file writes happen outside

- [ ] Task 5: ProjectContext bundle (AC: 1.2.4)
  - [ ] 5.1 Create `ProjectContext` dataclass/class bundling: `path`, `git_engine: GitStateEngine`, `state_writer: StateFileWriter`, `state_queue: StateOperationQueue`, `config: dict`
  - [ ] 5.2 Implement `ProjectContext.create(path, name)` — constructs all services for a new project
  - [ ] 5.3 Load project BMAD config from `path/_bmad/bmm/config.yaml` (or `_bmad/core/config.yaml`)
  - [ ] 5.4 Store in `MadFrogMCPServer.project` when `bmad_create_project` is called

- [ ] Task 6: bmad_create_project tool (AC: 1.2.3, 1.2.4, 1.2.6)
  - [ ] 6.1 Create `tools/project.py` with `bmad_create_project(server, arguments) -> dict`
  - [ ] 6.2 Validate arguments: `name` (required, string), `path` (required, string — workspace root)
  - [ ] 6.3 Check for duplicate project name: `os.path.exists(path / name)` → error if exists
  - [ ] 6.4 Guard `npx` availability: `shutil.which("npx")` → error "npx not found. Node.js required for BMAD installation." if missing
  - [ ] 6.5 Create directory: `os.makedirs(project_path)`
  - [ ] 6.6 Run `git init` via `GitStateEngine.init(project_path)`
  - [ ] 6.7 Create `.gitignore` with: `.env`, `*.secret`, `*.key`, `credentials.*`, `__pycache__/`, `.venv/`, `*.db`
  - [ ] 6.8 Run `subprocess.run(["npx", "bmad", "init"], cwd=project_path, check=True)` to scaffold `_bmad/`
  - [ ] 6.9 Initial commit: `[init] Project created with BMAD`
  - [ ] 6.10 Create `ProjectContext` and assign to `server.project`
  - [ ] 6.11 Write initial `state.json` via StateFileWriter
  - [ ] 6.12 Return success with project path and name

- [ ] Task 7: ArtifactValidator service (AC: 1.2.5)
  - [ ] 7.1 Create `services/artifact_validator.py` — validates artifact content before write
  - [ ] 7.2 Implement `validate(content, artifact_type)` returning `ValidationResult(valid: bool, issues: list[str])`
  - [ ] 7.3 Check YAML frontmatter present and parseable (title, type, date, phase required fields)
  - [ ] 7.4 Check wikilinks resolve to existing files within project (warning, not error)
  - [ ] 7.5 Check section structure (has at least one heading after frontmatter)

- [ ] Task 8: bmad_write_artifact tool (AC: 1.2.5, 1.2.7)
  - [ ] 8.1 Create `tools/artifact.py` with `bmad_write_artifact(server, arguments) -> dict`
  - [ ] 8.2 Call `server._require_project()` — fails if no project open
  - [ ] 8.3 Validate arguments: `artifact_type` (required), `filename` (required), `content` (required)
  - [ ] 8.4 Run `ArtifactValidator.validate(content, artifact_type)` — fail on critical, warn on non-critical
  - [ ] 8.5 Write file atomically: write to temp file → `os.replace()` to final path in `_bmad-output/<subdir>/`
  - [ ] 8.6 Determine output subdirectory from artifact_type (e.g., "planning" → `planning-artifacts/`)
  - [ ] 8.7 Enqueue git commit via StateOperationQueue: `[artifact] <type>: <filename>`
  - [ ] 8.8 Update state.json via StateFileWriter (add to `checkpoint_history`)
  - [ ] 8.9 Return success with file path and commit SHA

- [ ] Task 9: WorkspaceSetupScreen UI widget (AC: 1.2.1)
  - [ ] 9.1 Create `ui/workspace_setup.py` — Textual Screen modal (~50 lines)
  - [ ] 9.2 Input widget for absolute directory path
  - [ ] 9.3 Validate path: exists, is directory, is writable, is local filesystem
  - [ ] 9.4 Save to `.vibe/config.yaml` (create `.vibe/` directory if needed)
  - [ ] 9.5 Cannot be dismissed without valid path selection
  - [ ] 9.6 On completion, push WelcomeScreen

- [ ] Task 10: WelcomeScreen UI widget (AC: 1.2.2)
  - [ ] 10.1 Create `ui/welcome_screen.py` — Textual Screen (~100 lines)
  - [ ] 10.2 Display "Start new project" button prominently
  - [ ] 10.3 Initially just the "new project" action (project list and resume in story 1.3)
  - [ ] 10.4 New project action: prompt for name, call agent to create via bmad_create_project

- [ ] Task 11: MadFrogApp lifecycle update (AC: 1.2.1, 1.2.2)
  - [ ] 11.1 Update `app.py` `on_mount()` to check for `.vibe/config.yaml`
  - [ ] 11.2 If no config → push `WorkspaceSetupScreen` modal
  - [ ] 11.3 If config exists → push `WelcomeScreen`
  - [ ] 11.4 Add `state.json` file watching via watchdog (Toad dependency) for sidebar state sync

- [ ] Task 12: Update models.py (AC: foundation)
  - [ ] 12.1 Add `ProjectStatus` enum: `ACTIVE`, `ARCHIVED`, `UNHEALTHY`
  - [ ] 12.2 Expand `ProjectRecord` with: `id`, `path`, `method_version`, `created_at`, `last_active`, `status`
  - [ ] 12.3 Expand `Checkpoint` with: `git_sha`, `project_id`, `parent_sha`, `checkpoint_type`, `timestamp`
  - [ ] 12.4 Expand `Decision` with: `step`, `topic`, `decision`, `artifact_ref`
  - [ ] 12.5 Add TypedDict types for MCP results: `ProjectResult`, `ArtifactResult`

- [ ] Task 13: Update constants.py (AC: foundation)
  - [ ] 13.1 Add `AUTO_SAVE_INTERVAL = int(os.environ.get("MAD_FROG_AUTO_SAVE", "120"))`
  - [ ] 13.2 Add `DEFAULT_CONTEXT_WINDOW = int(os.environ.get("MAD_FROG_CONTEXT_WINDOW", "200000"))`
  - [ ] 13.3 Add `CONTEXT_SAVE_RATIO = 0.90`
  - [ ] 13.4 Remove `TOOL_ROOT` (tools now registered via `tools/__init__.py` registry)
  - [ ] 13.5 Add `COMMIT_PREFIXES` dict mapping prefix names to bracket strings

- [ ] Task 14: Test suite (AC: all)
  - [ ] 14.1 `tests/services/test_git_state_engine.py` — init, commit, is_dirty, tree_hash (5 tests)
  - [ ] 14.2 `tests/services/test_state_file.py` — atomic write, read, concurrent reads (4 tests)
  - [ ] 14.3 `tests/services/test_state_operation_queue.py` — priority ordering, enqueue_and_wait (4 tests)
  - [ ] 14.4 `tests/services/test_artifact_validator.py` — valid frontmatter, missing fields, broken wikilinks (4 tests)
  - [ ] 14.5 `tests/tools/test_project.py` — create success, duplicate name, npx missing, .gitignore (5 tests)
  - [ ] 14.6 `tests/tools/test_artifact.py` — write success, validation fail, atomic write, commit format (5 tests)
  - [ ] 14.7 `tests/ui/test_workspace_setup.py` — saves config, rejects invalid, modal not dismissable (3 tests)
  - [ ] 14.8 `tests/ui/test_welcome_screen.py` — renders, new project button (2 tests)
  - [ ] 14.9 Update `tests/test_mcp_server.py` — test dispatch with server instance, tool registry sync
  - [ ] 14.10 Update existing tests to match new tool handler signature

## Dev Notes

### Architecture Context — Week 1 Walking Skeleton (Post-Spike)

This story implements the three core tools identified in the architecture's Week 1 build sequence: `bmad_create_project`, `bmad_write_artifact`, and the infrastructure they depend on. Story 1.1 proved the three-process architecture works. This story makes it DO something — create real projects and write real artifacts.

The MCP server transitions from a simple dispatcher to a stateful two-phase system (projectless → project-active), and four infrastructure services come online: `GitStateEngine`, `StateFileWriter`, `StateOperationQueue`, and `ArtifactValidator`.

### Critical Technical Decisions (MUST FOLLOW)

**MCP Server becomes class-based (`MadFrogMCPServer`):** The current function-based server in `mcp_server.py` must become a class to hold project state. The two-phase lifecycle is critical:
- Phase 1 (projectless): handles `initialize`, `tools/list`, and `bmad_ping` only
- Phase 2 (project-active): `bmad_create_project` creates `ProjectContext`, enables all project-scoped tools

**Tool handler signature changes:** ALL tool handlers must follow this exact pattern:
```python
async def bmad_<tool_name>(server: "MadFrogMCPServer", arguments: dict) -> dict:
    """Docstring matches MCP schema description exactly."""
    # 1. _require_project() if project-scoped
    # 2. Validate arguments
    # 3. Call services via server.project.<service>
    # 4. Return CallToolResult dict
```

**Tool dispatch registry pattern:** Move from hardcoded dict in `mcp_server.py` to `tools/__init__.py`:
```python
from mad_frog.tools.project import bmad_create_project
from mad_frog.tools.artifact import bmad_write_artifact

TOOL_HANDLERS: dict[str, Callable] = {
    "bmad_create_project": bmad_create_project,
    "bmad_write_artifact": bmad_write_artifact,
    "bmad_ping": handle_bmad_ping,
}
```

**Tool definitions separate from handlers:** Create `tools/definitions.py` with all JSON Schema tool definitions. Consistency test: `assert {t["name"] for t in TOOL_DEFINITIONS} == set(TOOL_HANDLERS.keys())`

**Single production dependency — STILL just `batrachian-toad`:** GitPython is transitive via Toad. aiosqlite is transitive via Toad. Do NOT add these to `pyproject.toml`. Import `git` directly — it's available because Toad depends on GitPython 3.1.46.

**BMAD installed via `npx bmad init`, NOT copied:** The architecture explicitly states the tool doesn't ship BMAD — it installs it. Use `subprocess.run(["npx", "bmad", "init"], cwd=project_path)`. Guard with `shutil.which("npx")` check.

**Atomic file writes:** ALL file writes use write-to-temp-then-rename pattern: `write(temp_path)` → `os.replace(temp_path, final_path)`. This prevents partial files on crash (AC 1.2.7).

**StateOperationQueue serializes ONLY git-mutating operations:** File writes happen outside the queue. Only the subsequent `git commit` is enqueued. This prevents unnecessary serialization.

**Commit prefix registry:** Use these exact prefixes:
- `[init]` for `bmad_create_project`
- `[artifact]` for `bmad_write_artifact`
- All other prefixes documented but implemented in later stories

**`state.json` format (architecture-prescribed):**
```json
{
    "current_phase": "analysis",
    "workflows": {},
    "last_checkpoint": {"git_sha": "...", "summary": "...", "timestamp": "..."},
    "checkpoint_history": [],
    "auto_save": {"last_save": null, "interval_seconds": 120, "enabled": false},
    "session_lock": {"pid": null, "acquired_at": null},
    "updated_at": "..."
}
```

### Previous Story Intelligence (Story 1.1 Learnings)

**Toad circular import:** `toad.acp.agent` ↔ `toad.acp.messages` — resolved by importing `toad.acp.messages` first in `agent.py`. Keep this pattern.

**`textual-dev>=2.0` not available:** Story 1.1 pinned to `>=1.0` (latest is 1.8.0). Don't change this.

**`batrachian-toad` installed as v0.6.8:** Higher than the `>=0.5.35` minimum. Confirms GitPython and aiosqlite are available as transitives.

**MadFrogAgent monkey-patching pattern:** `__main__.py` patches `toad.widgets.conversation.Agent` with `MadFrogAgent`. This is the verified wiring mechanism — do not change it.

**Agent config loaded from `agents/claude.toml`:** App loads this TOML file and passes `agent_data` to `ToadApp.__init__()`. Confirmed working.

**Test patterns established:**
- Direct function testing for MCP dispatch (no I/O needed)
- `asyncio.StreamReader` with `feed_data/feed_eof` for message loop tests
- Actual subprocess spawning for process lifecycle tests
- `AsyncMock` for agent async testing
- `tmp_git_repo` fixture creates temp git repo with initial commit
- 35 tests, 90% coverage — maintain or improve this baseline

**Code review fixes to preserve:**
- `ComposeResult` return type on `compose()`
- `RuntimeError` raise (not assert) for None responses
- `asyncio.get_running_loop()` not deprecated `get_event_loop()`

### MCP Server Refactoring Guide

The current `mcp_server.py` is ~100 lines of functions. It needs to become:

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

    async def dispatch(self, msg: dict) -> dict | None:
        # Same dispatch logic, but tool calls pass `self` as first arg
        ...

    async def serve(self):
        # Same stdio loop
        ...
```

**Key changes from current code:**
1. `_dispatch()` → `self.dispatch()` (method, not function)
2. `TOOL_HANDLERS` imported from `tools/__init__.py`
3. `TOOLS` → `TOOL_DEFINITIONS` imported from `tools/definitions.py`
4. Tool calls: `await handler(self, arguments)` instead of `handler()`
5. `serve()` → `self.serve()` (method)
6. `main()` creates `MadFrogMCPServer()` and calls `server.serve()`

### Artifact Write Pipeline

```
Agent calls bmad_write_artifact(server, {"artifact_type": "prd", "filename": "prd.md", "content": "..."})
  → _require_project() — asserts project is active
  → ArtifactValidator.validate(content, "prd")
    → Check YAML frontmatter (title, type, date, phase)
    → Check wikilinks (warning only)
    → If critical failure → return error result immediately
  → Determine output path: project_path / "_bmad-output" / "planning-artifacts" / filename
  → Atomic write: tempfile in same dir → os.replace() to final path
  → Enqueue git commit via StateOperationQueue at INTENTIONAL priority:
    → git add <file_path>
    → git commit -m "[artifact] prd: prd.md"
  → Update state.json: append to checkpoint_history
  → Return: {"path": "...", "git_sha": "...", "validated": true}
```

### Project Structure Notes

New files to create in this story:
```
src/mad_frog/
├── mcp_server.py              # REFACTOR: function-based → MadFrogMCPServer class
├── tools/
│   ├── __init__.py            # CHANGE: add TOOL_HANDLERS registry
│   ├── definitions.py         # NEW: tool JSON Schema definitions
│   ├── ping.py                # UPDATE: new handler signature
│   ├── project.py             # NEW: bmad_create_project
│   └── artifact.py            # NEW: bmad_write_artifact
├── services/
│   ├── __init__.py            # unchanged (empty)
│   ├── git_state_engine.py    # NEW: GitPython wrapper (~200 lines)
│   ├── state_file.py          # NEW: atomic state.json writer
│   ├── state_operation_queue.py # NEW: async priority queue
│   └── artifact_validator.py  # NEW: frontmatter + wikilink validator
├── ui/
│   ├── __init__.py            # unchanged (empty)
│   ├── welcome_screen.py      # NEW: project list + new project
│   └── workspace_setup.py     # NEW: first-run workspace modal
├── models.py                  # UPDATE: expanded data models
├── constants.py               # UPDATE: new constants
└── app.py                     # UPDATE: on_mount lifecycle
```

New test files:
```
tests/
├── services/
│   ├── __init__.py
│   ├── test_git_state_engine.py    # NEW
│   ├── test_state_file.py          # NEW
│   ├── test_state_operation_queue.py # NEW
│   └── test_artifact_validator.py  # NEW
├── tools/
│   ├── __init__.py
│   ├── test_project.py             # NEW
│   └── test_artifact.py            # NEW
├── ui/
│   ├── __init__.py
│   ├── test_workspace_setup.py     # NEW
│   └── test_welcome_screen.py      # NEW
├── test_mcp_server.py              # UPDATE
├── test_mcp_server_async.py        # UPDATE
├── test_agent.py                   # unchanged
├── test_app.py                     # UPDATE
├── test_entrypoint.py              # unchanged
└── test_process_lifecycle.py       # UPDATE
```

### Alignment with Unified Project Structure

- All new files match architecture's prescribed directory structure [Source: architecture.md#Complete-Project-Directory-Structure]
- Tool modules follow `tools/<category>.py` pattern with handler functions
- Service modules follow `services/<service_name>.py` pattern
- UI modules follow `ui/<screen_name>.py` pattern
- All `__init__.py` files remain empty (no barrel exports) per architecture convention

### Git Intelligence Summary

Recent commit history shows:
1. `3fcd7a4` — restructured as mad-frog with Toad and MCP integration (Story 1.1 complete)
2. `e80a04e` — sprint status and workflow shortcuts added
3. `6ae3935` — epics breakdown completed
4. `3fc57ed` — UX design alignment
5. `d761ecf` — PRD alignment

The codebase is in a clean post-story-1.1 state. All foundation code is in place. The MCP server, agent, and app patterns are established and tested. This story builds directly on that foundation.

### Latest Tech Information

**batrachian-toad v0.6.8** (installed) — provides:
- `ToadApp` base class with `compose()`, `CSS_PATH`, Settings
- `Agent` base class with `acp_new_session()` override point
- GitPython 3.1.46 as transitive (confirmed working in story 1.1)
- aiosqlite 0.22.1 as transitive (available but not yet used)
- watchdog as transitive (needed for state.json file watching)

**Python 3.14.3** (stable, Feb 2026) — standard GIL mode. All stdlib features available.

**GitPython 3.1.46** — `git.Repo.init()`, `repo.git.add()`, `repo.git.commit()`, `repo.is_dirty()`, `repo.git.rev_parse()`. All needed operations are standard API.

**MCP protocol** — stdio JSON-RPC as implemented in story 1.1. No changes to transport layer needed.

### References

- [Source: _bmad-output/planning-artifacts/architecture.md#Tool-Interface-18-Functions] — bmad_create_project and bmad_write_artifact tool specifications
- [Source: _bmad-output/planning-artifacts/architecture.md#Infrastructure-Services-7] — GitStateEngine, StateOperationQueue, StateFileWriter, ArtifactValidator specs
- [Source: _bmad-output/planning-artifacts/architecture.md#Item-23] — MCP Server two-phase lifecycle (projectless → project-active)
- [Source: _bmad-output/planning-artifacts/architecture.md#Item-21] — Tool dispatch registry pattern
- [Source: _bmad-output/planning-artifacts/architecture.md#Item-12] — Tool schema quality standard
- [Source: _bmad-output/planning-artifacts/architecture.md#Item-15] — StateOperationQueue boundary (git ops only)
- [Source: _bmad-output/planning-artifacts/architecture.md#Item-17] — Node.js + npx guard
- [Source: _bmad-output/planning-artifacts/architecture.md#Item-25] — Commit prefix registry
- [Source: _bmad-output/planning-artifacts/architecture.md#BMAD-Method-Management] — npx bmad init/update pattern
- [Source: _bmad-output/planning-artifacts/architecture.md#Core-Data-Structures] — ProjectRecord, Checkpoint, Decision expanded schemas
- [Source: _bmad-output/planning-artifacts/architecture.md#Updated-Build-Sequence] — Week 1 walking skeleton scope
- [Source: _bmad-output/planning-artifacts/architecture.md#Decision-3] — MCP server implementation, tool return format
- [Source: _bmad-output/planning-artifacts/architecture.md#Two-Tier-State-Model] — Git durable, SQLite reconstructable, session volatile
- [Source: _bmad-output/planning-artifacts/architecture.md#Safety-Nets] — Atomic operations, auto-save, artifact detection
- [Source: _bmad-output/planning-artifacts/architecture.md#Updated-constants.py] — AUTO_SAVE_INTERVAL, DEFAULT_CONTEXT_WINDOW, CONTEXT_SAVE_RATIO
- [Source: _bmad-output/planning-artifacts/epics.md#Story-1.2] — Acceptance criteria source
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#Executive-Summary] — WorkspaceSetupScreen and WelcomeScreen UX context
- [Source: _bmad-output/implementation-artifacts/1-1-toad-integration-spike-and-walking-skeleton.md] — Story 1.1 learnings, code patterns, code review fixes
- [Source: _bmad-output/planning-artifacts/architecture.md#Design-Updates-Item-13] — state.json expanded format with checkpoint_history

## Dev Agent Record

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List
