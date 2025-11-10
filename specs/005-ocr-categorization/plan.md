# Implementation Plan: Leadrat Spec 5 — Hybrid OCR & Image Categorization

**Branch**: `005-ocr-categorization` | **Date**: 2025-11-10 | **Spec**: ./spec.md
**Input**: Feature specification from `/specs/005-ocr-categorization/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement an OCR pipeline over images extracted in Spec 4: preprocess with OpenCV, run pytesseract
and EasyOCR (default langs ['en','hi']), merge outputs, normalize text, extract key fields (tower,
BHK, areas, price, amenities), categorize images (Floor Plan, Layout, Amenities, Map, etc.), store
in SQLite, and expose `POST /extract-ocr-data` returning structured JSON suitable for Gemini.

## Technical Context

**Language/Version**: Backend Python 3.11.  
**Primary Dependencies**: Flask, SQLAlchemy/SQLite, OpenCV, pytesseract, EasyOCR, Pillow, NumPy, scikit-image, regex.  
**Storage**: SQLite table `ocr_extracted_data`; input images under `backend/static/images/`; processed images under `/processed/`.  
**Testing**: Manual validation on 5+ mixed images; log timing and outputs; compare raw vs processed OCR quality.  
**Target Platform**: Local development on Windows.  
**Project Type**: Backend feature (plus optional small viewer page).  
**Performance Goals**: 6–10 images processed in ≤ 10s; EasyOCR reader cached; basic parallelization allowed.  
**Constraints**: Security sanitization for filenames; limit to images from static set; no absolute paths.  
**Scale/Scope**: No LLM validation in this spec; basic keyword/regex extraction and categorization.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Reliability & Observability: Structured logs with filename + duration; safe error JSON; retries allowed.  
- Simplicity: Single endpoint `/extract-ocr-data`; straightforward schema.  
- Security & Privacy: Sanitize filenames; restrict paths; no secrets in logs.  
- Accessibility & Performance: Backend focus; performance targets defined.  

Gate Result: PASS.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
backend/
├── ocr/
│   ├── __init__.py
│   ├── preprocess.py         # OpenCV & skimage pipeline
│   ├── engines.py            # pytesseract + EasyOCR merge
│   ├── extract.py            # field extraction + categorize
│   └── utils.py              # regex helpers, caching
├── routes/
│   └── ocr_routes.py         # POST /extract-ocr-data
├── models/
│   └── ocr_extracted.py      # ocr_extracted_data table
└── static/images/            # inputs (from Spec 4) + processed/
```

**Structure Decision**: Add `ocr/` module for preprocessing, OCR engines, and extraction/categorization
logic; expose a single route and dedicated model/table.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
