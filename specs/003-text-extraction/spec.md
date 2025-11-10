# Feature Specification: Leadrat Spec 3 — PDF Text Extraction

**Feature Branch**: `[003-text-extraction]`  
**Created**: 2025-11-10  
**Status**: Draft  
**Input**: User description: "Extract text from uploaded PDFs using PyMuPDF (fitz) or pdfminer.six, clean and structure it, store temporarily in SQLite, and expose via `/extract-text` API."

## Clarifications

### Session 2025-11-10

- Q: What should be the default extraction engine? → A: PyMuPDF (fitz).
- Q: Where to store temp PDFs and how to purge? → A: backend/static/uploads/temp; purge daily (scheduled or on app start).
- Q: How to serialize missing fields in JSON? → A: null for scalars; empty arrays for lists; empty objects for nested maps.
- Q: What request parameter should /extract-text use? → A: filename query param (e.g., /extract-text?filename=brochure.pdf).

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

### User Story 1 - Extract and return structured text (Priority: P1)

As a developer, I want to extract and clean text from an uploaded PDF and return it via an API so downstream modules can analyze it.

**Why this priority**: Foundational capability for data analysis and AI structuring.

**Independent Test**: Call `/extract-text?filename=<pdf>` for a previously uploaded file → receive success JSON with cleaned structured fields and raw text length.

**Acceptance Scenarios**:

1. **Given** a valid text-based PDF was uploaded, **When** I call `/extract-text`, **Then** I receive a JSON object with `status=success`, `data` fields (project_name, amenities, contact, etc.), and `raw_text_length` > 0.
2. **Given** a corrupt or missing PDF, **When** I call `/extract-text`, **Then** I receive `status=error` with message `Failed to extract text from PDF` and HTTP 400/500 as applicable.

---

### User Story 2 - Switchable extraction engine (Priority: P2)

As a developer, I want to switch between PyMuPDF and pdfminer via a config flag so I can balance speed vs. fidelity.

**Why this priority**: Flexibility for different brochure types.

**Independent Test**: Toggle a config flag and observe that extraction is performed by the selected engine (verified via logs and output parity).

**Acceptance Scenarios**:

1. **Given** engine=`pymupdf`, **When** extraction runs, **Then** logs indicate PyMuPDF and results are produced.
2. **Given** engine=`pdfminer`, **When** extraction runs, **Then** logs indicate pdfminer and results are produced.

---

### User Story 3 - Temporary storage & retrieval (Priority: P3)

As a developer, I want extracted text stored temporarily so the API can serve it and old entries can be purged.

**Why this priority**: Enables quick retrieval and decouples extraction from consumption.

**Independent Test**: After extraction, verify an `extracted_text` row exists with filename, raw_text, structured_data JSON, and created_at; entries older than 24h can be purged by a maintenance job.

**Acceptance Scenarios**:

1. **Given** a completed extraction, **When** I query the DB, **Then** the row exists with correct fields and timestamps.

---

[Add more user stories as needed, each with an assigned priority]

### Edge Cases

- PDF with mixed text and images: return text only; OCR deferred to later spec.
- Non-UTF-8 symbols: replace or drop; ensure JSON-safe output.
- Hyphenated words at line breaks: join intelligently.
- Empty or encrypted PDF: return `status=error` with message.
- Large PDFs (10–20 pages): extraction finishes in ≤10s on local dev.

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: System MUST support two engines for text extraction: PyMuPDF (`fitz`) and pdfminer.six, switchable via config.
  - Default engine: PyMuPDF (fitz). Environment/config flag can change engine.
- **FR-002**: System MUST parse PDFs page by page and extract clean text.
- **FR-003**: Cleaning MUST remove unwanted line breaks, excessive spaces, non-UTF-8 symbols, and fix hyphenated words.
- **FR-004**: System MUST detect and structure fields when present: project_name, developer, amenities, contact (phone/email/website/address), location, pricing, highlights, rera_number.
- **FR-005**: System MUST tag amenities via keyword lookup and extract contact info with regex.
- **FR-006**: Results MUST be saved to SQLite `extracted_text` table with filename, raw_text, structured_data JSON, created_at.
- **FR-007**: Provide `GET /extract-text?filename=<name>` endpoint returning JSON with status, message, data, and raw_text_length.
  - Missing-field policy: null for scalars; empty arrays for list fields; empty objects for nested maps.
- **FR-008**: Temporary storage MUST allow purging entries older than 24h (maintenance function or script).
  - Temp directory: `backend/static/uploads/temp`. Purge daily (scheduled or on app start).
- **FR-009**: Logs MUST include timestamp, filename, duration, and success/failure without leaking raw content.
- **FR-010**: For corrupt/missing PDFs, return error JSON with appropriate HTTP status (400/500) and safe message.

Assumptions

- PDFs are uploaded via Spec 2 and available under `backend/static/uploads/` or a temp path.
- Temp PDFs stored at `backend/static/uploads/temp/`; purge cadence: daily.
- `VITE_API_BASE` is configured; extraction invoked via backend only.
- OCR for image-only PDFs is out of scope here (future spec).

### Key Entities *(include if feature involves data)*

- **extracted_text (SQLite)**:
  - id (PK, autoincrement)
  - filename (string)
  - raw_text (text)
  - structured_data (text JSON)
  - created_at (timestamp)

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: 10–20 page text-based PDF extracts in ≤ 10s and returns JSON with `raw_text_length` > 0.
- **SC-002**: JSON includes expected keys; missing fields are null/empty rather than omitted.
- **SC-003**: Cleaning reduces duplicate whitespace and stray symbols by ≥ 95% compared to raw.
- **SC-004**: Logs include filename and duration for 100% of extraction attempts.
