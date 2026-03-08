---
stepsCompleted:
  - 1
  - 2
  - 3
  - 4
  - 5
  - 6
inputDocuments:
  - _bmad-output/implementation-artifacts/repos/toad.xml
  - docs/bmad-toad-integration-spec.md
date: 2026-03-06
author: Linus
---

# Product Brief: vibe_visualiser

<!-- Content will be appended sequentially through collaborative workflow steps -->

## Executive Summary

The Vibe Visualiser project aims to democratize the BMAD (Build, Measure, Adapt, Deploy) methodology and agentic workflows by making them accessible to non-technical users via the Toad UI framework. Currently, the complexity of agent-driven workflows restricts their use to technical users. By leveraging Toad UI within a Dev Container, Vibe Visualiser provides a seamless, cross-platform terminal interface where users simply run `make start` to initiate or resume their projects. 

Crucially, Vibe Visualiser acts as a **Branching Agentic State Machine**. It provides dynamic, schema-validated guardrails that enforce the discipline of the BMAD methodology without overwhelming the user. To ensure rapid delivery, the MVP will focus on a "Thin Slice" approach: establishing file-based checkpoints and the native Toad UI state indicator to provide strict phase validation. Future iterations will introduce automated downstream reprocessing for complex branching. The system ensures every phase is fully completed and validated before unlocking the next, providing a paved, error-free road from a vague idea straight to actionable Agile user stories.

---

## Core Vision

### Problem Statement
Non-technical users cannot leverage the BMAD methodology or agentic workflows due to high technical barriers, leaving a powerful paradigm untapped. Without structured, built-in guardrails, even those who attempt these workflows often experience logic gaps and confusion, resulting in "spaghetti plans."

### Problem Impact
If left unsolved, fewer people will adopt agentic workflows, confining this transformative technology to a small technical niche. Furthermore, unstructured workflows lead to "garbage-in, garbage-out," resulting in poorly defined Epics and unactionable backlogs.

### Why Existing Solutions Fall Short
Agentic workflows are in an early stage, and current options are too complex or lack an accessible, guided interface. There is no standardized, state-managed way to engage with the BMAD method that actively validates user input and handles non-linear iterations gracefully.

### Proposed Solution
A terminal-based guided experience built on the Toad UI framework, delivered via a universally compatible Dev Container. Vibe Visualiser manages user progress via strict phase gates (Analysis → Planning → Solutioning → Implementation), providing contextual awareness through an omnipresent state indicator and "restore" functionality in the sidebar. The delivery strategy focuses on an MVP that immediately implements file-based schema validation and basic phase-gates.

### Key Differentiators
- **Branching Agentic State Machine:** Strict schema validation ensures the output of one stage is pristine before unlocking the next. If a past phase is edited, a new immutable branch is forked.
- **Thin-Slice MVP Delivery:** Focuses on immediate value by establishing the core Dev Container setup, Toad UI Sidebar, and foundational phase validation first, reserving complex auto-reprocessing for V2.
- **Fail-Safe Guided Workflows:** Enforces the discipline of the BMAD methodology invisibly, dotting every 'i' and crossing every 't'.
- **Universally Accessible:** Built on Toad UI and packaged in a Dev Container for a frictionless, cross-platform setup (`make start`).

## Target Users

### Primary Users

**Non-Technical Planners (e.g., Sarah, Project Manager)**
- **Context & Motivation:** Sarah oversees complex projects, timelines, and brainstorming sessions. She needs to ensure that every aspect of a project is thoroughly planned without missing logical gaps or bugs in the strategy.
- **Problem Experience:** Without a guided methodology, executing rigorous, multi-layered planning processes (like advanced elicitation or "Party Mode" reviews) is difficult and error-prone.
- **Success Vision:** Success means having a complete, reliable project plan with agile timelines connecting Epics to User Stories. She values the peace of mind knowing she has covered all bases and utilized AI-driven methodologies to stress-test her plans.

**Technical Builders (e.g., Alex, Software Developer)**
- **Context & Motivation:** Alex builds software, firmware, or data engineering projects and is new to the BMAD method. He wants to execute code efficiently but needs a solid foundation of requirements.
- **Problem Experience:** Planning is often a chore, and manual creation of comprehensive user stories and acceptance criteria is time-consuming and prone to oversight.
- **Success Vision:** Alex steps through the guidelines, resulting in a pristine backlog of Epics and User Stories with clear acceptance criteria. His ultimate success is automating the handoff—e.g., using an MCP to push the generated backlog (in a strict JSON/YAML schema) directly to GitHub Projects for his team to build.

### Secondary Users
*(N/A)*

### User Journey

**Discovery & Onboarding**
- **Sarah & Alex:** They discover Vibe Visualiser as an accessible tool (`make start`). They launch the Toad UI Dev Container and are immediately presented with a polished, guided wizard that completely abstracts away the intimidating terminal feel.
- **Differentiated Paths:** The system immediately forks their experience: Sarah enters the "Discovery Track" for deep, methodical planning, while Alex enters the "Fast-Track Execution" for streamlined requirements generation.

**Core Usage & "Aha!" Moment**
- **Sarah's Journey:** Her "Aha!" moment occurs when she uses iterative tools like "Party Mode" and "Advanced Elicitation." She realizes the UI actively iterates with her, finding holes in her logic and automatically updating downstream Epics.
- **Alex's Journey:** His "Aha!" moment is realizing the strict guardrails automatically cover edge cases. He finishes the Solutioning phase and instantly receives perfectly formatted User Stories ready for the MCP handoff to GitHub.

**Long-Term Impact**
- Vibe Visualiser becomes the mandatory first step of any initiative, seamlessly bridging the gap between high-level vision and granular technical execution (like GitHub Actions and Project Issues).

## Success Metrics

### User Success
- **Drastic Efficiency Gains:** The primary indicator of user success is massive time savings. Users like Sarah and Alex should be able to turn days of manual project planning, brainstorming, and ticket-writing into a few guided hours.
- **Ease of Organization:** Success is achieved when users feel the tool makes it inherently easier to organize their project needs without feeling lost in the methodology.
- **High-Value Output:** The moment a user realizes Vibe Visualiser is "worth it" is when they finish a workflow and instantly receive a comprehensive set of Epics and User Stories that they can immediately act on.

### Business Objectives
- **Project Adoption (0-6 Months):** Establish Vibe Visualiser as a reliable, go-to tool for planning new projects and initiatives, both internally and within the broader open-source community.
- **Community Growth:** Drive awareness and adoption, measured by an increase in GitHub stars, active contributors, and community feedback.
- **Demonstrable ROI:** Prove that using the Vibe Visualiser and the BMAD methodology yields a significantly faster time-to-market for software projects.

### Key Performance Indicators (KPIs)
- **Time-to-First-Epic:** Reduce the average time taken from initial project ideation to a fully generated Epic and User Story backlog by 80% compared to manual processes.
- **Session Output Volume:** Track the number of actionable artifacts (User Stories, Acceptance Criteria, Architecture Docs) successfully generated per completed session.
- **Workflow Completion Rate:** Measure the percentage of users who start a workflow (e.g., `make start`) and successfully navigate through to the Implementation phase without abandoning the tool.
- **Community Metrics:** Track GitHub stars, repository forks, and active community contributors within the first 6 months.

## MVP Scope

### Core Features
- **Toad UI Dev Container Environment:** A fully functional, universally accessible terminal UI launched via `make start`.
- **Guided Analysis & Brainstorming:** Interactive workflows that guide the user through the initial BMAD research and brainstorming processes.
- **Core Planning Artifacts:** Guided generation of the Product Brief, Product Requirements Document (PRD), and Architecture decisions.
- **Epic & User Story Generation:** The ability to "shard" the high-level plan into concrete Epics and slice those Epics into actionable, fully fleshed-out User Stories with Acceptance Criteria.
- **File-Based Checkpointing:** A simple, file-system-level state management system that provides basic guardrails to ensure phases are completed in order.

### Out of Scope for MVP
- **Automated Downstream Reprocessing:** The complex logic required to automatically rewrite downstream files when a user alters a previous checkpoint will wait for Version 2.0. In V1, changing a past checkpoint will feature an explicit UX warning that downstream state must be reset to prevent "spaghetti plans."
- **Direct GitHub/MCP Integration:** While the MVP will output perfectly formatted JSON/YAML files for Epics and Stories, automatically pushing these to a remote tracker (like GitHub Projects) via MCP is deferred to V2.

### MVP Success Criteria
- **Successful End-to-End Generation:** A user successfully runs `make start`, navigates the Analysis and Planning phases, and outputs a complete, usable backlog of User Stories without encountering logic gaps or perceived data-loss bugs.
- **Positive User Feedback:** Users report that the terminal UI successfully abstracted away methodology complexity and prevented "spaghetti plans."

### Future Vision
- **V2 and Beyond:** Vibe Visualiser evolves into a fully autonomous workflow orchestration engine. It will feature real-time downstream reprocessing (Branching Agentic State Machine), seamless integrations with GitHub/Jira via MCP, and robust support for non-software domains.