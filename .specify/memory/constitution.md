<!--
Sync Impact Report
- Version change: (none) → 1.0.0
- Modified principles: [placeholders] → Simplicity; Intelligence; Speed; Reliability; Delight; Data Privacy & Security; Accessibility & Performance; Observability & Logging
- Added sections: Technology & Architecture; Development Workflow & Quality Gates
- Removed sections: None
- Templates requiring updates:
  ✅ .specify/templates/plan-template.md (aligned)
  ✅ .specify/templates/spec-template.md (aligned)
  ✅ .specify/templates/tasks-template.md (aligned)
- Follow-up TODOs: None
-->

# Leadrat Constitution
<!-- Constitution for Leadrat: intelligent real estate brochure → interactive landing page system -->

## Core Principles

### Simplicity
Leadrat MUST offer an intuitive, streamlined workflow: upload → extract → structure → chat → auto-page.
UI elements MUST minimize cognitive load by adhering to the design system and avoiding unnecessary configuration.

### Intelligence
Use Gemini 2.5-Flash to structure brochure data into JSON (Overview, Amenities, Connectivity, Floor Plans, FAQs).
Combine PDF text, OCR results, and image metadata for context-aware outputs.

### Speed
Favor asynchronous processing, lazy loading, and optimized bundles.
Target Lighthouse performance scores ≥ 90.

### Reliability
Strong error handling with graceful fallbacks for OCR/LLM failures.
Use robust logging and clear user feedback (toasts, states).

### Delight
Employ modern aesthetics (glassmorphism, gradients) and subtle animations via Framer Motion.
Provide responsive, mobile-first experiences across screens.

### Data Privacy & Security
Do not persist API keys in code; use environment variables (`.env`).
Restrict uploaded PDF access to project scope. Sanitize inputs and handle files safely.

### Accessibility & Performance
Use ARIA labels, sufficient contrast, and keyboard navigation.
Lazy-load images; optimize and compress assets; implement responsive images.

### Observability & Logging
Log every major backend operation with contextual metadata.
Emit structured logs for extractions, OCR, LLM calls, and storage events.

## Technology & Architecture
<!-- Tech stack, constraints, storage, theming -->

- Frontend: React (Vite), Tailwind CSS, Framer Motion, Axios, React Router DOM,
  Lottie React, react-medium-image-zoom, ShadCN UI.
- Backend: Python Flask, Flask-CORS, PyMuPDF/pdfminer.six, pdf2image,
  pytesseract + EasyOCR, Google Generative AI SDK (Gemini 2.5-Flash), SQLite,
  python-dotenv, logging.
- Storage: `/uploads` for PDFs; `/static/images/` for extracted images;
  SQLite for uploads, extraction logs, structured data.
- Theming: Primary gradient from-indigo-500 to-purple-600, accent emerald-400,
  dark background #0f172a, fonts Inter/Poppins.
- Non-functional targets: Accessibility, performance (Lighthouse ≥ 90), security
  of secrets and user data, observability via structured logs.

## Development Workflow & Quality Gates
<!-- Workflow, reviews, gates, performance -->

- Upload: Drag-drop, PDF only, ≤ 25 MB, progress feedback, Lottie success.
- Extraction: `/api/extract-text` with cleaned structured text per page;
  image extraction to `/static/images/` with metadata; OCR preprocessing
  (grayscale, denoise, threshold, deskew) via Tesseract + EasyOCR.
- LLM Structuring: Merge text + OCR + image metadata → Gemini 2.5-Flash → JSON
  sections (Overview, Amenities, Connectivity, Floor Plans, FAQs) with loading
  animation during processing.
- Chatbot: Contextual Q&A powered by Gemini; when data is missing → respond
  "No idea based on brochure."
- Dynamic Landing Page: Auto-generate Hero, Amenities Grid, Connectivity Table,
  Floor Plan Gallery, FAQs; responsive with Framer Motion animations.
- UI/UX: Glassmorphism, gradient themes, micro-interactions, consistent
  typography and contrast.
- Error Handling & Logging: Python logging for major ops; try/except in Flask
  routes; user toasts for errors; graceful LLM/OCR failure handling.
- Performance & Accessibility: Lazy-loading images, ARIA labels, bundle size
  optimization, render-blocking reduction, Lighthouse ≥ 90.

## Governance
<!-- Example: Constitution supersedes all other practices; Amendments require documentation, approval, migration plan -->

This constitution supersedes other practices for Leadrat. All work MUST comply.

Amendments
- Propose via PR including a Sync Impact Report, version bump rationale, and any
  migration/communication plan.
- Changes considered:
  - MAJOR: Backward-incompatible governance updates or principle removals/
    redefinitions.
  - MINOR: New principles/sections or materially expanded guidance.
  - PATCH: Clarifications, non-semantic refinements, typos.

Approvals
- At least one backend and one frontend reviewer, or a designated domain lead.
- PRs MUST document compliance with principles and quality gates.

Security & Privacy
- API keys via `.env`; never committed. Handle PII cautiously; minimize
  retention and scope.

Observability
- Log extraction, OCR, LLM calls, and storage events with structured context.
  Avoid sensitive payloads in logs.

**Version**: 1.0.0 | **Ratified**: 2025-11-10 | **Last Amended**: 2025-11-10
<!-- Example: Version: 2.1.1 | Ratified: 2025-06-13 | Last Amended: 2025-07-16 -->
