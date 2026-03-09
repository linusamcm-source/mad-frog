---
stepsCompleted:
  - step-01-init
  - step-02-discovery
  - step-02b-vision
  - step-02c-executive-summary
  - step-03-success
  - step-04-journeys
  - step-05-domain
  - step-06-innovation
  - step-07-project-type
  - step-08-scoping
  - step-09-functional
  - step-10-nonfunctional
  - step-11-polish
  - step-12-complete
inputDocuments:
  - _bmad-output/planning-artifacts/product-brief-mad_frog-2026-03-06.md
  - docs/bmad-toad-integration-spec.md
documentCounts:
  briefs: 1
  research: 0
  brainstorming: 0
  projectDocs: 1
classification:
  projectType: 'Browser-served guided experience (Toad UI / Textual Web)'
  domain: 'Workflow Automation / Agentic Tooling'
  complexity: 'medium-high'
  projectContext: 'greenfield'
lastEdited: '2026-03-09'
editHistory:
  - date: '2026-03-09'
    reason: 'Align PRD with architecture decisions'
    inputDocument: '_bmad-output/planning-artifacts/architecture.md'
    changes:
      - 'CRITICAL: Rewrote Technical Architecture section for three-process model (MadFrogApp + AI Agent + MCP Server)'
      - 'Removed Codespaces references throughout (local Docker Desktop only)'
      - 'Updated all mad_frog serve / toad serve references to mad_frog'
      - 'Replaced credential management UI with Toad delegation model'
      - 'Added first-run workspace setup modal (FR49, user journey)'
      - 'Updated tool count to 18 across 5 categories'
      - 'Added bmad_detect_changes tool reference (FR59)'
      - 'Updated Python version to 3.14, added Node.js dependency'
      - 'Changed bmad rebuild-index from user command to automatic startup rebuild'
  - date: '2026-03-09'
    reason: 'Party Mode validation — 24 findings cross-referencing PRD against architecture'
    inputDocument: '_bmad-output/planning-artifacts/architecture.md'
    changes:
      - 'CRITICAL: Marked FR53-54 as deferred (architecture explicitly defers conversation transcript persistence)'
      - 'HIGH: Marked FR85 as deferred (architecture defers telemetry to post-MVP)'
      - 'HIGH: Added FR8a-8d for 5 onboarding paths (method upgrade, existing git, version mismatch, brownfield)'
      - 'HIGH: Added FR45a for context-aware pre-emptive save (bmad_report_context tool)'
      - 'HIGH: Fixed startup command — removed ~/my-project path argument (workspace modal handles selection)'
      - 'MEDIUM: Fixed service count 8→7 (removed phantom StateFileWriter)'
      - 'MEDIUM: Moved FR55 from Conversation section to Obsidian section (artifact traceability, not transcripts)'
      - 'MEDIUM: Added deployment model section (stateless peer tool)'
      - 'MEDIUM: Added two-phase MCP server lifecycle description'
      - 'MEDIUM: Added two-tier state model summary to State Persistence section'
      - 'MEDIUM: Clarified npx bmad init delegated by project.create() tool'
      - 'MEDIUM: Moved bmad validate-workflow to Post-MVP in Technical Architecture'
      - 'MEDIUM: FR52 replaced with .obsidianignore proposal (original scenario impossible with one-time modal)'
      - 'MEDIUM: FR48 qualified as optimistic wikilink resolution'
      - 'MEDIUM: FR10 clarified as agent-enforced via BMAD workflow instructions'
      - 'MEDIUM: Added FR84a for unwritten artifact detection safety net'
      - 'LOW: Fixed partyModeInsight tool count 15→18 and added WorkspaceSetupScreen'
      - 'LOW: Added WorkspaceSetupScreen to DD5 widget list'
      - 'LOW: FR41 updated with session lock takeover option'
      - 'LOW: Context window risk mitigation updated with bmad_report_context'
      - 'LOW: Phase 2 MCP integration priorities moved from Technical Architecture to Post-MVP'
      - 'LOW: Deferred FRs added to Post-MVP Phase 2 list'
partyModeInsights:
  - 'Git-backed state engine replacing file-based checkpointing (commit per phase, branches for versioning, git-hash as checkpoint PK)'
  - 'SQLite checkpoint index with projects table (multi-project support) and checkpoints table (git SHA as PK, parent_hash foreign key chain)'
  - 'Visual Journey Map sidebar widget (metro-map style, clickable nodes, stale detection with warning indicators)'
  - 'Bind mount persistence (default for non-technical), git remote (opt-in for technical users)'
  - 'Obsidian-native artifact output (frontmatter + wikilinks baked into templates, zero extra code via agent write)'
  - 'Web-first delivery via toad serve (localhost:8000, browser-based, no terminal knowledge required)'
  - 'Toad widget mapping: BMADJourneyMap (Tree-based sidebar), WelcomeScreen, WorkspaceSetupScreen, ConversationPanel; 18 tool functions across project/artifact/state/workflow/session categories'
  - 'MVP scope shift: click-back navigation and stale detection pulled into V1 (cheap with Git); auto-reprocessing deferred to V2'
workflowType: 'prd'
date: 2026-03-06
author: Linus
---

# Product Requirements Document - mad_frog

**Author:** Linus
**Date:** 2026-03-06

## Executive Summary

Mad Frog is an institutional memory engine that happens to produce planning artifacts. It guides users through the BMAD methodology — Analysis, Planning, Solutioning, Implementation — via a browser-based experience where conversational wizards turn vague ideas into actionable, fully-traced project plans.

Users open a browser, see their projects, and step through structured phases. A visual Journey Map in the sidebar shows every milestone. Clicking any past decision reopens it for revision, automatically preserving all downstream work on a separate path. Nothing is ever lost. Six months after launch, a user can trace exactly why the project was scoped the way it was — every decision, every rejected path, every "let's rethink this" moment is preserved and navigable.

Planning artifacts are written as Obsidian-native markdown with frontmatter and wikilinks. As users complete each phase, their briefs, PRDs, architecture docs, and stories appear directly in their Obsidian vault — interlinked, searchable, and visualised in Obsidian's graph view. The planning tool and the knowledge base are the same thing.

Under the hood, a Git-backed state engine tracks every checkpoint and branch point, indexed by SQLite for fast navigation. The user never sees Git or a terminal — the entire experience is served to the browser via Toad UI's web server, launched with a single command from a Dev Container.

Primary users are non-technical planners who need rigorous project planning without methodology overhead, knowledge workers who live in tools like Obsidian, and technical builders who want a structured path from idea to backlog. All three get the same browser UI with zero setup beyond `make start`.

### What Makes This Special

Planning is nonlinear — people backtrack, revise, and branch constantly. Every other planning tool produces a final document and discards the journey. Mad Frog treats the complete decision history as a first-class deliverable. The branching agentic state machine maps directly onto Git's proven branching model, making nonlinear planning native rather than bolted on. The output isn't just a backlog — it's the full intellectual journey that produced it.

## Project Classification

- **Project Type:** Browser-based guided experience (Toad UI / Textual Web)
- **Domain:** Workflow Automation / Agentic Tooling
- **Complexity:** Medium-High
- **Project Context:** Greenfield

## Success Criteria

### User Success

- **First session delight:** Within 15 minutes of first use, the user has seen at least one artifact appear in their Obsidian vault and understood the Journey Map. The "oh, THIS is what this does" moment.
- **Real-time documentation emergence:** Users watch structured artifacts appear in their Obsidian vault as they converse with the agent. The conversation IS the documentation — no separate write-up step.
- **Bidirectional workspace:** Users drop markdown into the project folder — meeting notes, research, sketches — and the agent already knows. "I dropped my budget discussion notes in the folder and the agent referenced them in the next session." No import wizards, no upload flows.
- **Total recall:** When users return days or weeks later, the full decision context is navigable via the Journey Map and Obsidian graph view. Every "why did we decide this?" has an answer.
- **Zero learning curve for the tool itself:** Users comfortable in a browser and Obsidian can operate Mad Frog without any terminal, Git, or methodology knowledge.

### Business Success

- **Active projects (primary):** 200+ projects created across all users within 6 months of public launch.
- **Phase depth:** 40%+ of projects reach Solutioning phase (beyond Brief/PRD).
- **Workflow completion rate:** 60%+ of users who start a project complete at least through the Planning phase.
- **Active contributors:** 10+ community contributors submitting PRs within 6 months.
- **Community signal (secondary):** 500+ GitHub stars, organic mentions in Obsidian community forums, Reddit, and developer blogs.

### Technical Success

- **Data durability:** Zero data loss. Container is fully disposable — all project state persists on the bind mount. Rebuild, restart, or destroy the container with no impact on user data.
- **Proven rebuild guarantee:** CI acceptance test on every PR — spin up container, create project, complete 2 phases, destroy container, rebuild, assert all checkpoints, artifacts, and Journey Map state are identical.
- **Rebuildable index:** SQLite checkpoint index is automatically rebuilt from Git history on every startup. SQLite is a cache, not a source of truth. Tested automatically.
- **State integrity:** Git-backed checkpoints are always consistent. Git is the single source of truth.
- **Sub-second navigation:** Journey Map click-back and artifact loading completes in under 1 second for projects with up to 50 checkpoints.
- **Obsidian compatibility:** All output artifacts render correctly in Obsidian with working frontmatter, wikilinks, and graph view integration. No manual cleanup needed.

### Measurable Outcomes

| Metric | Target | Measurement |
|--------|--------|-------------|
| First artifact in Obsidian | Under 15 minutes from first launch | Session timestamps in Git history |
| Time from idea to first Epic | Under 4 hours of guided sessions | Session timestamps in Git history |
| Active projects created | 200+ in 6 months | SQLite projects table across opted-in telemetry |
| Container rebuild recovery | 100% state preservation | CI acceptance test on every PR |
| Index rebuild | Full SQLite reconstruction from Git | Automated test: delete DB, rebuild, assert parity |
| Obsidian rendering | Zero broken links or frontmatter errors | Automated lint on artifact output |

## Project Scoping & Phased Development

### MVP Strategy & Philosophy

**MVP Approach:** Experience MVP — deliver the core value loop (converse → watch docs appear in Obsidian → navigate the journey) with full BMAD agent capabilities. Prove the institutional memory concept works with the complete agent roster before expanding workflow modes.

**Resource Requirements:** Multi-agent development team leveraging BMAD methodology. The Toad framework and BMAD module provide the foundation; agents handle story implementation, testing, code review, and QA.

### MVP Feature Set (Phase 1)

**Core User Journeys Supported:**
- Sarah (guided workflow, full BMAD phases)
- Alex (guided workflow with adaptive pacing — agent adjusts depth based on user confidence)
- Kai (Obsidian integration, bidirectional workspace)
- Returning User (project resume with context recall)

**Must-Have Capabilities:**
- Dev Container with `make start` → `mad_frog` → browser at localhost:8000
- Welcome screen (start new project / resume existing project)
- Multi-project support (lightweight — project list on welcome screen, branch-prefix isolation in Git, `projects` table in SQLite)
- Guided workflow mode: Analysis → Planning → Solutioning → Implementation
- Adaptive pacing — agent adjusts question depth based on user confidence level (terse confident answers = fewer follow-ups, vague answers = deeper probing). Prompt engineering, not a separate mode
- Git-backed state engine with SQLite checkpoint index
- Journey Map sidebar (metro-map, clickable completed nodes, current position indicator)
- Click-back navigation with version preservation (Git branching under the hood, "time travel" UX)
- Obsidian-native artifact output (frontmatter + wikilinks)
- Bidirectional file workspace (agent reads user-added markdown)
- Full Party Mode — complete agent roster, multi-persona facilitation at any phase
- Full BMAD methodology — all workflows, all agents, no capability restrictions
- Bind mount persistence (container-data separation)
- First-launch workspace setup modal (asks user for project directory path)
- Structured commit metadata for session context recall

**MVP Acceptance Tests (ship-blocking):**
- Container kill/restart recovery — mid-operation kill, restart, assert full state recovery
- 50-checkpoint stress test — assert sub-second Journey Map navigation
- Obsidian output lint — all artifacts have valid frontmatter, wikilinks resolve, graph view works
- Session resume context recall — stop mid-phase, restart, agent's first message references last discussion topic
- Multi-project isolation — create 2 projects, verify no state bleed between them

### Post-MVP Features

**Phase 2 (Growth):**
- Creative freeform mode (River's journey — CIS tools without phase-gates)
- CIS standalone workflows launchable from sidebar
- Phase-contextual CIS suggestions
- Freeform Journey Map (flat session list)
- Freeform-to-BMAD upgrade path
- Stale detection with warning indicators on downstream artifacts
- `bmad validate-workflow` command + CI validation
- Non-software artifact templates
- Git remote opt-in for cross-device portability
- Conversation transcript persistence as Obsidian-native markdown (FR53-54)
- Anonymous usage telemetry via tool call logging (FR85)

**Phase 3 (Expansion):**
- MCP integrations (prioritised): GitHub Projects/Issues → Linear → Jira → Azure DevOps (output format adapts per target)
- Automatic downstream reprocessing (revise Brief → PRD auto-regenerates)
- Branch comparison / diff views between artifact versions
- Mermaid-rendered full project visualisation (exportable)
- Richer Obsidian MCP integration (dashboard notes, auto-tagging)
- Multi-user collaborative sessions
- Non-software domain templates (business strategy, research, event planning)
- Plugin ecosystem for community-contributed workflow modules
- Self-hosted web deployment for team use

### Risk Mitigation Strategy

See the detailed risk mitigation table in Innovation & Novel Patterns for comprehensive risk analysis. Key risks summarised here for scoping context:

- **Technical:** Git state engine reliability — mitigated by chaos testing as ship-blocking acceptance criteria (NFR-REL-10)
- **Market:** Users don't see value vs ChatGPT + Google Docs — mitigated by shipping Obsidian integration in MVP (the real-time "watch docs appear" hook)
- **Resource:** Toad upstream changes — mitigated by pinning version (NFR-INT-02) and testing before adoption

## User Journeys

### Journey 1: Sarah — The Non-Technical Planner

**Who she is:** Sarah is a project manager at a mid-size consultancy. She's brilliant at stakeholder management and strategic thinking but has never opened a terminal in her life. She lives in PowerPoint, Excel, and recently discovered Obsidian for personal knowledge management. She's heard about AI-assisted planning but every tool she's tried feels like it was built for developers.

**Opening Scene:** Sarah has just been given ownership of a new client initiative — a complex digital transformation project. She has a vague brief from the client, scattered notes from three discovery meetings, and a deadline to present a structured project plan in two weeks. She's staring at a blank Google Doc, unsure where to start.

She finds Mad Frog on GitHub. The README has a "Getting Started" section at the top: clone the repo and open in Dev Container with Docker Desktop. She clicks "Open in Dev Container," waits 30 seconds, and a browser tab opens with the Toad UI. On first launch, a modal asks "Where are your projects?" — she enters her Documents folder path. Then the welcome screen appears: three options — "Start a guided project," "Launch a creative session," or "Resume a project." She picks "Start a guided project."

**Rising Action:** Sarah creates her project — "Acme Digital Transformation" — and the system asks which phase she'd like to begin. She starts with Analysis. A friendly agent greets her and begins asking about her client's situation. It feels like talking to a senior consultant.

She drops her meeting notes — three markdown files she'd already been keeping in Obsidian — into the project folder. The agent immediately references them: "I see from your March 3rd notes that the client mentioned concerns about legacy system migration. Let's explore that."

Her eyes widen. She didn't upload anything. She just put files in a folder.

As they talk, she glances at her Obsidian vault. A new note has appeared: `Product Brief - Acme Digital Transformation.md`. It has proper frontmatter, backlinks to her meeting notes, and a structured summary of everything they've discussed. The graph view shows connections forming.

**Climax:** Sarah reaches the Planning phase and invokes Party Mode. Five specialist agents debate her requirements — the architect pushes back on scope, the analyst spots a gap in her market assumptions, the UX designer reframes a user journey she'd missed. She watches, occasionally steering the conversation. When it's done, her PRD has been stress-tested more rigorously than any document she's ever produced.

She clicks back to the Product Brief in the Journey Map — she wants to revise the scope based on what the architect said. The system says: "Going back will create a new version. Your current PRD progress is saved." She clicks confirm, revises the brief, and the PRD node flips to a yellow warning: "Based on an earlier version of your Product Brief." She clicks it, re-runs the Planning phase, and a new PRD emerges — incorporating her revision. The old version is still there if she needs it.

**Resolution:** Two weeks later, Sarah presents to the client. Her plan has Epics, User Stories with acceptance criteria, an architecture overview, and a risk analysis. When the client asks "why did you scope it this way?", she opens her Obsidian vault and walks them through the decision trail. The client has never seen this level of traceability from a PM. Sarah's new reality: she never starts a project without Mad Frog.

**Requirements revealed:** Dev Container setup (Docker Desktop), browser-based access, welcome screen with three entry modes, bidirectional file workspace, real-time Obsidian output, Party Mode at any phase, click-back navigation, stale detection, version preservation, Journey Map sidebar.

### Journey 2: Alex — The Technical Builder

**Who he is:** Alex is a full-stack developer who's been building side projects for years. He's great at coding but terrible at planning — he usually jumps straight to implementation and pays for it later with scope creep and rework. He's tried writing PRDs manually but they always feel like busywork that he abandons halfway through.

**Opening Scene:** Alex has an idea for a developer tool — a CLI that auto-generates API documentation from code comments. He knows the tech but hasn't thought through who'd use it, what the MVP is, or how it's different from existing tools. He opens the Dev Container, runs `make start`, and sees the Toad UI in his browser. He selects "Start a guided project."

**Rising Action:** The agent detects Alex's confidence immediately — his answers are terse, direct, decisive. It adapts: crisp questions: "What problem does this solve? Who's it for? What exists today?" Alex answers quickly, sometimes in bullet points. The agent doesn't mind — it synthesises his terse answers into a structured brief.

He's surprised when the agent pushes back: "You said it's for 'developers' — but which developers? Someone writing a public API has very different needs from someone documenting an internal service." Alex hadn't thought about that. He refines his personas.

Within an hour, he has a Product Brief in his Obsidian vault. He moves to Planning. The PRD takes another two hours of conversation. The agent keeps connecting his answers back to the brief: "This feature wasn't in your MVP scope — do you want to add it or defer it?"

**Climax:** Alex reaches Solutioning and generates Epics and Stories. Each story has acceptance criteria, links back to the PRD requirement it addresses, and clear technical notes. He opens his Obsidian vault and sees the full graph: Brief → PRD → Architecture → Epics → Stories, all interlinked. He can click any story and trace it back to the original requirement, back to the user persona, back to the problem statement.

"This would have taken me a week," he thinks. "And I would have skipped half of it."

**Resolution:** Alex starts coding with a clear backlog. Three weeks in, he realises the architecture needs to change. He opens Mad Frog, clicks back to the Architecture checkpoint in the Journey Map, revises it, and the downstream stories are flagged as stale. He re-runs Solutioning, and the stories update to reflect the new architecture. His Git history shows the exact moment and reason for the pivot. Alex's new reality: planning takes hours, not days, and he never throws away a plan — he evolves it.

**Requirements revealed:** Adaptive pacing (agent adjusts depth based on user confidence), agent pushback on vague answers, artifact interlinking with traceability, efficient session pacing, stale detection and re-run workflow.

### Journey 3: Kai — The Obsidian Knowledge Worker

**Who they are:** Kai is a product strategist at a startup. They've built an elaborate Obsidian vault over two years — daily notes, project folders, research clippings, book highlights, all interconnected with tags and backlinks. Their vault is their second brain. Every new tool they adopt must integrate with it or they won't use it.

**Opening Scene:** Kai has been tasked with defining the product strategy for a new market vertical. They have research scattered across their vault — competitor analyses in one folder, customer interview notes in another, a half-formed thesis in a daily note from last Tuesday. They need to pull it all together into a coherent strategy document with actionable next steps.

They hear about Mad Frog's Obsidian integration. They configure the bind mount to point at their existing vault: `~/ObsidianVault/Projects/new-vertical/`. They run `make start`.

**Rising Action:** Kai drops their existing research files into the project folder — competitor analyses, interview transcripts, market data. The agent loads all of it automatically. "I see you've done extensive competitor analysis. You've identified three main players. Let me build on this."

Kai starts the Analysis phase. As they converse, new notes appear in their vault — but they're not isolated documents. They have `[[backlinks]]` to Kai's existing research: `As identified in [[Competitor Analysis - Q1 2026]], the gap in...`. The Obsidian graph view lights up — their existing knowledge is now connected to structured planning artifacts.

Kai invokes a Design Thinking session with Maya. They run through empathy mapping for their target customers, building on the interview notes already in the vault. The session output — an empathy map and "How Might We" statements — appears as new Obsidian notes, linked to both the interviews and the emerging Product Brief.

**Climax:** Kai finishes the Planning phase and opens Obsidian's graph view. Their vault has transformed. What was a loose collection of research and notes is now a structured knowledge graph: research → brief → PRD → epics, all interconnected with their existing notes via backlinks. They can navigate from a customer quote in an interview transcript to the specific user story it influenced — through the brief, PRD, and epic that connected them.

Their second brain didn't just gain planning artifacts. It gained *structure*.

**Resolution:** Kai presents the strategy to the leadership team using their Obsidian vault as the presentation — clicking through the graph, showing the traceability from research to recommendations. The leadership team approves. Three months later, when priorities shift, Kai opens the Journey Map, clicks back to the strategic assumptions, revises them, and the downstream plan updates accordingly. The vault's graph view shows the fork point — old strategy and new strategy, both preserved. Kai's new reality: Mad Frog isn't a separate tool. It's an extension of their vault.

**Requirements revealed:** Configurable bind mount to existing Obsidian vault, wikilink generation referencing existing vault notes, agent ingestion of pre-existing markdown, graph-view-optimised output structure, Design Thinking CIS integration.

### Journey 4: River — The Creative Professional

**Who they are:** River is a freelance brand strategist. They don't build software — they build brand identities, marketing strategies, and creative campaigns. They've never heard of BMAD, don't know what a PRD is, and wouldn't recognise a user story if it walked up and introduced itself. But they ARE a structured thinker who loves frameworks, and they use Obsidian obsessively for client work.

**Opening Scene:** River has a new client — a sustainable fashion startup that needs a complete brand strategy. River has a mood board, some competitor screenshots, and a gut feeling about the positioning, but nothing structured. They usually free-write in Obsidian until a strategy emerges, but this client needs something rigorous and presentable.

A friend mentions Mad Frog's creative tools. River is sceptical — "isn't that a coding thing?" — but tries it because it works with Obsidian. They open the welcome screen and choose **"Launch a creative session"** — no phases, no methodology jargon. Just a project name and the CIS tools in the sidebar.

**Rising Action:** River launches a brainstorming session with Carson. Carson's energy is infectious: "Let's generate 50 positioning ideas in 10 minutes. No filtering, no judgement. GO." River types fast. Carson builds on every idea: "YES AND — what if that sustainable angle wasn't about guilt but about luxury?" Ideas River would never have reached alone start flowing.

They follow up with an Innovation Strategy session with Victor. Victor reframes the competitive landscape: "Your client isn't competing with other sustainable brands. They're competing with fast fashion on *desire*. How do you make sustainability more desirable than disposability?" River's strategic thesis crystallises.

Each session produces an Obsidian note — the brainstorming output, the innovation strategy framework, the positioning statement — all interlinked and timestamped in the Git history. The Journey Map shows a flat session list:

```
Brand Strategy (freeform)
  - Brainstorming Session 1
  - Innovation Strategy Review
  - Design Thinking Workshop
  - Brand Narrative Draft
```

**Climax:** River runs a Design Thinking session with Maya, empathy-mapping the target customer. Then they invoke Party Mode and ask all the CIS agents to stress-test the brand positioning. The storyteller, Sophia, rewrites the brand narrative. The problem solver, Dr. Quinn, finds a logical gap in the pricing strategy. The brainstorming coach, Carson, suggests a campaign concept that ties everything together.

River watches their Obsidian vault fill with a structured brand strategy — and the complete creative journey that produced it. Every brainstorm, every reframe, every "what if" is preserved. This isn't just a strategy document. It's proof of creative rigour. When River presents to the client and walks them through the Obsidian graph — from raw brainstorm to final positioning through every twist and challenge — the client doesn't just see a recommendation. They see the depth of thinking behind it. For a freelancer, that's the difference between "here's my deliverable" and "here's why I'm worth what I charge."

**Resolution:** River's client approves the strategy and asks them to extend the engagement. River uses Mad Frog for every client now. Six months later, they upgrade one project from freeform to full BMAD mode — the creative sessions become inputs to a structured Analysis phase, and River discovers that the methodology they thought was "a coding thing" is actually how they've always wanted to think. They just needed a non-software door into it.

**Requirements revealed:** Creative freeform mode (no phase-gates), CIS tools accessible without full BMAD workflow, freeform Journey Map (flat session list), upgrade path from freeform to full BMAD, non-software artifact templates, narrative quality in all outputs.

### Journey 5: Community Contributor (Light Journey)

**Who they are:** Morgan is a developer who's been using Mad Frog for their own projects and wants to contribute a new workflow template for data science projects.

**Journey:** Morgan forks the repo, studies the existing BMAD workflow structure (`step-XX.md` files, templates, CSV data), and creates a new "Data Science Project" workflow with domain-specific phases (Data Discovery → Feature Engineering → Model Design → Deployment). They submit a PR. The CI tests validate the workflow structure. The community reviews, iterates, and merges.

**Requirements revealed:** Clear workflow authoring documentation, template/step-file conventions that are learnable, CI validation of workflow structure, contribution guidelines.

### Journey 6: Returning User (Light Journey)

**Who they are:** Any of the above personas, coming back to a project after days or weeks away.

**Journey:** They run `make start`, browser opens, and the welcome screen shows their projects with status: "Acme Digital Transformation — Planning phase, PRD in progress. Last active: 12 days ago." They click in. The Journey Map shows exactly where they left off. The agent greets them with full context: "Welcome back. Last time we were working on the functional requirements section of your PRD. You'd identified three capability areas and we were about to explore the notification system. Ready to continue?"

This context recall works because every Git commit includes structured metadata — not just what files changed, but what was discussed, what decisions were made, and what the next topic was going to be. The agent reads the last commit's metadata and reconstructs the conversational context. It feels like they never left.

**Requirements revealed:** Project resume with context recall, last-active timestamps, structured commit metadata (discussion summary, decisions made, next topic), agent context reconstruction from Git history, welcome screen with project status.

### Journey Requirements Summary

| Capability | Revealed By | Acceptance Test |
|-----------|-------------|-----------------|
| Dev Container setup (Docker Desktop) | Sarah | User opens in Dev Container, reaches welcome screen in under 60 seconds |
| Welcome screen with three entry modes | Sarah, River, Returning User | Welcome screen displays guided, creative, and resume options; each navigates to correct flow |
| Full guided workflow mode | Sarah, Kai | User completes Analysis to Planning with all phase-gate prompts and CIS suggestions |
| Adaptive pacing mode | Alex | Agent detects confident responses and reduces follow-ups; total session time under 3 hours for Brief + PRD |
| Creative freeform mode | River | User launches CIS session without creating a BMAD project; artifacts checkpointed in Git |
| Freeform-to-BMAD upgrade | River | Freeform project converts to guided mode; existing sessions become Analysis phase inputs |
| Browser-based access (`mad_frog`) | Sarah, Kai, River | `make start` launches browser; full UI functional with no terminal interaction |
| Bidirectional file workspace | Sarah, Kai | Drop markdown file into project folder; agent references file content within first 3 interactions of next session |
| Real-time Obsidian output with wikilinks | Sarah, Kai, River | Artifact appears in vault within 10 seconds of phase completion; wikilinks resolve correctly |
| Configurable bind mount to existing vault | Kai | Set vault path in config; artifacts appear in specified location with backlinks to existing vault notes |
| Agent ingestion of pre-existing markdown | Sarah, Kai | Agent references content from user-added files accurately in conversation |
| Party Mode at any phase | Sarah, Alex | Invoke Party Mode mid-phase; multiple agents respond; return to workflow preserves state |
| CIS standalone workflows | River | Launch brainstorming/design thinking/innovation from sidebar; session produces Obsidian artifact |
| CIS phase-contextual suggestions | Sarah, Kai | System suggests relevant CIS engagement after completing a phase |
| Click-back navigation with version preservation | Sarah, Alex, Kai | Click completed node; confirm; workspace reverts; previous version preserved on separate branch |
| Stale detection and re-run workflow | Sarah, Alex | Revise parent artifact; downstream nodes show stale indicator; re-run produces updated artifact |
| Freeform Journey Map (flat session list) | River | Freeform project shows sessions as flat list, not phase tree |
| CIS sub-nodes in Journey Map | Sarah, Kai, River | CIS sessions appear as sub-nodes under parent phase or in flat list |
| Agent pushback on vague inputs | Alex | Agent asks clarifying question when user provides ambiguous persona/scope definition |
| Full artifact traceability | Alex, Kai | Click any story; navigate backlinks through epic to PRD to brief to original requirement |
| Non-software artifact templates | River | Creative freeform produces brand strategy/research artifacts, not PRDs/epics |
| Narrative quality in outputs | River, Sarah | Generated artifacts read as professional prose, not template fill-in |
| Project resume with context recall | Returning User | Stop mid-phase, restart; agent's first message references last discussion topic and pending decisions |
| Structured commit metadata | Returning User | Git commits include JSON metadata: discussion summary, decisions made, next topic |
| Workflow authoring documentation | Community Contributor | New contributor creates valid workflow template following docs without direct assistance |
| CI validation of workflow structure | Community Contributor | PR with malformed step file fails CI; PR with valid structure passes |

## Innovation & Novel Patterns

### Innovation Architecture

Mad Frog's innovations form a deliberate hierarchy — each layer building on the one below:

**Foundation — Git as an Invisible Planning State Machine**
Git's branching model — designed for source code versioning — maps 1:1 to how planning actually works: nonlinear, iterative, with frequent backtracking. Mad Frog repurposes Git's battle-tested infrastructure (commits, branches, tags, diffs) as the backbone of a planning workflow engine. The user never sees Git. They see a time machine — a Journey Map where they can "go back to Tuesday's version" or "see what the project looked like before the scope change." Underneath, every decision is a commit, every revision forks a branch, and every artifact maintains a traceable parent chain. Zero invention risk, maximum architectural leverage.

**Value Proposition — The Decision Journey as a First-Class Deliverable**
Existing planning tools produce final documents — a PRD, a backlog, a strategy deck. The process that created them is lost to Slack threads, meeting notes, and memory. Mad Frog inverts this: the complete intellectual journey — every brainstorm, every rejected path, every "let's rethink this" moment — is preserved, navigable, and presentable. The history IS the product. This is institutional memory as a service.

**Distribution — Integration by Convention (Obsidian-Native Output)**
Rather than building plugins, APIs, or sync layers, Mad Frog writes Obsidian-native markdown (frontmatter + wikilinks) directly to the filesystem via bind mount. The agent's file-write capability IS the integration. Zero dependencies, zero integration code, full Obsidian compatibility including graph view, backlinks, and tag search. This pattern — "integration by convention" — is transferable to any markdown-based tool (Logseq, Dendron, plain filesystem). It reaches Obsidian's 1M+ users without a single line of plugin code.

**Growth — Creative Freeform as a Methodology On-Ramp**
The three-mode welcome screen (guided project, creative session, resume) isn't just a UX pattern — it's a distribution strategy. Non-software users who would never adopt "BMAD methodology" enter through brainstorming and design thinking tools. Over time, they discover that their creative sessions can be upgraded into structured planning workflows. The methodology finds them, not the other way around. This inverts the typical adoption funnel for structured methodologies.

**Experience — Multi-Persona Agentic Facilitation in a Browser**
Party Mode — where distinct specialist agents with unique personalities debate, challenge, and build on each other's perspectives in real time — is a new interaction paradigm. It's not a chatbot. It's a simulated expert panel that stress-tests ideas from multiple angles simultaneously. Delivered via `mad_frog` in a browser, accessible to non-technical users, with the full session checkpointed in Git.

### Market Context & Competitive Landscape

**The real competitor is the status quo.** Today, 90% of AI-assisted planning looks like this: open ChatGPT in a browser, have a conversation, copy-paste the output into Google Docs, lose the context, start over next session. Mad Frog's positioning: "You're already doing this. We make it structured, traceable, and permanent instead of ephemeral chat sessions you'll never find again."

Adjacent products occupy partial overlap but none combine all five innovation layers:

- **ChatGPT / Claude in browser** — ephemeral conversations, no state, no traceability, no methodology. The dominant "tool" for AI planning today.
- **Notion / Confluence** — collaborative docs but no guided methodology, no decision history, no agentic facilitation
- **Linear / Jira** — backlog management but no upstream planning, no traceability to ideation
- **Miro / FigJam** — brainstorming tools but no structured output, no state management, no methodology enforcement
- **Obsidian plugins** — knowledge management but no guided workflows, no agentic interaction

Mad Frog occupies a new category: **agentic planning infrastructure** — a guided, state-managed, multi-agent system that produces traceable planning artifacts as knowledge-base-native markdown.

### Validation Approach

| Innovation | Validation Method | Success Signal |
|-----------|------------------|----------------|
| Git as state machine | MVP chaos testing: mid-commit container kill, restart, assert recovery. Concurrent access: two browser tabs, same project, assert no corruption. Stress test: 100 checkpoints, 10 branches, assert sub-second navigation | Zero state corruption across all chaos, concurrency, and stress scenarios |
| Decision journey as deliverable | Ship and track organic sharing — do users share their Obsidian journey graphs on social media? Organic sharing > controlled user testing | Users voluntarily showcase decision trails in community posts and social media |
| Integration by convention | Automated test suite across Obsidian, Logseq, and plain filesystem | All wikilinks resolve, graph view works, zero manual cleanup across all targets |
| Creative freeform on-ramp | Track freeform-to-guided upgrade rate via opt-in telemetry from day one | 20%+ of freeform users upgrade to full BMAD within 3 months |
| Multi-persona facilitation | Public "PRD challenge" — same product idea, single-agent vs Party Mode, community judges output quality | Party Mode produces PRDs with measurably fewer gaps in community-judged adversarial review |

### Risk Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| Git repository size over time | Slow operations, storage bloat with multi-project, multi-version artifacts | Git LFS for binary artifacts (diagrams, images). Completed projects archived to separate bare repos. Automated `git gc` on container startup. SQLite handles all read queries — Git is write-path only during normal use |
| Users confused by versioning concepts | Abandonment, data anxiety | Mental model is **time travel**, not branching. Users "go back to Tuesday's version," never "checkout a branch." Journey Map shows dates and descriptions, not branch names. Modal confirmations for all destructive-seeming actions |
| Obsidian format changes break compatibility | Broken wikilinks, lost frontmatter | Obsidian's markdown format is stable and community-standard. Automated lint tests catch format issues on every artifact write |
| Creative freeform users never upgrade to structured workflows | CIS becomes a toy, not a pipeline | Phase-contextual suggestions nudge toward structure. Freeform artifacts include "upgrade to full project" prompt after 3+ sessions. Track conversion funnel from day one |
| LLM quality variance across providers | Inconsistent Party Mode quality | Document minimum model capability requirements. Default to most capable available model for Party Mode sessions |
| Agent context window limits | Token exhaustion on large projects with rich history and bidirectional file ingestion | `bmad_report_context` tool queries agent for context window size; silent pre-emptive save at 90% capacity (`[context-save]` commit). Selective context loading: only artifacts relevant to current phase. Commit metadata as compact JSON summaries, not full transcripts |
| Mid-operation container failure | Potential state corruption if container killed during Git write | Chaos testing as MVP acceptance criteria: mid-commit kill, restart, assert full state recovery. Atomic commit operations with rollback on failure |
| Concurrent browser tab access | State corruption from parallel writes | MVP: Single-session enforcement. One active session per project. Second tab receives read-only Journey Map view with "Session active in another tab" indicator. Eliminates concurrency entirely. Post-MVP: evaluate if sequential write queue is needed for multi-user |

## Technical Architecture

### Project-Type Overview

Mad Frog is a browser-served Terminal UI application built on the Toad framework (Textual Web). It is an overlay/composition layer — not a fork. `MadFrogApp` subclasses `ToadApp`, adding BMAD workflow management, state engine, and Journey Map widgets while inheriting Toad's agent layer, settings system, and ACP protocol handling. The startup command is `mad_frog`, wrapped by `make start`. Project selection happens via the welcome screen.

### Deployment Model

Mad Frog is a stateless peer tool, not a container for projects. The tool repo (`mad_frog/`) sits alongside project repos as sibling directories within the user's workspace. Each project is an independent Git repo. All durable state lives in project repositories — the tool is independently upgradeable without affecting any project. Cross-project config is a lightweight path registry in `.vibe/config.yaml`.

### Three-Process Architecture

Mad Frog runs as three cooperating processes:

1. **MadFrogApp** (Process 1) — `MadFrogApp(ToadApp)` subclass. Textual UI: sidebar navigation (Journey Map), welcome screen, workspace setup modal. Watches `.mad_frog/state.json` for MCP server state changes via `watchdog`.
2. **AI Agent** (Process 2) — Claude or any ACP-compliant agent. Launched by Toad. Speaks ACP to Toad (file I/O, terminal) and MCP to our server (BMAD tools).
3. **Mad Frog MCP Server** (Process 3) — stdio MCP server launched by the AI agent. Starts in projectless mode (can list projects, handle config). After `bmad_open_project` or `bmad_create_project`, transitions to project-active mode: exposes full 18 BMAD tools via `tools/list`, manages git state, auto-save timer, state file writer.

### Technical Architecture Considerations

**Agent Provider Layer (Delegated to Toad)**
- Toad manages all LLM provider connections via ACP (Agent Client Protocol)
- Toad manages all credential handling — API keys as environment variables, forwarded via `devcontainer.json` `remoteEnv`
- Mad Frog makes no direct LLM API calls and has no credential UI

**Tool Exposure via MCP Server**
- 18 BMAD tools exposed via a stdio MCP server (JSON-RPC over stdin/stdout)
- AI agent discovers tools via standard MCP `tools/list` — no system prompt injection
- MadFrogAgent overrides `acp_new_session` to inject MCP server via ACP's `mcpServers` parameter
- Agent-agnostic: any ACP agent (Claude, Codex, Gemini, etc.) discovers tools automatically
- Tools across 5 categories: project (6), artifact (3), state (3), workflow (3), session (3+)

**First-Run Workspace Setup**
- On first launch, a browser modal asks "Where are your projects?" — user enters their workspace root path
- Path stored in `.vibe/config.yaml` — one-time setup, never asked again
- Projects are sibling directories within the workspace root
- BMAD method snapshot copied into target projects by `project.create()` tool (which delegates to `npx bmad init` for fresh projects or `npx bmad update` for existing)

**Configuration & Settings**
- Workspace root: collected via first-run modal, stored in `.vibe/config.yaml`
- Project-level configuration (project metadata, phase state) via state file in `.mad_frog/` directory
- Container-level configuration (port, startup mode) via `devcontainer.json` and `Makefile`

**Output Format Strategy**
- **MVP:** Obsidian-native markdown only (frontmatter + wikilinks). All artifacts are markdown files written directly to the project directory
- **Post-MVP:** MCP integrations for external project trackers (see Post-MVP Features Phase 3)

**Extension Model**
- Community-contributed workflow templates are markdown step-files dropped into a designated folder structure
- Follows existing BMAD conventions: `step-XX-name.md` files, `workflow.md` entry point, `templates/` folder, `data/` CSVs
- No plugin registry or build step — file-based discovery at runtime
- Post-MVP: `bmad validate-workflow` command validates structure and runs in CI on PRs

### Implementation Considerations

**Toad Integration Boundary**
Mad Frog is an overlay layer — `MadFrogApp(ToadApp)` subclass pattern:
- Custom widgets: `BMADJourneyMap` (Tree-based sidebar), `WelcomeScreen`, `WorkspaceSetupScreen`
- 18 tool functions exposed via MCP server across 5 categories: `project`, `artifact`, `state`, `workflow`, `session`
- Sidebar extension with Journey Map widget (reads `state.json` via watchdog for cross-process state sync)
- Welcome screen with three-mode entry (guided, creative, resume)
- 7 infrastructure services: GitStateEngine, SQLiteCheckpointIndex, StateOperationQueue, AutoSaveService, SessionLockManager, VaultHealthMonitor, ArtifactValidator
- Toad stays upstream; Mad Frog tracks it as a pinned dependency. Upstream improvements flow in after validation

**Container Architecture**
- Dev Container based on Python 3.14 with Toad and Node.js (required for `npx bmad init`)
- Single production dependency: `batrachian-toad>=0.5.35,<0.7` — GitPython, aiosqlite are transitive via Toad
- `make start` runs `mad_frog`, forwarding port 8000
- Bind mount for persistent state (default: host filesystem via Docker Desktop)
- Agent subprocesses launched by Toad inherit container environment variables

**Keyboard & Interaction Model**
- Full mouse support in browser (click Journey Map nodes, sidebar items, menus)
- Keyboard navigation: `Ctrl+B` toggle sidebar, arrow keys in Journey Map, `Enter` to navigate/expand, `Escape` to dismiss modals
- Conversational input via Toad's existing prompt widget
- Menu selections via Toad's existing menu/list view system

## Functional Requirements

### Project Lifecycle Management

- FR1: User can create a new project with a name from the welcome screen
- FR2: System prevents duplicate project names and guides the user to choose a unique name
- FR3: User can view a list of all existing projects with their current phase and last-active date
- FR4: User can resume any existing project from the welcome screen
- FR5: User can archive a project (hidden from welcome screen, preserved in Git)
- FR6: System creates a Git-backed state record for each new project with branch-prefix isolation
- FR7: System maintains a SQLite checkpoint index with project and checkpoint tables (Git SHA as primary key)
- FR8: System supports one active project session at a time — user switches projects via the welcome screen
- FR8a: User can upgrade a project's BMAD method version to the tool's current version via explicit action. Upgrade copies the latest `_bmad/` snapshot and summarises changes
- FR8b: When opening a directory with `.git/` but no `_bmad/`, system offers to set up BMAD planning in the existing repo
- FR8c: When opening a project whose `_bmad/` method version differs from the tool's version, system prompts user to continue with the project's version or migrate
- FR8d: When opening a directory with `_bmad-output/` artifacts but no structured Git state, system offers to validate existing artifacts and infer phase state (brownfield onboarding)

### Guided Workflow Engine

- FR9: User can progress through BMAD phases sequentially (Analysis → Planning → Solutioning → Implementation)
- FR10: Phases require validated artifacts to unlock — enforced by agent via BMAD workflow instructions, not by system-level phase gates. Artifacts can be generated conversationally or imported with agent validation
- FR11: User can import existing artifacts and have the agent validate them to mark a phase complete
- FR12: Agent adapts conversational approach based on user response patterns — probes deeper on vague inputs, moves faster with confident responses
- FR13: User can invoke any BMAD workflow available in the installed module during the appropriate phase
- FR14: System creates a Git commit with structured metadata at each phase completion (discussion summary, decisions made, next topic)
- FR15: System loads the appropriate agent context and workflow instructions when transitioning between phases
- FR16: User can ask the agent for help or explanation at any point without losing workflow progress
- FR17: User can request a current project status summary at any time (phase, progress, what's next)
- FR18: User can request to revisit and revise a previous answer within the current session

### Solutioning & Implementation

- FR19: User can generate architecture decision records during Solutioning phase
- FR20: User can generate epics from PRD requirements
- FR21: User can generate user stories with acceptance criteria from epics
- FR22: System maintains traceability links between stories, epics, PRD, and brief
- FR23: User can generate sprint plans that sequence stories into sprints
- FR24: Implementation phase MVP scope: sprint plan and story file generation. Code review, QA automation, and retrospective are Phase 2

### Journey Map & Navigation

- FR25: User can view a visual Journey Map in the sidebar showing all phases and their completion state
- FR26: Journey Map nodes display three visual states: completed (clickable), in-progress, locked
- FR27: Journey Map nodes display dates and human-readable descriptions (no technical identifiers)
- FR28: User can click any completed phase node in the Journey Map to navigate back to that checkpoint
- FR29: Click-back navigation presents a confirmation modal before creating a new version
- FR30: System preserves all downstream work on a separate Git branch when user navigates back
- FR31: System displays the current position in the Journey Map with a distinct indicator
- FR32: User can view version history for any completed phase node
- FR33: User can create a manual checkpoint with a custom label at any point during a session
- FR34: Journey Map sidebar scrolls vertically when content exceeds viewport height; completed phases can be collapsed
- FR35: System manages Git branches internally — users never see branch names, commit hashes, or Git terminology
- FR36: System displays dates and times in the user's local timezone

### State Persistence & Recovery

State follows a two-tier model: **Tier 1 (durable)** — Git commits, artifact files, decision registry, `_bmad/` snapshot (survives container destruction). **Tier 1.5 (reconstructable)** — SQLite checkpoint index (rebuilt from Git on startup). **Tier 2 (session)** — conversation buffer, workflow position, in-progress drafts (lost on restart, rebuilt from Tier 1 on resume). Maximum data loss: last auto-save interval (~2 min) + uncommitted conversation.

- FR37: System persists all project state to a bind-mounted directory on the host filesystem
- FR38: System fully recovers all project state after container rebuild, restart, or destruction
- FR39: System stores session context in Git commit metadata sufficient for agent context reconstruction
- FR40: Agent greets returning users with context from their last session (last topic, pending decisions, next steps)
- FR41: Single active session enforced per project — second browser tab receives read-only Journey Map view with artifact browsing, or the option to take over the session lock (gracefully degrading the original session)
- FR42: System ensures artifact write and Git commit are atomic — both succeed or both roll back
- FR43: System auto-saves uncommitted changes every 2 minutes via deterministic commit templates. Intentional checkpoints (phase completion or manual save) use structured metadata commits. Auto-save commits are filtered from the Journey Map display
- FR44: System detects state format version on startup and performs any necessary migrations
- FR45: System handles browser disconnection gracefully — user can reconnect and resume from last stable state
- FR45a: System silently pre-empts context window exhaustion by querying agent context budget via `bmad_report_context` tool and triggering an automatic save (`[context-save]` commit) when usage exceeds 90% — no user notification required

### Obsidian Integration

- FR46: System writes all artifacts as Obsidian-native markdown with YAML frontmatter and wikilinks
- FR47: System generates wikilinks that reference other project artifacts (e.g., PRD links to Product Brief)
- FR48: Agent generates optimistic wikilinks to pre-existing vault notes when referencing user-provided content (best-effort resolution — full vault indexing deferred to post-MVP)
- FR49: User configures workspace root via first-run modal. Projects within the workspace that are inside an Obsidian vault are auto-detected via `.obsidian/` parent walk
- FR50: System generates artifacts that render correctly in Obsidian's graph view with working backlinks
- FR51: Artifacts include Obsidian-compatible frontmatter (aliases, tags, phase, project, parent references)
- FR52: For vault-resident projects, system proposes `.obsidianignore` entries for `.git/`, `src/`, `_bmad/` during project setup
- FR55: Any artifact can be traced through its full parent chain to the original requirement via wikilinks

### Conversation & Transcript Management (Deferred — Post-MVP)

- ~~FR53: System persists conversation transcripts as structured Obsidian-native markdown files linked to checkpoints via wikilinks~~ (Deferred: decision registry + Git metadata sufficient for MVP)
- ~~FR54: Conversation transcripts include frontmatter identifying phase, checkpoint, date, and participating agents~~ (Deferred: decision registry + Git metadata sufficient for MVP)

### Bidirectional File Workspace

- FR56: User can add markdown files to the project folder at any time
- FR57: Agent automatically ingests user-added markdown files as context in subsequent sessions
- FR58: Agent references content from user-added files accurately in conversation
- FR59: System detects new, modified, or deleted files in the project folder via `bmad_detect_changes` tool (compares current filesystem against last git commit) and handles changes gracefully
- FR60: System tracks markdown files in Git — binary files in the project folder are accessible to the agent but not version-tracked

### Multi-Agent Facilitation (Party Mode)

- FR61: User can invoke Party Mode at any point during any workflow phase
- FR62: System loads the complete agent roster from the installed BMAD agent manifest
- FR63: System selects 2-3 most relevant agents per discussion round based on topic analysis
- FR64: Agents maintain distinct personalities, communication styles, and expertise boundaries
- FR65: System visually identifies each agent in Party Mode with their name, icon, and distinct styling
- FR66: Agents can reference and build on each other's contributions within a round
- FR67: System halts and waits for user input when an agent asks a direct question
- FR68: User can exit Party Mode and return to the guided workflow with state preserved

### Credential & Provider Management

- FR69: Toad manages all credential validation and provider setup — Mad Frog has no credential UI
- FR70: API keys are forwarded from host environment via `devcontainer.json` `remoteEnv`
- FR71: Toad manages all LLM provider connections — Mad Frog makes no direct LLM API calls

### Container & Access

- FR72: User can launch the full application via `make start` which runs `mad_frog`
- FR73: System serves the complete UI to a browser at localhost:8000
- FR74: On first launch, system displays a workspace setup modal asking user for their project directory path. Path is stored and never asked again
- FR75: System forwards the serve port automatically in Dev Container environments
- FR76: System performs health checks on startup (Git repo, SQLite index, bind mount) and reports issues with recovery guidance
- FR77: System integrates project state management with Toad's existing session infrastructure rather than replacing it

### User Experience & Feedback

- FR78: System provides phase completion feedback including artifact summary, decisions made, and next phase preview
- FR79: System presents project completion summary showing all artifacts created, total decision history depth, and link to view full project graph
- FR80: System generates artifacts as professional narrative prose, not template fill-in
- FR81: Agent has access to all previous decisions and constraints when generating responses within a session
- FR82: System handles agent response failures gracefully with clear feedback and option to retry
- FR83: System displays clear error messages when state operations fail and offers recovery guidance
- FR84: Keyboard navigation available for all primary interactions
- FR84a: System detects artifact-like content in conversation (structured markdown with frontmatter) that was not saved via a tool call, and prompts the user to save it

### Telemetry (Deferred — Post-MVP)

- ~~FR85: User can opt in to anonymous usage telemetry (project count, phase completion rates, session duration, feature usage)~~ (Deferred: trivial to add later via tool call logging)

### Extension & Community

- FR86: Community contributors can add new workflow templates by placing markdown step-files in the designated folder structure
- FR87: System discovers workflow templates at runtime from the file system (no build step or registry)
- FR88: System provides an on-demand health check accessible from the UI (sidebar action or settings menu) that reports project integrity status including total checkpoints, total artifacts, Git repository status, SQLite index consistency, and any orphaned files

### Explicit MVP Exclusions

- EX1: System does NOT execute code or run builds
- EX2: System does NOT connect to external services (no API calls to GitHub, Jira, etc.)
- EX3: System does NOT modify files outside the project folder / bind mount
- EX4: System does NOT store credentials — delegates entirely to Toad/agent env vars
- EX5: System does NOT perform automatic downstream reprocessing when a parent artifact changes
- EX6: Mobile browser support is not guaranteed — system targets desktop browsers
- EX7: In-app search is not provided — search is delegated to Obsidian's native search capabilities
- EX8: Concurrent different-project tabs are not supported — one active project at a time

### Design Decisions

- DD1: Mental model is "time travel," not "branching" — all UX language uses temporal metaphors
- DD2: Search is delegated to Obsidian — Mad Frog does not duplicate search functionality
- DD3: Agent introduces concepts naturally during conversation rather than a separate onboarding tutorial
- DD4: Conversation transcripts stored as separate markdown files, not loaded into agent context by default — agent searches them on demand
- DD5: Widget components (BMADJourneyMap, WelcomeScreen, WorkspaceSetupScreen, ConversationPanel) are designed as independently testable units via Textual's pilot testing framework — this is an architectural constraint, not a runtime quality attribute

## Non-Functional Requirements

### Performance

- NFR-PERF-01: Journey Map renders and responds to click navigation within 500ms for projects with up to 50 checkpoints
- NFR-PERF-02: Atomic artifact-write-plus-commit operations complete within 3 seconds on standard hardware. Operations exceeding 3 seconds display a progress indicator. Tested against both native Linux bind mount and Docker Desktop macOS VirtioFS
- NFR-PERF-03: Welcome screen project list loads within 1 second for up to 20 projects
- NFR-PERF-04: SQLite checkpoint queries return within 100ms for projects with up to 200 checkpoints
- NFR-PERF-05: Browser UI remains responsive (no frozen frames) during agent processing — loading indicators displayed for operations exceeding 500ms
- NFR-PERF-06: Container cold start (from `make start` to browser-ready) completes within 30 seconds on a standard development machine
- NFR-PERF-07: System disk footprint remains under 500MB per project for projects with up to 100 checkpoints and 50 artifacts. Git garbage collection runs automatically on container startup
- NFR-PERF-08: System warm restart (container restart with existing state) completes health checks and reaches browser-ready within 15 seconds, including recovery from incomplete operations
- NFR-PERF-09: System remains responsive after 4 hours of continuous use with no memory leaks. Textual Web server memory consumption stays below 512MB for a single active session. Tested via accelerated memory pressure simulation — 1000 rapid interactions compressed into 10 minutes, memory sampled at intervals, linear regression asserts no upward trend exceeding 5% of baseline
- NFR-PERF-10: After Journey Map navigation to a completed checkpoint, the workspace panel displays the artifact content within 2 seconds. Agent context reconstruction (for resuming conversation at that checkpoint) completes within 5 seconds. Total user-perceived latency from Journey Map click to fully rendered workspace content: under 3 seconds (excluding agent context reconstruction)
- NFR-PERF-11: System handles individual artifact files up to 500KB without performance degradation in workspace panel rendering. Artifacts exceeding 500KB display a warning suggesting the user split the content. Git operations remain performant with individual files up to 1MB

### Security

- NFR-SEC-01: API keys are never logged, displayed in UI, or written to any artifact or Git history
- NFR-SEC-02: `.env` files containing credentials are gitignored by default and verified on startup
- NFR-SEC-03: System does not transmit project data to any external service except the configured LLM provider via Toad's agent protocol. Tested via network traffic capture during a complete workflow session — all outbound connections logged and validated against an allowlist containing only the configured LLM provider endpoint
- NFR-SEC-04: System reads and writes only within the configured project directory and the SQLite database path. System does not traverse parent directories, access other bind mounts, or modify system files. Tested via filesystem access audit in CI

### Reliability & Data Integrity

- NFR-REL-01: Zero data loss guarantee — all committed state survives container destruction and rebuild
- NFR-REL-02: Atomic checkpoint operations — artifact write + Git commit succeed together or both roll back. No partial state
- NFR-REL-03: SQLite index rebuild (triggered automatically on startup) deletes the existing SQLite database, reconstructs it from Git history, and produces a byte-identical database to the original (verified by checksum comparison). Test: create project, complete 3 phases, checksum DB, delete DB, restart, checksum again, assert match
- NFR-REL-04: System recovers gracefully from mid-operation container kill — startup detects and resolves incomplete Git operations
- NFR-REL-05: Browser disconnection does not corrupt state — user reconnects to last stable checkpoint
- NFR-REL-06: System startup health check validates: Git repo integrity (`git fsck`), SQLite index consistency (checksum verification against Git state), bind mount read/write accessibility, and state format version compatibility — completing within 10 seconds. If any check fails, system displays specific diagnosis (not generic errors) and recovery guidance referencing a concrete action. System does not accept user interaction until all health checks pass or user explicitly acknowledges degraded mode
- NFR-REL-07: Session lock acquisition is atomic. If two browser connections attempt to start a session within the same 100ms window, exactly one succeeds and the other receives the read-only view. Tested via automated concurrent connection test
- NFR-REL-08: On-demand health check (FR88) completes within 5 seconds and reports all metrics in a single summary view
- NFR-REL-09: System detects network connectivity loss during agent interaction and preserves all conversation state up to the last complete agent response. User receives clear feedback ("Connection to AI provider lost — your progress is saved") with option to retry when connectivity returns. No partial agent responses are committed to state
- NFR-REL-10: System passes a chaos test suite comprising 5 individual test cases: (a) container kill during Git commit, (b) container kill during SQLite write, (c) container kill during artifact file write, (d) browser disconnect during agent response, (e) disk full during write operation. In all cases, system recovers to last consistent state on restart with zero data loss. Each scenario is independently pass/fail. Failure in any single scenario blocks ship. Ship-blocking MVP acceptance test

### Accessibility

- NFR-ACC-01: All primary interactions (navigation, menu selection, form input) are keyboard-accessible
- NFR-ACC-02: UI text elements (Journey Map labels, menu items, status indicators, modal content) maintain minimum 4.5:1 contrast ratio against their background. Agent conversation text inherits Toad's default theme contrast. Contrast ratios validated via manual inspection of theme CSS values against WCAG AA calculator; automated regression via Textual snapshot comparison to detect unintended theme changes
- NFR-ACC-03: Journey Map node states are distinguishable by shape/icon in addition to colour (not colour-only signalling)
- NFR-ACC-04: Error messages and status indicators use text labels, not icon-only communication

### Integration & Compatibility

- NFR-INT-01: All generated artifacts pass automated validation: (a) YAML frontmatter parses without errors, (b) all `[[wikilinks]]` resolve to existing files within the project directory, (c) frontmatter `aliases` and `tags` fields are present and non-empty. Graph view rendering validated via manual QA checkpoint — explicitly documented as a manual gate, not automated
- NFR-INT-02: System declares a pinned Toad version in dependency configuration. Upstream Toad updates are validated against the full test suite before version bump. No automatic upstream adoption
- NFR-INT-03: Generated markdown is CommonMark-compliant and renders correctly in standard markdown viewers (not only Obsidian)
- NFR-INT-04: Git operations use standard Git commands — no reliance on Git extensions or non-standard features
- NFR-INT-05: System runs on Docker Desktop (macOS, Windows, Linux) without platform-specific configuration
- NFR-INT-06: System handles UTF-8 encoded markdown files with Unicode content, including emoji, CJK characters, and diacritics. File paths with spaces and standard special characters (parentheses, hyphens, underscores) are supported. Filenames with characters illegal on Windows (`<>:"/\|?*`) are rejected with clear error message

### Observability

- NFR-OBS-01: State operation logs are structured (JSON format), include operation type, timestamp, affected artifact, and outcome (success/failure). Log files are rotated at 10MB to prevent unbounded growth. Logs are retained within the project directory for the lifetime of the project
- NFR-OBS-02: Error log entries include: failed operation identifier, system state snapshot before failure, error classification (recoverable/fatal), and specific recovery action. No error message displays a raw stack trace or technical identifier to the user

### Maintainability

- NFR-MNT-01: State format includes a version identifier — system detects version mismatches on startup and performs automated migrations
- NFR-MNT-02: Workflow templates follow documented conventions — `bmad validate-workflow` catches structural errors before runtime
- NFR-MNT-04: State format migrations are non-destructive — original state preserved via Git tag before migration. Migration completes within 30 seconds for projects with up to 200 checkpoints. Migration failures roll back cleanly with user-facing error message
- NFR-MNT-05: Core state operations (checkpoint creation, branch management, index queries, atomic commits, rollback) maintain 90%+ branch coverage. Journey Map widget and workspace panel maintain 80%+ line coverage via Textual pilot tests. Coverage thresholds enforced in CI — PRs that drop below threshold are blocked
- NFR-MNT-06: New frontmatter fields added in future versions are additive only — V1 artifacts render correctly in V2 without migration. Tested via backwards compatibility test suite that validates all V1 fixture artifacts against current version

### User Experience Quality

- NFR-UX-01: Generated artifacts pass automated structural validation: frontmatter completeness, section coherence (no orphaned headers), wikilink resolution, and minimum content length per section. Prose quality validated via human review during acceptance testing — explicitly documented as a manual QA gate

### Ship-Blocking Priority

| Priority | NFRs |
|----------|------|
| **Ship-blocking (MVP must pass)** | REL-01, REL-02, REL-06, REL-07, REL-10, PERF-01, PERF-06, SEC-01, SEC-02, INT-01 |
| **Important (target for MVP)** | PERF-09, REL-09, OBS-01, OBS-02, MNT-05, INT-06 |
| **V2 quality gates** | MNT-06, PERF-07 |
