---
stepsCompleted:
  - step-01-validate-prerequisites
  - step-02-design-epics
  - step-03-create-stories
  - step-04-final-validation
inputDocuments:
  - _bmad-output/planning-artifacts/prd.md
  - _bmad-output/planning-artifacts/architecture.md
  - _bmad-output/planning-artifacts/ux-design-specification.md
---

# vibe_visualiser - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for vibe_visualiser, decomposing the requirements from the PRD, UX Design, and Architecture into implementable stories.

## Requirements Inventory

### Functional Requirements

FR1: User can create a new project with a name from the welcome screen
FR2: System prevents duplicate project names and guides the user to choose a unique name
FR3: User can view a list of all existing projects with their current phase and last-active date
FR4: User can resume any existing project from the welcome screen
FR5: User can archive a project (hidden from welcome screen, preserved in Git)
FR6: System creates a Git-backed state record for each new project with branch-prefix isolation
FR7: System maintains a SQLite checkpoint index with project and checkpoint tables (Git SHA as primary key)
FR8: System supports one active project session at a time -- user switches projects via the welcome screen
FR8a: User can upgrade a project's BMAD method version to the tool's current version via explicit action
FR8b: When opening a directory with `.git/` but no `_bmad/`, system offers to set up BMAD planning in the existing repo
FR8c: When opening a project whose `_bmad/` method version differs from the tool's version, system prompts user to continue or migrate
FR8d: When opening a directory with `_bmad-output/` artifacts but no structured Git state, system offers to validate existing artifacts and infer phase state (brownfield onboarding)
FR9: User can progress through BMAD phases sequentially (Analysis -> Planning -> Solutioning -> Implementation)
FR10: Phases require validated artifacts to unlock -- enforced by agent via BMAD workflow instructions, not by system-level phase gates
FR11: User can import existing artifacts and have the agent validate them to mark a phase complete
FR12: Agent adapts conversational approach based on user response patterns
FR13: User can invoke any BMAD workflow available in the installed module during the appropriate phase
FR14: System creates a Git commit with structured metadata at each phase completion
FR15: System loads the appropriate agent context and workflow instructions when transitioning between phases
FR16: User can ask the agent for help or explanation at any point without losing workflow progress
FR17: User can request a current project status summary at any time
FR18: User can request to revisit and revise a previous answer within the current session
FR19: User can generate architecture decision records during Solutioning phase
FR20: User can generate epics from PRD requirements
FR21: User can generate user stories with acceptance criteria from epics
FR22: System maintains traceability links between stories, epics, PRD, and brief
FR23: User can generate sprint plans that sequence stories into sprints
FR24: Implementation phase MVP scope: sprint plan and story file generation
FR25: User can view a visual Journey Map in the sidebar showing all phases and their completion state
FR26: Journey Map nodes display three visual states: completed (clickable), in-progress, locked
FR27: Journey Map nodes display dates and human-readable descriptions
FR28: User can click any completed phase node in the Journey Map to navigate back to that checkpoint
FR29: Click-back navigation presents a confirmation modal before creating a new version
FR30: System preserves all downstream work on a separate Git branch when user navigates back
FR31: System displays the current position in the Journey Map with a distinct indicator
FR32: User can view version history for any completed phase node (right-click/long-press shows version list with timestamps and summaries)
FR33: User can create a manual checkpoint with a custom label at any point during a session (Ctrl+S)
FR34: Journey Map sidebar scrolls vertically when content exceeds viewport; completed phases can be collapsed
FR35: System manages Git branches internally -- users never see branch names, commit hashes, or Git terminology
FR36: System displays dates and times in the user's local timezone
FR37: System persists all project state to a bind-mounted directory on the host filesystem
FR38: System fully recovers all project state after container rebuild, restart, or destruction
FR39: System stores session context in Git commit metadata sufficient for agent context reconstruction
FR40: Agent greets returning users with context from their last session
FR41: Single active session enforced per project -- second browser tab receives read-only view or option to take over
FR42: System ensures artifact write and Git commit are atomic -- both succeed or both roll back
FR43: System auto-saves uncommitted changes every 2 minutes via deterministic commit templates
FR44: System detects state format version on startup and performs any necessary migrations
FR45: System handles browser disconnection gracefully -- user can reconnect and resume from last stable state
FR45a: System silently pre-empts context window exhaustion by querying agent context budget via bmad_report_context tool and triggering automatic save when usage exceeds 90%
FR46: System writes all artifacts as Obsidian-native markdown with YAML frontmatter and wikilinks
FR47: System generates wikilinks that reference other project artifacts
FR48: Agent generates optimistic wikilinks to pre-existing vault notes when referencing user-provided content
FR49: User configures workspace root via first-run modal
FR50: System generates artifacts that render correctly in Obsidian's graph view with working backlinks
FR51: Artifacts include Obsidian-compatible frontmatter (aliases, tags, phase, project, parent references)
FR52: For vault-resident projects, system proposes .obsidianignore entries during project setup
FR55: Any artifact can be traced through its full parent chain to the original requirement via wikilinks
~~FR53~~: *(Deferred)* Conversation transcripts as structured Obsidian-native markdown files
~~FR54~~: *(Deferred)* Conversation transcripts include frontmatter identifying phase, checkpoint, date, and participating agents
FR56: User can add markdown files to the project folder at any time
FR57: Agent automatically ingests user-added markdown files as context in subsequent sessions
FR58: Agent references content from user-added files accurately in conversation
FR59: System detects new, modified, or deleted files in the project folder via bmad_detect_changes tool
FR60: System tracks markdown files in Git -- binary files are accessible but not version-tracked
FR61: User can invoke Party Mode at any point during any workflow phase
FR62: System loads the complete agent roster from the installed BMAD agent manifest
FR63: System selects 2-3 most relevant agents per discussion round based on topic analysis
FR64: Agents maintain distinct personalities, communication styles, and expertise boundaries
FR65: System visually identifies each agent in Party Mode with their name, icon, and distinct styling
FR66: Agents can reference and build on each other's contributions within a round
FR67: System halts and waits for user input when an agent asks a direct question
FR68: User can exit Party Mode and return to the guided workflow with state preserved
FR69: Toad manages all credential validation and provider setup -- Mad Frog has no credential UI
FR70: API keys are forwarded from host environment via devcontainer.json remoteEnv
FR71: Toad manages all LLM provider connections -- Mad Frog makes no direct LLM API calls
FR72: User can launch the full application via `make start` which runs `mad_frog`
FR73: System serves the complete UI to a browser at localhost:8000
FR74: On first launch, system displays a workspace setup modal asking user for their project directory path
FR75: System forwards the serve port automatically in Dev Container environments
FR76: System performs health checks on startup and reports issues with recovery guidance
FR77: System integrates project state management with Toad's existing session infrastructure
FR78: System provides phase completion feedback including artifact summary, decisions made, and next phase preview
FR79: System presents project completion summary showing all artifacts created, total decision history depth, and link to view full project graph
FR80: System generates artifacts as professional narrative prose, not template fill-in
FR81: Agent has access to all previous decisions and constraints when generating responses within a session
FR82: System handles agent response failures gracefully with clear feedback and option to retry
FR83: System displays clear error messages when state operations fail and offers recovery guidance
FR84: Keyboard navigation available for all primary interactions
FR84a: System detects artifact-like content in conversation that was not saved via a tool call, and prompts user to save
~~FR85~~: *(Deferred)* User can opt in to anonymous usage telemetry
FR86: Community contributors can add new workflow templates by placing markdown step-files in the designated folder structure
FR87: System discovers workflow templates at runtime from the file system (no build step or registry)
FR88: System provides an on-demand health check accessible from the UI (sidebar button + Ctrl+H)

### NonFunctional Requirements

NFR-PERF-01: Journey Map renders and responds to click navigation within 500ms for projects with up to 50 checkpoints
NFR-PERF-02: Atomic artifact-write-plus-commit operations complete within 3 seconds; progress indicator if exceeded
NFR-PERF-03: Welcome screen project list loads within 1 second for up to 20 projects
NFR-PERF-04: SQLite checkpoint queries return within 100ms for projects with up to 200 checkpoints
NFR-PERF-05: Browser UI remains responsive during agent processing; loading indicators for ops >500ms
NFR-PERF-06: Container cold start completes within 30 seconds
NFR-PERF-07: Disk footprint under 500MB per project for up to 100 checkpoints and 50 artifacts
NFR-PERF-08: Warm restart completes health checks within 15 seconds
NFR-PERF-09: System responsive after 4 hours continuous use; memory below 512MB; no memory leaks
NFR-PERF-10: Checkpoint navigation: artifact display within 2s, context reconstruction within 5s
NFR-PERF-11: Handles individual artifact files up to 500KB; warning for larger files
NFR-SEC-01: API keys never logged, displayed in UI, or written to artifacts/Git
NFR-SEC-02: .env files gitignored by default and verified on startup
NFR-SEC-03: No data transmitted except to configured LLM provider via Toad
NFR-SEC-04: System reads/writes only within configured project directory and SQLite path
NFR-REL-01: Zero data loss -- all committed state survives container destruction
NFR-REL-02: Atomic checkpoint operations -- write + commit succeed together or roll back
NFR-REL-03: SQLite index rebuild produces byte-identical database from Git history
NFR-REL-04: Graceful recovery from mid-operation container kill
NFR-REL-05: Browser disconnection does not corrupt state
NFR-REL-06: Startup health check validates Git, SQLite, bind mount, state version within 10s
NFR-REL-07: Atomic session lock acquisition; concurrent connection handling
NFR-REL-08: On-demand health check completes within 5 seconds
NFR-REL-09: Network connectivity loss detection; conversation state preserved
NFR-REL-10: Chaos test suite: 5 failure scenarios, all recover to consistent state
NFR-ACC-01: All primary interactions keyboard-accessible
NFR-ACC-02: UI text elements maintain minimum 4.5:1 contrast ratio (WCAG AA)
NFR-ACC-03: Journey Map states distinguishable by shape/icon, not colour-only
NFR-ACC-04: Error messages use text labels, not icon-only communication
NFR-INT-01: Artifacts pass automated validation: YAML frontmatter, wikilinks, frontmatter fields
NFR-INT-02: Pinned Toad version; upstream updates validated before bump
NFR-INT-03: CommonMark-compliant markdown output
NFR-INT-04: Standard Git commands only -- no extensions
NFR-INT-05: Runs on Docker Desktop (macOS, Windows, Linux) without platform-specific config
NFR-INT-06: UTF-8/Unicode support; handles spaces and special chars in file paths
NFR-OBS-01: Structured JSON logs with rotation at 10MB
NFR-OBS-02: Error logs include operation ID, state snapshot, classification, recovery action
NFR-MNT-01: State format version identifier with automated migrations
NFR-MNT-02: Workflow templates follow documented conventions
NFR-MNT-03: Non-destructive state migrations with Git tag backup; completes within 30s
NFR-MNT-04: Core state operations 90%+ branch coverage; UI widgets 80%+ line coverage
NFR-MNT-05: Backwards compatibility: V1 artifacts render in V2 without migration
NFR-UX-01: Artifacts pass automated structural validation; prose quality via human review

### Additional Requirements

**From Architecture:**

- Three-process model: MadFrogApp (UI) + AI Agent (Toad) + MCP Server (stdio)
- 18 MCP tools across 5 categories: Project (6), Artifact (3), State (3), Workflow (3), Session (7)
- 7 infrastructure services: GitStateEngine, SQLiteCheckpointIndex, StateOperationQueue, AutoSaveService, SessionLockManager, VaultHealthMonitor, ArtifactValidator
- Single production dependency: batrachian-toad>=0.5.35,<0.7 (no click, no Pydantic)
- CLI uses argparse (stdlib), not click
- MCP server two-phase lifecycle: projectless mode -> project-active mode
- state.json atomic file sync between MCP server and UI via watchdog
- Prescribed project structure: ~40 files across src/mad_frog/{tools,services,ui}, tests
- Dev Container: Python 3.14, Node.js (for npx bmad init), uv package manager
- Spike verification required: ToadApp.CSS_PATH, agent wiring, acp_new_session
- Commit prefix registry: [checkpoint], [artifact], [session-auto], [context-save], [init], [bmad-update]
- 5 onboarding paths: Greenfield, Existing Git, Resume, Version mismatch, Brownfield
- 12 explicit anti-patterns forbidden (wildcard imports, bare except, os.path, etc.)
- @traced decorator mandatory on every function
- Constructor injection, no module-level mutable state
- Process boundary: no direct imports between ui/ and tools/services/ (different processes)
- SQLite index is ephemeral -- rebuilt from Git on every startup
- Two-tier state: Git (durable) + SQLite (reconstructable) + session (volatile)
- Architecture prescribes build sequence: Spike -> Week 1 (skeleton) -> Week 2 (persistence) -> Week 3 (polish)

**From UX Design:**

- 14 custom UI components to build (BMADJourneyMap, CeremonyBanner, ProjectCompletionSummary, ArtifactPanel, VaultStatusIndicator, ContentProgressIndicator, PartyModePanel, TopicLandmark, ProjectListItem, ErrorRecoveryPanel, DecisionCounter, WorkspaceSetupScreen, WelcomeScreen, HealthCheckPanel)
- ConversationEntry class hierarchy: 8 typed entry classes for RichLog
- 4 responsive width tiers (100+, 80-99, 60-79, <60 columns)
- Full keyboard shortcut table with Ctrl+B, Ctrl+S, Ctrl+H
- Reassurance-first error pattern: safe -> happened -> action
- Agent behavioral rules: one question per message, adaptive pacing, agency protection, substantive content boundary
- Party Mode: 8 colour slots, ~150 word soft limit, 2-3 agents per round
- Browser pre-flight HTML shim (WebSocket + viewport check)
- RichLog max_lines: 10,000 with pruning
- Topic landmark scroll-to linking from Journey Map
- DecisionCounter hidden until 5 decisions
- ContentProgressIndicator for artifact section tracking
- Triple encoding for all states (icon + colour + text)
- Width-aware agent messaging via LayoutState
- Integration tests at 120, 80, and 60 columns

### FR Coverage Map

| FR | Epic | Description |
|----|------|-------------|
| FR1 | 1 | Create new project |
| FR2 | 1 | Prevent duplicate names |
| FR3 | 1 | View project list |
| FR4 | 1 | Resume existing project |
| FR5 | 8 | Archive project |
| FR6 | 1 | Git-backed state record |
| FR7 | 1 | SQLite checkpoint index |
| FR8 | 3 | One active session |
| FR8a | 8 | Method version upgrade |
| FR8b | 8 | Existing Git repo onboarding |
| FR8c | 8 | Version mismatch handling |
| FR8d | 8 | Brownfield onboarding |
| FR9 | 2 | Sequential phase progression |
| FR10 | 2 | Phase unlock via validated artifacts |
| FR11 | 2 | Import existing artifacts |
| FR12 | 5 | Adaptive pacing |
| FR13 | 2 | Invoke BMAD workflows |
| FR14 | 2 | Phase completion Git commits |
| FR15 | 2 | Agent context loading on phase transition |
| FR16 | 5 | Help/explanation without losing progress |
| FR17 | 5 | Project status summary on demand |
| FR18 | 5 | Revisit previous answer in session |
| FR19 | 6 | Architecture decision records |
| FR20 | 6 | Generate epics from PRD |
| FR21 | 6 | Generate stories with acceptance criteria |
| FR22 | 6 | Traceability links |
| FR23 | 6 | Sprint plan generation |
| FR24 | 6 | Implementation phase MVP scope |
| FR25 | 4 | Visual Journey Map in sidebar |
| FR26 | 4 | Three visual states |
| FR27 | 4 | Dates and descriptions |
| FR28 | 4 | Click-back to completed nodes |
| FR29 | 4 | Confirmation modal for click-back |
| FR30 | 4 | Preserve downstream on Git branch |
| FR31 | 4 | Current position indicator |
| FR32 | 4 | Version history for completed nodes |
| FR33 | 4 | Manual checkpoint with label (Ctrl+S) |
| FR34 | 4 | Scrollable, collapsible sidebar |
| FR35 | 4 | Git branches invisible to user |
| FR36 | 4 | Local timezone display |
| FR37 | 1 | Bind mount persistence |
| FR38 | 3 | Full recovery after container rebuild |
| FR39 | 3 | Session context in Git metadata |
| FR40 | 3 | Context recall on resume |
| FR41 | 3 | Session lock with read-only fallback |
| FR42 | 1 | Atomic artifact write + commit |
| FR43 | 3 | Auto-save every 2 minutes |
| FR44 | 3 | State format migration |
| FR45 | 3 | Browser disconnect recovery |
| FR45a | 3 | Pre-emptive context save at 90% |
| FR46 | 1 | Obsidian-native markdown output |
| FR47 | 2 | Wikilinks between project artifacts |
| FR48 | 7 | Optimistic wikilinks to vault notes |
| FR49 | 1 | Workspace root via first-run modal |
| FR50 | 2 | Graph view with backlinks |
| FR51 | 1 | Obsidian-compatible frontmatter |
| FR52 | 2 | .obsidianignore proposals |
| FR53 | -- | Deferred (post-MVP) |
| FR54 | -- | Deferred (post-MVP) |
| FR55 | 2 | Artifact parent chain traceability |
| FR56 | 7 | Add markdown to project folder |
| FR57 | 7 | Agent ingests user-added files |
| FR58 | 7 | Agent references user files accurately |
| FR59 | 7 | Detect changes via bmad_detect_changes |
| FR60 | 7 | Git-track markdown, not binaries |
| FR61 | 7 | Invoke Party Mode anytime |
| FR62 | 7 | Load agent roster from manifest |
| FR63 | 7 | Select 2-3 relevant agents per round |
| FR64 | 7 | Distinct agent personalities |
| FR65 | 7 | Visual agent identity in Party Mode |
| FR66 | 7 | Agents build on each other |
| FR67 | 7 | Halt for user input on direct question |
| FR68 | 7 | Exit Party Mode with state preserved |
| FR69 | 1 | Toad manages credentials |
| FR70 | 1 | API key passthrough via devcontainer |
| FR71 | 1 | Toad manages LLM connections |
| FR72 | 1 | Launch via make start |
| FR73 | 1 | UI at localhost:8000 |
| FR74 | 1 | First-launch workspace setup modal |
| FR75 | 1 | Port forwarding in Dev Container |
| FR76 | 1 | Startup health checks |
| FR77 | 1 | Integrate with Toad session infra |
| FR78 | 2 | Phase completion feedback |
| FR79 | 5 | Project completion summary |
| FR80 | 2 | Narrative prose artifacts |
| FR81 | 5 | Agent access to all previous decisions |
| FR82 | 5 | Agent failure handling with retry |
| FR83 | 5 | Clear error messages with recovery |
| FR84 | 5 | Keyboard navigation |
| FR84a | 5 | Unwritten artifact detection |
| FR85 | -- | Deferred (post-MVP) |
| FR86 | 8 | Community workflow templates |
| FR87 | 8 | Runtime template discovery |
| FR88 | 5 | On-demand health check |

### NFR Allocation Map

| NFR | Primary Epic | Rationale |
|-----|-------------|-----------|
| NFR-PERF-01, PERF-10 | Epic 4 | Journey Map rendering targets |
| NFR-PERF-02 | Epic 1 | Artifact commit performance |
| NFR-PERF-03, PERF-04 | Epic 1 | Welcome screen + SQLite query perf |
| NFR-PERF-05, PERF-06, PERF-08 | Epic 1 | Cold start, warm restart, UI responsiveness |
| NFR-PERF-07, PERF-09, PERF-11 | Epic 5 | Long-session memory, disk footprint, large files |
| NFR-SEC-01 through SEC-04 | Epic 1 | Security from day one |
| NFR-REL-01, REL-02 | Epic 1 | Core data integrity (atomic operations) |
| NFR-REL-03, REL-04, REL-05, REL-06 | Epic 3 | Recovery and rebuild |
| NFR-REL-07 | Epic 3 | Concurrent session handling |
| NFR-REL-08 | Epic 5 | On-demand health check diagnostics |
| NFR-REL-09, REL-10 | Epic 3 | Network loss + chaos tests |
| NFR-ACC-01 through ACC-04 | Epic 5 | Accessibility sweep |
| NFR-INT-01 through INT-06 | Epic 2 | Obsidian + cross-platform validation |
| NFR-OBS-01, OBS-02 | Epic 1 | Logging framework from first story |
| NFR-MNT-01, MNT-03 | Epic 3 | State format versioning + migrations |
| NFR-MNT-02 | Epic 2 | Workflow template conventions |
| NFR-MNT-04 | Epic 3 | Test coverage enforcement |
| NFR-MNT-05 | Epic 3 | Backwards compatibility |
| NFR-UX-01 | Epic 2 | Artifact structural validation |

**Ship-blocking NFRs (must pass before release):** REL-01, REL-02, REL-06, REL-07, REL-10, PERF-01, PERF-06, SEC-01, SEC-02, INT-01 -- all allocated to Epics 1-4.

## Epic List

### Epic 1: Launch App & Create First Project
User can launch Mad Frog, set up their workspace, create a new project, list and resume existing projects, and see their first artifact committed to Git.
**FRs covered:** FR1, FR2, FR3, FR4, FR6, FR7, FR37, FR42, FR46, FR51, FR69, FR70, FR71, FR72, FR73, FR74, FR75, FR76, FR77
**Embedded NFRs:** PERF-02, PERF-03, PERF-04, PERF-05, PERF-06, PERF-08, SEC-01, SEC-02, SEC-03, SEC-04, REL-01, REL-02, OBS-01, OBS-02

### Epic 2: Guided Conversation & Phase Progression
User can progress through BMAD phases with agent guidance, produce validated Obsidian-compatible artifacts with wikilinks and frontmatter, and receive phase completion feedback.
**FRs covered:** FR9, FR10, FR11, FR13, FR14, FR15, FR47, FR49, FR50, FR52, FR55, FR78, FR80
**Embedded NFRs:** INT-01, INT-02, INT-03, INT-04, INT-05, INT-06, MNT-02, UX-01

### Epic 3: Session Persistence & Safe Recovery
User can close their browser, restart their container, or lose connection -- and resume exactly where they left off with full context recall and zero data loss.
**FRs covered:** FR8, FR38, FR39, FR40, FR41, FR43, FR44, FR45, FR45a
**Embedded NFRs:** REL-03, REL-04, REL-05, REL-06, REL-07, REL-09, REL-10, MNT-01, MNT-03, MNT-04, MNT-05

### Epic 4: Journey Map & Time Travel
User can visualize their project journey in a sidebar, navigate back to any completed checkpoint, view version history, and create manual save points -- all using temporal metaphors with no Git terminology.
**FRs covered:** FR25, FR26, FR27, FR28, FR29, FR30, FR31, FR32, FR33, FR34, FR35, FR36
**Embedded NFRs:** PERF-01, PERF-10

### Epic 5: Polished Workflow Experience
User gets adaptive conversational pacing, in-session help, answer revision, keyboard navigation, accessibility, graceful error handling, project completion summary, and on-demand diagnostics.
**FRs covered:** FR12, FR16, FR17, FR18, FR79, FR81, FR82, FR83, FR84, FR84a, FR88
**Embedded NFRs:** PERF-07, PERF-09, PERF-11, ACC-01, ACC-02, ACC-03, ACC-04, REL-08

### Epic 6: Solutioning & Implementation Planning
User can generate architecture decision records, epics from PRD requirements, stories with acceptance criteria, traceability links, and sprint plans -- completing the full planning lifecycle.
**FRs covered:** FR19, FR20, FR21, FR22, FR23, FR24

### Epic 7: Bidirectional Workspace & Party Mode
User can drop markdown files into their project for agent context, and invoke multi-agent Party Mode discussions with visually distinct agent identities for richer collaborative planning.
**FRs covered:** FR48, FR56, FR57, FR58, FR59, FR60, FR61, FR62, FR63, FR64, FR65, FR66, FR67, FR68

### Epic 8: Advanced Onboarding & Community Extensions
User can onboard existing Git repos, handle BMAD version mismatches, upgrade method versions, archive projects, and community members can contribute new workflow templates.
**FRs covered:** FR5, FR8a, FR8b, FR8c, FR8d, FR86, FR87


# BMAD Vibe Visualiser — Epic & Story Breakdown

## Epic 1: Launch App & Create First Project

**Goal:** Enable a user to launch the application for the first time, configure their workspace, create a new BMAD project, and produce their first planning artifact — establishing the foundational architecture (three-process model, Git-backed persistence, SQLite index) that all subsequent epics build upon.

### Story 1.1: Toad Integration Spike & Walking Skeleton

As a user, I want to launch the application and have all three processes (TUI, MCP server, agent) start and connect automatically, so that I have a working system without manual setup.

**Acceptance Criteria:**

**AC 1.1.1 — Dev Container & Project Skeleton**
- Given a fresh clone of the repository
- When I open the project in VS Code or GitHub Codespaces
- Then the Dev Container builds successfully with Python 3.14, Node.js, and uv available on PATH
- And `pyproject.toml` declares a single dependency on `batrachian-toad`
- And `Makefile` provides `make dev`, `make test`, and `make lint` targets
- And a CI workflow executes linting and tests on push

**AC 1.1.2 — Three-Process Launch**
- Given the Dev Container is running
- When I execute `mad_frog` via the argparse CLI entrypoint
- Then `MadFrogApp` (extending `ToadApp`) launches in the terminal using `ToadApp.CSS_PATH` for styling
- And the MCP server process starts on a local socket
- And the agent process connects to the MCP server within 3 seconds

**AC 1.1.3 — MCP Tool Discovery**
- Given all three processes are running
- When the agent issues a `tools/list` request to the MCP server
- Then the response includes at least the `bmad_ping` tool
- And the round-trip completes within 500ms

**AC 1.1.4 — ACP Session Initialization**
- Given the agent has connected to the MCP server
- When `acp_new_session` is called
- Then a session identifier is returned
- And the session is recorded in application state

**AC 1.1.5 — Dev Container Environment & Port Forwarding (FR70, FR73, FR75)**
- Given the Dev Container is running
- When I inspect the environment
- Then `ANTHROPIC_API_KEY` is forwarded from the host via `remoteEnv` in `devcontainer.json`
- And port 8000 is forwarded automatically for browser access
- And the application serves the UI at localhost:8000

**AC 1.1.6 — Launch via make start (FR72)**
- Given the Dev Container is running
- When I execute `make start`
- Then the `mad_frog` CLI entry point is invoked
- And the full application launches successfully

**AC 1.1.7 — Graceful Shutdown**
- Given all three processes are running
- When the user presses Ctrl+C or closes the terminal
- Then all three processes shut down within 2 seconds without orphaned subprocesses

---

### Story 1.2: Create Project & Write First Artifact

As a user, I want to create a new BMAD project in my chosen workspace directory and write my first planning artifact, so that I can begin the guided planning process with all work safely committed to Git.

**Acceptance Criteria:**

**AC 1.2.1 — First-Run Workspace Configuration**
- Given the application launches and no workspace path has been configured
- When `WorkspaceSetupScreen` is displayed as a modal
- Then I can browse to or type an absolute directory path
- And the path is validated to be writable and on a local filesystem (not a network mount)
- And the chosen path is persisted for future launches
- And the modal cannot be dismissed without selecting a valid path

**AC 1.2.2 — Welcome Screen with New Project Action**
- Given the workspace path is configured
- When `WelcomeScreen` renders
- Then a "Start new project" button is prominently displayed
- And the screen renders within 1 second of launch (PERF-02)

**AC 1.2.3 — Duplicate Project Name Prevention (FR2)**
- Given a project named "my-project" already exists
- When I attempt to create a new project with the name "my-project"
- Then the system rejects the name with a clear message explaining the conflict
- And I am guided to choose a unique name before proceeding

**AC 1.2.4 — Project Creation via bmad_create_project**
- Given I click "Start new project" and provide a project name
- When `bmad_create_project` is invoked
- Then a new directory is created under the workspace path
- And `git init` initializes a repository in that directory
- And `npx bmad init` scaffolds the BMAD method files into `_bmad/`
- And a branch-prefix namespace is established for this project (e.g., `project-name/main`)
- And a `ProjectRecord` is persisted in the SQLite index via `SQLiteCheckpointIndex`
- And `GitStateEngine` is initialized for the new repository

**AC 1.2.4 — First Artifact Write via bmad_write_artifact**
- Given a project has been created and the agent is in the Analysis phase
- When `bmad_write_artifact` is called with artifact content
- Then the artifact file is written atomically (write-to-temp then rename)
- And the file includes valid Obsidian frontmatter (title, type, date, phase)
- And YAML frontmatter passes validation against the expected schema
- And a Git commit is created with the artifact content
- And the commit message follows the convention `[artifact] <type>: <title>`

**AC 1.2.5 — Sensitive File Protection (SEC-01)**
- Given a project has been created
- When I inspect the project directory
- Then `.env` is listed in `.gitignore`
- And no files matching `*.secret`, `*.key`, or `credentials.*` are tracked by Git

**AC 1.2.6 — Crash Recovery of Partial Write (REL-01, REL-02)**
- Given an artifact write is in progress
- When the process is killed mid-write
- Then on next launch, no partial artifact file exists in the working tree
- And Git history contains only complete, valid commits

---

### Story 1.3: Project List, Resume & Switch

As a user, I want to see all my projects with their current status and resume any project where I left off, so that I can manage multiple planning efforts without losing progress.

**Acceptance Criteria:**

**AC 1.3.1 — Project List Display**
- Given I have created two or more projects
- When `WelcomeScreen` renders
- Then each project appears as a `ProjectListItem` showing project name, current phase, and last-active timestamp
- And projects are sorted by last-active descending
- And the list renders within 500ms for up to 50 projects (PERF-03)

**AC 1.3.2 — Project Resume via bmad_open_project**
- Given I select a project from the list
- When `bmad_open_project` is invoked
- Then the project's `state.json` is loaded into memory
- And `SQLiteCheckpointIndex` is rebuilt from Git history if the index file is missing or stale
- And a session lock is acquired for this project
- And the UI transitions to the project's current phase within 2 seconds (PERF-04)

**AC 1.3.3 — Project Listing via bmad_list_projects**
- Given multiple projects exist in the workspace
- When `bmad_list_projects` is called by the agent
- Then it returns a JSON array with each project's name, phase, last-active timestamp, and path

**AC 1.3.4 — Stale SQLite Index Rebuild**
- Given a project's SQLite index file has been deleted
- When `bmad_open_project` is invoked for that project
- Then the index is rebuilt from Git commit history
- And the rebuilt index produces identical query results to the original

---

### Story 1.4: Startup Health Checks & Observability

As a user, I want the application to verify its own integrity on startup and provide clear diagnostics when something is wrong, so that I can trust my data is safe and get actionable guidance if recovery is needed.

**Acceptance Criteria:**

**AC 1.4.1 — Health Check Execution via bmad_health_check**
- Given the application is starting up
- When `bmad_health_check` is invoked
- Then it runs `git fsck` on the project repository and reports any corruption
- And it verifies the bind mount (workspace directory) is accessible and writable
- And it validates SQLite index consistency against Git history
- And all checks complete within 5 seconds (PERF-05)

**AC 1.4.2 — Structured JSON Logging (OBS-01, OBS-02)**
- Given the application is running
- When any tool is invoked or any error occurs
- Then a structured JSON log entry is written with timestamp, level, component, operation, and duration
- And the `@traced` decorator is applied to all MCP tool handlers, recording entry, exit, and elapsed time
- And log output is directed to a rotating file (not stdout, which is reserved for TUI rendering)

**AC 1.4.3 — Gitignore Verification (SEC-02, SEC-03, SEC-04)**
- Given a project repository exists
- When startup validation runs
- Then it confirms `.env` is in `.gitignore`
- And it warns if any file matching sensitive patterns (`*.key`, `*.secret`, `credentials.*`) is tracked
- And the warning includes specific remediation steps

**AC 1.4.4 — Startup Failure Recovery Guidance**
- Given a health check detects a problem (e.g., corrupt Git repo, inaccessible workspace)
- When the results are displayed to the user
- Then a clear, jargon-free message describes what is wrong
- And specific recovery steps are provided (e.g., "Run `git fsck --full` to repair" or "Check that your workspace folder exists")
- And the application does not proceed to the main UI until critical checks pass

**AC 1.4.5 — Performance Budget Compliance (PERF-06, PERF-08)**
- Given the application is launching
- When startup completes (including health checks)
- Then total cold-start time is under 8 seconds
- And memory usage at idle does not exceed 150MB

---

## Epic 2: Guided Conversation & Phase Progression

**Goal:** Enable the agent to guide the user through the BMAD methodology phases (Analysis, Planning, Solutioning, Implementation) in a structured, sequential conversation — with each phase producing validated artifacts, proper checkpoint commits, and Obsidian-compatible output that forms a navigable knowledge graph.

### Story 2.1: Workflow State & Phase Advancement

As a user, I want the system to guide me through planning phases in the correct order, so that I follow the BMAD methodology without skipping critical steps.

**Acceptance Criteria:**

**AC 2.1.1 — Sequential Phase Enforcement**
- Given a project is in the Analysis phase
- When the agent or user attempts to advance to Solutioning (skipping Planning)
- Then the system rejects the advancement with a message explaining which phase must be completed first
- And the project remains in the Analysis phase

**AC 2.1.2 — Phase Advancement via bmad_advance_workflow**
- Given all required artifacts for the current phase are complete
- When `bmad_advance_workflow` is called with the next phase identifier
- Then the project's workflow state transitions to the new phase
- And `state.json` is updated atomically
- And a Git commit records the phase transition with message `[workflow] advance to <phase>`

**AC 2.1.3 — Workflow State Query via bmad_get_workflow_state**
- Given a project is open
- When `bmad_get_workflow_state` is called
- Then it returns the current phase, completed phases, required artifacts for the current phase, and completion status of each

**AC 2.1.4 — Step Prompt Retrieval via bmad_get_step_prompt**
- Given the agent needs to guide the user through a specific step
- When `bmad_get_step_prompt` is called with a step identifier
- Then it returns the prompt template with all template variables resolved (project name, existing artifact references, current phase context)
- And the resolved prompt is valid CommonMark (INT-01)

**AC 2.1.5 — Phase Sequence Definition**
- Given the BMAD methodology
- When the workflow engine is initialized
- Then it enforces the sequence: Analysis → Planning → Solutioning → Implementation
- And each phase defines its required artifact types

---

### Story 2.2: Phase Completion with Structured Commits

As a user, I want clear feedback when I complete a planning phase with all my progress safely checkpointed, so that I know my work is saved and I can confidently move forward.

**Acceptance Criteria:**

**AC 2.2.1 — Checkpoint Creation via bmad_checkpoint**
- Given a phase's required artifacts are all written
- When `bmad_checkpoint` is called
- Then a Git commit is created with the prefix `[checkpoint]` in the commit message
- And the commit metadata includes structured JSON: `summary`, `decisions` (list), and `next_topic`
- And the checkpoint is recorded in `state.json` under `checkpoint_history`

**AC 2.2.2 — Ceremony Banner Display**
- Given a phase checkpoint commit succeeds
- When the UI receives the checkpoint confirmation
- Then a `CeremonyBanner` component renders at the top of the conversation area
- And it displays the completed phase name, a brief summary, and a "Continue to next phase" prompt
- And it auto-dismisses after 10 seconds or on user interaction

**AC 2.2.3 — Checkpoint Idempotency**
- Given a checkpoint has already been created for the current phase
- When `bmad_checkpoint` is called again without new changes
- Then no duplicate commit is created
- And the tool returns a message indicating the checkpoint already exists

---

### Story 2.3: Wikilink Generation & Obsidian Graph View

As a user, I want my planning artifacts to be interconnected with wikilinks so that I can navigate between related documents in Obsidian's graph view and understand how decisions flow through the project.

**Acceptance Criteria:**

**AC 2.3.1 — Automatic Wikilink Insertion**
- Given `bmad_write_artifact` is writing an artifact that references another artifact (e.g., a PRD referencing the Project Brief)
- When the artifact content is finalized
- Then references to other artifacts are rendered as Obsidian wikilinks (`[[Artifact Name]]`)
- And the wikilink target matches the exact filename (without extension) of the referenced artifact

**AC 2.3.2 — Parent Chain Traceability**
- Given an artifact has a parent artifact (e.g., Epic → PRD → Brief)
- When the artifact's frontmatter is written
- Then it includes a `parent` field with a wikilink to the parent artifact
- And the full chain is navigable: any artifact can be traced back to the Project Brief

**AC 2.3.3 — CommonMark Compliance (INT-01, INT-03)**
- Given any artifact written by `bmad_write_artifact`
- When the content is parsed by a CommonMark parser
- Then it produces zero parsing errors
- And the output is narrative prose (not raw data dumps or bullet-only content)

**AC 2.3.4 — Obsidian Graph View Compatibility**
- Given a project with 5+ interconnected artifacts
- When opened in Obsidian
- Then the graph view renders all artifacts as nodes
- And edges correctly reflect the wikilink relationships between artifacts

**AC 2.3.5 — UX Writing Standards (UX-01)**
- Given any artifact content generated by the agent
- When reviewed
- Then it uses narrative prose with section headings
- And technical jargon is explained on first use
- And content is structured for scannability (short paragraphs, clear hierarchy)

---

### Story 2.4: Vault Detection & Setup

As a user, I want the system to detect my existing Obsidian vault configuration and integrate seamlessly, so that BMAD projects appear in my knowledge management workflow without manual setup.

**Acceptance Criteria:**

**AC 2.4.1 — Vault Detection via VaultHealthMonitor**
- Given the workspace path is configured
- When `VaultHealthMonitor` runs on project open
- Then it walks parent directories looking for `.obsidian/` to detect if the workspace is inside an Obsidian vault
- And if found, the vault root path is stored in project configuration

**AC 2.4.2 — Obsidianignore Proposal (INT-04, INT-05, INT-06)**
- Given the project is inside an Obsidian vault
- When the vault does not have a `.obsidianignore` that excludes BMAD internal files
- Then the system proposes adding entries to `.obsidianignore` for `_bmad/` internal directories (not output artifacts)
- And the proposal is shown to the user for approval before any file is modified

**AC 2.4.3 — Workspace Root from First-Run Modal (INT-02)**
- Given the `WorkspaceSetupScreen` modal is displayed
- When the user selects a workspace path
- Then the system checks if the path is within an Obsidian vault
- And displays the detected vault root (if any) for confirmation

**AC 2.4.4 — Vault Status Indicator**
- Given a project is open
- When the footer bar renders
- Then a `VaultStatusIndicator` component shows whether the project is inside an Obsidian vault
- And displays a green indicator if vault integration is active, or a grey indicator if standalone

---

### Story 2.5: Artifact Import & Phase Unlock

As a user, I want to import existing planning artifacts into my project so that I do not have to redo work I have already completed outside the tool.

**Acceptance Criteria:**

**AC 2.5.1 — Artifact Import**
- Given I have a markdown file with valid BMAD frontmatter outside the project
- When I place the file in the project's artifact directory and the agent detects it
- Then the system ingests the file and validates it against the expected schema for its artifact type via `ArtifactValidator`

**AC 2.5.2 — Phase Completion via Import**
- Given all required artifacts for a phase have been imported and pass validation
- When the agent evaluates phase completeness
- Then the phase is marked as complete
- And the user is offered advancement to the next phase via `bmad_advance_workflow`

**AC 2.5.3 — Incomplete Import Feedback (MNT-02)**
- Given an imported artifact fails validation (missing required sections, invalid frontmatter)
- When the validation result is returned
- Then the agent identifies the specific validation errors
- And provides guidance on what sections or fields need to be added or corrected

**AC 2.5.4 — Import Does Not Overwrite**
- Given an artifact with the same name already exists in the project
- When an import is attempted
- Then the system rejects the import with a clear message
- And the existing artifact remains unchanged

---

## Epic 3: Session Persistence & Safe Recovery

**Goal:** Ensure that no user work is ever lost — whether the container is destroyed, the browser disconnects, the disk fills up, or the application crashes mid-operation — by leveraging Git as the authoritative store and providing transparent, automatic recovery.

### Story 3.1: Auto-Save & State Operation Queue

As a user, I want my work to be automatically saved at regular intervals without interrupting my conversation, so that I never lose more than two minutes of progress.

**Acceptance Criteria:**

**AC 3.1.1 — Auto-Save Timer**
- Given a project is open and changes have been made since the last save
- When 2 minutes elapse without a manual save or checkpoint
- Then `AutoSaveService` creates a Git commit with the prefix `[session-auto]`
- And the commit includes all modified tracked files

**AC 3.1.2 — State Operation Queue Priority**
- Given an auto-save is pending and an intentional operation (`bmad_write_artifact`, `bmad_checkpoint`) is triggered
- When both operations compete for Git access
- Then `StateOperationQueue` (backed by `asyncio.PriorityQueue`) executes the intentional operation first
- And the auto-save is deferred until the intentional operation completes

**AC 3.1.3 — Atomic State File Sync (REL-03)**
- Given `state.json` needs to be updated
- When `StateFileWriter` performs the write
- Then it writes to a temporary file in the same directory first
- And renames the temporary file to `state.json` atomically
- And a partial `state.json` file is never visible to any reader

**AC 3.1.4 — Auto-Save Does Not Interrupt UX**
- Given the user is mid-conversation with the agent
- When an auto-save triggers
- Then no modal, banner, or notification is displayed
- And the conversation flow is uninterrupted

---

### Story 3.2: Session Lock Manager

As a user, I want only one active session per project at a time, so that concurrent edits cannot corrupt my project state.

**Acceptance Criteria:**

**AC 3.2.1 — Lock Acquisition**
- Given I open a project
- When `SessionLockManager` acquires the lock
- Then a lock file is created in the project directory containing the current PID and timestamp
- And the lock is held for the duration of the session

**AC 3.2.2 — Stale Lock Detection**
- Given a lock file exists but the PID recorded in it is no longer running
- When a new session attempts to open the project
- Then `SessionLockManager` detects the stale lock
- And automatically removes it
- And acquires a fresh lock for the new session

**AC 3.2.3 — Active Lock Conflict (REL-07)**
- Given a lock file exists and the owning PID is still running
- When a second tab or instance attempts to open the same project
- Then the user is presented with two options: open in read-only mode or take over the session
- And if takeover is chosen, the original session is notified and gracefully releases the lock

**AC 3.2.4 — Lock Release on Exit**
- Given a session is active with a lock held
- When the application exits (normally or via signal)
- Then the lock file is removed
- And no orphaned lock file remains

---

### Story 3.3: Container Recovery & State Rebuild

As a user, I want to resume my work exactly where I left off after my Dev Container is destroyed and rebuilt, so that container ephemerality does not threaten my project data.

**Acceptance Criteria:**

**AC 3.3.1 — Full State Recovery from Git (REL-04)**
- Given a container has been destroyed and a new container is created
- When I launch the application and open an existing project (whose Git repo is on a persistent volume)
- Then the application reconstructs all project state from Git history
- And `state.json` is regenerated from commit metadata
- And the project opens in the correct phase with all artifacts present

**AC 3.3.2 — SQLite Byte-Identical Rebuild**
- Given the SQLite index file has been lost (container destruction)
- When `SQLiteCheckpointIndex` rebuilds from Git history
- Then the rebuilt index produces query results identical to the original
- And all checkpoint history, artifact metadata, and phase records are present

**AC 3.3.3 — Incomplete Git Operation Detection (MNT-04)**
- Given a Git operation (commit, merge) was interrupted by container kill
- When the application starts and detects an incomplete operation (e.g., `.git/MERGE_HEAD` exists, index.lock present)
- Then it resolves the incomplete operation automatically (abort the partial merge, remove stale locks)
- And logs the recovery action taken
- And the repository is left in a consistent state

---

### Story 3.4: Context Recall on Resume

As a user, I want the agent to remember what we were discussing when I return to a project, so that I do not have to re-explain my context.

**Acceptance Criteria:**

**AC 3.4.1 — Session Context in Git Metadata**
- Given a session auto-save or checkpoint is created
- When the Git commit is written
- Then the commit message trailer includes structured context: `Last-Topic`, `Pending-Decisions`, and `Next-Steps` fields

**AC 3.4.2 — Context-Aware Greeting on Resume**
- Given I reopen a project after closing it
- When the agent initializes the conversation
- Then it greets me with a summary of: what we were last discussing, any pending decisions awaiting my input, and suggested next steps
- And the greeting references specific artifact names and decision points

**AC 3.4.3 — Session Info Tool**
- Given the agent needs to reconstruct context
- When `bmad_session_info` is called
- Then it returns the last checkpoint summary, list of pending decisions, current phase and step, and last 3 commit messages with their structured metadata

---

### Story 3.5: Browser Disconnect & Network Loss Recovery

As a user, I want the application to handle browser disconnects and network interruptions gracefully, so that I do not lose my conversation or project state.

**Acceptance Criteria:**

**AC 3.5.1 — Graceful Disconnect Handling (REL-05)**
- Given the browser tab is closed or the WebSocket connection drops
- When the server-side process detects the disconnection
- Then it triggers an immediate auto-save with prefix `[disconnect-save]`
- And the agent process is paused (not terminated)
- And the session lock is retained for 5 minutes

**AC 3.5.2 — Reconnect to Last Stable State**
- Given a browser disconnect occurred within the last 5 minutes
- When I reopen the application and navigate to the project
- Then the session resumes from the last saved state
- And the conversation history is restored
- And no duplicate messages appear

**AC 3.5.3 — Network Loss User Feedback (REL-09)**
- Given the network connection is lost while the application is open
- When the TUI detects the loss (WebSocket heartbeat failure)
- Then a non-blocking banner displays "Connection lost — your work is saved locally"
- And when connectivity is restored, the banner updates to "Reconnected" and auto-dismisses

---

### Story 3.6: Pre-emptive Context Save

As a user, I want the system to automatically save context before the agent's memory fills up, so that conversation continuity is preserved without me needing to manage it.

**Acceptance Criteria:**

**AC 3.6.1 — Context Budget Query**
- Given the agent is in an active conversation
- When `bmad_report_context` is called
- Then it returns the current context usage as a percentage of the total budget

**AC 3.6.2 — Automatic Context Save at 90%**
- Given context usage reaches 90% of the budget
- When the threshold is crossed
- Then a `[context-save]` Git commit is created containing conversation state and key decisions
- And the save occurs silently without user notification or interruption
- And the agent can reconstruct essential context from the saved commit on next session

**AC 3.6.3 — Context Save Content**
- Given a `[context-save]` commit is created
- When its contents are inspected
- Then it includes: current topic summary, all decisions made in this session, pending questions, and artifact references
- And this data is sufficient for the agent to provide a coherent greeting on resume

---

### Story 3.7: State Format Migration

As a user, I want the system to automatically upgrade my project data format when a new version is released, so that I can update the application without losing or corrupting my projects.

**Acceptance Criteria:**

**AC 3.7.1 — Version Identifier in State (MNT-01)**
- Given any `state.json` file
- When it is written or read
- Then it contains a `format_version` field (e.g., `"1"`, `"2"`)
- And the application checks this field on every project open

**AC 3.7.2 — Automated Migration (MNT-03)**
- Given a project's `state.json` has `format_version: "1"` and the application expects version `"2"`
- When the project is opened
- Then the migration runs automatically without user action
- And a Git tag `pre-migration-v1` is created before any changes are made
- And `state.json` is updated to `format_version: "2"` with all fields correctly transformed

**AC 3.7.3 — Non-Destructive Migration (MNT-05)**
- Given a migration has been applied
- When the pre-migration Git tag is checked out
- Then the original state is fully intact and the project can be opened by a V1-compatible application

**AC 3.7.4 — Backwards Compatibility**
- Given a V2 application reads a V1 state file
- When the V1 content renders
- Then all V1 fields are displayed correctly (no data loss or corruption)
- And a migration prompt is offered but not forced

---

### Story 3.8: Chaos Test Suite

As a user, I want confidence that the system recovers correctly from any failure scenario, so that I can trust it with my planning work.

**Acceptance Criteria:**

**AC 3.8.1 — Container Kill During Git Commit**
- Given an artifact write is creating a Git commit
- When the container is killed via `SIGKILL` mid-commit
- Then on restart, the system detects the incomplete commit (index.lock or partial objects)
- And resolves to the last consistent state
- And no data corruption is present

**AC 3.8.2 — Container Kill During SQLite Write**
- Given the SQLite index is being updated
- When the container is killed via `SIGKILL` mid-write
- Then on restart, the index is rebuilt from Git history
- And all data is consistent

**AC 3.8.3 — Container Kill During Artifact Write**
- Given `bmad_write_artifact` is performing an atomic write (temp file exists, rename not yet done)
- When the container is killed
- Then on restart, the temporary file is cleaned up
- And the artifact either fully exists (rename completed) or does not exist at all (rename did not occur)

**AC 3.8.4 — Browser Disconnect During Agent Response**
- Given the agent is mid-response streaming to the TUI
- When the browser/terminal disconnects
- Then the server-side auto-save captures all state up to the disconnection point
- And on reconnect, no partial agent response is displayed as if it were complete

**AC 3.8.5 — Disk Full Scenario (REL-10)**
- Given the filesystem has less than 1MB free
- When any write operation is attempted
- Then the operation fails with a clear error message: "Disk space critically low — free space to continue"
- And no partial files or corrupt state remain
- And previously saved data is intact

---

## Epic 4: Journey Map & Time Travel

**Goal:** Provide a visual, non-technical representation of project progress that allows users to navigate backwards through their planning history — viewing, branching, and restoring previous states — without ever exposing Git concepts.

### Story 4.1: Journey Map Sidebar Widget

As a user, I want to see a visual map of my project journey in the sidebar, so that I always know where I am in the planning process and what I have completed.

**Acceptance Criteria:**

**AC 4.1.1 — Journey Map Component**
- Given a project is open
- When the sidebar renders
- Then a `BMADJourneyMap` widget (extending Textual `Tree`) is displayed
- And it reads `checkpoint_history` from `state.json` to populate nodes

**AC 4.1.2 — Triple Encoding for Visual States**
- Given checkpoint nodes exist in various states
- When the Journey Map renders each node
- Then completed nodes show a check icon, green colour, and "(done)" text suffix
- And the in-progress node shows an arrow icon, amber colour, and "(current)" text suffix
- And locked/future nodes show a lock icon, grey colour, and "(locked)" text suffix
- And all three encoding channels (icon, colour, text) are always present simultaneously

**AC 4.1.3 — Current Position Indicator**
- Given the user is working on the Planning phase
- When the Journey Map renders
- Then the Planning node is visually highlighted as the current position
- And the map auto-scrolls to keep the current node visible

**AC 4.1.4 — Scrollable and Collapsible**
- Given a project has 20+ checkpoints
- When the Journey Map renders
- Then the widget is scrollable via keyboard and mouse
- And phase groups can be collapsed/expanded

**AC 4.1.5 — Render Performance (PERF-01)**
- Given a project with 50 checkpoints
- When the Journey Map renders
- Then it completes rendering within 200ms
- And scrolling is smooth with no visible lag

---

### Story 4.2: Temporal Labels & Local Timezone

As a user, I want journey map nodes to show human-readable dates and descriptions instead of technical identifiers, so that my project timeline is intuitive to read.

**Acceptance Criteria:**

**AC 4.2.1 — Human-Readable Labels**
- Given checkpoint nodes in the Journey Map
- When they render
- Then each node displays a human-readable description (e.g., "Completed Project Brief", "Started Technical Architecture")
- And no Git terminology (commit, hash, SHA, branch) is visible anywhere in the Journey Map

**AC 4.2.2 — Local Timezone Display**
- Given the user's system timezone is set (e.g., America/New_York)
- When dates are displayed on Journey Map nodes
- Then all timestamps are shown in the user's local timezone
- And the format is human-friendly (e.g., "Mar 10, 2:30 PM" not "2026-03-10T19:30:00Z")

**AC 4.2.3 — Label Abbreviation at Narrow Widths**
- Given the sidebar is resized to a narrow width (< 30 characters)
- When Journey Map labels would overflow
- Then labels are intelligently abbreviated (e.g., "Completed Project Brief" → "Project Brief ✓")
- And no horizontal scrollbar appears

---

### Story 4.3: Click-Back Navigation with Confirmation

As a user, I want to click on a completed step in my journey map to review what I had at that point, so that I can revisit past decisions and potentially make different choices.

**Acceptance Criteria:**

**AC 4.3.1 — Click-Back on Completed Node**
- Given a completed node in the Journey Map
- When I click on it
- Then a confirmation modal appears explaining: "This will show your project as it was at this point. You can create a new version from here."
- And the modal has "Continue" and "Cancel" buttons

**AC 4.3.2 — Navigation to Historical State**
- Given I confirm the click-back navigation
- When the historical state loads
- Then all artifacts display their content as of that checkpoint
- And the Journey Map updates to show the selected node as the current position
- And content displays within 2 seconds of confirmation (PERF-10)

**AC 4.3.3 — Cancel Preserves Current State**
- Given the confirmation modal is displayed
- When I click "Cancel"
- Then the modal dismisses
- And my current position and all state remain unchanged

---

### Story 4.4: Version Preservation on Click-Back

As a user, I want the system to keep all my downstream work safe when I go back to an earlier point and make changes, so that I never lose anything I have already done.

**Acceptance Criteria:**

**AC 4.4.1 — Downstream Work Preserved**
- Given I navigate back to a completed checkpoint and begin making new changes
- When the system creates a new version from that point
- Then all work that was downstream of the click-back point is preserved on a separate Git branch
- And the branch management is entirely invisible to the user (no branch names, no merge prompts)

**AC 4.4.2 — Temporal Metaphors Only**
- Given the user interacts with any version or branching feature
- When any UI text, modal, or agent message references this functionality
- Then only temporal metaphors are used (e.g., "version", "timeline", "earlier point", "new path")
- And no Git terminology appears (no "branch", "checkout", "merge", "rebase")

**AC 4.4.3 — Return to Latest**
- Given I navigated back and then want to return to my most recent work
- When I click the most recent node in the Journey Map
- Then I return to the latest state with all recent work intact
- And no confirmation modal is needed (returning to latest is non-destructive)

---

### Story 4.5: Version History for Completed Nodes

As a user, I want to see all versions of a completed step so that I can choose which version to review or branch from.

**Acceptance Criteria:**

**AC 4.5.1 — Version List Display**
- Given a completed node in the Journey Map that has multiple versions (from click-back branching)
- When I right-click or long-press on the node
- Then a version list appears showing each version with its timestamp and summary
- And versions are ordered chronologically (newest first)

**AC 4.5.2 — Version Selection**
- Given the version list is displayed
- When I select a specific version
- Then the confirmation modal from Story 4.3 appears
- And on confirmation, the project navigates to that specific version's state

**AC 4.5.3 — Single Version Node**
- Given a completed node with only one version
- When I right-click or long-press on it
- Then the version list shows a single entry
- And the interaction is consistent with multi-version nodes

---

### Story 4.6: Manual Checkpoints

As a user, I want to create a manual checkpoint with a custom label at any time, so that I can mark important moments in my planning process.

**Acceptance Criteria:**

**AC 4.6.1 — Manual Checkpoint via Ctrl+S**
- Given a project is open with unsaved changes
- When I press Ctrl+S
- Then a small input field appears prompting for an optional label (e.g., "Before big pivot")
- And on submit (Enter), a `[checkpoint]` Git commit is created with the custom label in the summary
- And on dismiss (Escape), no checkpoint is created

**AC 4.6.2 — Topic Landmark in Conversation**
- Given a manual checkpoint is created
- When the conversation view renders
- Then a `TopicLandmark` component appears inline in the conversation at the point the checkpoint was created
- And it displays the custom label and timestamp
- And it serves as a visual separator in the conversation history

**AC 4.6.3 — Journey Map Update**
- Given a manual checkpoint is created
- When the Journey Map refreshes
- Then the new checkpoint appears as a node within the current phase
- And it displays the custom label instead of an auto-generated description

---

## Epic 5: Polished Workflow Experience

**Goal:** Elevate the user experience from functional to delightful — with adaptive agent communication, comprehensive accessibility, robust error handling, and thoughtful quality-of-life features that make the planning process feel effortless.

### Story 5.1: Adaptive Pacing & Agent Communication

As a user, I want the agent to match my communication style and never overwhelm me with too many questions at once, so that the planning conversation feels natural and respectful of my time.

**Acceptance Criteria:**

**AC 5.1.1 — One Question Per Message**
- Given the agent needs to gather information from me
- When it sends a message
- Then it asks at most one question per message
- And any additional questions are queued for subsequent turns

**AC 5.1.2 — Verbose User Adaptation**
- Given I consistently provide detailed, multi-paragraph responses
- When the agent responds
- Then it shifts to more targeted, specific follow-up questions
- And reduces explanatory preamble

**AC 5.1.3 — Terse User Adaptation**
- Given I consistently provide short, minimal responses
- When the agent responds
- Then it provides more structured prompts with concrete options (e.g., "Would you prefer A, B, or C?")
- And includes brief context to help me answer

**AC 5.1.4 — Unsure User Adaptation**
- Given I express uncertainty (e.g., "I'm not sure", "maybe", "I don't know")
- When the agent responds
- Then it offers 2-3 concrete options with brief explanations of trade-offs
- And reassures that the choice can be revisited later

**AC 5.1.5 — Agency Protection**
- Given the user has confirmed a decision
- When the agent processes the confirmation
- Then it does not ask for re-confirmation more than once (maximum 2 total confirmations per decision)
- And substantive content is provided in every message (no empty acknowledgments)

---

### Story 5.2: In-Session Help & Project Status

As a user, I want to ask for help or check my project status at any time without derailing the current conversation, so that I always feel oriented and supported.

**Acceptance Criteria:**

**AC 5.2.1 — Help Without Context Loss**
- Given I am mid-conversation about a specific artifact
- When I ask "What can I do?" or "Help"
- Then the agent provides a brief overview of available actions relevant to my current phase
- And after the help response, the agent returns to the previous topic without requiring me to re-state it

**AC 5.2.2 — Project Status Summary**
- Given I ask "What's my project status?" or similar
- When the agent responds
- Then it provides: current phase, percentage of phase completion, list of completed artifacts, currently in-progress artifact, and suggested next steps
- And the status is accurate to the current `state.json`

---

### Story 5.3: In-Session Answer Revision

As a user, I want to go back and change an answer I gave earlier in the current session, so that I can correct mistakes without starting over.

**Acceptance Criteria:**

**AC 5.3.1 — Revision Request**
- Given I previously answered a question about the project brief
- When I say "Actually, I want to change my answer about the target audience"
- Then the agent acknowledges the revision request
- And re-asks the specific question with my previous answer shown for reference

**AC 5.3.2 — Artifact Update After Revision**
- Given I provide a revised answer
- When the agent processes the revision
- Then any affected artifacts are updated with the new information via `bmad_write_artifact`
- And a new Git commit records the change with message `[revision] <artifact>: <summary>`

**AC 5.3.3 — Cascading Revision Notification**
- Given the revised answer affects downstream artifacts
- When the revision is applied
- Then the agent identifies which other artifacts may be affected
- And offers to update them as well (but does not force the update)

---

### Story 5.4: Decision Context Access

As a user, I want the agent to always have access to my previous decisions when generating responses, so that it never contradicts or forgets what I have already decided.

**Acceptance Criteria:**

**AC 5.4.1 — Decision History Available to Agent**
- Given decisions have been made and recorded in artifacts and checkpoint metadata
- When the agent generates a new response
- Then it has access to all previous decisions and constraints
- And it does not suggest options that conflict with established decisions

**AC 5.4.2 — Decision Reference on Conflict**
- Given a new user request conflicts with a previous decision
- When the agent detects the conflict
- Then it cites the specific previous decision (including which artifact and when)
- And asks whether the user wants to revise the earlier decision or adjust the new request

---

### Story 5.5: Error Handling & Agent Failure Recovery

As a user, I want clear, reassuring error messages when something goes wrong, so that I know my data is safe and what I can do to continue.

**Acceptance Criteria:**

**AC 5.5.1 — Reassurance-First Error Pattern**
- Given any error occurs (tool failure, Git error, agent timeout)
- When the `ErrorRecoveryPanel` renders
- Then the first line confirms data safety (e.g., "Your work is saved.")
- And the second line explains what happened in plain language
- And the third line provides a specific action (e.g., "Click Retry or press R to try again")

**AC 5.5.2 — Agent Response Failure**
- Given the agent fails to respond within 30 seconds
- When the timeout is detected
- Then the `ErrorRecoveryPanel` displays with a "Retry" button
- And clicking Retry resends the last user message
- And the conversation history remains intact

**AC 5.5.3 — Accessibility of Error Messages (ACC-04)**
- Given an error panel is displayed
- When a screen reader encounters it
- Then the error is announced with role="alert"
- And all recovery actions are keyboard-accessible

---

### Story 5.6: Keyboard Navigation & Accessibility

As a user, I want to navigate the entire application using only my keyboard and have all visual information conveyed through accessible means, so that the tool is usable regardless of my abilities or preferences.

**Acceptance Criteria:**

**AC 5.6.1 — Keyboard Shortcuts**
- Given the application is running
- When I press Ctrl+B
- Then the sidebar toggles open/closed
- And when I press Tab, focus moves through interactive elements in logical order
- And when I press Escape, the current modal or panel dismisses

**AC 5.6.2 — Contrast Compliance (ACC-01, ACC-02)**
- Given any text element in the application
- When its contrast ratio is measured against its background
- Then it meets WCAG AA minimum of 4.5:1 for normal text and 3:1 for large text

**AC 5.6.3 — Triple Encoding for All States (ACC-03)**
- Given any state indicator in the application (phase status, vault status, health status)
- When it renders
- Then it uses at least three encoding channels: icon/shape, colour, and text label
- And no information is conveyed by colour alone

**AC 5.6.4 — No Icon-Only Controls**
- Given any interactive control in the application
- When it renders
- Then it has a visible text label or an aria-label equivalent
- And icon-only buttons are never the sole means of interaction

---

### Story 5.7: Unwritten Artifact Detection

As a user, I want the system to notice when the agent produces artifact-like content in conversation that has not been saved, so that important structured output is never lost in chat history.

**Acceptance Criteria:**

**AC 5.7.1 — Artifact Content Detection**
- Given the agent sends a message containing structured markdown with YAML frontmatter (matching BMAD artifact patterns)
- When the message is rendered in the conversation
- Then the system detects the artifact-like content
- And displays a prompt: "This looks like an artifact. Would you like to save it?"

**AC 5.7.2 — Save Prompt Action**
- Given the save prompt is displayed
- When I click "Save" or press Enter
- Then `bmad_write_artifact` is invoked with the detected content
- And the artifact is committed to Git
- And the save prompt is replaced with a confirmation: "Saved as <filename>"

**AC 5.7.3 — Dismiss Prompt**
- Given the save prompt is displayed
- When I click "Dismiss" or press Escape
- Then the prompt disappears
- And the content remains in conversation history but is not saved as an artifact
- And the same content does not trigger another prompt

---

### Story 5.8: Project Completion Summary

As a user, I want a comprehensive summary when my project planning is complete, so that I can see everything I have accomplished and have a clear overview of the project.

**Acceptance Criteria:**

**AC 5.8.1 — Completion Summary Display**
- Given all four phases (Analysis, Planning, Solutioning, Implementation) are complete
- When the final checkpoint is created
- Then a `ProjectCompletionSummary` component renders showing: total artifact count, list of all artifacts grouped by phase, total decisions made, and phase-by-phase summary

**AC 5.8.2 — Project Graph Link**
- Given the project is inside an Obsidian vault
- When the completion summary renders
- Then it includes a link/instruction to open the project graph in Obsidian
- And the graph accurately represents all artifact relationships

**AC 5.8.3 — Completion Summary Persistence**
- Given the completion summary is displayed
- When I close and reopen the project
- Then the completion summary is accessible from the project view
- And it is also saved as an artifact (`project-summary.md`) in the project directory

---

### Story 5.9: On-Demand Health Check

As a user, I want to run a system health check at any time to verify the integrity of my project data, so that I have confidence in the system and can catch issues early.

**Acceptance Criteria:**

**AC 5.9.1 — Health Check Trigger**
- Given a project is open
- When I click the health check button in the sidebar or press Ctrl+H
- Then a `HealthCheckPanel` modal opens and begins running diagnostics

**AC 5.9.2 — Diagnostic Results (PERF-07, PERF-09)**
- Given the health check is running
- When it completes (within 5 seconds)
- Then it displays: checkpoint count and integrity status, artifact count and validation results, Git repository status, SQLite index consistency, and any orphaned files (temp files, partial writes)
- And each item shows a pass/fail indicator with details on failures

**AC 5.9.3 — Health Check Non-Destructive (PERF-11, REL-08)**
- Given the health check is running
- When it accesses project data
- Then it performs read-only operations (no modifications to any file, Git ref, or SQLite table)
- And the project remains fully usable during and after the check

---

## Epic 6: Solutioning & Implementation Planning

**Goal:** Enable the agent to guide users through the Solutioning and Implementation Planning phases — generating Architecture Decision Records, epics, stories with acceptance criteria, traceability links, and sprint plans — completing the full BMAD methodology lifecycle.

### Story 6.1: Architecture Decision Records

As a user, I want the agent to help me create Architecture Decision Records during the Solutioning phase, so that my technical choices are documented with their rationale and alternatives considered.

**Acceptance Criteria:**

**AC 6.1.1 — ADR Generation**
- Given the project is in the Solutioning phase
- When the agent and I discuss an architectural decision
- Then the agent generates an ADR artifact with sections: Title, Status, Context, Decision, Consequences, and Alternatives Considered
- And the ADR is saved via `bmad_write_artifact` with type `adr` in frontmatter

**AC 6.1.2 — ADR Wikilinks**
- Given an ADR references the PRD, technical constraints, or other ADRs
- When the ADR artifact is written
- Then it contains wikilinks to all referenced artifacts (e.g., `[[PRD]]`, `[[ADR-001 Database Selection]]`)
- And the frontmatter `parent` field links to the parent artifact in the chain

**AC 6.1.3 — ADR Obsidian Compatibility**
- Given an ADR artifact is written
- When opened in Obsidian
- Then frontmatter renders correctly in reading view
- And all wikilinks resolve to their target files

---

### Story 6.2: Epic Generation from PRD

As a user, I want the agent to generate development epics from my PRD requirements, so that high-level functional requirements are organized into deliverable work packages.

**Acceptance Criteria:**

**AC 6.2.1 — Epic Generation**
- Given the project has a completed and validated PRD
- When the agent generates epics
- Then each epic is saved as an artifact with: title, goal statement, list of included functional requirements (FR references), and embedded non-functional requirements
- And every FR in the PRD is covered by at least one epic (complete coverage)

**AC 6.2.2 — FR Coverage Mapping**
- Given epics have been generated
- When the coverage is evaluated
- Then a mapping artifact is created showing which FRs map to which epics
- And no FR is unmapped
- And the mapping is saved with wikilinks to both the PRD and each epic

**AC 6.2.3 — Incomplete PRD Error**
- Given the PRD is missing required sections (e.g., no functional requirements defined)
- When epic generation is attempted
- Then the agent identifies the specific missing sections
- And declines to generate epics until the PRD is complete
- And offers to help complete the missing sections

---

### Story 6.3: Story Generation with Acceptance Criteria

As a user, I want the agent to break epics down into development stories with Given/When/Then acceptance criteria, so that each unit of work is clearly defined and testable.

**Acceptance Criteria:**

**AC 6.3.1 — Story Generation**
- Given a completed epic artifact
- When the agent generates stories for that epic
- Then each story follows the format: "As a user, I want... so that..."
- And each story includes at least two acceptance criteria in Given/When/Then format
- And stories are sized appropriately for a single development agent to complete

**AC 6.3.2 — Story Artifact Structure**
- Given stories are generated
- When they are saved via `bmad_write_artifact`
- Then each story's frontmatter includes: `type: story`, `parent: [[Epic Name]]`, `status: draft`
- And the story body includes the user story, acceptance criteria, and any technical notes

**AC 6.3.3 — Conflicting Requirements Error**
- Given the epic contains requirements that conflict with each other or with existing ADRs
- When story generation encounters the conflict
- Then the agent identifies the specific conflicting requirements
- And presents the conflict to the user with options for resolution
- And does not generate stories for the conflicting area until resolved

---

### Story 6.4: Traceability Links

As a user, I want every artifact to be traceable through the full parent chain from story to epic to PRD to project brief, so that I can understand why every piece of work exists.

**Acceptance Criteria:**

**AC 6.4.1 — Full Parent Chain**
- Given a story artifact
- When its traceability is followed via `parent` frontmatter fields and wikilinks
- Then the chain resolves: Story → Epic → PRD → Project Brief
- And each link in the chain resolves to an existing artifact file

**AC 6.4.2 — Traceability Validation**
- Given all artifacts for a project have been generated
- When the system validates traceability
- Then every story has a parent epic, every epic has a parent PRD, and every PRD has a parent brief
- And any broken links are reported with the specific artifact and field that is broken

**AC 6.4.3 — Broken Traceability Error**
- Given an artifact's parent reference points to a non-existent file
- When the traceability check runs (at checkpoint or on-demand health check)
- Then the broken link is flagged with the specific artifact name and expected parent
- And the agent offers to repair the link by identifying the correct target

---

### Story 6.5: Sprint Plan & Project Completion

As a user, I want the agent to sequence stories into a sprint plan, so that I have a clear implementation roadmap.

**Acceptance Criteria:**

**AC 6.5.1 — Sprint Plan Generation**
- Given all stories have been generated and validated
- When the agent creates a sprint plan
- Then stories are sequenced into sprints with dependency ordering (no forward dependencies within a sprint)
- And each sprint has a clear goal and list of included stories with wikilinks
- And the sprint plan is saved as an artifact with `type: sprint-plan`

**AC 6.5.2 — Dependency Ordering**
- Given stories have implicit dependencies (e.g., database schema before API endpoints)
- When the sprint plan sequences them
- Then dependent stories appear in later sprints than their prerequisites
- And the agent explains the ordering rationale

**AC 6.5.3 — Implementation Phase Completion**
- Given the sprint plan is complete and checkpointed
- When the Implementation Planning phase concludes
- Then `bmad_advance_workflow` transitions the project to complete status
- And the `ProjectCompletionSummary` from Story 5.8 is triggered

---

## Epic 7: Bidirectional Workspace & Party Mode

**Goal:** Enable two-way interaction between the user's filesystem and the application — detecting external file changes, referencing user-added content, and generating optimistic vault links — while also providing a multi-agent "Party Mode" for creative brainstorming with distinct agent personalities.

### Story 7.1: Workspace File Detection & Ingestion

As a user, I want the system to notice when I add markdown files to my project folder, so that my external research and notes are automatically incorporated into the planning context.

**Acceptance Criteria:**

**AC 7.1.1 — Change Detection via bmad_detect_changes**
- Given I add a new markdown file to the project directory outside the application
- When `bmad_detect_changes` runs (triggered periodically or on focus)
- Then it executes `git status --porcelain` to detect untracked and modified files
- And newly detected markdown files are reported to the agent

**AC 7.1.2 — Markdown Tracking**
- Given new markdown files are detected
- When the system processes them
- Then markdown files (`.md`) are added to Git tracking via `git add`
- And binary files (images, PDFs) are not added to Git tracking
- And a commit is created with prefix `[ingest]` listing the added files

**AC 7.1.3 — Agent Context Ingestion**
- Given a new markdown file has been tracked
- When the agent processes the ingestion notification
- Then it reads and incorporates the file content as context for future responses
- And acknowledges the new file in the conversation (e.g., "I've incorporated your notes on X")

**AC 7.1.4 — Large File Protection**
- Given a markdown file exceeds 100KB
- When detection processes it
- Then the system warns the user and asks for confirmation before ingesting
- And does not automatically add it to Git

---

### Story 7.2: Agent File Referencing

As a user, I want the agent to accurately reference content from files I have added to the project, so that my external notes directly inform the planning process.

**Acceptance Criteria:**

**AC 7.2.1 — Accurate Content Referencing**
- Given I added a file `research-notes.md` containing specific technical findings
- When I ask the agent about a topic covered in that file
- Then the agent references the specific content from `research-notes.md` accurately
- And attributes the reference (e.g., "Based on your research notes...")

**AC 7.2.2 — Wikilink to User Files**
- Given the agent references a user-added file in an artifact
- When the artifact is written via `bmad_write_artifact`
- Then the reference is rendered as a wikilink (e.g., `[[research-notes]]`)
- And the link resolves correctly in Obsidian

---

### Story 7.3: Optimistic Vault Wikilinks

As a user, I want the agent to create wikilinks to notes that already exist in my Obsidian vault, so that BMAD artifacts integrate with my broader knowledge base.

**Acceptance Criteria:**

**AC 7.3.1 — Optimistic Link Generation**
- Given the project is inside an Obsidian vault with existing notes
- When the agent generates an artifact that references a concept matching an existing vault note
- Then it generates an optimistic wikilink to that note (best-effort filename match)
- And the link uses the note's exact filename without path (Obsidian's shortest-path resolution)

**AC 7.3.2 — Graceful Degradation**
- Given an optimistic wikilink targets a note that does not exist
- When the artifact is viewed in Obsidian
- Then the link renders as an unresolved wikilink (standard Obsidian behavior, displayed in a different colour)
- And no error or warning is generated by the application

---

### Story 7.4: Party Mode Agent Roster & Selection

As a user, I want to invoke a multi-agent brainstorming mode where relevant specialist agents join the conversation, so that I get diverse expert perspectives on my planning decisions.

**Acceptance Criteria:**

**AC 7.4.1 — Agent Roster via bmad_list_agents**
- Given Party Mode is available
- When `bmad_list_agents` is called
- Then it returns the full roster of available specialist agents with their names, expertise areas, and personality descriptions

**AC 7.4.2 — Agent Persona Retrieval**
- Given a specific agent is selected
- When `bmad_get_agent_persona` is called with the agent identifier
- Then it returns the full persona definition including expertise, communication style, and perspective biases

**AC 7.4.3 — Topic-Based Agent Selection**
- Given I invoke Party Mode during a discussion about database architecture
- When the system selects agents for the round
- Then 2-3 agents are chosen based on topic relevance (e.g., Data Architect, Backend Engineer, DevOps Specialist)
- And the selection rationale is briefly explained to the user

**AC 7.4.4 — Invoke Party Mode Anytime**
- Given I am in any phase of the project
- When I request Party Mode (via command or conversation)
- Then Party Mode activates regardless of current phase
- And the current conversation context is preserved and shared with the specialist agents

---

### Story 7.5: Party Mode Visual Identity & Interaction

As a user, I want each specialist agent in Party Mode to have a distinct visual identity and personality, so that I can easily distinguish between perspectives and the discussion feels like a genuine roundtable.

**Acceptance Criteria:**

**AC 7.5.1 — Distinct Visual Styling**
- Given Party Mode is active with 3 agents
- When `PartyModePanel` renders their messages
- Then each agent has a unique colour from the 8-slot palette
- And each message shows an emoji icon and bold agent name
- And agent colours are consistent throughout the session

**AC 7.5.2 — Response Length Limit**
- Given an agent in Party Mode is generating a response
- When it responds
- Then the response is approximately 150 words or fewer (soft limit)
- And the response is focused and opinionated (not generic)

**AC 7.5.3 — Agents Build on Each Other**
- Given Agent A has provided a perspective
- When Agent B responds
- Then Agent B references or builds upon Agent A's points (agreement, counterpoint, or extension)
- And the discussion progresses rather than repeating the same ground

**AC 7.5.4 — Distinct Personalities**
- Given multiple agents are participating
- When their responses are compared
- Then each agent has a recognizable communication style (e.g., one is cautious, one is bold, one is detail-oriented)
- And personality traits remain consistent across multiple rounds

---

### Story 7.6: Party Mode User Flow & Exit

As a user, I want to be able to ask questions during Party Mode and exit gracefully when I am ready, so that the brainstorming session serves my needs and transitions smoothly back to normal mode.

**Acceptance Criteria:**

**AC 7.6.1 — User Direct Questions**
- Given Party Mode is active and agents are discussing
- When I type a question or comment
- Then the agent discussion pauses
- And the relevant agent(s) respond to my question directly before resuming their discussion

**AC 7.6.2 — Graceful Exit**
- Given Party Mode is active
- When I say "exit party mode", "done", or use a designated exit action
- Then Party Mode ends gracefully
- And the primary agent provides a brief summary of the key points and decisions from the discussion
- And the summary is offered for saving as an artifact

**AC 7.6.3 — State Preservation on Exit**
- Given I exit Party Mode
- When I return to normal conversation
- Then all decisions and insights from the Party Mode discussion are available to the primary agent
- And the conversation continues from where I left off (pre-Party-Mode context is intact)
- And any decisions made during Party Mode are recorded in the project state

---

## Epic 8: Advanced Onboarding & Community Extensions

**Goal:** Support users coming from diverse starting points — existing Git repos, partial BMAD setups, and version mismatches — and enable community contributors to extend the workflow with custom templates, ensuring the tool adapts to users rather than forcing users to adapt to the tool.

### Story 8.1: Existing Git Repo Onboarding

As a user, I want to open an existing Git repository that does not have BMAD set up and have the system offer to initialize it, so that I can apply structured planning to projects already in progress.

**Acceptance Criteria:**

**AC 8.1.1 — Git Repo Detection Without BMAD**
- Given I open a directory that contains `.git/` but no `_bmad/` directory
- When the application inspects the directory
- Then it detects the existing Git repository
- And displays a prompt: "This is a Git repository without BMAD planning. Would you like to set up BMAD planning here?"

**AC 8.1.2 — BMAD Initialization in Existing Repo**
- Given I confirm the setup prompt
- When initialization runs
- Then `npx bmad init` scaffolds the `_bmad/` directory structure
- And the existing Git history is preserved (no rebase, no force operations)
- And a commit is created with message `[init] BMAD planning setup`
- And the project is registered in `SQLiteCheckpointIndex`

**AC 8.1.3 — Decline Initialization**
- Given I decline the setup prompt
- When the prompt dismisses
- Then the directory is not modified in any way
- And the application returns to the Welcome Screen

---

### Story 8.2: Brownfield Artifact Detection

As a user, I want the system to recognize and adopt existing BMAD artifacts when I open a project that has them but was not created with this tool, so that I can continue from where previous planning left off.

**Acceptance Criteria:**

**AC 8.2.1 — Existing Artifact Detection**
- Given I open a directory with `_bmad-output/` containing markdown artifacts but no `state.json` or structured Git state
- When the application inspects the directory
- Then it scans `_bmad-output/` for artifact files
- And validates each artifact's frontmatter against known BMAD artifact types

**AC 8.2.2 — Phase State Inference**
- Given valid artifacts are detected
- When the system infers the project state
- Then it determines the most advanced completed phase based on artifact types present (e.g., if epics exist, Solutioning is at least partially complete)
- And creates a `state.json` with the inferred phase and artifact registry

**AC 8.2.3 — User Confirmation of Inferred State**
- Given the system has inferred a project state
- When the results are presented
- Then the user sees a summary: "Found N artifacts. It looks like you've completed through the Planning phase. Is this correct?"
- And the user can confirm or adjust the inferred phase
- And on confirmation, Git state is initialized and the project is registered

**AC 8.2.4 — Invalid Artifact Handling**
- Given some files in `_bmad-output/` fail validation (missing frontmatter, unknown types)
- When the scan results are presented
- Then invalid files are listed with their specific issues
- And the user can choose to import them as-is or skip them

---

### Story 8.3: Method Version Upgrade & Mismatch

As a user, I want the system to detect when my project uses an older version of the BMAD method and offer to upgrade, so that I benefit from methodology improvements without losing existing work.

**Acceptance Criteria:**

**AC 8.3.1 — Version Mismatch Detection**
- Given a project's `_bmad/` directory contains method files at version 1.0
- When the application (shipping method version 2.0) opens the project
- Then it detects the version mismatch
- And displays: "This project uses BMAD method v1.0. The current version is v2.0."

**AC 8.3.2 — Continue or Migrate Prompt**
- Given a version mismatch is detected
- When the prompt is displayed
- Then it offers two options: "Continue with v1.0" and "Upgrade to v2.0"
- And the "Continue" option lets me work with the existing method files without modification
- And the "Upgrade" option runs `bmad_update_method`

**AC 8.3.3 — Method Upgrade via bmad_update_method**
- Given I choose to upgrade
- When `bmad_update_method` runs
- Then a Git tag `pre-method-upgrade-v1.0` is created before any changes
- And `_bmad/` method files are updated to v2.0
- And existing artifacts in `_bmad-output/` are not modified
- And a commit is created with message `[method] upgrade from v1.0 to v2.0`

**AC 8.3.4 — Rollback After Upgrade**
- Given a method upgrade has been applied
- When I decide I want to revert
- Then I can navigate to the pre-upgrade tag via the Journey Map
- And the project reverts to v1.0 method files cleanly

---

### Story 8.4: Project Archiving

As a user, I want to archive completed or abandoned projects so that they do not clutter my Welcome Screen while remaining fully recoverable.

**Acceptance Criteria:**

**AC 8.4.1 — Archive Action**
- Given a project appears on the Welcome Screen
- When I select the archive action for that project
- Then a confirmation modal appears: "Archive '<project name>'? It will be hidden from the project list but preserved in Git."
- And the modal has "Archive" and "Cancel" buttons

**AC 8.4.2 — Archived Project Hidden**
- Given I confirm the archive
- When the Welcome Screen re-renders
- Then the archived project no longer appears in the default project list
- And the project's Git repository and all files remain intact on disk

**AC 8.4.3 — Show Archived Toggle**
- Given I have archived projects
- When I toggle "Show archived" on the Welcome Screen
- Then archived projects appear in the list with a visual indicator (e.g., grey text, "(archived)" suffix)
- And I can select an archived project to unarchive or open it in read-only mode

**AC 8.4.4 — Unarchive Action**
- Given an archived project is visible via the toggle
- When I select the unarchive action
- Then the project reappears in the default project list
- And it is fully functional with all history intact

---

### Story 8.5: Community Workflow Templates & Runtime Discovery

As a user, I want to install community-contributed workflow templates by simply adding files to a directory, so that I can extend the methodology without code changes or build steps.

**Acceptance Criteria:**

**AC 8.5.1 — Template Discovery at Runtime**
- Given a workflow template directory exists (e.g., `_bmad/workflows/`)
- When the application starts or a project is opened
- Then it scans the directory for markdown step-files matching the naming convention (`NN-step-name.md`)
- And newly discovered templates are available for use without any build step or application restart

**AC 8.5.2 — Template File Format**
- Given a community contributor creates a template
- When they write a markdown step-file with frontmatter (title, phase, required_inputs, outputs)
- Then the system validates the frontmatter schema
- And makes the template available in the corresponding phase's workflow

**AC 8.5.3 — Template Isolation**
- Given a community template contains invalid content or references non-existent artifacts
- When the system loads it
- Then the invalid template is skipped with a warning in the log
- And all other templates and the core workflow remain unaffected

**AC 8.5.4 — Template Listing**
- Given community templates are installed
- When the agent queries available workflow steps
- Then both built-in and community templates appear in the step list
- And community templates are marked with their source (e.g., "(community)" suffix)