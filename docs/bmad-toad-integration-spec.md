# BMAD Method & Toad UI Integration Specification

## Overview
This document specifies the architecture and implementation plan for integrating the **BMAD (Build, Measure, Adapt, Deploy) Methodology** into the **Toad UI agentic framework**. The goal is to provide a guided, zero-configuration experience for non-technical users, allowing them to traverse the BMAD lifecycle directly from the Toad UI's left-hand sidebar.

## Objectives
1. **Guided Experience:** Abstract the complexity of the BMAD method's Markdown-based prompts and directory structures into an interactive, step-by-step UI wizard.
2. **Seamless UI Integration:** Leverage Toad's Textual-based `SideBar`, `Menu`, and `Panel` widgets to present the BMAD workflows.
3. **Agentic Automation:** Enable Toad's underlying agents to parse user inputs at each step and automatically advance the BMAD state machine (from Analysis to Implementation).

---

## Architecture & Integration Strategy

### 1. Sidebar Structure (`SideBar` Widget)
The BMAD methodology consists of distinct phases that perfectly map to Toad's `Collapsible` or `Panel` sections within the `SideBar` container. 

The left-hand sidebar should be updated to include a **"BMAD Methodology"** binding group, categorized into the following collapsible sections:

*   **Phase 1: Analysis & Research**
    *   Create Product Brief
    *   Domain Research
    *   Market Research
    *   Technical Research
*   **Phase 2: Planning & Design**
    *   Create Product Requirements Document (PRD)
    *   Create UX Design
*   **Phase 3: Solutioning**
    *   Create Architecture Decision Records (ADR)
    *   Design Epics & Stories
    *   Implementation Readiness Check
*   **Phase 4: Implementation & Agile**
    *   Sprint Planning
    *   Development (Quick Dev / Story Dev)
    *   Code Review & QA
    *   Sprint Retrospective

### 2. Guided State Machine (The "Wizard" Flow)
Each phase contains a sequence of steps (e.g., `step-01-init.md` to `step-06-complete.md`). Toad UI will manage the state of the active project.

*   **UI Component (`ListView` / `Menu`):** When a user clicks a workflow (e.g., "Create Product Brief") in the Sidebar, Toad UI will render a guided `Menu` in the main workspace. 
*   **Step-by-Step Prompting:** Instead of asking the user to read the `step-xx.md` files, Toad will render the content of each step as an interactive conversational prompt using its messaging interface.
*   **Agentic Handoff:** As the user answers questions (e.g., "What is the vision for your product?"), the active Toad agent (e.g., `Analyst`, `PM`, or `Architect`) will process the input, generate the required artifacts (like `product-brief.md`), and automatically transition the UI to the next logical step.

### 3. Modifying Toad UI (`src/toad/widgets/`)

To implement this, the following Toad UI modifications are required:

1.  **Extend `SideBar` (`src/toad/widgets/sidebar.py`):**
    *   Inject a new module: `BMADSideBar(containers.Vertical)`.
    *   Use `SideBarCollapsible` for each of the 4 BMAD phases.
    *   Populate each collapsible with `Action` buttons that dispatch events (e.g., `messages.BMADWorkflowStart(workflow="create-prd")`).

2.  **State Management (`src/toad/app.py` or Session Controller):**
    *   Listen for `BMADWorkflowStart` events.
    *   Load the corresponding workflow YAML/MD from the BMAD module directory (e.g., `bmm/workflows/1-analysis/create-product-brief/steps/`).
    *   Initialize a specific agent context (`pm.agent.yaml` or `architect.agent.yaml`) based on the selected workflow.

3.  **Conversational Menus (`src/toad/menus.py`):**
    *   Introduce a `BMADWizardMenu` that subclasses `Menu(ListView)`.
    *   The menu will display predefined options parsed from the BMAD `workflow.md` checklists (e.g., [Continue], [Revise Vision], [Skip to Research]).

---

## Implementation Plan for Agents

Agents building out this functionality should follow these steps:

### Phase A: Data Ingestion & State Parsing
1. Parse the BMAD `_bmad-output/implementation-artifacts/repos/bmad-method.xml` structure to create a Python-native state machine map (e.g., converting the `step-XX.md` sequences into an ordered JSON/Dict structure).
2. Create a `BMADStateManager` class in Toad that tracks the current project's progress through the phases.

### Phase B: UI Scaffolding
1. Update `toad.xml` UI definitions to include the new `SideBarCollapsible` groups.
2. Bind the new sidebar items to Toad's `OptionList` or `Menu` system so clicking an item changes the central workspace view.

### Phase C: Agent Integration
1. Map BMAD personas to Toad agents (e.g., Map BMAD's `tech-writer.agent.yaml` to a Toad conversation session).
2. Implement file-writing hooks: When a phase completes (e.g., "Create PRD" reaches `step-12-complete.md`), Toad must automatically write the resulting `prd-template.md` to the user's workspace using `write_file` or equivalent agent actions.

## User Experience Example

1. **User opens Toad.** The left Sidebar shows "BMAD Methodology".
2. **User clicks "Phase 1: Create Product Brief".** 
3. **Main View updates:** A welcome message introduces the Analyst agent. A `Menu` appears asking: "Would you like to start a new brief or upload existing context?"
4. **User selects "Start New".** Toad reads `step-02-vision.md` and asks the user for their vision.
5. **Conversational loop:** The user chats natively. Toad's agent ensures all required metrics, scopes, and user personas are gathered, checking off internal checklist items automatically.
6. **Completion:** Toad generates the final Markdown artifact, saves it, and the Sidebar updates to visually unlock "Phase 2: Planning & Design".