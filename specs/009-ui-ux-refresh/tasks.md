---

description: "Task list for Spec 009: Global UI/UX Refresh — Glassmorphism, Gradients, Motion, Lottie"
---

# Tasks: Spec 009 — Global UI/UX Refresh

**Input**: Design documents from `/specs/009-ui-ux-refresh/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: No automated tests requested; rely on manual visual checks across breakpoints and reduced‑motion settings.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Frontend**: `frontend/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Add theme & motion tokens, Lottie assets, base wrappers

- [ ] T001 Create theme tokens file `frontend/src/theme/tokens.js` (gradients, glass, radii, shadows, text colors)
- [ ] T002 [P] Create motion tokens file `frontend/src/theme/motion.js` (durations, easings, variants, reduced‑motion helpers)
- [ ] T003 [P] Add Lottie assets folder `frontend/public/lottie/` with placeholders: `upload_success.json`, `loading.json`, `page_transition.json`
- [ ] T004 Add global CSS utilities in `frontend/src/index.css` (glass panel utilities using Tailwind @apply)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Page shell, providers, and layout wrappers

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 Create page shell with motion wrapper `frontend/src/components/ui/PageShell.jsx` (page enter/exit variants)
- [ ] T006 [P] Wrap root route with PageShell `frontend/src/App.jsx` (apply motion page transitions)
- [ ] T007 [P] Update Navbar to glassmorphism `frontend/src/components/Navbar.jsx` (blur + gradient + rounded + shadow)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 — Unified visual theme & responsiveness (Priority: P1) 🎯 MVP

**Goal**: Apply glassmorphism + gradients and responsive refinements to all primary screens

**Independent Test**: Mobile/tablet/desktop: no layout breakage, consistent theme, readable contrast

- [ ] T008 [P] [US1] Upload screen glass theme and spacing in `frontend/src/pages/Upload.jsx` (use glass utilities; rounded‑2xl)
- [ ] T009 [P] [US1] Results dashboard panels to glass theme in `frontend/src/pages/Results.jsx` (cards, grids responsive)
- [ ] T010 [P] [US1] Chatbot panel restyle (glass card + spacing) in `frontend/src/components/chat/ChatWindow.jsx`
- [ ] T011 [US1] Dynamic landing sections (Hero/Amenities/Connectivity/FloorPlans/FAQs) ensure unified theme in `frontend/src/components/dynamic/*Section.jsx`
- [ ] T012 [US1] Ensure all screens use consistent typography and spacing scale (tokens) across components

**Checkpoint**: User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 — Smooth motion & transitions (Priority: P2)

**Goal**: Page transitions, section reveals, and hover micro‑interactions

**Independent Test**: Route change transitions ≤300ms; smooth section reveals; subtle hover effects

- [ ] T013 [P] [US2] Add section reveal variants to landing sections `frontend/src/components/dynamic/*Section.jsx`
- [ ] T014 [P] [US2] Hover micro‑interactions on cards/buttons/icons (scale/shadow) across `frontend/src/components/**/**.jsx`
- [ ] T015 [US2] Ensure reduced‑motion: disable/shorten transitions using helpers from `theme/motion.js`

**Checkpoint**: User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 — Interactive feedback with Lottie (Priority: P3)

**Goal**: Lottie animations for upload success, loading/processing, and optional transitions

**Independent Test**: Upload success triggers celebratory Lottie; long operations show subtle loader; page transition Lottie optional

- [ ] T016 [P] [US3] Add upload success Lottie component `frontend/src/components/ui/UploadSuccessLottie.jsx` and use in upload flow
- [ ] T017 [P] [US3] Add loading/processing Lottie component `frontend/src/components/ui/LoadingLottie.jsx` and wire in long operations
- [ ] T018 [US3] Optional: page/section transition Lottie `frontend/src/components/ui/PageTransitionLottie.jsx` and invoke in PageShell

**Checkpoint**: All user stories should now be independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Tooltips, smooth scroll, accessibility, performance

- [ ] T019 [P] Add smooth scroll helpers where applicable (e.g., Navbar links → sections) in `frontend/src/components/ui/*`
- [ ] T020 [P] Add interactive tooltips/highlights (e.g., on action buttons) using a lightweight tooltip lib or Tailwind popovers across `frontend/src/components/**/**.jsx`
- [ ] T021 [P] Validate contrast on glass panels (darken backgrounds or elevate text) across all pages
- [ ] T022 (Optional) Add theme switch or intensity toggle for motion (reduced visual effects)

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

- **User Story 1 (P1)**: Depends on theme/motion tokens, PageShell
- **User Story 2 (P2)**: Depends on US1 theming pass
- **User Story 3 (P3)**: Independent of US2 but benefits from PageShell

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
4. STOP and VALIDATE: Test User Story 1 independently across breakpoints
5. Demo refreshed screens

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Demo (MVP)
3. Add User Story 2 → Test independently → Demo
4. Add User Story 3 → Test independently → Demo
