---

description: "Task list for Spec 3: PDF Text Extraction"
---

# Tasks: Leadrat Spec 3 — PDF Text Extraction

**Input**: Design documents from `/specs/003-text-extraction/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: No automated tests requested; rely on manual verification steps.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Configuration and dependencies

- [ ] T001 Add dependencies to `backend/requirements.txt`: PyMuPDF (fitz), pdfminer.six
- [ ] T002 [P] Create `backend/extraction/__init__.py`, `backend/extraction/engines.py`, `backend/extraction/clean.py`, `backend/extraction/structure.py`
- [ ] T003 [P] Add config flag for engine selection in `backend/config.py` (e.g., `TEXT_ENGINE=pymupdf|pdfminer`)
- [ ] T004 Ensure temp directory exists at `backend/static/uploads/temp/` (create on startup in `backend/app.py`)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Data model and route skeletons

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 Create SQLAlchemy model `backend/models/extracted_text.py` with fields: id, filename, raw_text (Text), structured_data (Text JSON), created_at (DateTime)
- [ ] T006 [P] Create route file `backend/routes/extract_routes.py` with `GET /extract-text` skeleton (reads `filename` query param, returns 400 if missing)
- [ ] T007 [P] Wire blueprint import/register in `backend/app.py` for `extract_routes`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Extract and return structured text (Priority: P1) 🎯 MVP

**Goal**: Extract PDF text, clean, structure, store, and return JSON

**Independent Test**: Call `/extract-text?filename=<pdf>` for an uploaded text PDF → success JSON with `data` fields and `raw_text_length` > 0.

### Engine + Pipeline
- [ ] T008 [P] [US1] Implement PyMuPDF extraction path in `backend/extraction/engines.py` (page-by-page, return raw text)
- [ ] T009 [P] [US1] Implement cleaning in `backend/extraction/clean.py` (normalize whitespace, remove non-UTF-8, fix hyphenations)
- [ ] T010 [P] [US1] Implement structuring in `backend/extraction/structure.py` (keywords/regex for fields; amenities tagging; contact regex)

### Route + Storage
- [ ] T011 [US1] In `backend/routes/extract_routes.py`, integrate pipeline: locate file under `backend/static/uploads/` (or temp), extract → clean → structure → compute raw_text_length
- [ ] T012 [US1] Insert row into `extracted_text` table with filename, raw_text, structured_data (JSON string), created_at
- [ ] T013 [US1] Return JSON `{status, message, data, raw_text_length}` with missing-field policy (null/[]/{})

**Checkpoint**: User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Switchable extraction engine (Priority: P2)

**Goal**: Toggle engine via config flag

**Independent Test**: Toggle engine to `pymupdf` and `pdfminer` and see logs reflect engine path used with results produced.

- [ ] T014 [P] [US2] Implement pdfminer extraction path in `backend/extraction/engines.py`
- [ ] T015 [US2] Read `TEXT_ENGINE` from config and route to selected engine; log the choice

**Checkpoint**: User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Temporary storage & retrieval (Priority: P3)

**Goal**: Serve extracted data from SQLite and manage temp files

**Independent Test**: After extraction, DB row exists and can be fetched; purge job removes rows >24h as designed.

- [ ] T016 [P] [US3] Implement DB fetch by `filename` in `backend/routes/extract_routes.py` when data already exists
- [ ] T017 [US3] Implement daily purge function (on app start or separate script) to delete rows older than 24h and remove files in `backend/static/uploads/temp/` older than 24h

**Checkpoint**: All user stories should now be independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Robustness, logging, and performance

- [ ] T018 [P] Add structured logging around extraction: start/end timestamps, duration, filename in `extract_routes`
- [ ] T019 Return safe error JSON with 400/500 codes on failures (e.g., corrupt PDF, missing file) and map common exceptions (fitz/pdfminer)
- [ ] T020 Performance check: Extract a 10–20 page PDF ≤ 10s locally; if exceeded, add minor optimizations (streaming/page batching)

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

- **User Story 1 (P1)**: Depends on Foundational model and route skeleton
- **User Story 2 (P2)**: Depends on US1 pipeline to compare engine outputs
- **User Story 3 (P3)**: Depends on US1 storage and model

### Parallel Opportunities

- Setup tasks T002–T004 can run in parallel
- Foundational T006–T007 can run in parallel
- US1 pipeline components T008–T010 can be developed concurrently

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. STOP and VALIDATE: Test User Story 1 independently
5. Demo extraction JSON

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Demo (MVP)
3. Add User Story 2 → Test independently → Demo
4. Add User Story 3 → Test independently → Demo
