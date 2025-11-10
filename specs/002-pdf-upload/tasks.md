---

description: "Task list for Spec 2: PDF Upload & Storage"
---

# Tasks: Leadrat Spec 2 — PDF Upload & Storage

**Input**: Design documents from `/specs/002-pdf-upload/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: No automated tests requested; rely on manual verification steps.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/`, `frontend/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prep configuration for uploads and routing

- [X] T001 Set Flask `MAX_CONTENT_LENGTH` and ensure uploads dir exists in `backend/app.py`
- [X] T002 [P] Add `UPLOAD_FOLDER=static/uploads` and confirm absolute save path handling in `backend/config.py`
- [X] T003 [P] Ensure frontend routing is available for UploadPage (React Router present) in `frontend/src/App.jsx`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Data model and contract readiness

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Add fields to `backend/models/pdf_model.py`: `size` (Float MB), `path` (String)
- [ ] T005 [P] Run DB migration step (simple re-create for dev): ensure table reflects new fields
- [X] T006 [P] Document `/upload` contract in `specs/002-pdf-upload/contracts/openapi.yaml`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Upload a PDF with progress (Priority: P1) 🎯 MVP

**Goal**: Upload PDF with progress UI and success toast; save file; return JSON

**Independent Test**: From UploadPage, select a valid `.pdf` < 20MB → progress animates → success toast → server stores file and returns metadata.

### Backend
- [X] T007 [P] [US1] Implement `POST /upload` handler in `backend/routes/upload_routes.py` to accept `multipart/form-data` with key `file`
- [X] T008 [P] [US1] Sanitize filename with `secure_filename`, compute save path under `backend/static/uploads/`, and save file
- [X] T009 [US1] Calculate file size in MB and return JSON `{status, filename, path, size, uploaded_at}`

### Frontend
- [X] T010 [P] [US1] Implement drag-and-drop/picker UI with progress in `frontend/src/pages/UploadPage.jsx`
- [X] T011 [P] [US1] Wire Axios upload to `${import.meta.env.VITE_API_BASE}/upload` with `onUploadProgress`
- [X] T012 [US1] Show success toast and render returned file info block after completion

**Checkpoint**: User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Validation & errors (Priority: P2)

**Goal**: PDF-only, 20MB limit; clear error messages and toasts

**Independent Test**: Try uploading non-PDF or >20MB; receive error toast; backend rejects with 400.

### Backend
- [X] T013 [P] [US2] Validate extension `.pdf` (case-insensitive); return `400` with JSON error
- [X] T014 [P] [US2] Enforce 20MB limit (use `MAX_CONTENT_LENGTH` and explicit size check); return `400`
- [X] T015 [US2] Ensure error responses are structured and do not leak sensitive info

### Frontend
- [X] T016 [P] [US2] Block non-PDF selection in `input accept=".pdf"` and show error toast on mismatch
- [X] T017 [P] [US2] Show error toast on size > 20MB (pre-check) and on 400 responses from backend

**Checkpoint**: User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Store metadata in DB (Priority: P3)

**Goal**: Persist upload metadata (filename, size MB, path, uploaded_at)

**Independent Test**: After successful upload, confirm new DB row with expected fields; values consistent (size ±0.1MB)

- [X] T018 [P] [US3] Insert PDFUpload row in `backend/routes/upload_routes.py` with `filename`, `size`, `path`, `upload_date`
- [X] T019 [US3] Verify DB write and return `uploaded_at` from row

**Checkpoint**: All user stories should now be independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: UX/robustness improvements

- [X] T020 [P] Show graceful UI state for network drop (reset progress, error toast) in `frontend/src/pages/UploadPage.jsx`
- [X] T021 Apply unique rename with numeric suffix policy on filename conflicts in `backend/routes/upload_routes.py`
- [X] T022 Ensure logs are structured JSON and exclude secrets; add INFO logs for upload attempts (no payloads)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Standalone after Foundational
- **User Story 2 (P2)**: Depends on US1 route existing; otherwise independent
- **User Story 3 (P3)**: Depends on US1 (successful upload flow) and model fields from Foundational

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- Foundational tasks T005–T006 can run in parallel
- Within US1/US2, frontend and backend [P] tasks can proceed concurrently

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. STOP and VALIDATE: Test User Story 1 independently
5. Demo upload success

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Demo (MVP)
3. Add User Story 2 → Test independently → Demo
4. Add User Story 3 → Test independently → Demo
