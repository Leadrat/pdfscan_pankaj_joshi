# Quickstart: Robust Error Handling & Logging

## Overview
Add friendly error handling, structured logging, and graceful fallbacks across:
- PDF upload
- OCR extraction
- Gemini LLM processing
- UI rendering (Error Boundaries)

## Frontend
- Toasts: React Hot Toast
- Error Boundaries: wrap primary trees; show fallback with "Try Again"
- Messages:
  - Invalid PDF → "Invalid or unreadable PDF. Please try a different file."
  - OCR failure → "Some text could not be extracted — partial data shown."
  - LLM failure/timeout → "AI data extraction failed. Please retry later."
- Retry: Provide CTA to re‑attempt extraction/fetch when logical

## Backend
- Structured JSON logs for steps: pdf_upload, ocr_extraction, gemini_request, ui_render
- Fields: timestamp, step, status (success/failure), duration_ms?, safe context
- Rotation: 10 MB/file, keep 5 files, 7‑day cap under /logs
- LLM retries: up to 2 with backoff (1s, 2s)

## Testing Scenarios
- Upload a corrupted PDF → expect invalid PDF toast, no crash
- Force OCR error (bad image) → partial data toast; UI shows placeholders
- Simulate Gemini timeout → retry then friendly error; partial UI still renders
- Throw in a component → Error Boundary shows fallback; retry remounts component
