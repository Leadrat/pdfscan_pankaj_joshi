---

description: "Task list for Spec 010: Robust Error Handling & Logging"
---

# Tasks: Spec 010 — Robust Error Handling & Logging

**Input**: Design documents from `/specs/010-error-handling/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: No automated tests requested; rely on manual validation scenarios and log inspection.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/`
- **Frontend**: `frontend/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Common helpers for toasts, error boundaries, and logging base

 - [X] T001 Create Toast helpers `frontend/src/components/ui/toast.js` (success/error/info wrappers using React Hot Toast)
 - [X] T002 [P] Create Error Boundary `frontend/src/components/ui/ErrorBoundary.jsx` (friendly fallback with "Try Again")
 - [X] T003 [P] Prepare logs directory `backend/logs/` (ensure exists on startup in `backend/app.py`)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Backend logging/rotation and LLM retry policy; global error boundary wiring

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

 - [X] T004 Add rotating file handler (10MB/file, keep 5, 7-day cap) in `backend/app.py` under `/logs` (JSON log format)
 - [X] T005 [P] Standardize step logs (pdf_upload, ocr_extraction, gemini_request, ui_render) across routes/services in `backend/routes/*.py`
 - [X] T006 [P] Implement LLM retry/backoff (1s, 2s) in `backend/services/structuring_service.py` (apply to Gemini calls)
 - [X] T007 Wire top-level ErrorBoundary around primary routes in `frontend/src/App.jsx`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 — Friendly user feedback & partial UI (Priority: P1) 🎯 MVP

**Goal**: Clear toasts and partial data rendering for upload/OCR/LLM failures

**Independent Test**: Simulate invalid PDF, OCR failure, and LLM failure; verify toasts and partial content display

 - [X] T008 [P] [US1] Invalid/unreadable PDF toast in `frontend/src/pages/UploadPage.jsx` and validation guard
 - [X] T009 [P] [US1] OCR failure → partial data toast + placeholder sections in `frontend/src/components/dynamic/*Section.jsx`
 - [X] T010 [US1] LLM failure → friendly toast + render available OCR/partial data in `frontend/src/components/dynamic/DynamicLandingPage.jsx`
 - [X] T011 [US1] Add "Retry Extraction" CTA where logical in `frontend/src/pages/UploadPage.jsx`

**Checkpoint**: User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 — Structured backend logging (Priority: P2)

**Goal**: JSON logs for every major step with minimal safe context and timing

**Independent Test**: Trigger success/failure paths; verify logs for step, status, and duration

 - [X] T012 [P] [US2] pdf_upload logs (initiated/success/failure) in `backend/routes/upload_routes.py`
 - [X] T013 [P] [US2] ocr_extraction logs (started/completed/failed) in `backend/routes/ocr_routes.py`
 - [X] T014 [US2] gemini_request logs (sent/received/error) in `backend/routes/structure_routes.py` and `backend/services/structuring_service.py`
 - [X] T015 [US2] ui_render log hook (on server-side events) in `backend/app.py` after `db.create_all()` and on key responses

**Checkpoint**: User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 — UI stability via Error Boundaries (Priority: P3)

**Goal**: Prevent blank screens by catching render errors and offering recovery

**Independent Test**: Simulate component crash; confirm friendly fallback and retry remount

 - [X] T016 [P] [US3] Wrap Chat window and dynamic landing parent with ErrorBoundary in `frontend/src/components/chat/ChatButton.jsx` and `frontend/src/components/dynamic/DynamicLandingPage.jsx`
 - [X] T017 [US3] Add error logging from ErrorBoundary to console (and optional backend endpoint) in `frontend/src/components/ui/ErrorBoundary.jsx`

**Checkpoint**: All user stories should now be independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Consistency, accessibility, and resilience

 - [X] T018 [P] Debounce toasts to avoid spam; consolidate repeated failures in `frontend/src/components/ui/toast.js`
 - [X] T019 [P] Add reduced-motion compliant fade-in for toasts (Framer Motion or library theme) in `frontend/src/components/ui/toast.js`
 - [ ] T020 [P] Add placeholders/skeletons for empty states across sections `frontend/src/components/dynamic/*Section.jsx`
 - [ ] T021 (Optional) Add backend log export/diagnostics endpoint `backend/routes/log_routes.py`

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

- **User Story 1 (P1)**: Depends on error boundary wiring and logging base
- **User Story 2 (P2)**: Depends on logging base and LLM retry policy
- **User Story 3 (P3)**: Depends on ErrorBoundary component

### Parallel Opportunities

- Setup tasks T002–T003 can run in parallel
- Foundational tasks T005–T007 can run in parallel
- US phases marked [P] can run concurrently where files do not overlap

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. STOP and VALIDATE: Test User Story 1 independently with simulated failures
5. Demo user feedback and partial UI

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Demo (MVP)
3. Add User Story 2 → Test independently → Demo
4. Add User Story 3 → Test independently → Demo
