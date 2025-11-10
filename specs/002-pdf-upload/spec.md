# Feature Specification: Leadrat Spec 2 — PDF Upload & Storage

**Feature Branch**: `[002-pdf-upload]`  
**Created**: 2025-11-10  
**Status**: Draft  
**Input**: User description: "Users can upload PDF brochures with progress, validation, storage to backend/static/uploads, and metadata saved to SQLite; animated, responsive UI with Framer Motion + Tailwind and toasts."

## Clarifications

### Session 2025-11-10

- Q: How to handle duplicate filenames on upload? → A: Unique rename with numeric suffix (e.g., sample(1).pdf).

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

### User Story 1 - Upload a PDF with progress (Priority: P1)

As a user, I want to upload a real-estate brochure (PDF) and see progress so that I know the status and result of my upload.

**Why this priority**: Enables data ingestion pipeline; prerequisite for all extraction specs.

**Independent Test**: From UploadPage, select a valid .pdf < 20MB → progress animates → success toast → server stores file and returns metadata.

**Acceptance Scenarios**:

1. **Given** a valid brochure.pdf (≤ 20MB), **When** I upload it, **Then** I see progress, then a success toast, and response shows filename, path, size, and uploaded_at.
2. **Given** no file selected, **When** I click upload, **Then** I see an error toast "No file selected" and no request is sent.

---

### User Story 2 - Validation & errors (Priority: P2)

As a user, I want invalid uploads to be rejected with clear messages so I don’t waste time.

**Why this priority**: Prevents invalid input and improves UX.

**Independent Test**: Try uploading non-PDF or >20MB; receive error toast; backend rejects with 400.

**Acceptance Scenarios**:

1. **Given** a .png file, **When** I upload, **Then** I get a toast "Please upload a valid PDF file." and the server returns 400.
2. **Given** a 25MB PDF, **When** I upload, **Then** I get a toast "File too large (max 20MB)." and the server returns 400.

---

### User Story 3 - Store metadata in DB (Priority: P3)

As a developer, I want the backend to persist upload metadata so later phases can use it.

**Why this priority**: Required linkage between uploaded file and subsequent extraction steps.

**Independent Test**: After successful upload, verify a new PDFUpload row contains filename, size (MB), path, uploaded_at.

**Acceptance Scenarios**:

1. **Given** a successful upload, **When** I query the database, **Then** I find a PDFUpload row matching filename and size within ±0.1MB.

---

[Add more user stories as needed, each with an assigned priority]

### Edge Cases

- Duplicate filename: server applies unique rename with numeric suffix (e.g., sample(1).pdf) to avoid conflicts.
- Rapid double-submit: UI disables button during upload; backend guards against partial writes.
- Network drop mid-upload: UI shows error toast and resets progress.
- Large but valid ≤20MB file: progress updates smoothly; success upon completion.

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: Frontend MUST provide drag-and-drop or file picker restricted to `.pdf` with progress UI and toasts.
- **FR-002**: Backend MUST expose `POST /upload` accepting `multipart/form-data` with `file` key.
- **FR-003**: Backend MUST validate: extension `.pdf` and max size 20MB; return 400 on violation.
- **FR-004**: On success, backend MUST save file to `backend/static/uploads/` and return JSON: status, filename, path, size (MB), uploaded_at.
- **FR-005**: Backend MUST persist PDFUpload(filename, size, path, upload_date default now) to SQLite.
- **FR-006**: UI MUST animate progress using Framer Motion and show success UI on completion.
- **FR-007**: Errors MUST surface to users via toast messages; no secrets logged.

Assumptions

- Upload size limit: 20MB.
- Duplicate handling default: unique rename with suffix to avoid overwrite.
- API base URL provided via `VITE_API_BASE`.

### Key Entities *(include if feature involves data)*

- **PDFUpload**: id (PK), filename (str, required), size (float MB), path (str), upload_date (datetime default now).

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: Uploading a 5MB PDF completes with visible progress and returns success JSON in ≤ 10s on local dev.
- **SC-002**: Non-PDF or >20MB uploads are rejected with 400 and show error toast within ≤ 1s.
- **SC-003**: DB contains a new PDFUpload row with filename, size ±0.1MB of actual, and valid path.
- **SC-004**: No secrets in logs; errors are user-friendly and actionable.
