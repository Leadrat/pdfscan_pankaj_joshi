# Research: Gemini-Driven Property Data Structuring

## Decisions

- Conflict resolution priority: Prefer OCR-derived values when they include explicit numeric patterns or clearer contextual evidence; otherwise keep previously extracted values.
- Input limits: Max combined input size 1,000,000 characters; 12s end-to-end timeout.
- Minimum required overview fields: project_name, developer_name, location.
- Language handling: English-only (discard non-English) prior to structuring.
- Logging scope: Summaries + key metrics with PII-safe redaction; do not persist raw prompts/responses.

## Rationale

- Numeric OCR precedence: Numeric entities (areas, counts, prices) often appear as labels in floor plan images; OCR can capture these where PDFs omit or compress tables.
- Limits: 1M / 12s provides headroom for rich brochures while bounding worst-case latency; aligns with “fast UX” and Flash model performance.
- Overview minimums: Identity and context (name, developer, location) make outputs actionable across UI and analytics.
- English-only: Reduces noise and improves schema accuracy given current audience; non-English can be supported later.
- Logging: Privacy-first while retaining observability for debugging and audits.

## Alternatives Considered

- Always prefer PDF: Rejected due to loss of image-only details in floor plans.
- No input cap: Rejected due to risk of timeouts and cost.
- Multilingual passthrough: Rejected for this phase; potential future enhancement with language routing.
- Full prompt/response logging: Rejected due to privacy and compliance risk.

## Best Practices & Patterns

- Preprocessing: Normalize whitespace, deduplicate, remove watermarks/boilerplate before prompting.
- Prompt engineering: Provide schema and strict JSON-only instruction; include examples; set low temperature.
- Validation: Strict JSON parsing with schema validation; fallback repair pass on malformed JSON.
- Storage: Persist final structured JSON and minimal audit logs; avoid raw LLM content.
