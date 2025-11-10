---

description: "Task list for Spec 4: PDF Image Extraction & Gallery"
---

# Tasks: Leadrat Spec 4 — PDF Image Extraction & Gallery

**Input**: Design documents from `/specs/004-image-extraction/`
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

**Purpose**: Dependencies, directories, and config

- [ ] T001 Add dependencies to `backend/requirements.txt`: PyMuPDF (fitz), Pillow (PIL)
- [ ] T002 [P] Ensure images directory exists on startup: create `backend/static/images/` in `backend/app.py`
- [ ] T003 [P] Add optional file logger `backend/logs/image_extraction.log` (graceful if path missing)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Data model and endpoint skeleton

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Create SQLAlchemy model `backend/models/extracted_image.py` with fields: id, filename, page_number, width, height, file_path, created_at
- [ ] T005 [P] Implement route skeleton `backend/routes/image_routes.py` with `POST /extract-images?filename=<name>` (validate/sanitize filename; return 400 on missing)
- [ ] T006 [P] Wire blueprint import/register in `backend/app.py` for `image_routes`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Extract images and return JSON (Priority: P1) 🎯 MVP

**Goal**: Extract images from PDF and return list with metadata and URLs

**Independent Test**: POST `/extract-images?filename=<pdf>` → JSON with `status=success`, `total_images` > 0, valid `/static/images/...` URLs

### Backend Extraction
- [ ] T007 [P] [US1] Implement page iteration using PyMuPDF (fitz) in `backend/routes/image_routes.py`
- [ ] T008 [P] [US1] Extract images via `page.get_images(full=True)` and `doc.extract_image(xref)`
- [ ] T009 [US1] Save PNG as `{original}_page{n}_img{m}.png` under `backend/static/images/`
- [ ] T010 [US1] Build response JSON with `total_images` and `[ { id, filename, page_number, dimensions, url } ]`

**Checkpoint**: User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Store metadata and compress images (Priority: P2)

**Goal**: PNG compression and metadata persistence

**Independent Test**: After extraction, DB contains metadata; images >2MB are resized by ~25% preserving aspect ratio

- [ ] T011 [P] [US2] Use Pillow to convert to PNG; if file size >2MB, resize (~0.75 scale) with aspect ratio maintained
- [ ] T012 [P] [US2] Insert metadata row into `extracted_images` with filename, page_number, width, height, file_path
- [ ] T013 [US2] Ensure API uses DB id in response and `dimensions` string as `"{width}x{height}"`

**Checkpoint**: User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Interactive gallery with zoom (Priority: P3)

**Goal**: Responsive grid with zoom modal and navigation

**Independent Test**: Gallery shows 4/2/1 columns on desktop/tablet/mobile; clicking opens zoom modal with arrows and close

- [ ] T014 [P] [US3] Create `frontend/src/pages/ImageGallery.jsx` grid (Tailwind: 4/2/1 columns) with hover animations
- [ ] T015 [P] [US3] Integrate `react-medium-image-zoom` or build modal with Framer Motion (zoom/pan, ESC/close, arrows)
- [ ] T016 [US3] Fetch `/extract-images?filename=<pdf>` and render returned images with alt captions and lazy-loading attributes

**Checkpoint**: All user stories should now be independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Robustness, logging, performance

- [ ] T017 [P] Username/filename sanitization and ensure no absolute paths in response; URLs under `/static/images/...` only (in `image_routes.py`)
- [ ] T018 [P] Log filename, total_images, duration, errors to console and file if available
- [ ] T019 Avoid duplicate reprocessing: if DB has entries for filename and `reextract!=true`, return existing entries
- [ ] T020 Performance: Large PDFs extract within practical time; verify gallery render ≤1s after data fetch (local)

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

- **User Story 1 (P1)**: Depends on endpoint skeleton and image dir
- **User Story 2 (P2)**: Depends on US1 save path; adds DB writes
- **User Story 3 (P3)**: Depends on US1 API for data fetch

### Parallel Opportunities

- Setup tasks T002–T003 can run in parallel
- Foundational tasks T005–T006 can run in parallel
- US phases marked [P] can run concurrently where files do not overlap

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
