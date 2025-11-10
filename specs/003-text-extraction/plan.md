# Implementation Plan: Leadrat Spec 3 — PDF Text Extraction

**Branch**: `003-text-extraction` | **Date**: 2025-11-10 | **Spec**: ./spec.md
**Input**: Feature specification from `/specs/003-text-extraction/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a switchable PDF text extraction pipeline (default PyMuPDF; pdfminer alternative) to parse
uploaded PDFs, clean and structure content (project details, amenities, contact, etc.), store the
result temporarily in SQLite, and expose it via `GET /extract-text?filename=<name>` returning a
clean JSON with `raw_text_length`. Temp files live in `backend/static/uploads/temp` with a daily
purge. Missing fields use null (scalars), [] (lists), {} (objects).

## Technical Context

**Language/Version**: Backend Python 3.11.  
**Primary Dependencies**: PyMuPDF (`fitz`), pdfminer.six, Flask, SQLite, python-dotenv, regex libs.  
**Storage**: SQLite `pdf_data.db` (table `extracted_text`), temp files under `backend/static/uploads/temp`.  
**Testing**: Manual validation on 5 sample PDFs with logs and JSON inspection; automated tests deferred.  
**Target Platform**: Local development on Windows.  
**Project Type**: Web backend feature (integrated with existing Flask app).  
**Performance Goals**: 10–20 page text-based PDF extracts ≤ 10s; memory usage stable (no full file memory load).  
**Constraints**: Default engine PyMuPDF; filename query param; missing-field policy enforced; daily purge of temp.  
**Scale/Scope**: Extraction only (no OCR); structured fields best-effort via keywords/regex.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Reliability & Observability: Structured logs (duration, filename), clear error JSON; no secrets.  
- Simplicity: One endpoint `/extract-text`, simple flag for engine selection.  
- Security & Privacy: Sanitized filenames, PDF-only, size limits inherited from Spec 2, temp purge.  
- Accessibility & Performance: Backend focus; performance target defined; responsive pipeline.  

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
├── extraction/
│   ├── __init__.py
│   ├── engines.py               # engine switch (pymupdf/pdfminer)
│   ├── clean.py                 # whitespace/encoding/hyphen fixes
│   └── structure.py             # regex/keyword structuring
├── routes/
│   └── extract_routes.py        # GET /extract-text
├── models/
│   └── extracted_text.py        # SQLAlchemy model
└── static/uploads/temp/         # temp PDFs
```

**Structure Decision**: Add `extraction/` module for pluggable engines and cleaning; one route for
serving results; a dedicated model for `extracted_text`.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
