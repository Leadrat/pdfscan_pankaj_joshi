# Feature Specification: Leadrat Spec 1 — Base Environment Setup

**Feature Branch**: `[001-base-setup]`  
**Created**: 2025-11-10  
**Status**: Draft  
**Input**: User description: "Set up React+Vite+Tailwind+Framer Motion frontend, Flask backend with SQLite, .env config for GEMINI_API_KEY, and a working test connection route; no heavy logic."

## Clarifications

### Session 2025-11-10

- Q: What is the development CORS policy? → A: Configurable via ENV (default http://localhost:5173).
- Q: How should env files be handled? → A: Commit `.env.example`; gitignore real `.env`.
- Q: Which Python version for backend? → A: Python 3.11.
- Q: How should the frontend set API base URL? → A: `VITE_API_BASE` env with default `http://localhost:5000`.
- Q: What is the backend logging format baseline? → A: Structured JSON logs (level, message, context).

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - Backend ping route and DB init (Priority: P1)

As a developer, I want a running Flask server with a `/test` route and initialized SQLite DB so that the frontend can verify connectivity and the project has a persistent data layer.

**Why this priority**: Unblocks all subsequent specs by confirming backend availability and persistence foundations.

**Independent Test**: Start Flask server and visit `http://localhost:5000/test` → receive `{ "message": "Backend connected successfully!" }`. Create DB via `db.create_all()` without errors.

**Acceptance Scenarios**:

1. **Given** Flask app started, **When** GET `/test`, **Then** JSON `{ message: "Backend connected successfully!" }` with HTTP 200.
2. **Given** database config present, **When** running `db.create_all()`, **Then** `database.db` file exists.

---

### User Story 2 - Frontend boot and fetch (Priority: P2)

As a user, I want to see the Leadrat starter UI and a message fetched from the backend so I know the system is connected end-to-end.

**Why this priority**: Validates end-to-end connectivity and CORS configuration before implementing extraction flows.

**Independent Test**: Start Vite dev server and load `http://localhost:5173` to see heading and fetched message from `/test`.

**Acceptance Scenarios**:

1. **Given** frontend dev server running, **When** visiting the app, **Then** the page renders "Leadrat Real Estate App" and displays the message returned by backend `/test`.

---

### User Story 3 - Environment configuration (.env) (Priority: P3)

As a developer, I want secrets and environment variables managed via `.env` so keys like `GEMINI_API_KEY` are not hardcoded and can be changed safely.

**Why this priority**: Enables secure configuration for later LLM calls and toggling environments.

**Independent Test**: Provide `.env` with `GEMINI_API_KEY` and confirm app loads without logging secrets; backend reads env without errors.

**Acceptance Scenarios**:

1. **Given** `.env` exists with key placeholders, **When** backend starts, **Then** configuration loads and app runs without exposing secrets in logs.

---

[Add more user stories as needed, each with an assigned priority]

### Edge Cases

- Missing `.env` file → backend starts but LLM features remain disabled; logs a clear warning without crashing.
- CORS misconfiguration → frontend fetch to `/test` fails; display console error and handle gracefully in UI.
- Port conflicts (5000/5173) → document override steps; startup should fail fast with clear message.
- SQLite file lock or permission issue → DB init fails; return actionable error with logging.

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: Backend MUST expose `/test` returning `{ message: "Backend connected successfully!" }` with HTTP 200.
- **FR-002**: Backend MUST configure SQLite at `sqlite:///database.db` and initialize tables via `db.create_all()`.
- **FR-003**: Frontend MUST render a starter page and fetch the `/test` endpoint, displaying the response.
- **FR-004**: CORS MUST be configurable via environment (e.g., `FRONTEND_ORIGIN`), defaulting to `http://localhost:5173`, and enforced for development.
- **FR-005**: Environment variables MUST be read from `.env` (e.g., `GEMINI_API_KEY`, `FLASK_ENV`). Secrets MUST NOT be logged.
- **FR-006**: Project MUST include documented folder structures for backend and frontend matching the roadmap.
- **FR-007**: Repository MUST include `.env.example` with placeholders and `.gitignore` MUST exclude `.env`.
- **FR-008**: Frontend MUST read API base URL from `VITE_API_BASE` with default `http://localhost:5000`; URLs MUST NOT be hardcoded in code.
- **FR-009**: Backend MUST emit structured JSON logs (at minimum: `level`, `message`, `context`) with dev default level `INFO`, excluding secrets.

Assumptions

- Dev URLs: backend `http://localhost:5000`, frontend `http://localhost:5173`.
- OS: Windows development environment. Python and Node are available.
- Backend Python version: 3.11.
- Frontend env: `VITE_API_BASE` provided in `.env.example`.

### Key Entities *(include if feature involves data)*

- **PDFUpload**: Represents uploaded brochure metadata (filename, upload_date). Created in later specs but DB readiness is required now.
- **Config**: Runtime configuration surface (e.g., GEMINI_API_KEY, paths). Loaded from `.env`.

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: Visiting `http://localhost:5000/test` consistently returns HTTP 200 with the expected JSON within ≤ 150ms locally.
- **SC-002**: Frontend loads at `http://localhost:5173` and displays the fetched backend message within ≤ 1s after initial bundle load.
- **SC-003**: Database file `database.db` is created on init and writable by the app process.
- **SC-004**: No secrets printed in console/logs during normal startup and fetch cycles.
