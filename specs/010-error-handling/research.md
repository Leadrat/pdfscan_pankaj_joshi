# Research: Robust Error Handling & Logging

## Decisions

- Frontend toasts: React Hot Toast (concise API; minimal overhead; suits our stack).
- Log rotation: Size+count (10 MB/file, keep 5 files) with 7‑day cap.
- LLM retries: Up to 2 retries with exponential backoff (1s, 2s) before surfacing failure.
- JSON logs: Structured with timestamp, step, status, duration_ms (when applicable), and minimal context (avoid sensitive payloads).
- Error Boundaries: Wrap primary React trees; friendly fallback with retry action; log boundary errors to console + optional endpoint.

## Rationale

- Hot Toast: Small footprint and fast integration; replace generic toasts; supports actions and theming.
- Rotation: Provides sufficient history while capping disk usage; 7‑day retention suits dev/test; can extend in prod.
- Backoff: Balances user latency and resiliency; avoids burst retries and rate limits.
- Structured logging: Enables quick filtering/searching; compatible with aggregators; protects PII.

## Alternatives Considered

- Material Snackbar: Heavier dependency; unnecessary for project scope.
- Time‑only rotation: Simpler but can bloat disk; size+count safer.
- 3+ retries: Increases latency; diminishing returns.

## Best Practices

- Frontend: Centralize toast helpers (success/error) to standardize copy and behavior; fade‑in with Framer Motion or library defaults.
- Backend: Log start/end of steps with the same step name; include duration; ensure errors include safe summaries; never log secrets or raw LLM prompts.
- Fallbacks: Keep placeholder content and badges (e.g., “Partial Data”) to set user expectations.
