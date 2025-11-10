---

description: "Task list for Spec 007: Chatbot Q&A from Brochure Data"
---

# Tasks: Spec 007 — Chatbot Q&A from Brochure Data

**Input**: Design documents from `/specs/007-chatbot-qa/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: No automated tests requested; rely on manual validation and schema checks.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/` and `frontend/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: API contract, limits, and logging policy

- [X] T001 Add Chatbot API contract `specs/007-chatbot-qa/contracts/openapi.yaml` (already present) and reference in quickstart
- [X] T002 [P] Enforce 500-char max question in backend validation (route level) `backend/routes/chatbot_routes.py`
- [X] T003 [P] Prepare frontend session policy (page-lifetime) in `frontend/src/hooks/useChatbot.js`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Service and route skeleton with validation & logging hooks

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Create service module `backend/services/chatbot_service.py` with interfaces: `build_prompt()`, `call_gemini()`, `ground_answer()`, `validate_response()`
- [X] T005 [P] Implement route skeleton `backend/routes/chatbot_routes.py` with `POST /chatbot/query` (accepts `{question, context}`), validates max length and schema, returns 400 on invalid
- [X] T006 [P] Wire blueprint import/register in `backend/app.py` for `chatbot_routes`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 — Context‑limited answers with fallback (Priority: P1) 🎯 MVP

**Goal**: Accept question + structured context; answer strictly from data or return exact fallback

**Independent Test**: Ask an in-scope question → get correct concise answer; ask an out-of-scope question → get exact fallback phrase

- [X] T007 [P] [US1] Implement `ground_answer()` to restrict responses to context; detect out-of-scope and use fallback in `backend/services/chatbot_service.py`
- [X] T008 [P] [US1] Implement Gemini call via `google-generativeai` (temperature≈0.3) in `backend/services/chatbot_service.py`
- [X] T009 [US1] Validate JSON response structure `{ "answer": "..." }` and sanitize output in `backend/services/chatbot_service.py`
- [X] T010 [US1] Integrate service into `backend/routes/chatbot_routes.py` and return validated JSON

**Checkpoint**: User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 — Chat entry and modern UI (Priority: P2)

**Goal**: Floating icon appears after extraction complete; animated chat window with greeting and input

**Independent Test**: After extraction complete flag is set, icon appears; clicking opens window with animation and greeting; question submission works

- [X] T011 [P] [US2] Add floating ChatButton with tooltip in `frontend/src/components/chat/ChatButton.jsx`
- [X] T012 [P] [US2] Add ChatWindow with animation + greeting in `frontend/src/components/chat/ChatWindow.jsx`
- [X] T013 [P] [US2] Add ChatMessage bubble component in `frontend/src/components/chat/ChatMessage.jsx`
- [X] T014 [US2] Implement `useChatbot.js` for session state (page-lifetime), 500-char limit, extraction-complete gating in `frontend/src/hooks/useChatbot.js`

**Checkpoint**: User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 — Session chat history (Priority: P3)

**Goal**: Maintain visible chat history during page session

**Independent Test**: Ask multiple questions; see message list preserved within page session

- [X] T015 [P] [US3] Persist in-session messages in hook state (page-lifetime) in `frontend/src/hooks/useChatbot.js`
- [X] T016 [US3] Render conversation history (user/assistant roles) in `frontend/src/components/chat/ChatWindow.jsx`

**Checkpoint**: All user stories should now be independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Robustness, logging, performance

- [X] T017 [P] Structured logging: summaries + key metrics, no raw prompts/responses in `backend/routes/chatbot_routes.py`
- [X] T018 [P] Error handling: safe error JSON and friendly UI error states (typing indicator, retry) in `frontend/src/components/chat/ChatWindow.jsx`
- [X] T019 [P] Enforce question truncation with notice and disable send while awaiting response in `frontend/src/hooks/useChatbot.js`
- [ ] T020 (Optional) Store minimal chat logs in SQLite (e.g., `backend/models/chat_log.py`) and retrieval route

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

- **User Story 1 (P1)**: Depends on route/service skeleton
- **User Story 2 (P2)**: Depends on US1 backend working endpoint
- **User Story 3 (P3)**: Depends on US2 UI components and hook

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
4. STOP and VALIDATE: Test User Story 1 independently with sample payload
5. Demo grounded answers and fallback

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Demo (MVP)
3. Add User Story 2 → Test independently → Demo
4. Add User Story 3 → Test independently → Demo
