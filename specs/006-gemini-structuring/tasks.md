---

description: "Task list for Spec 006: Gemini-Driven Property Data Structuring"
---

# Tasks: Spec 006 — Gemini-Driven Property Data Structuring

**Input**: Design documents from `/specs/006-gemini-structuring/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: No automated tests requested; rely on manual validation and schema checks.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Dependencies, configs, logging policy

- [X] T001 Add LLM deps to `backend/requirements.txt`: google-generativeai
- [X] T002 [P] Add env config keys to `backend/config.py` (read `GEMINI_API_KEY` and structuring limits: `STRUCTURE_MAX_CHARS=1000000`, `STRUCTURE_TIMEOUT_SECONDS=12`)
- [X] T003 [P] Add English-only filter utility in `backend/services/structuring_service.py` (stub)
- [X] T004 Add OpenAPI contract to repo `specs/006-gemini-structuring/contracts/openapi.yaml` (already present) and reference in quickstart

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Service and route skeleton with validation & logging hooks

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Create service module `backend/services/structuring_service.py` with interfaces: `normalize_inputs()`, `build_prompt()`, `call_gemini()`, `validate_output()`
- [X] T006 [P] Implement route skeleton `backend/routes/structure_routes.py` with `POST /structure-data` (accepts `pdf_text`, `ocr_text`, optional `image_metadata`, `project_name`), enforces limits, returns 400 on invalid
- [X] T007 [P] Wire blueprint import/register in `backend/app.py` for `structure_routes`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 — Structure a single property's data (Priority: P1) 🎯 MVP

**Goal**: Combine inputs, normalize, construct Gemini prompt with schema, call model, validate JSON, return output

**Independent Test**: Provide sample `pdf_text` + `ocr_text` + labels; receive schema-valid JSON with populated `project_overview` when present

- [X] T008 [P] [US1] Implement normalization & merge in `backend/services/structuring_service.py` (dedupe, watermark removal, English-only)
- [X] T009 [P] [US1] Implement conflict resolution per spec (prefer OCR numeric/context) in `backend/services/structuring_service.py`
- [X] T010 [US1] Implement prompt building with schema + examples in `backend/services/structuring_service.py`
- [X] T011 [US1] Implement Gemini call via `google-generativeai` (temperature≈0.2–0.3) in `backend/services/structuring_service.py`
- [X] T012 [US1] Implement schema validation and repair pass in `backend/services/structuring_service.py` using OpenAPI `contracts/openapi.yaml`
- [X] T013 [US1] Integrate service into `backend/routes/structure_routes.py` and return validated JSON

**Checkpoint**: User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 — Floor plans & image references (Priority: P2)

**Goal**: Ensure floor plan items are extracted and linked to best image_reference

**Independent Test**: Provide OCR text with BHK/area and image labels; receive `floor_plans` with matched `image_reference`

- [X] T014 [P] [US2] Enhance prompt and postprocessing to detect BHK/areas/tower in `backend/services/structuring_service.py`
- [X] T015 [US2] Image reference attachment logic in `backend/services/structuring_service.py` using categories/labels from `image_metadata`

**Checkpoint**: User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 — Connectivity, FAQs, and highlights (Priority: P3)

**Goal**: Extract connectivity lists and FAQs consistently

**Independent Test**: Provide brochure text with nearby schools and Q&A; receive normalized arrays and faq pairs

- [X] T016 [P] [US3] Update prompt and postprocessing to populate `connectivity` arrays in `backend/services/structuring_service.py`
- [X] T017 [US3] Extract FAQs (question/answer pairs) in `backend/services/structuring_service.py`

**Checkpoint**: All user stories should now be independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Robustness, logging, performance

- [X] T018 [P] Structured logging: summaries + key metrics, no raw prompts/responses in `backend/routes/structure_routes.py`
- [X] T019 [P] Error handling: single retry for incomplete outputs; safe error JSON in `backend/services/structuring_service.py`
- [X] T020 [P] Config guards: enforce limits (`STRUCTURE_MAX_CHARS`, `STRUCTURE_TIMEOUT_SECONDS`) and return 400 on violations in `backend/routes/structure_routes.py`
- [ ] T021 (Optional) Persist structured JSON in SQLite (e.g., `backend/models/structured_data.py`) and add retrieval route

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

- **User Story 1 (P1)**: Depends on service and route skeleton
- **User Story 2 (P2)**: Depends on US1 structured text
- **User Story 3 (P3)**: Depends on US1 structured text

### Parallel Opportunities

- Setup tasks T002–T003 can run in parallel
- Foundational tasks T006–T007 can run in parallel
- US phases marked [P] can run concurrently where files do not overlap

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. STOP and VALIDATE: Test User Story 1 independently with sample payload
5. Demo structured JSON

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Demo (MVP)
3. Add User Story 2 → Test independently → Demo
4. Add User Story 3 → Test independently → Demo
