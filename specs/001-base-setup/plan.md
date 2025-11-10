# Implementation Plan: Leadrat Spec 1 — Base Environment Setup

**Branch**: `001-base-setup` | **Date**: 2025-11-10 | **Spec**: ./spec.md
**Input**: Feature specification from `/specs/001-base-setup/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Establish the base full‑stack environment for Leadrat. Deliver a running Flask backend with `/test`,
SQLite initialization, React+Vite+Tailwind frontend that fetches from `/test`, environment config via
`.env`/`.env.example`, ENV‑configurable CORS, `VITE_API_BASE`, and structured JSON logging baseline.

## Technical Context

**Language/Version**: Backend Python 3.11; Frontend Vite (Node 18+).  
**Primary Dependencies**: Flask, Flask-CORS, SQLAlchemy, python-dotenv; React, TailwindCSS, Framer Motion, Axios, React Router.  
**Storage**: SQLite file `database.db` (local dev).  
**Testing**: Manual verification for Spec 1 (ping route + DB create); pytest to be introduced in later specs.  
**Target Platform**: Local development on Windows.  
**Project Type**: Web (frontend + backend).  
**Performance Goals**: `/test` responds in ≤150ms locally; frontend initial fetch within ≤1s after bundle load.  
**Constraints**: CORS configurable via ENV (default http://localhost:5173); secrets not logged; API base via `VITE_API_BASE`.  
**Scale/Scope**: Scope limited to bootstrapping, no heavy extraction/LLM logic in this spec.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Logging & error handling present: Structured JSON logging baseline specified (FR-009).  
- Async/lazy strategies: Deferred; not applicable to Spec 1 heavy flows.  
- Structured JSON schemas: Not required in Spec 1 (no extraction/LLM yet).  
- Accessibility & performance targets: Frontend bootstrap only; Lighthouse targets apply from later specs.  
- Chatbot context constraints: N/A in Spec 1.  

Gate Result: PASS (Spec 1 scope limited; non-applicable gates deferred to subsequent specs per roadmap).

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
backend/
├── app.py
├── routes/
│   ├── __init__.py
│   └── upload_routes.py
├── models/
│   ├── __init__.py
│   └── pdf_model.py
├── static/
│   └── uploads/
├── database.db
├── .env (gitignored; see .env.example)
├── requirements.txt
└── config.py

frontend/
├── src/
│   ├── components/
│   │   └── Navbar.jsx
│   ├── pages/
│   │   └── UploadPage.jsx
│   ├── App.jsx
│   └── main.jsx
├── index.html
├── package.json
├── tailwind.config.js
└── .env.example (contains VITE_API_BASE)
```

**Structure Decision**: Web application layout (frontend + backend) per Spec 1. Paths above will be realized during implementation.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
