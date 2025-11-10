# Data Model: Robust Error Handling & Logging

## Entities

### LogEvent
- timestamp: string (ISO)
- step: string (e.g., "pdf_upload", "ocr_extraction", "gemini_request", "ui_render")
- status: string ("success" | "failure")
- duration_ms?: number
- context?: object (safe, minimal; no secrets)

### UserToast
- id: string
- message: string
- type: string ("success" | "error" | "info")
- action?: { label: string, onClick: string }

### ErrorBoundaryState
- hasError: boolean
- errorInfo?: string

## Validation Rules
- LogEvent must include timestamp, step, status; duration_ms when measurable.
- UserToast messages must be user‑friendly and never contain technical stack traces.
- ErrorBoundary must render fallback UI with retry capability.
