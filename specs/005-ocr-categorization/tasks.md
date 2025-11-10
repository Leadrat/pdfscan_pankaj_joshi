---

description: "Task list for Spec 5: Hybrid OCR & Image Categorization"
---

# Tasks: Leadrat Spec 5 — Hybrid OCR & Image Categorization

**Input**: Design documents from `/specs/005-ocr-categorization/`
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

**Purpose**: Dependencies, modules, and config

- [X] T001 Add OCR deps to `backend/requirements.txt`: opencv-python, pytesseract, easyocr, numpy, scikit-image
- [X] T002 [P] Create OCR module files: `backend/ocr/__init__.py`, `backend/ocr/preprocess.py`, `backend/ocr/engines.py`, `backend/ocr/extract.py`, `backend/ocr/utils.py`
- [X] T003 [P] Add `OCR_LANGS=en,hi` env/config and cache EasyOCR reader
- [X] T004 Ensure processed dir exists: `backend/static/images/processed/` (create on startup in `backend/app.py`)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Data model and route skeleton

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Create SQLAlchemy model `backend/models/ocr_extracted.py` with fields: id, image_name, category, extracted_text, structured_json, created_at
- [X] T006 [P] Implement route skeleton `backend/routes/ocr_routes.py` with `POST /extract-ocr-data` (iterate files under `static/images/`, return 400 on none)
- [X] T007 [P] Wire blueprint import/register in `backend/app.py` for `ocr_routes`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - OCR pipeline with preprocessing (Priority: P1) 🎯 MVP

**Goal**: Preprocess images and run pytesseract + EasyOCR; merge outputs and normalize

**Independent Test**: Call `/extract-ocr-data` and confirm non-empty text and structured fields exist for subset of images

### Preprocessing + OCR
- [X] T008 [P] [US1] Implement preprocessing in `backend/ocr/preprocess.py` (grayscale, threshold, denoise, morphology, deskew, CLAHE, resize≥1024)
- [X] T009 [P] [US1] Implement OCR engines in `backend/ocr/engines.py` (pytesseract + EasyOCR ['en','hi']) with cached EasyOCR reader
- [X] T010 [US1] Merge texts and normalize in `backend/ocr/extract.py` (deduplicate lines, remove watermarks/specials)

**Checkpoint**: User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Categorize images (Priority: P2)

**Goal**: Categorize images via keywords and optional visual cues

**Independent Test**: Mixed set produces at least one non-empty category with reasonable mapping

- [X] T011 [P] [US2] Implement keyword-based categorization in `backend/ocr/extract.py` (BHK/sq.ft → Floor Plan; Gym/Club → Amenities; Map/Road → Location Map)
- [ ] T012 [US2] (Optional) Add basic visual cue detection using contours/layout density in `backend/ocr/extract.py`

**Checkpoint**: User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Structured output, storage, API (Priority: P3)

**Goal**: Store JSON in SQLite and return through API

**Independent Test**: POST `/extract-ocr-data` returns list with `{image, category, details{…}}` and DB has corresponding rows

- [X] T013 [P] [US3] Implement field extraction (tower, bhk, areas, price, amenities) in `backend/ocr/extract.py`
- [X] T014 [P] [US3] Insert row per image into `ocr_extracted_data` and return structured JSON in `backend/routes/ocr_routes.py`
- [X] T015 [US3] Return per-image error entries where OCR fails (`{"error": "Text not detected"}`)

**Checkpoint**: All user stories should now be independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Robustness, logging, performance

- [X] T016 [P] Add structured logging (filename, duration, success/failure) in `backend/routes/ocr_routes.py`
- [X] T017 [P] Security: sanitize filenames and restrict to `backend/static/images/` set; no absolute paths in response
- [ ] T018 [P] Performance: cache EasyOCR reader and parallelize per-image processing (safe thread-usage)
- [ ] T019 (Optional) Add minimal OCR Viewer page to display per-image details and filters

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

- **User Story 1 (P1)**: Depends on model and route skeleton
- **User Story 2 (P2)**: Depends on US1 text outputs
- **User Story 3 (P3)**: Depends on US1 text outputs and table

### Parallel Opportunities

- Setup tasks T002–T004 can run in parallel
- Foundational tasks T006–T007 can run in parallel
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
