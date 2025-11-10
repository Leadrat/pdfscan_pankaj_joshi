# Feature Specification: Leadrat Spec 4 — PDF Image Extraction & Gallery

**Feature Branch**: `[004-image-extraction]`  
**Created**: 2025-11-10  
**Status**: Draft  
**Input**: User description: "Extract images from uploaded PDFs using PyMuPDF, save PNGs with metadata, expose `/extract-images` API, and build a React gallery with zoom and responsive layout."

## Clarifications

### Session 2025-11-10

- Q: What is the default re-extraction behavior? → A: Do not re-extract by default; allow `reextract=true` to force.

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

### User Story 1 - Extract images and return JSON (Priority: P1)

As a developer, I want to extract all images from a previously uploaded PDF and return their metadata and URLs so the frontend can render a gallery.

**Why this priority**: Core data feed for the gallery and later analysis.

**Independent Test**: POST `/extract-images?filename=<pdf>` → JSON response with `total_images` > 0 and an array of `{filename, page_number, dimensions, url}`.

**Acceptance Scenarios**:

1. **Given** a PDF containing images, **When** I hit `/extract-images`, **Then** the API returns status=success with a non-empty list and valid URLs.
2. **Given** a PDF with no images, **When** I hit `/extract-images`, **Then** the API returns status=error and message `No images found in PDF.`

---

### User Story 2 - Store metadata and compress images (Priority: P2)

As a developer, I want image files saved efficiently as PNG with metadata in SQLite so retrieval and display are fast and consistent.

**Why this priority**: Enables efficient local storage and consistent image quality.

**Independent Test**: After extraction, check `extracted_images` table contains filename, page_number, width, height, file_path; large images are compressed with preserved aspect ratio.

**Acceptance Scenarios**:

1. **Given** an extracted image > 2MB, **When** saved, **Then** it is resized by ~25% (maintaining aspect ratio) and stored as `.png`.
2. **Given** saved metadata, **When** I query the DB, **Then** the record exists and `file_path` matches the URL returned by the API.

---

### User Story 3 - Interactive gallery with zoom (Priority: P3)

As a user, I want to browse and zoom into extracted images in a responsive gallery so I can inspect details clearly on any device.

**Why this priority**: Delivers the core UX value.

**Independent Test**: Gallery page loads grid with responsive columns; clicking an image opens a zoom modal with navigation and close.

**Acceptance Scenarios**:

1. **Given** a grid of images, **When** I click an image, **Then** a modal opens and allows zoom and pan; ESC or (X) closes.
2. **Given** a mobile viewport, **When** I open the gallery, **Then** the grid shows 1 per row and zoom modal scales appropriately.

---

[Add more user stories as needed, each with an assigned priority]

### Edge Cases

- PDFs with mixed formats (JPEG/PNG/JBIG2/JPEG2000) → convert to PNG consistently.
- Corrupt images → skip with error log; continue processing others.
- Duplicate extraction for same file → avoid reprocessing by checking DB presence; return existing entries.
- Very large images → compress and maintain aspect ratio; never upscale.

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: Backend MUST extract images from PDF using PyMuPDF and save PNGs to `backend/static/images/` with name `{original}_page{n}_img{m}.png`.
- **FR-002**: Backend MUST store metadata in SQLite table `extracted_images` (id, filename, page_number, width, height, file_path, created_at).
- **FR-003**: Backend MUST expose `POST /extract-images?filename=<name>` returning `{status, total_images, images:[{id, filename, page_number, dimensions, url}]}`.
- **FR-004**: If no images found, return error JSON with message `No images found in PDF.`
- **FR-005**: Images > 2MB MUST be compressed by ~25% while preserving aspect ratio (using Pillow); all outputs `.png`.
- **FR-006**: Frontend MUST render a responsive gallery grid (4/2/1 columns for desktop/tablet/mobile) with hover animations.
- **FR-007**: Frontend MUST open a zoom viewer modal on click (react-medium-image-zoom or Framer Motion), with navigation arrows and close.
- **FR-008**: Filenames MUST be sanitized; API responses MUST NOT expose absolute filesystem paths; URLs SHOULD be under `/static/images/...`.
- **FR-009**: Logs MUST include filename, total_images, duration, and errors; log file: `/logs/image_extraction.log` (if available) and console.
- **FR-010**: Avoid reprocessing same PDF by checking existing DB entries; allow explicit re-extract via query flag (NEEDS CLARIFICATION: default false).
  - Default: No re-extraction; force via `reextract=true` query flag.

Assumptions

- Uploaded PDFs exist under `backend/static/uploads/` or temp; filenames from Spec 2.
- Frontend uses existing Vite React app from Spec 1.
- Zoom viewer can be implemented with `react-medium-image-zoom` or Framer Motion-based custom modal.

### Key Entities *(include if feature involves data)*

- **extracted_images (SQLite)**:
  - id (PK, autoincrement)
  - filename (string) — saved image file name
  - page_number (int)
  - width (int)
  - height (int)
  - file_path (string) — relative `/static/images/...`
  - created_at (timestamp)

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: `/extract-images` returns success with `total_images` matching extracted file count and valid URLs.
- **SC-002**: Gallery renders within 1s after data fetched (local dev) and supports smooth zoom without visible pixelation.
- **SC-003**: At least 95% of images are stored under 2MB after compression without noticeable distortion.
- **SC-004**: Logs include filename and duration for 100% of extraction attempts; errors logged when present.
