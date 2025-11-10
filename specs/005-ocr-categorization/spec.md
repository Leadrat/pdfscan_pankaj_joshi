# Feature Specification: Leadrat Spec 5 — Hybrid OCR & Image Categorization

**Feature Branch**: `[005-ocr-categorization]`  
**Created**: 2025-11-10  
**Status**: Draft  
**Input**: User description: "Use pytesseract + EasyOCR with OpenCV preprocessing to extract floor plan details (area, tower, BHK, price) and categorize images (floor plan, layout, amenities, map); store structured JSON + SQLite; expose /extract-ocr-data API and lightweight viewer."

## Clarifications

### Session 2025-11-10

- Q: Which OCR languages to load by default? → A: English + Hindi (`['en','hi']`).

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

### User Story 1 - OCR pipeline with preprocessing (Priority: P1)

As a developer, I want to preprocess images and run pytesseract + EasyOCR to extract clean text so we can reliably capture floor-plan details.

**Why this priority**: OCR quality determines downstream structured insights.

**Independent Test**: Run `/extract-ocr-data` on images in `/static/images/` → success JSON with non-empty text and structured fields for at least a subset of images.

**Acceptance Scenarios**:

1. **Given** a floor plan image, **When** preprocessing (grayscale, threshold, denoise, deskew, CLAHE, resize) + OCR runs, **Then** combined text contains expected patterns (BHK, sq.ft, tower).
2. **Given** a noisy image, **When** OCR runs, **Then** output is still produced with best-effort cleaning (or an error entry recorded).

---

### User Story 2 - Categorize images (Priority: P2)

As a developer, I want to categorize images (Floor Plan, Layout, Amenities, Location Map, Elevation, Master Plan) using textual patterns and basic visual cues so results can be filtered.

**Why this priority**: Enables quick grouping and filtering in the UI and later AI steps.

**Independent Test**: On a mixed set, classification returns at least one non-empty category with a reasonable mapping based on detected keywords (BHK, sq.ft, Gym, Map, Road).

**Acceptance Scenarios**:

1. **Given** an image containing “3BHK” and “1200 sq.ft”, **When** categorized, **Then** it is labeled as “Floor Plan”.
2. **Given** an image containing “Gym” and “Club”, **When** categorized, **Then** it is labeled as “Amenities”.

---

### User Story 3 - Structured output, storage, and API (Priority: P3)

As a developer, I want the system to store structured OCR results in SQLite and return a clean JSON via API so downstream modules (Gemini) can consume it.

**Why this priority**: Provides a consistent interface for later specs.

**Independent Test**: POST `/extract-ocr-data` returns success JSON with `total_images_processed` and per-image `{image, category, details{…}}`; DB table has corresponding rows.

**Acceptance Scenarios**:

1. **Given** processed images, **When** I query the DB, **Then** I see one row per image with extracted_text and structured_json.

---

[Add more user stories as needed, each with an assigned priority]

### Edge Cases

- Images with very small fonts → upscale to minimum 1024px width before OCR.
- Multilingual text → EasyOCR supports multiple langs; default en; add ‘hi’ if needed.
- Watermarks/background artifacts → removed by morphological ops and thresholding where possible.
- Unreadable images → record `{ "error": "Text not detected" }` for that image.

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: Preprocess images (grayscale, threshold, denoise, morphology, deskew, CLAHE, resize to ≥1024px width) and save outputs under `/processed/`.
- **FR-002**: Run OCR using pytesseract and EasyOCR (default languages `['en','hi']`); merge outputs (deduplicate lines; prefer clearer segments).
- **FR-003**: Post-process text: regex normalization for units (sq.ft, sqmt), BHK patterns, price formats; remove special chars/watermarks.
- **FR-004**: Extract fields when present: tower_name, bhk_type, carpet_area, super_area, price; and amenity references.
- **FR-005**: Categorize images using keyword-based rules; optionally add simple visual cues (contours/layout density).
- **FR-006**: Store results in SQLite table `ocr_extracted_data(image_name, category, extracted_text, structured_json, created_at)`; one row per image.
- **FR-007**: Provide `POST /extract-ocr-data` endpoint returning `{status, total_images_processed, data:[{image, category, details{…}}]}`; include errors per image when present.
- **FR-008**: Log file/console with filename, duration, success/failure; cache EasyOCR reader to avoid reloads.
- **FR-009**: Security: sanitize filenames, restrict to files in `/static/images/` set, do not expose absolute paths.
- **FR-010**: Performance: process typical batch (6–10 images) in ≤ 10s locally; parallelize or cache where useful.

Assumptions

- Images come from Spec 4 and are available in `backend/static/images/`.
- OCR languages default to English + Hindi (`['en','hi']`); can extend later.
- API is backend-only; a simple frontend viewer is a stretch goal.

### Key Entities *(include if feature involves data)*

- **ocr_extracted_data (SQLite)**:
  - id (PK, autoincrement)
  - image_name (string)
  - category (string)
  - extracted_text (text)
  - structured_json (text JSON)
  - created_at (timestamp)

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: On a batch of 6–10 mixed images, endpoint completes ≤ 10s and returns non-empty structured fields for at least 50% of floor plan images.
- **SC-002**: Structured JSON follows consistent keys; missing values are null/empty rather than omitted.
- **SC-003**: Logs include filename and duration for 100% of processed images; errors captured for failures.
- **SC-004**: Preprocessing improves OCR text length/quality by ≥ 20% vs. raw (spot check).
