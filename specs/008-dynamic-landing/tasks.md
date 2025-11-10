---

description: "Task list for Spec 008: Dynamic Landing Page (Auto‑Generated)"
---

# Tasks: Spec 008 — Dynamic Landing Page (Auto‑Generated)

**Input**: Design documents from `/specs/008-dynamic-landing/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: No automated tests requested; rely on manual validation and visual checks.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Frontend**: `frontend/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project scaffolding for dynamic landing components and assets

- [X] T001 Create dynamic folder structure under `frontend/src/components/dynamic/`
- [X] T002 [P] Add placeholder image asset `frontend/src/assets/placeholder-floorplan.png`
- [X] T003 [P] Ensure TailwindCSS and Framer Motion are available (already in package.json); import MotionProvider as needed in top-level UI entry

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Parent container and data shape adapters

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Create parent component `frontend/src/components/dynamic/DynamicLandingPage.jsx` (accepts `data` prop and orchestrates sections; hides empty sections)
- [X] T005 [P] Add connectivity normalizer `frontend/src/components/dynamic/utils/normalizeConnectivity.js` (convert separate lists or strings into {type,label,distance}[])
- [X] T006 [P] Add section anchor IDs and smooth scroll helpers `frontend/src/components/dynamic/utils/scroll.js`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 — Render complete page from JSON (Priority: P1) 🎯 MVP

**Goal**: Render all sections from structured JSON without hardcoded data

**Independent Test**: Provide sample structured JSON → all sections render or hide gracefully

- [X] T007 [P] [US1] Implement `HeroSection.jsx` in `frontend/src/components/dynamic/HeroSection.jsx` (project_name, developer_name, location, possession_date, hero image optional)
- [X] T008 [P] [US1] Implement `AmenitiesSection.jsx` in `frontend/src/components/dynamic/AmenitiesSection.jsx` (grid rendering, empty hides)
- [X] T009 [P] [US1] Implement `ConnectivitySection.jsx` in `frontend/src/components/dynamic/ConnectivitySection.jsx` (table/list rendering from normalized items)
- [X] T010 [P] [US1] Implement `FloorPlanSection.jsx` in `frontend/src/components/dynamic/FloorPlanSection.jsx` (card grid without zoom behavior yet; empty hides)
- [X] T011 [US1] Implement `FAQsSection.jsx` in `frontend/src/components/dynamic/FAQsSection.jsx` (accordion; empty hides)
- [X] T012 [US1] Wire all sections in `DynamicLandingPage.jsx` and pass data props; ensure sections hide when arrays empty

**Checkpoint**: User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 — Beautiful animated UI (Priority: P2)

**Goal**: Add Framer Motion animations (fade/slide/parallax) and hover effects

**Independent Test**: Scroll reveals and hover animations function smoothly; hero parallax visible

- [X] T013 [P] [US2] Add section reveal animations using IntersectionObserver + Framer Motion variants in each section component
- [X] T014 [P] [US2] Add hover scale/shadow micro‑interactions for amenity cards and floor plan cards
- [X] T015 [US2] Add hero parallax background effect in `HeroSection.jsx` using motion value + scroll

**Checkpoint**: User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 — Image zoom for floor plans (Priority: P3)

**Goal**: Integrate lightbox/zoom for floor plan images

**Independent Test**: Clicking “View” opens image in lightbox with responsive zoom

- [X] T016 [P] [US3] Integrate React Image Lightbox (or equivalent) in `FloorPlanSection.jsx` with keyboard/touch navigation
- [X] T017 [US3] Implement fallback image usage for missing/broken URLs in `FloorPlanSection.jsx`

**Checkpoint**: All user stories should now be independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Robustness, performance, responsiveness

- [X] T018 [P] Add responsive refinements and typography adjustments across sections (mobile/tablet breakpoints)
- [X] T019 [P] Lazy-load large images and set width/height to reduce layout shift in `FloorPlanSection.jsx`
- [X] T020 [P] Add smooth scroll navigation links (e.g., from Hero “Know More” to Amenities) `frontend/src/components/dynamic/DynamicLandingPage.jsx`
- [ ] T021 (Optional) Add a minimal navbar or section dots for quick navigation

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

- **User Story 1 (P1)**: Depends on parent container and utils
- **User Story 2 (P2)**: Depends on US1 rendered sections
- **User Story 3 (P3)**: Depends on US1 floor plan cards

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
4. STOP and VALIDATE: Test User Story 1 independently with sample JSON
5. Demo rendered landing page

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Demo (MVP)
3. Add User Story 2 → Test independently → Demo
4. Add User Story 3 → Test independently → Demo
