# Research: Chatbot Q&A from Brochure Data

## Decisions

- Session scope: Page-lifetime (resets on full reload; persists within SPA navigation).
- Max message length: 500 characters (truncate with notice if exceeded).
- Extraction-complete trigger: Explicit frontend flag set after Spec 6 response; chat icon renders only when flag=true.
- Answer policy: Strictly grounded to provided structured JSON; fallback phrase exactly "No idea based on brochure." when absent.
- Latency target: ≤ 3 seconds typical; show typing animation if > 600ms.

## Rationale

- Page-lifetime offers predictable behavior without complex storage; aligns with privacy.
- 500-char cap avoids prompt bloat and UI overflow; sufficient for factual queries.
- Explicit flag prevents race conditions and brittle inference of readiness.
- Grounded answers + exact fallback reduce hallucination risk and ambiguity.
- Typing animation improves perceived responsiveness for slower responses.

## Alternatives Considered

- Tab-lifetime/sessionStorage: Acceptable but may persist across reloads unexpectedly.
- LocalStorage persistence: Rejected for privacy; keep within session.
- Inferred readiness (e.g., DOM/data presence): Rejected; fragile and error-prone.

## Best Practices

- Build a minimal, immutable system prompt instructing grounding + fallback.
- Sanitize user input; enforce max length client-side and server-side.
- Log summaries/metrics only; avoid raw LLM content.
- Debounce input sends; disable submit while awaiting response.
