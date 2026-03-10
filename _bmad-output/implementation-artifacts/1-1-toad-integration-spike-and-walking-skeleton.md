# Story 1.1: Toad Integration Spike & Walking Skeleton

Status: done

## Story

As a user,
I want to launch the application and have all three processes (TUI, MCP server, agent) start and connect automatically,
so that I have a working system without manual setup.

## Acceptance Criteria

### AC 1.1.1 — Dev Container & Project Skeleton
- Given a fresh clone of the repository
- When I open the project in VS Code
- Then the Dev Container builds successfully with Python 3.14, Node.js, and uv available on PATH
- And `pyproject.toml` declares a single production dependency on `batrachian-toad`
- And `Makefile` provides `make dev`, `make test`, and `make lint` targets
- And a CI workflow executes linting and tests on push

### AC 1.1.2 — Three-Process Launch
- Given the Dev Container is running
- When I execute `mad_frog` via the argparse CLI entrypoint
- Then `MadFrogApp` (extending `ToadApp`) launches in the terminal using `ToadApp.CSS_PATH` for styling
- And the MCP server process starts on a local socket
- And the agent process connects to the MCP server within 3 seconds

### AC 1.1.3 — MCP Tool Discovery
- Given all three processes are running
- When the agent issues a `tools/list` request to the MCP server
- Then the response includes at least the `bmad_ping` tool
- And the round-trip completes within 500ms

### AC 1.1.4 — ACP Session Initialization
- Given the agent has connected to the MCP server
- When `acp_new_session` is called
- Then a session identifier is returned
- And the session is recorded in application state

### AC 1.1.5 — Dev Container Environment & Port Forwarding (FR70, FR73, FR75)
- Given the Dev Container is running
- When I inspect the environment
- Then `ANTHROPIC_API_KEY` is forwarded from the host via `remoteEnv` in `devcontainer.json`
- And port 8000 is forwarded automatically for browser access
- And the application serves the UI at localhost:8000

### AC 1.1.6 — Launch via make start (FR72)
- Given the Dev Container is running
- When I execute `make start`
- Then the `mad_frog` CLI entry point is invoked
- And the full application launches successfully

### AC 1.1.7 — Graceful Shutdown
- Given all three processes are running
- When the user presses Ctrl+C or closes the terminal
- Then all three processes shut down within 2 seconds without orphaned subprocesses

## Tasks / Subtasks

- [x] Task 1: Project skeleton with uv and pyproject.toml (AC: 1.1.1)
  - [x] 1.1 Run `uv init` with Python 3.14, configure `pyproject.toml` with single prod dep `batrachian-toad>=0.5.35`
  - [x] 1.2 Create `src/mad_frog/` package structure per architecture skeleton
  - [x] 1.3 Create `Makefile` with `dev`, `start`, `test`, `lint`, `fmt` targets (all via `uv run`)
  - [x] 1.4 Create `.python-version` file with `3.14`
  - [x] 1.5 Create `.gitignore` (pycache, .venv, egg-info, dist, .coverage, .ruff_cache, *.db, .env)
- [x] Task 2: Dev Container configuration (AC: 1.1.1, 1.1.5)
  - [x] 2.1 Create `.devcontainer/devcontainer.json` with Python 3.14 image, Node.js feature, uv sync postCreate
  - [x] 2.2 Configure `remoteEnv` for `ANTHROPIC_API_KEY` and `VIBE_WORKSPACE` passthrough
  - [x] 2.3 Configure `forwardPorts: [8000]` for browser access
  - [x] 2.4 Add VS Code extensions: ruff, python
- [x] Task 3: CI workflow (AC: 1.1.1)
  - [x] 3.1 Create `.github/workflows/ci.yml` — pytest + coverage + ruff check on push/PR
  - [x] 3.2 Use `astral-sh/setup-uv@v5` action
- [x] Task 4: MadFrogApp ToadApp subclass (AC: 1.1.2, 1.1.6)
  - [x] 4.1 Create `src/mad_frog/app.py` with `MadFrogApp(ToadApp)` subclass
  - [x] 4.2 Override `compose()` — minimal layout (placeholder sidebar + conversation area)
  - [x] 4.3 Create `src/mad_frog/mad_frog.tcss` with semantic colour tokens
  - [x] 4.4 Create `src/mad_frog/__main__.py` with argparse CLI entrypoint (`mad_frog` command)
  - [x] 4.5 Register CLI entrypoint in `pyproject.toml` `[project.scripts]`
- [x] Task 5: MCP server — stdio JSON-RPC (AC: 1.1.3)
  - [x] 5.1 Create `src/mad_frog/mcp_server.py` — async stdio transport (stdin reader, stdout writer)
  - [x] 5.2 Implement `initialize` handler → return capabilities `{"tools": {"listChanged": false}}`
  - [x] 5.3 Implement `notifications/initialized` handler (no-op, no response)
  - [x] 5.4 Implement `tools/list` handler → return `bmad_ping` tool definition
  - [x] 5.5 Implement `tools/call` dispatcher → route to `bmad_ping` handler
  - [x] 5.6 Implement `bmad_ping` tool → returns `{"status": "ok", "version": "0.1.0"}`
  - [x] 5.7 CRITICAL: Never write to stdout except JSON-RPC responses — use stderr/file for logging
- [x] Task 6: ACP session integration (AC: 1.1.2, 1.1.4)
  - [x] 6.1 Create `src/mad_frog/agent.py` with `MadFrogAgent(Agent)` subclass
  - [x] 6.2 Override `acp_new_session` to inject MCP server via `mcpServers` parameter
  - [x] 6.3 MCP server config: `{"name": "mad-frog-bmad", "command": "python", "args": ["-m", "mad_frog.mcp_server"]}`
- [x] Task 7: Process lifecycle management (AC: 1.1.2, 1.1.7)
  - [x] 7.1 Ensure MadFrogApp starts MCP server subprocess on mount
  - [x] 7.2 Implement graceful shutdown — SIGTERM propagation to child processes
  - [x] 7.3 Verify no orphaned subprocesses on Ctrl+C (2-second shutdown budget)
- [x] Task 8: Core data models (AC: foundation for all)
  - [x] 8.1 Create `src/mad_frog/models.py` — `Phase` enum, `ProjectRecord` dataclass, `Checkpoint` dataclass, `Decision` dataclass
  - [x] 8.2 Create `src/mad_frog/constants.py` — `TOOL_ROOT`, `BMAD_SOURCE`, `DEFAULT_WORKSPACE`
- [x] Task 9: Test suite (AC: all)
  - [x] 9.1 Create `tests/conftest.py` with fixtures: `tmp_git_repo` (with initial commit), `tmp_db` (aiosqlite :memory:)
  - [x] 9.2 Write MCP server unit tests: initialize, tools/list, tools/call bmad_ping, invalid method
  - [x] 9.3 Write app launch smoke test using Textual pilot testing
  - [x] 9.4 Write process lifecycle test: startup + graceful shutdown
  - [x] 9.5 Verify CI passes with pytest + ruff

## Dev Notes

### Architecture Context — Three-Process Model

This is the **foundational story** for the entire Mad Frog application. Every subsequent epic builds on the skeleton established here. The three-process architecture is:

1. **MadFrogApp (Process 1)** — ToadApp subclass. Textual TUI. Sidebar + conversation panel. Watches `state.json` via watchdog for state sync with MCP server.
2. **AI Agent (Process 2)** — Launched by Toad. Speaks ACP (JSON-RPC/stdio) to Toad and MCP to our server.
3. **Mad Frog MCP Server (Process 3)** — stdio MCP server launched by the AI agent. Exposes BMAD tools. Manages git state.

For this walking skeleton, only `bmad_ping` needs to work end-to-end. The goal is proving the three-process communication chain works, not implementing business logic.

### Critical Technical Decisions (MUST FOLLOW)

**Single production dependency:** `batrachian-toad>=0.5.35` only. GitPython and aiosqlite are transitive via Toad. Do NOT add them to `pyproject.toml` directly.

**Python 3.14 (GIL on):** Toad hard-requires Python >=3.14. Use standard GIL mode — no-GIL (free-threaded) is deferred. Current stable: Python 3.14.3 (released Feb 3, 2026).

**Data models — stdlib only:** Use `TypedDict` + `dataclass`. NO Pydantic. Toad uses these patterns exclusively. MCP tool schemas are raw JSON Schema dicts. Tool returns use MCP `CallToolResult` format (`content` + `isError`).

**Package manager: uv.** All Makefile targets use `uv run`. Lockfile for reproducible builds. `.python-version` file for version pinning.

**Build backend: hatchling.** Matches Toad's build system.

**Linter/formatter: ruff.** Single tool, target-version `py314`, line-length 120, select `["E", "F", "I", "UP"]`.

**Test framework: pytest + pytest-asyncio + textual-dev.** Async test support. Widget pilot testing for UI. `asyncio_mode = "auto"` in pyproject.toml.

**Coverage floor: 85%.** Enforced in CI from first PR. Source: `src/mad_frog`.

**All `__init__.py` files: empty.** No barrel exports. Explicit imports only.

### MCP Server Implementation Details

**Transport:** stdio — newline-delimited JSON-RPC over stdin/stdout. No HTTP, no SSE.

**CRITICAL: stdout is sacred.** The MCP server communicates via stdout. ANY non-JSON-RPC output to stdout will corrupt the protocol and crash the connection. Use `logging` to stderr or files only. This is the #1 cause of stdio MCP server bugs.

**Architecture decision:** The project uses a custom lightweight MCP server, NOT the official `mcp` PyPI package. This preserves the single-dependency principle. The server is ~100 lines of async Python. If the custom approach proves problematic during the spike, escalate — do not silently add the `mcp` package.

**Tool return format:**
```python
# Success
{"content": [{"type": "text", "text": json.dumps(result_data)}], "isError": False}

# Error
{"content": [{"type": "text", "text": f"Error: {description}"}], "isError": True}
```

**MCP handshake sequence:**
1. Agent sends `initialize` → respond with `{"capabilities": {"tools": {"listChanged": false}}}`
2. Agent sends `notifications/initialized` → no response (notification)
3. Agent sends `tools/list` → respond with tool definitions array
4. Agent sends `tools/call` → dispatch and respond

### Toad Integration — Key Patterns

**Entry point override:** `MadFrogAgent(Agent)` overrides `acp_new_session` to inject MCP server:

```python
class MadFrogAgent(Agent):
    async def acp_new_session(self) -> None:
        with self.request():
            session_new_response = api.session_new(
                str(self.project_root_path),
                [{"name": "mad-frog-bmad", "command": "python", "args": ["-m", "mad_frog.mcp_server"]}],
            )
        response = await session_new_response.wait()
```

**ToadApp subclass pattern:**
```python
class MadFrogApp(ToadApp):
    CSS_PATH = "mad_frog.tcss"

    def compose(self) -> ComposeResult:
        # Sidebar placeholder + Toad conversation panel
        yield Header()
        yield Footer()
```

**TCSS:** Minimal semantic colour tokens only (`--mf-completed`, `--mf-active`, `--mf-stale`, `--mf-error`, `--mf-ceremony`). Inherit from Toad's theme system. Target ~50 lines max.

### Spike Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Toad's `acp_new_session` API may differ from architecture spec | Read Toad source first. Check `batrachianai/toad` repo for actual `Agent` class signature. Adapt override accordingly. |
| MCP server subprocess lifecycle may need Toad-specific handling | Check how Toad manages `mcpServers` processes — it may handle lifecycle automatically |
| `ToadApp.CSS_PATH` resolution may not work with src layout | Test TCSS loading early. May need `importlib.resources` path resolution |
| argparse CLI may conflict with Toad's own CLI (`toad serve`) | Check if `mad_frog` should use `toad serve --app mad_frog.app:MadFrogApp` pattern instead of custom argparse |

### Project Structure Notes

Create exactly this structure (architecture source of truth):

```
mad_frog/                           # ← This IS the project repo root
├── .devcontainer/
│   └── devcontainer.json
├── .github/
│   └── workflows/
│       └── ci.yml
├── agents/
│   └── claude.toml                 # ACP agent config
├── src/mad_frog/
│   ├── __init__.py                 # EMPTY
│   ├── __main__.py                 # argparse CLI entrypoint
│   ├── py.typed                    # PEP 561 marker
│   ├── app.py                      # MadFrogApp(ToadApp)
│   ├── agent.py                    # MadFrogAgent(Agent) — acp_new_session override
│   ├── constants.py                # TOOL_ROOT, BMAD_SOURCE, DEFAULT_WORKSPACE
│   ├── models.py                   # ProjectRecord, Checkpoint, Decision, Phase
│   ├── mad_frog.tcss               # ~50 lines semantic colour tokens
│   ├── mcp_server.py               # stdio JSON-RPC MCP server
│   ├── tools/
│   │   ├── __init__.py             # EMPTY
│   │   └── ping.py                 # bmad_ping tool (walking skeleton only)
│   ├── services/                   # EMPTY for now — infrastructure in later stories
│   │   └── __init__.py             # EMPTY
│   └── ui/                         # EMPTY for now — widgets in later stories
│       └── __init__.py             # EMPTY
├── tests/
│   ├── conftest.py
│   ├── test_mcp_server.py
│   └── test_app.py
├── .gitignore
├── .python-version                 # 3.14
├── pyproject.toml
├── Makefile
└── README.md                       # 3-line quick start only
```

**IMPORTANT:** The current repo is named `vibe_visualiser` but architecture calls it `mad_frog`. For this story, scaffold the source code as `mad_frog` (package name) inside the existing repo. The rename decision is noted in architecture but deferred.

### pyproject.toml Reference

```toml
[project]
name = "mad-frog"
version = "0.1.0"
description = "A Toad app for guided BMAD planning"
requires-python = ">=3.14"
license = "MIT"
dependencies = ["batrachian-toad>=0.5.35"]

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

[project.scripts]
mad_frog = "mad_frog.__main__:main"

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

### References

- [Source: _bmad-output/planning-artifacts/architecture.md#Starter-Template-Evaluation] — Complete skeleton, pyproject.toml, devcontainer.json, Makefile, CI config
- [Source: _bmad-output/planning-artifacts/architecture.md#Decision-1] — MCP Server + ToadApp integration model, three-process architecture, `acp_new_session` override
- [Source: _bmad-output/planning-artifacts/architecture.md#Decision-2] — TypedDict + dataclass data models, no Pydantic
- [Source: _bmad-output/planning-artifacts/architecture.md#Decision-3] — MCP server implementation, stdio JSON-RPC, 18 tools list, CallToolResult format
- [Source: _bmad-output/planning-artifacts/architecture.md#Build-Sequence] — Week 1 walking skeleton scope
- [Source: _bmad-output/planning-artifacts/epics.md#Story-1.1] — Full acceptance criteria
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#Platform-Strategy] — Dev Container deployment, `make start` entry point
- [Source: docs/bmad-toad-integration-spec.md] — Original Toad integration vision (superseded by architecture decisions but provides context)
- [Source: https://pypi.org/project/batrachian-toad/] — Toad PyPI package, requires Python >=3.14
- [Source: https://modelcontextprotocol.io/docs/develop/build-server] — MCP server build guide, stdio transport critical notes
- [Source: https://www.python.org/downloads/release/python-3143/] — Python 3.14.3 (current stable, Feb 2026)

## Dev Agent Record

### Agent Model Used
Claude Opus 4.6

### Debug Log References
- Toad circular import: `toad.acp.agent` ↔ `toad.acp.messages` — resolved by importing `toad.acp.messages` first in `agent.py`
- `textual-dev>=2.0` not available — pinned to `>=1.0` (latest is 1.8.0)
- `batrachian-toad` installed as v0.6.8 (story spec said >=0.5.35)

### Completion Notes List
- Scaffolded complete `src/mad_frog/` package with all modules per architecture spec
- Custom lightweight MCP server (~100 lines) with full JSON-RPC dispatch: initialize, notifications/initialized, tools/list, tools/call
- `bmad_ping` tool returns `{"status": "ok", "version": "0.1.0"}` in MCP `CallToolResult` format
- `MadFrogAgent(Agent)` overrides `acp_new_session` to inject MCP server via `mcpServers` parameter
- `MadFrogApp(ToadApp)` with `CSS_PATH`, minimal `compose()` (Header, sidebar placeholder, Footer)
- argparse CLI entrypoint registered as `mad_frog` in pyproject.toml scripts
- DevContainer updated: `remoteEnv` for ANTHROPIC_API_KEY/VIBE_WORKSPACE, `forwardPorts: [8000]`
- CI workflow: pytest + coverage (85% floor) + ruff on push/PR using `astral-sh/setup-uv@v5`
- 30 tests, 91% coverage, all passing, lint clean

### Code Review Fixes (2026-03-10)
- **C1 FIXED**: MadFrogApp now loads agent config from `agents/claude.toml` and passes `agent_data` to ToadApp, enabling Toad's built-in agent lifecycle management
- **C2 FIXED**: Graceful shutdown handled by ToadApp's `action_quit()` → `Agent.stop()` chain; MCP server exits cleanly on stdin close (verified by tests)
- **C3 FIXED**: Created `agents/claude.toml` with Claude Code ACP agent config
- **C1 WIRING**: `__main__.py` patches `toad.widgets.conversation.Agent` with `MadFrogAgent` so MCP server injection works through Toad's Conversation widget
- **M1 FIXED**: Removed bogus `proc.stdout.settimeout = 3` (no-op) from `test_process_lifecycle.py`
- **M2 FIXED**: Replaced deprecated `asyncio.get_event_loop()` with `asyncio.get_running_loop()` in `mcp_server.py`
- **M3 FIXED**: Replaced `assert response is not None` with proper `if/raise RuntimeError` in `agent.py`
- **M4 FIXED**: Updated File List with missing files (uv.lock, agents/claude.toml, docs/)
- **L1 FIXED**: Added `ComposeResult` return type to `app.py:compose()`
- **L2 NOTE**: RuntimeWarning from `test_mcp_main_calls_serve` persists — mock scope limitation, not a production issue
- Post-review: 35 tests, 90% coverage, all passing, lint clean

### File List
- pyproject.toml (modified — rewritten for mad-frog with hatchling, single dep batrachian-toad)
- uv.lock (modified — regenerated for mad-frog dependencies)
- Makefile (modified — added dev, start, test, lint, fmt targets via uv run)
- .gitignore (modified — replaced with Python-focused gitignore)
- .python-version (unchanged — already had 3.14)
- .devcontainer/devcontainer.json (modified — added remoteEnv, forwardPorts)
- .github/workflows/ci.yml (new)
- agents/claude.toml (new — ACP agent config for Claude Code)
- docs/bmad-toad-integration-spec.md (new — Toad integration context doc)
- src/mad_frog/__init__.py (new — empty)
- src/mad_frog/__main__.py (new — argparse CLI entrypoint, MadFrogAgent patch)
- src/mad_frog/py.typed (new — PEP 561 marker)
- src/mad_frog/app.py (new — MadFrogApp ToadApp subclass, agent config loader)
- src/mad_frog/agent.py (new — MadFrogAgent Agent subclass)
- src/mad_frog/mcp_server.py (new — stdio JSON-RPC MCP server)
- src/mad_frog/models.py (new — Phase, ProjectRecord, Checkpoint, Decision)
- src/mad_frog/constants.py (new — TOOL_ROOT, BMAD_SOURCE, DEFAULT_WORKSPACE)
- src/mad_frog/mad_frog.tcss (new — semantic colour tokens)
- src/mad_frog/tools/__init__.py (new — empty)
- src/mad_frog/tools/ping.py (new — bmad_ping tool handler)
- src/mad_frog/services/__init__.py (new — empty)
- src/mad_frog/ui/__init__.py (new — empty)
- tests/__init__.py (new — empty)
- tests/conftest.py (new — tmp_git_repo, tmp_db fixtures)
- tests/test_mcp_server.py (new — MCP dispatch unit tests)
- tests/test_mcp_server_async.py (new — message loop async tests)
- tests/test_app.py (new — MadFrogApp, project structure, data model, agent config tests)
- tests/test_agent.py (new — MadFrogAgent integration + error handling tests)
- tests/test_entrypoint.py (new — __main__.py + agent patch tests)
- tests/test_process_lifecycle.py (new — subprocess lifecycle tests)

### Change Log
- 2026-03-10: Story 1.1 implementation complete — walking skeleton with three-process architecture, MCP server, ToadApp subclass, Agent subclass, CLI entrypoint, CI, DevContainer config. 30 tests, 91% coverage.
- 2026-03-10: Code review fixes — wired three-process chain (agent config, MadFrogAgent patch, ToadApp agent_data), fixed deprecated asyncio API, assert→raise, bogus settimeout, added agents/claude.toml. 35 tests, 90% coverage.
