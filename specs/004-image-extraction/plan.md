# Implementation Plan: Leadrat Spec 4 — PDF Image Extraction & Gallery

**Branch**: `004-image-extraction` | **Date**: 2025-11-10 | **Spec**: ./spec.md
**Input**: Feature specification from `/specs/004-image-extraction/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement image extraction from PDFs using PyMuPDF, saving PNGs to `backend/static/images/` with
metadata in SQLite. Expose `POST /extract-images?filename=<name>[&reextract=true]` returning a list of
image URLs and metadata. Build a responsive React gallery with zoom (react-medium-image-zoom or
Framer Motion modal) and navigation. Compress images >2MB by ~25% while preserving aspect ratio.

## Technical Context

**Language/Version**: Backend Python 3.11; Frontend Vite React.  
**Primary Dependencies**: PyMuPDF (fitz), Pillow (PIL), Flask, SQLAlchemy/SQLite; Frontend: react-medium-image-zoom or Framer Motion + Tailwind.  
**Storage**: SQLite table `extracted_images`; files under `backend/static/images/`.  
**Testing**: Manual validation with mixed PDFs (floor plans, layouts, high-res maps).  
**Target Platform**: Local development on Windows.  
**Project Type**: Web (frontend + backend).  
**Performance Goals**: Extraction completes within practical time; gallery renders ≤1s after data fetch; images compressed >2MB.  
**Constraints**: No deploy; local only; reextract=false by default with `reextract=true` override.  
**Scale/Scope**: Image extraction only (no OCR layer); viewer zoom/pan with responsive grid.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Reliability & Observability: Log filename, total_images, duration, and errors; safe error JSON.  
- Simplicity: Single endpoint `/extract-images`; consistent PNG outputs and naming.  
- Security & Privacy: Sanitize filenames; PDF-only; do not expose absolute paths.  
- Accessibility & Performance: Responsive grid; lazy-loading recommended; compression for large files.  

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
├── routes/
│   └── image_routes.py          # POST /extract-images
├── models/
│   └── extracted_image.py       # extracted_images table
├── static/
│   └── images/                  # extracted PNGs
└── logs/image_extraction.log    # optional file log

frontend/
└── src/pages/ImageGallery.jsx   # responsive grid + zoom modal
```

**Structure Decision**: Extend existing backend with `image_routes.py` and a dedicated `extracted_images`
model; add a new `ImageGallery` page in frontend using zoom library or Framer Motion modal.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
