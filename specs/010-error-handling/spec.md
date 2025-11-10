# Feature Specification: Robust Error Handling & Logging

**Feature Branch**: `010-error-handling`  
**Created**: 2025-11-10  
**Status**: Draft  
**Input**: Make the entire PDF→OCR→LLM→Landing pipeline fault‑tolerant with user‑friendly feedback and structured backend logs. Handle invalid PDFs, OCR failures (fallback/partial), Gemini timeouts/invalid JSON, and UI crashes (Error Boundaries). Show friendly toasts with retry actions and never leave the UI empty.

## Clarifications

### Session 2025-11-10

- Q: Preferred frontend toast library? → A: React Hot Toast.
 - Q: Log retention/rotation policy? → A: Size+count rotation (10 MB/file, keep 5 files) with 7‑day cap.
 - Q: LLM retry attempts and backoff? → A: 2 retries with exponential backoff (1s, 2s).

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - Friendly, actionable user feedback (Priority: P1)

As a user, whenever something fails (invalid PDF, OCR issues, LLM timeout), I see a clear toast/snackbar with a short message and, where appropriate, a retry button. The app continues to function and shows partial data or placeholders.

**Why this priority**: Prevents confusion and abandonment; keeps experience professional.

**Independent Test**: Force an invalid PDF upload, an OCR error, and an LLM timeout; observe accurate messages and presence of a Retry where relevant.

**Acceptance Scenarios**:

1. **Given** a corrupted PDF, **When** I upload it, **Then** I see “Invalid or unreadable PDF. Please try a different file.”
2. **Given** an OCR failure, **When** extraction runs, **Then** I see “Some text could not be extracted — partial data shown.” and the UI renders partial results.

---

### User Story 2 - Structured backend logging (Priority: P2)

As a developer, I need structured JSON logs for each major step (upload, OCR, LLM, page render) with timestamps and status, to diagnose issues quickly.

**Why this priority**: Improves traceability and reduces MTTR.

**Independent Test**: Trigger success and failure paths and verify logs contain step names, status, and minimal context.

**Acceptance Scenarios**:

1. **Given** an LLM timeout, **When** the error occurs, **Then** a JSON log is emitted with step="gemini_request", status="failure", and a safe error summary.
2. **Given** a successful OCR, **When** completed, **Then** a JSON log is emitted with step="ocr_extraction", status="success", and duration.

---

### User Story 3 - UI stability via Error Boundaries (Priority: P3)

As a user, the app never crashes to a blank screen. If a component throws, an Error Boundary shows a friendly message and a “Try Again” action.

**Why this priority**: Protects UX from unforeseen client errors.

**Independent Test**: Simulate a render error; ensure the boundary displays a friendly message and recovery option.

**Acceptance Scenarios**:

1. **Given** a render exception in a section, **When** it occurs, **Then** a friendly fallback appears and navigation remains usable.
2. **Given** a retry action, **When** clicked, **Then** the component remounts and attempts to recover.

---

### Edge Cases

- Very large PDFs or network interruptions mid‑upload → show progress errors and allow retry
- Mixed partial data from OCR/LLM → render placeholders and badges like “Partial Data”
- Invalid JSON from LLM → attempt repair; if impossible, show fallback and keep UI functional
- Repeated failures → avoid toast spam; consolidate messages and suggest alternative actions

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Detect invalid/corrupted PDFs and show “Invalid or unreadable PDF. Please try a different file.”
- **FR-002**: On OCR failures, present partial data with the message “Some text could not be extracted — partial data shown.”
- **FR-003**: On Gemini failures/timeouts/invalid JSON, show “AI data extraction failed. Please retry later.” and render available partial data.
  - Clarification: Apply up to 2 retries with exponential backoff (1s, 2s) before failing and surfacing the friendly error.
- **FR-004**: Wrap primary React trees with Error Boundaries; render friendly fallback UI with retry.
- **FR-005**: Use a toast/snackbar system for user‑visible errors; no raw technical errors exposed to users.
  - Clarification: Use React Hot Toast for toasts.
- **FR-006**: Provide retry actions where logical (e.g., re‑attempt extraction or fetch).
- **FR-007**: Emit structured JSON logs for key steps with timestamp, step name, status (success/failure), and minimal context. Store under `/logs` when file logging is enabled.
  - Clarification: Rotate by size/count (10 MB/file, keep 5 files) and cap retention at 7 days.
- **FR-008**: Always render some UI (placeholders) even during partial failures; never blank screens.

*NEEDS CLARIFICATION (max 3):*

- **NC-1**: Preferred frontend toast library (React Hot Toast vs Material Snackbar)? [NEEDS CLARIFICATION]
- **NC-2**: Log retention policy and rotation on disk? [NEEDS CLARIFICATION]
- **NC-3**: Maximum retry attempts and backoff strategy for LLM calls? [NEEDS CLARIFICATION]

### Key Entities *(include if feature involves data)*

- **LogEvent**: { timestamp, step, status, duration_ms?, context } (structured JSON)
- **UserToast**: { id, message, type, action? } (frontend only)
- **ErrorBoundaryState**: { hasError, errorInfo? }

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All failure scenarios produce friendly user messages with no raw errors displayed.
- **SC-002**: Backend structured logs exist for each major step on both success and failure paths.
- **SC-003**: The UI never renders a blank page; placeholders or partial content appear instead.
- **SC-004**: Retry flows succeed where possible; otherwise the system degrades gracefully without loops or crashes.
