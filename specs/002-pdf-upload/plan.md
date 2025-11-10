# Implementation Plan: Leadrat Spec 2 — PDF Upload & Storage

**Branch**: `002-pdf-upload` | **Date**: 2025-11-10 | **Spec**: ./spec.md
**Input**: Feature specification from `/specs/002-pdf-upload/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement a secure, animated PDF uploader. Frontend provides drag-and-drop/picker with progress
and toasts. Backend exposes `POST /upload` to validate PDF and size (≤20MB), stores files under
`backend/static/uploads/`, persists metadata (filename, size MB, path, uploaded_at) into SQLite,
and returns success JSON. Duplicate filenames are handled via unique numeric suffix.

## Technical Context

**Language/Version**: Backend Python 3.11; Frontend Vite (Node 18+).  
**Primary Dependencies**: Flask, Flask-CORS, Flask-SQLAlchemy, python-dotenv; React, TailwindCSS,
Framer Motion, Axios, React Router, react-toastify.  
**Storage**: SQLite file `backend/database.db`; files in `backend/static/uploads/`.  
**Testing**: Manual verification via browser and curl/Postman; automated tests deferred.  
**Target Platform**: Local development on Windows.  
**Project Type**: Web (frontend + backend).  
**Performance Goals**: Upload UX responsive; typical 5MB upload completes and returns JSON ≤10s.  
**Constraints**: Max upload 20MB; PDF-only; duplicate filenames → numeric suffix; no secrets logged.  
**Scale/Scope**: Single-file uploads; multi-file/batch deferred.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Reliability & Observability: Return clear 400 messages; log attempts (structured JSON) without secrets.  
- Simplicity: Minimal API surface (`/upload`) with clear contract.  
- Security & Privacy: Validate type/size; sanitize filenames; store under static path only; `.env` secrets not logged.  
- Accessibility & Performance: Progress feedback; responsive UI; no heavy blocking.  

Gate Result: PASS (aligns with constitution principles for this scope).

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
├── routes/
│   └── upload_routes.py        # add POST /upload with validation and save
├── models/
│   └── pdf_model.py            # add fields: size (float MB), path (str)
└── static/uploads/             # saved PDFs

frontend/
├── src/pages/UploadPage.jsx    # drag-drop/picker, progress, toasts
└── src/components/             # shared components
```

**Structure Decision**: Extend existing web app layout; implement `/upload` route, update `PDFUpload`
fields, and add UploadPage on the frontend.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
