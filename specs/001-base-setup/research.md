# Research: Leadrat Spec 1 — Base Environment Setup

## Decisions

- CORS Policy: ENV-configurable (default http://localhost:5173)
  - Rationale: Secure-by-default in dev while allowing overrides without code changes.
  - Alternatives: Allow all (*) — rejected due to security risk; Fixed list — less flexible.

- Env Handling: Commit `.env.example`; `.env` gitignored
  - Rationale: Standard practice to share config shape without secrets.
  - Alternatives: Commit `.env` with placeholders — risk of leaks; OS-only env — higher friction for onboarding.

- Backend Python Version: 3.11
  - Rationale: Widely supported, performant, minimal compatibility risk compared to 3.12.
  - Alternatives: 3.10 — older; 3.12 — some library lag.

- Frontend API Base URL: `VITE_API_BASE` with default `http://localhost:5000`
  - Rationale: Keeps URLs out of code, supports multiple environments via Vite.
  - Alternatives: Hardcode — brittle; Derive from location — brittle across proxies.

- Logging Format: Structured JSON (level, message, context)
  - Rationale: Preps for observability pipelines; easier parsing during dev.
  - Alternatives: Plain text — less machine-friendly; Disable logs — reduces diagnosability.

## Open Questions (Deferred to later specs)

- Async/background processing for extraction/OCR/LLM
- Structured schemas for text/image/OCR/Gemini outputs
- Accessibility and Lighthouse measurement process

## References
- Project constitution (v1.0.0)
- Spec: ./spec.md
