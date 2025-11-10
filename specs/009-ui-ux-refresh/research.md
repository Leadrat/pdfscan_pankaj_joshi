# Research: Global UI/UX Refresh — Glassmorphism, Gradients, Motion, Lottie

## Decisions

- Lottie library: `lottie-react` (simple React wrapper, SSR-friendly patterns, good performance for small loops).
- Gradient palette: Primary indigo→purple (consistent with earlier specs); secondary blue→teal for accents.
- Motion baseline: 180–240ms for transitions; ease-out for enters, ease-in for exits; respect `prefers-reduced-motion`.
- Glassmorphism tokens: backdrop-blur-md/lg, bg-white/10–20 with border-white/20, subtle shadows.
- Hover micro‑interactions: scale 1.02–1.04, shadow-lg on hover; reduced on low-power.

## Rationale

- `lottie-react` provides a clean API; avoids direct DOM imperative control; supports autoplay/loop props.
- Indigo→purple aligns with existing brand and keeps visual continuity.
- 180–240ms is a good middle ground: snappy yet noticeable; maintaining perceived speed.
- Glassmorphism requires careful contrast: layer gradient backgrounds with frosted cards and adequate text contrast.

## Alternatives Considered

- `lottie-web` directly: more control, but more boilerplate; not necessary for current scale.
- Blue→teal primary: attractive but deviates from current brand palette; keep as secondary.
- Heavier motion (300–400ms): risks sluggish feel; keep interactions quick.

## Best Practices

- Provide fallbacks for Lottie (skeleton or spinner) when assets fail to load.
- Centralize theme/motion tokens to ensure consistency.
- Test across mobile/tablet/desktop; validate reduced-motion flows.
