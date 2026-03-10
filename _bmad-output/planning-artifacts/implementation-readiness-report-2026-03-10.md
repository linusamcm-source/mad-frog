# Implementation Readiness Assessment Report

**Date:** 2026-03-10
**Project:** vibe_visualiser

---

## Step 1: Document Discovery

**stepsCompleted:** [step-01-document-discovery, step-02-prd-analysis, step-03-epic-coverage-validation, step-04-ux-alignment, step-05-epic-quality-review, step-06-final-assessment]

### Document Inventory

| Document Type | File | Size | Modified |
|---|---|---|---|
| PRD | prd.md | 70 KB | Mar 9 22:45 |
| PRD Validation | prd-validation-report.md | 682 B | Mar 9 22:23 |
| Architecture | architecture.md | 114 KB | Mar 9 22:08 |
| Epics & Stories | epics.md | 89 KB | Mar 10 00:10 |
| UX Design | ux-design-specification.md | 135 KB | Mar 9 23:00 |

### Issues
- No duplicate documents found
- No missing required documents
- All four required document types present

### Files Selected for Assessment
- `_bmad-output/planning-artifacts/prd.md`
- `_bmad-output/planning-artifacts/architecture.md`
- `_bmad-output/planning-artifacts/epics.md`
- `_bmad-output/planning-artifacts/ux-design-specification.md`

---

## Step 2: PRD Analysis

### Functional Requirements

| ID | Requirement |
|---|---|
| FR1 | User can create a new project with a name from the welcome screen |
| FR2 | System prevents duplicate project names and guides the user to choose a unique name |
| FR3 | User can view a list of all existing projects with their current phase and last-active date |
| FR4 | User can resume any existing project from the welcome screen |
| FR5 | User can archive a project (hidden from welcome screen, preserved in Git) |
| FR6 | System creates a Git-backed state record for each new project with branch-prefix isolation |
| FR7 | System maintains a SQLite checkpoint index with project and checkpoint tables (Git SHA as primary key) |
| FR8 | System supports one active project session at a time -- user switches projects via the welcome screen |
| FR8a | User can upgrade a project's BMAD method version to the tool's current version via explicit action |
| FR8b | When opening a directory with `.git/` but no `_bmad/`, system offers to set up BMAD planning in the existing repo |
| FR8c | When opening a project whose `_bmad/` method version differs from the tool's version, system prompts user to continue or migrate |
| FR8d | When opening a directory with `_bmad-output/` artifacts but no structured Git state, system offers to validate existing artifacts and infer phase state (brownfield onboarding) |
| FR9 | User can progress through BMAD phases sequentially (Analysis -> Planning -> Solutioning -> Implementation) |
| FR10 | Phases require validated artifacts to unlock -- enforced by agent via BMAD workflow instructions, not by system-level phase gates |
| FR11 | User can import existing artifacts and have the agent validate them to mark a phase complete |
| FR12 | Agent adapts conversational approach based on user response patterns |
| FR13 | User can invoke any BMAD workflow available in the installed module during the appropriate phase |
| FR14 | System creates a Git commit with structured metadata at each phase completion |
| FR15 | System loads the appropriate agent context and workflow instructions when transitioning between phases |
| FR16 | User can ask the agent for help or explanation at any point without losing workflow progress |
| FR17 | User can request a current project status summary at any time |
| FR18 | User can request to revisit and revise a previous answer within the current session |
| FR19 | User can generate architecture decision records during Solutioning phase |
| FR20 | User can generate epics from PRD requirements |
| FR21 | User can generate user stories with acceptance criteria from epics |
| FR22 | System maintains traceability links between stories, epics, PRD, and brief |
| FR23 | User can generate sprint plans that sequence stories into sprints |
| FR24 | Implementation phase MVP scope: sprint plan and story file generation |
| FR25 | User can view a visual Journey Map in the sidebar showing all phases and their completion state |
| FR26 | Journey Map nodes display three visual states: completed (clickable), in-progress, locked |
| FR27 | Journey Map nodes display dates and human-readable descriptions |
| FR28 | User can click any completed phase node in the Journey Map to navigate back to that checkpoint |
| FR29 | Click-back navigation presents a confirmation modal before creating a new version |
| FR30 | System preserves all downstream work on a separate Git branch when user navigates back |
| FR31 | System displays the current position in the Journey Map with a distinct indicator |
| FR32 | User can view version history for any completed phase node |
| FR33 | User can create a manual checkpoint with a custom label at any point during a session |
| FR34 | Journey Map sidebar scrolls vertically when content exceeds viewport; completed phases can be collapsed |
| FR35 | System manages Git branches internally -- users never see branch names, commit hashes, or Git terminology |
| FR36 | System displays dates and times in the user's local timezone |
| FR37 | System persists all project state to a bind-mounted directory on the host filesystem |
| FR38 | System fully recovers all project state after container rebuild, restart, or destruction |
| FR39 | System stores session context in Git commit metadata sufficient for agent context reconstruction |
| FR40 | Agent greets returning users with context from their last session |
| FR41 | Single active session enforced per project -- second browser tab receives read-only view or option to take over |
| FR42 | System ensures artifact write and Git commit are atomic -- both succeed or both roll back |
| FR43 | System auto-saves uncommitted changes every 2 minutes via deterministic commit templates |
| FR44 | System detects state format version on startup and performs any necessary migrations |
| FR45 | System handles browser disconnection gracefully -- user can reconnect and resume from last stable state |
| FR45a | System silently pre-empts context window exhaustion by querying agent context budget via `bmad_report_context` tool |
| FR46 | System writes all artifacts as Obsidian-native markdown with YAML frontmatter and wikilinks |
| FR47 | System generates wikilinks that reference other project artifacts |
| FR48 | Agent generates optimistic wikilinks to pre-existing vault notes when referencing user-provided content |
| FR49 | User configures workspace root via first-run modal |
| FR50 | System generates artifacts that render correctly in Obsidian's graph view with working backlinks |
| FR51 | Artifacts include Obsidian-compatible frontmatter (aliases, tags, phase, project, parent references) |
| FR52 | For vault-resident projects, system proposes `.obsidianignore` entries during project setup |
| FR55 | Any artifact can be traced through its full parent chain to the original requirement via wikilinks |
| ~~FR53~~ | *(Deferred)* Conversation transcripts as structured Obsidian-native markdown files |
| ~~FR54~~ | *(Deferred)* Conversation transcripts include frontmatter identifying phase, checkpoint, date, and participating agents |
| FR56 | User can add markdown files to the project folder at any time |
| FR57 | Agent automatically ingests user-added markdown files as context in subsequent sessions |
| FR58 | Agent references content from user-added files accurately in conversation |
| FR59 | System detects new, modified, or deleted files in the project folder via `bmad_detect_changes` tool |
| FR60 | System tracks markdown files in Git -- binary files are accessible but not version-tracked |
| FR61 | User can invoke Party Mode at any point during any workflow phase |
| FR62 | System loads the complete agent roster from the installed BMAD agent manifest |
| FR63 | System selects 2-3 most relevant agents per discussion round based on topic analysis |
| FR64 | Agents maintain distinct personalities, communication styles, and expertise boundaries |
| FR65 | System visually identifies each agent in Party Mode with their name, icon, and distinct styling |
| FR66 | Agents can reference and build on each other's contributions within a round |
| FR67 | System halts and waits for user input when an agent asks a direct question |
| FR68 | User can exit Party Mode and return to the guided workflow with state preserved |
| FR69 | Toad manages all credential validation and provider setup -- Mad Frog has no credential UI |
| FR70 | API keys are forwarded from host environment via `devcontainer.json` `remoteEnv` |
| FR71 | Toad manages all LLM provider connections -- Mad Frog makes no direct LLM API calls |
| FR72 | User can launch the full application via `make start` which runs `mad_frog` |
| FR73 | System serves the complete UI to a browser at localhost:8000 |
| FR74 | On first launch, system displays a workspace setup modal asking user for their project directory path |
| FR75 | System forwards the serve port automatically in Dev Container environments |
| FR76 | System performs health checks on startup and reports issues with recovery guidance |
| FR77 | System integrates project state management with Toad's existing session infrastructure |
| FR78 | System provides phase completion feedback including artifact summary, decisions made, and next phase preview |
| FR79 | System presents project completion summary showing all artifacts created |
| FR80 | System generates artifacts as professional narrative prose, not template fill-in |
| FR81 | Agent has access to all previous decisions and constraints when generating responses within a session |
| FR82 | System handles agent response failures gracefully with clear feedback and option to retry |
| FR83 | System displays clear error messages when state operations fail and offers recovery guidance |
| FR84 | Keyboard navigation available for all primary interactions |
| FR84a | System detects artifact-like content in conversation that was not saved via a tool call, and prompts user to save |
| ~~FR85~~ | *(Deferred)* User can opt in to anonymous usage telemetry |
| FR86 | Community contributors can add new workflow templates by placing markdown step-files in the designated folder structure |
| FR87 | System discovers workflow templates at runtime from the file system (no build step or registry) |
| FR88 | System provides an on-demand health check accessible from the UI |

**Total Active FRs:** 76
**Total Deferred FRs:** 3 (FR53, FR54, FR85)

### Non-Functional Requirements

| ID | Category | Requirement |
|---|---|---|
| NFR-PERF-01 | Performance | Journey Map renders within 500ms for up to 50 checkpoints |
| NFR-PERF-02 | Performance | Atomic artifact-write-plus-commit within 3 seconds; progress indicator if exceeded |
| NFR-PERF-03 | Performance | Welcome screen project list loads within 1 second for up to 20 projects |
| NFR-PERF-04 | Performance | SQLite checkpoint queries return within 100ms for up to 200 checkpoints |
| NFR-PERF-05 | Performance | Browser UI remains responsive during agent processing; loading indicators for ops >500ms |
| NFR-PERF-06 | Performance | Container cold start completes within 30 seconds |
| NFR-PERF-07 | Performance | Disk footprint under 500MB per project for up to 100 checkpoints and 50 artifacts |
| NFR-PERF-08 | Performance | Warm restart completes health checks within 15 seconds |
| NFR-PERF-09 | Performance | System responsive after 4 hours continuous use; memory below 512MB; no memory leaks |
| NFR-PERF-10 | Performance | Checkpoint navigation: artifact display within 2s, context reconstruction within 5s |
| NFR-PERF-11 | Performance | Handles individual artifact files up to 500KB; warning for larger files |
| NFR-SEC-01 | Security | API keys never logged, displayed in UI, or written to artifacts/Git |
| NFR-SEC-02 | Security | `.env` files gitignored by default and verified on startup |
| NFR-SEC-03 | Security | No data transmitted except to configured LLM provider via Toad |
| NFR-SEC-04 | Security | System reads/writes only within configured project directory and SQLite path |
| NFR-REL-01 | Reliability | Zero data loss -- all committed state survives container destruction |
| NFR-REL-02 | Reliability | Atomic checkpoint operations -- write + commit succeed together or roll back |
| NFR-REL-03 | Reliability | SQLite index rebuild produces byte-identical database from Git history |
| NFR-REL-04 | Reliability | Graceful recovery from mid-operation container kill |
| NFR-REL-05 | Reliability | Browser disconnection does not corrupt state |
| NFR-REL-06 | Reliability | Startup health check validates Git, SQLite, bind mount, state version within 10s |
| NFR-REL-07 | Reliability | Atomic session lock acquisition; concurrent connection handling |
| NFR-REL-08 | Reliability | On-demand health check completes within 5 seconds |
| NFR-REL-09 | Reliability | Network connectivity loss detection; conversation state preserved |
| NFR-REL-10 | Reliability | Chaos test suite: 5 failure scenarios, all recover to consistent state |
| NFR-ACC-01 | Accessibility | All primary interactions keyboard-accessible |
| NFR-ACC-02 | Accessibility | UI text elements maintain minimum 4.5:1 contrast ratio (WCAG AA) |
| NFR-ACC-03 | Accessibility | Journey Map states distinguishable by shape/icon, not colour-only |
| NFR-ACC-04 | Accessibility | Error messages use text labels, not icon-only communication |
| NFR-INT-01 | Integration | Artifacts pass automated validation: YAML frontmatter, wikilinks, frontmatter fields |
| NFR-INT-02 | Integration | Pinned Toad version; upstream updates validated before bump |
| NFR-INT-03 | Integration | CommonMark-compliant markdown output |
| NFR-INT-04 | Integration | Standard Git commands only -- no extensions |
| NFR-INT-05 | Integration | Runs on Docker Desktop (macOS, Windows, Linux) without platform-specific config |
| NFR-INT-06 | Integration | UTF-8/Unicode support; handles spaces and special chars in file paths |
| NFR-OBS-01 | Observability | Structured JSON logs with rotation at 10MB |
| NFR-OBS-02 | Observability | Error logs include operation ID, state snapshot, classification, recovery action |
| NFR-MNT-01 | Maintainability | State format version identifier with automated migrations |
| NFR-MNT-02 | Maintainability | Workflow templates follow documented conventions; `bmad validate-workflow` catches errors |
| NFR-MNT-04 | Maintainability | Non-destructive state migrations with Git tag backup; completes within 30s |
| NFR-MNT-05 | Maintainability | Core state operations 90%+ branch coverage; UI widgets 80%+ line coverage |
| NFR-MNT-06 | Maintainability | Backwards compatibility: V1 artifacts render in V2 without migration |
| NFR-UX-01 | UX Quality | Artifacts pass automated structural validation; prose quality via human review |

**Total NFRs:** 43 (Performance: 11, Security: 4, Reliability: 10, Accessibility: 4, Integration: 6, Observability: 2, Maintainability: 5, UX Quality: 1)
*Note: NFR-MNT-03 is missing from the PRD -- potential gap*

### Additional Requirements & Constraints

**Explicit MVP Exclusions:**
- EX1: System does NOT execute code or run builds
- EX2: No connection to external services (GitHub, Jira, etc.)
- EX3: No file modification outside project folder / bind mount
- EX4: No credential storage -- delegates to Toad/agent env vars
- EX5: No automatic downstream reprocessing when parent artifact changes
- EX6: No mobile browser support guarantee
- EX7: No in-app search -- delegates to Obsidian
- EX8: No concurrent different-project tabs

**Design Decisions:**
- DD1: Mental model is "time travel," not "branching"
- DD2: Search delegated to Obsidian
- DD3: Agent introduces concepts naturally during conversation (no onboarding tutorial)
- DD4: Conversation transcripts stored as separate markdown files, not loaded into agent context by default
- DD5: Widget components designed as independently testable units via Textual pilot framework

**Architectural Constraints:**
- Three-process model: MadFrogApp + AI Agent + MCP Server
- Two-tier state persistence: Git (durable) + SQLite (reconstructable) + session (volatile)
- 7 infrastructure services
- Dev Container on Python 3.14 with Toad and Node.js
- Single production dependency: `batrachian-toad>=0.5.35,<0.7`
- Stateless peer tool deployment model

### PRD Completeness Assessment
- PRD is comprehensive with 76 active FRs, 43 NFRs, 8 exclusions, and 5 design decisions
- NFR-MNT-03 is missing (gap in numbering) -- should be investigated
- FR numbering has gaps (no FR53, FR54 active; no FR85 active) -- these are documented as deferred
- Sub-requirements (FR8a-d, FR45a, FR84a) extend base requirements appropriately
- Ship-blocking NFR classification is documented and clear

---

## Step 3: Epic Coverage Validation

### Coverage Matrix

| FR | PRD Requirement | Epic | Status |
|---|---|---|---|
| FR1 | Create new project from welcome screen | Epic 1 | Covered |
| FR2 | Prevent duplicate project names | Epic 1 | Covered |
| FR3 | View list of all existing projects | Epic 5 | Covered |
| FR4 | Resume any existing project | Epic 5 | Covered |
| FR5 | Archive a project | Epic 9 | Covered |
| FR6 | Git-backed state record with branch-prefix isolation | Epic 1 | Covered |
| FR7 | SQLite checkpoint index | Epic 1 | Covered |
| FR8 | One active project session at a time | Epic 5 | Covered |
| FR8a | Method version upgrade | Epic 9 | Covered |
| FR8b | Existing Git repo onboarding | Epic 9 | Covered |
| FR8c | Version mismatch handling | Epic 9 | Covered |
| FR8d | Brownfield onboarding | Epic 9 | Covered |
| FR9 | Sequential phase progression | Epic 2 | Covered |
| FR10 | Phase unlock via validated artifacts | Epic 2 | Covered |
| FR11 | Import existing artifacts | Epic 2 | Covered |
| FR12 | Adaptive conversational pacing | Epic 3 | Covered |
| FR13 | Invoke BMAD workflows | Epic 2 | Covered |
| FR14 | Phase completion Git commits | Epic 2 | Covered |
| FR15 | Agent context loading on phase transition | Epic 2 | Covered |
| FR16 | Help/explanation without losing progress | Epic 3 | Covered |
| FR17 | Project status summary on demand | Epic 3 | Covered |
| FR18 | Revisit previous answer in session | Epic 3 | Covered |
| FR19 | Architecture decision records | Epic 6 | Covered |
| FR20 | Generate epics from PRD | Epic 6 | Covered |
| FR21 | Generate stories with acceptance criteria | Epic 6 | Covered |
| FR22 | Traceability links | Epic 6 | Covered |
| FR23 | Sprint plan generation | Epic 6 | Covered |
| FR24 | Implementation phase MVP scope | Epic 6 | Covered |
| FR25 | Visual Journey Map in sidebar | Epic 4 | Covered |
| FR26 | Three visual states for nodes | Epic 4 | Covered |
| FR27 | Dates and human-readable descriptions | Epic 4 | Covered |
| FR28 | Click-back to completed nodes | Epic 4 | Covered |
| FR29 | Confirmation modal for click-back | Epic 4 | Covered |
| FR30 | Preserve downstream on Git branch | Epic 4 | Covered |
| FR31 | Current position indicator | Epic 4 | Covered |
| FR32 | Version history for completed nodes | Epic 4 | Covered |
| FR33 | Manual checkpoint with label | Epic 4 | Covered |
| FR34 | Scrollable, collapsible sidebar | Epic 4 | Covered |
| FR35 | Git branches invisible to user | Epic 4 | Covered |
| FR36 | Local timezone display | Epic 4 | Covered |
| FR37 | Bind mount persistence | Epic 1 | Covered |
| FR38 | Full recovery after container rebuild | Epic 5 | Covered |
| FR39 | Session context in Git metadata | Epic 5 | Covered |
| FR40 | Context recall on resume | Epic 5 | Covered |
| FR41 | Session lock with read-only fallback | Epic 5 | Covered |
| FR42 | Atomic artifact write + commit | Epic 1 | Covered |
| FR43 | Auto-save every 2 minutes | Epic 5 | Covered |
| FR44 | State format migration | Epic 5 | Covered |
| FR45 | Browser disconnect recovery | Epic 5 | Covered |
| FR45a | Pre-emptive context save at 90% | Epic 5 | Covered |
| FR46 | Obsidian-native markdown output | Epic 1 | Covered |
| FR47 | Wikilinks between project artifacts | Epic 2 | Covered |
| FR48 | Optimistic wikilinks to vault notes | Epic 7 | Covered |
| FR49 | Workspace root via first-run modal | Epic 2 | Covered |
| FR50 | Graph view with backlinks | Epic 2 | Covered |
| FR51 | Obsidian-compatible frontmatter | Epic 1 | Covered |
| FR52 | .obsidianignore proposals | Epic 2 | Covered |
| FR55 | Artifact parent chain traceability | Epic 2 | Covered |
| FR56 | Add markdown to project folder | Epic 7 | Covered |
| FR57 | Agent ingests user-added files | Epic 7 | Covered |
| FR58 | Agent references user files accurately | Epic 7 | Covered |
| FR59 | Detect changes via bmad_detect_changes | Epic 7 | Covered |
| FR60 | Git-track markdown, not binaries | Epic 7 | Covered |
| FR61 | Invoke Party Mode anytime | Epic 7 | Covered |
| FR62 | Load agent roster from manifest | Epic 7 | Covered |
| FR63 | Select 2-3 relevant agents per round | Epic 7 | Covered |
| FR64 | Distinct agent personalities | Epic 7 | Covered |
| FR65 | Visual agent identity in Party Mode | Epic 7 | Covered |
| FR66 | Agents build on each other | Epic 7 | Covered |
| FR67 | Halt for user input on direct question | Epic 7 | Covered |
| FR68 | Exit Party Mode with state preserved | Epic 7 | Covered |
| FR69 | Toad manages credentials | Epic 1 | Covered |
| FR70 | API key passthrough via devcontainer | Epic 1 | Covered |
| FR71 | Toad manages LLM connections | Epic 1 | Covered |
| FR72 | Launch via make start | Epic 1 | Covered |
| FR73 | UI at localhost:8000 | Epic 1 | Covered |
| FR74 | First-launch workspace setup modal | Epic 1 | Covered |
| FR75 | Port forwarding in Dev Container | Epic 1 | Covered |
| FR76 | Startup health checks | Epic 1 | Covered |
| FR77 | Integrate with Toad session infra | Epic 1 | Covered |
| FR78 | Phase completion feedback | Epic 2 | Covered |
| FR79 | Project completion summary | Epic 6 | Covered |
| FR80 | Narrative prose artifacts | Epic 2 | Covered |
| FR81 | Agent access to all previous decisions | Epic 3 | Covered |
| FR82 | Agent failure handling with retry | Epic 3 | Covered |
| FR83 | Clear error messages with recovery | Epic 3 | Covered |
| FR84 | Keyboard navigation | Epic 3 | Covered |
| FR84a | Unwritten artifact detection | Epic 3 | Covered |
| FR86 | Community workflow templates | Epic 9 | Covered |
| FR87 | Runtime template discovery | Epic 9 | Covered |
| FR88 | On-demand health check | Epic 5 | Covered |
| ~~FR53~~ | *(Deferred)* Conversation transcripts | -- | Deferred |
| ~~FR54~~ | *(Deferred)* Transcript frontmatter | -- | Deferred |
| ~~FR85~~ | *(Deferred)* Anonymous telemetry | -- | Deferred |

### Missing Requirements

No active FRs are missing from epic coverage. All 76 active functional requirements have a traceable path to at least one epic.

### Coverage Statistics

- Total PRD FRs: 79 (76 active + 3 deferred)
- FRs covered in epics: 76/76 active FRs (100%)
- FRs deferred (post-MVP): 3 (FR53, FR54, FR85)
- Coverage percentage: **100%** of active FRs

### Epic Distribution

| Epic | Name | FR Count |
|---|---|---|
| Epic 1 | Project Foundation & First Artifact | 17 |
| Epic 2 | Guided Conversation & Artifact Creation | 13 |
| Epic 3 | Polished Workflow Experience | 9 |
| Epic 4 | Journey Map & Decision Navigation | 12 |
| Epic 5 | Session Persistence & Safe Recovery | 12 |
| Epic 6 | Solutioning & Implementation Planning | 7 |
| Epic 7 | Bidirectional Workspace & Party Mode | 14 |
| Epic 8 | Hardening & Ship-Gate | 0 (NFR-only) |
| Epic 9 | Advanced Onboarding & Community Extensions | 7 |

### Observations
- Epic 8 covers no FRs -- it is a pure NFR/hardening epic, which is appropriate
- Epic 7 is the largest FR carrier (14 FRs) combining two distinct concerns (workspace + party mode)
- FR distribution across epics is well-balanced with no single epic overloaded

---

## Step 4: UX Alignment Assessment

### UX Document Status

**Found:** `ux-design-specification.md` (135 KB, comprehensive)

### Contradictions (Must Resolve)

1. **CredentialSetupScreen:** Architecture includes `credential_screen.py` but PRD FR69 explicitly states "Mad Frog has no credential UI" and UX spec has no credential screen. Architecture must remove this.
2. **`click` dependency:** Architecture CLI code uses `click` which would be an additional dependency, violating PRD's "single production dependency" principle. Party mode insights say use `argparse` but code not updated.
3. **Codespaces references:** Architecture still references GitHub Codespaces in deployment model despite PRD explicitly removing all Codespaces references (local Docker Desktop only).
4. **Tool count inconsistency:** Architecture cites 15/16/18 tools at different points; PRD says 18. Need single authoritative count.
5. **Manual checkpoint shortcut:** Architecture references `Ctrl+S` for manual checkpoint (FR33) but UX spec's keyboard binding table omits it.

### Alignment Gaps (Need Design/Specification)

1. **FR79** (project completion summary) -- PRD requires it but UX spec has no design for it
2. **FR88** (on-demand health check UI access) -- PRD requires sidebar action or settings menu entry, UX spec has no design
3. **FR5** (archive project) -- PRD requires it but UX spec has no flow (only mentions "delete project" modal)
4. **FR32** (view version history for completed nodes) -- partially addressed in UX; no explicit "view history" interaction
5. **ContentProgressIndicator** -- designed in UX spec but has no corresponding PRD FR or architecture support
6. **DecisionCounter** -- designed in UX spec but no PRD FR; `state.json` schema lacks `decision_count` field
7. **`state.json` schema gaps:** Missing fields needed by UX components: `decision_count`, `vault_status`, `checkpoint_history`
8. **Conversation landmark-to-scroll linking** -- UX spec specifies `landmark_id` for Journey Map scroll-to-navigate but no architectural support documented
9. **FR56-60** mapped to wrong tools in architecture's requirements-to-structure table (should be `workspace.*` tools, not `project.*`)
10. **Width adaptation** -- detailed responsive design in UX spec (4 width tiers) but no PRD NFRs for responsive terminal width handling

### Warnings

1. **Creative freeform mode scope ambiguity:** PRD user journeys describe it as MVP, UX spec defers to Post-MVP -- needs explicit scope decision
2. **ConversationPanel naming:** PRD DD5 lists "ConversationPanel" as independently testable, but architecture removes custom panel in favor of Toad's built-in. UX spec's `ConversationEntry` class hierarchy and ceremony/landmark rendering may not be supported by Toad's default panel
3. **Agent communication patterns:** UX spec's detailed agent behavior rules (one question per message, adaptive pacing, substantive content boundary) are not captured as testable PRD requirements
4. **Party Mode word limits:** UX spec specifies ~150 word soft limits per panel -- not in PRD
5. **Browser compatibility gate:** UX spec specifies a pre-Textual HTML shim checking WebSocket/viewport -- not in PRD
6. **RichLog 10,000-line scrollback limit:** UX spec specifies memory management for conversation history -- no NFR covers this

---

## Step 5: Epic Quality Review

### Critical Violations (3)

**C1: Stories 1.1-1.4 are developer infrastructure stories with no direct user value**
- Stories: 1.1 (Starter Skeleton), 1.2 (MCP Server Bootstrap), 1.3 (Data Models), 1.4 (SQLite Checkpoint Index)
- All four are "As a developer" stories delivering infrastructure, not user outcomes
- Remediation: Fold into Story 1.5 (Project Creation) or 1.7 (MadFrogApp Shell) as implementation tasks. First user story should be "As a user, I can launch the app and create my first project" with infrastructure as implementation details

**C2: Epic 8 (Hardening & Ship-Gate) is a pure technical epic with zero user value**
- All 8 stories (8.1-8.8) are "As a developer" stories
- Delivers zero direct user value -- "Structured JSON Logging," "Chaos Test Suite," "Coverage Enforcement," "Security Audit" are all internal quality concerns
- Remediation: Distribute as acceptance criteria or embedded NFRs into the epics where they naturally belong. Chaos tests -> Epic 5 recovery stories. Coverage -> CI config. Logging -> Epic 1. Or reframe around user outcomes: "As a user, I can trust my data survives any failure"

**C3: Story 1.2 (MCP Server Bootstrap) has a forward dependency**
- AC states `tools/list` returns "an empty tool list (tools added in subsequent stories)"
- Delivers incomplete functionality only useful when later stories add tools
- Remediation: Merge into first story that registers a tool (1.5) or include at least one real tool

### Major Issues (6)

**M1: Database tables created upfront (Story 1.4)**
- Creates both `projects` and `checkpoints` tables plus `rebuild()` before any project or checkpoint exists
- Anti-pattern: "create all tables in Epic 1 Story 1"
- Remediation: `projects` table in Story 1.5, `checkpoints` table in Story 2.3, `rebuild()` in Story 5.5

**M2: Data models created before consumption (Story 1.3)**
- Creates ProjectRecord, Checkpoint, Decision, Phase models and GitStateEngine standalone
- Only consumed starting in Story 1.5
- Remediation: Define models incrementally as stories need them

**M3: Vague acceptance criteria in Epic 8 stories**
- Stories 8.1, 8.3, 8.4, 8.5 lack proper Given/When/Then or testable specifics
- Example: Story 8.3 memory test says "linear regression asserts no upward trend exceeding 5%" but doesn't specify baseline methodology
- Remediation: Add concrete test methodology to each AC

**M4: Story 5.7 combines two unrelated concerns**
- Conflates context window exhaustion detection (FR45a) with state format migration (FR44)
- Different triggers, implementation paths, and testing strategies
- Remediation: Split into 5.7a (Pre-emptive Context Save) and 5.7b (State Format Migration)

**M5: Story 1.9 / Story 8.8 partial duplication**
- Story 1.9 implements startup health checks (Git, SQLite, bind mount)
- Story 8.8 implements "comprehensive startup validation" checking the same three things
- Remediation: Story 1.9 implements basic framework with bind-mount only; Story 8.8 extends to full suite

**M6: WelcomeScreen incomplete without Epic 5**
- Story 1.8 creates WelcomeScreen with "Start new project" only
- Story 5.3 adds "Resume existing project" (FR3, FR4) later
- Users who create multiple projects can't switch between them until Epic 5
- Remediation: Move project listing and resume into Epic 1 as Story 1.10

### Minor Concerns (6)

1. **Inconsistent persona usage:** Stories 1.1-1.4 and 8.1-8.8 use "As a developer" while all others use "As a user"
2. **Story 3.1 (Adaptive Pacing) untestable ACs:** Behavioral guidelines for AI agent, not testable system behaviors. Reframe as configuration parameters
3. **Story 2.4 misplaced NFR:** Toad version pinning (NFR-INT-02) included in Artifact Validation Pipeline story -- should be in Story 1.1
4. **Epic 6 stories (6.1-6.5) missing error condition ACs:** Only happy paths covered; no handling for incomplete PRD, generation conflicts, or broken traceability
5. **Story 4.5 bundles two concerns:** Version history viewing + manual checkpoint creation are distinct user actions
6. **FR85 undefined:** Referenced in coverage map as "Deferred" but never defined in the FR list (numbering jumps FR84a to FR86)

### Best Practices Compliance Summary

| Epic | User Value | Independence | Story Sizing | No Forward Deps | DB When Needed | Clear ACs | FR Traceability |
|---|---|---|---|---|---|---|---|
| Epic 1 | Partial (1.1-1.4 fail) | Pass | Pass | Fail (1.2) | Fail (1.4) | Pass | Pass |
| Epic 2 | Pass | Pass | Pass | Pass | Pass | Pass (minor: 2.4) | Pass |
| Epic 3 | Pass | Pass | Pass | Pass | N/A | Partial (3.1) | Pass |
| Epic 4 | Pass | Pass | Minor (4.5) | Pass | N/A | Pass | Pass |
| Epic 5 | Pass | Pass | Fail (5.7) | Pass | N/A | Pass | Pass |
| Epic 6 | Pass | Pass | Pass | Pass | N/A | Partial (missing errors) | Pass |
| Epic 7 | Pass | Pass | Pass | Pass | N/A | Pass | Pass |
| Epic 8 | **FAIL** | Pass | Pass | Pass | N/A | Partial | N/A (NFR-only) |
| Epic 9 | Pass | Pass | Pass | Pass | N/A | Pass | Pass |

---

## Summary and Recommendations

### Overall Readiness Status

**NEEDS WORK** -- The project has strong foundations (comprehensive PRD, 100% FR coverage in epics, detailed UX spec) but contains cross-document contradictions and epic structure violations that must be resolved before implementation begins.

### Issue Summary

| Category | Critical | Major | Minor | Warnings |
|---|---|---|---|---|
| Cross-Document Contradictions | 3 | 2 | 0 | 0 |
| UX Alignment Gaps | 0 | 7 | 3 | 6 |
| Epic Quality Violations | 3 | 6 | 6 | 0 |
| PRD Gaps | 0 | 1 | 1 | 0 |
| **Total** | **6** | **16** | **10** | **6** |

### Critical Issues Requiring Immediate Action

1. **Architecture contradicts PRD on credentials (CredentialSetupScreen):** Architecture includes `credential_screen.py` but PRD FR69 and UX spec both exclude any credential UI. Remove from architecture.

2. **Architecture introduces undeclared dependency (`click`):** PRD states single production dependency (`batrachian-toad`). Architecture CLI code uses `click`. Party mode insights already suggest `argparse` but code is not updated. Fix architecture to use `argparse`.

3. **Architecture retains Codespaces references:** PRD explicitly removed all Codespaces references. Architecture deployment model still references them. Clean up.

4. **Epic 8 is a pure technical epic with no user value:** All 8 stories are "As a developer." This violates fundamental epic design principles. Distribute NFR concerns as acceptance criteria into functional epics or reframe around user outcomes.

5. **Stories 1.1-1.4 deliver no user value:** Four consecutive developer infrastructure stories at the start of the backlog. Consolidate as implementation tasks within user-facing stories.

6. **Story 1.2 has a forward dependency:** MCP Server Bootstrap delivers an empty tool list, only useful when later stories add tools. Merge with first tool-registering story.

### Recommended Next Steps

1. **Resolve architecture contradictions (Priority 1):** Remove CredentialSetupScreen, replace `click` with `argparse`, remove Codespaces references, establish authoritative tool count of 18.

2. **Restructure Epic 1 stories (Priority 2):** Consolidate Stories 1.1-1.4 into implementation tasks within user-facing stories. First deliverable story should be "User can launch the app and create a project." Move project listing/resume (FR3, FR4) from Epic 5 into Epic 1.

3. **Resolve Epic 8 (Priority 2):** Either distribute NFR stories as embedded acceptance criteria in Epics 1-7, or reframe each story around user-facing quality outcomes.

4. **Fill UX design gaps (Priority 3):** Add UX designs for FR79 (project completion summary), FR88 (on-demand health check UI), FR5 (archive project), and FR32 (version history interaction).

5. **Fix story-level issues (Priority 3):** Split Story 5.7 into two stories, delineate Story 1.9 vs 8.8 scope, add error condition ACs to Epic 6 stories.

6. **Resolve scope ambiguity (Priority 3):** Make explicit decision on creative freeform mode -- MVP or Post-MVP. PRD and UX spec currently disagree.

7. **Update architecture `state.json` schema (Priority 3):** Add missing fields needed by UX components: `decision_count`, `vault_status`, `checkpoint_history`.

8. **Address minor gaps:** Define NFR-MNT-03 or acknowledge the numbering gap. Define FR85 or remove from coverage map. Add `Ctrl+S` to UX keyboard bindings or remove from architecture.

### Strengths

- **PRD is comprehensive:** 76 active FRs, 43 NFRs, 8 exclusions, 5 design decisions with clear ship-blocking classification
- **100% FR coverage:** Every active FR maps to at least one epic with an explicit coverage map
- **Detailed UX specification:** 135 KB of thorough design with component specifications, interaction patterns, and accessibility considerations
- **Strong traceability:** FR-to-Epic mapping is explicit and complete
- **Good epic sequencing:** Epics 2-7 and 9 show proper user-value focus and sequential independence

### Final Note

This assessment identified **38 issues** across **4 categories** (6 critical, 16 major, 10 minor, 6 warnings). The critical issues center on architecture-PRD contradictions and epic structure violations. None of the issues indicate fundamental design flaws -- they are resolvable through document alignment and story restructuring. Address the 6 critical issues before proceeding to implementation. The remaining issues can be resolved during sprint planning or implementation.

**Assessed by:** Implementation Readiness Workflow
**Date:** 2026-03-10
**Report:** `_bmad-output/planning-artifacts/implementation-readiness-report-2026-03-10.md`
