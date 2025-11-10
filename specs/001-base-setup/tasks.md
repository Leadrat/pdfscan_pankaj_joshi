---

description: "Task list for Spec 1: Base Environment Setup"
---

# Tasks: Leadrat Spec 1 — Base Environment Setup

**Input**: Design documents from `/specs/001-base-setup/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are OPTIONAL. For Spec 1, no automated tests requested; rely on manual verification steps in User Stories.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/`, `frontend/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create backend project structure per plan at `backend/` (app.py, routes/, models/, static/uploads/, config.py)
- [X] T002 Create frontend project structure per plan at `frontend/` (src/, index.html, package.json, tailwind.config.js)
- [X] T003 Add `.gitignore` rules at repository root for Python/Node artifacts and `.env` files
- [X] T004 [P] Create `backend/requirements.txt` with Flask, Flask-CORS, Flask-SQLAlchemy, python-dotenv, requests, PyMuPDF, pdfminer.six
- [X] T005 [P] Add `specs/001-base-setup/contracts/openapi.yaml` (already scaffolded) and verify path inclusion

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 Implement Flask app bootstrap in `backend/app.py` with CORS and SQLAlchemy init
- [X] T007 [P] Create `backend/config.py` loading env (SQLALCHEMY_DATABASE_URI, UPLOAD_FOLDER, FRONTEND_ORIGIN)
- [X] T008 [P] Create `.env.example` at `backend/.env.example` with placeholders (FRONTEND_ORIGIN, GEMINI_API_KEY, FLASK_ENV)
- [X] T009 [P] Create SQLAlchemy models package `backend/models/__init__.py`
- [X] T010 [P] Prepare routes package `backend/routes/__init__.py`
- [X] T011 Add structured JSON logging setup in `backend/app.py` (level, message, context) per FR-009

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Backend ping route and DB init (Priority: P1) 🎯 MVP

**Goal**: Running Flask server with `/test` route and initialized SQLite DB

**Independent Test**: Start Flask and GET `http://localhost:5000/test` → `{ "message": "Backend connected successfully!" }`. Run `db.create_all()` → `backend/database.db` exists.

- [X] T012 [P] [US1] Implement `/test` endpoint in `backend/routes/upload_routes.py`
- [X] T013 [US1] Register blueprint in `backend/app.py` (`from routes.upload_routes import upload_bp; app.register_blueprint(upload_bp)`)
- [X] T014 [P] [US1] Create `backend/models/pdf_model.py` with `PDFUpload` entity (id, filename, upload_date)
- [X] T015 [US1] Initialize database tables via `db.create_all()` path in `backend/app.py` (guarded under main or init step)
- [X] T016 [US1] Verify database file created at `backend/database.db` and permissions are correct

**Checkpoint**: User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Frontend boot and fetch (Priority: P2)

**Goal**: Starter UI that fetches `/test` from backend and displays message

**Independent Test**: Start Vite dev server and load `http://localhost:5173` to see heading and fetched message from `/test`.

- [X] T017 [P] [US2] Add Tailwind setup in `frontend/tailwind.config.js` and `frontend/src/index.css`
- [X] T018 [P] [US2] Create `frontend/src/App.jsx` that fetches `${import.meta.env.VITE_API_BASE}/test` and renders message
- [X] T019 [P] [US2] Create `frontend/src/main.jsx` and ensure React app mounts
- [X] T020 [P] [US2] Create `frontend/src/components/Navbar.jsx` (basic shell per theme)
- [X] T021 [P] [US2] Create `frontend/src/pages/UploadPage.jsx` (placeholder page)
- [ ] T022 [US2] Verify CORS works: message renders; handle and log error gracefully if fetch fails

**Checkpoint**: User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Environment configuration (.env) (Priority: P3)

**Goal**: Secrets and environment variables managed via `.env` and `.env.example`

**Independent Test**: Provide `.env` with `GEMINI_API_KEY` and confirm app loads without logging secrets; backend reads env without errors.

- [X] T023 [P] [US3] Create `frontend/.env.example` with `VITE_API_BASE=http://localhost:5000`
- [X] T024 [US3] Update repository root `.gitignore` to exclude `frontend/.env` and `backend/.env`
- [X] T025 [US3] Update `backend/app.py` to use `Config` for CORS origin (ENV-configurable, default http://localhost:5173)
- [X] T026 [US3] Manual verification: No secrets printed in backend logs; `.env` not committed

**Checkpoint**: All user stories should now be independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T027 [P] Documentation: Ensure `specs/001-base-setup/quickstart.md` is accurate and up-to-date
- [X] T028 Code cleanup and formatting (flake8/prettier config placeholders)
- [X] T029 Performance: Confirm `/test` latency ≤ 150ms locally
- [X] T030 Security: Confirm `.env` is ignored and logs exclude secrets

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

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Depends on US1 only for verifying backend endpoint exists
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Independent, but validates configuration used by US1/US2

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, user stories can start in parallel (if team capacity allows)
- All [P] tasks within stories can run in parallel where file paths do not overlap

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. STOP and VALIDATE: Test User Story 1 independently
5. Demo connectivity

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Demo (MVP)
3. Add User Story 2 → Test independently → Demo
4. Add User Story 3 → Test independently → Demo

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently
