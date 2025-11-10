# Research: Dynamic Landing Page (Auto‑Generated)

## Decisions

- Image zoom library: React Image Lightbox (or Headless Lightbox) with simple API and good mobile support.
- Fallback image for floor plans: `/assets/placeholder-floorplan.png` (neutral gray grid with icon).
- Connectivity schema: Accept both formats — (A) separate lists (schools/hospitals/transport) and (B) single array of strings; normalize into an internal list of {type, label, distance}.
- Animations: Framer Motion with fade/slide on section reveal (intersection observer), subtle hover scale on cards, parallax on hero background via motion value + scroll.
- Theming: Tailwind gradient from indigo→purple (consistent with earlier specs), glassmorphism cards, Inter/Poppins fonts.

## Rationale

- Lightbox choice: Widely used, SSR-friendly patterns exist, minimal code to integrate; good keyboard/touch navigation.
- Fallback image: Prevents broken UI when a URL is missing while signaling that content is unavailable.
- Schema normalization: Real data may vary; an adapter ensures robust rendering without changing upstream specs.
- Framer Motion: Declarative animations, integrates smoothly with React; motion optimizations for performance.
- Theming: Consistent brand look across specs; accessible contrast.

## Alternatives Considered

- React Image Zoom only: Good for zoom-in-place but less elegant for gallery/lightbox UX.
- Dedicated gallery frameworks: Heavier dependencies; unnecessary for MVP.
- Enforcing a single connectivity schema: Simpler but brittle to source variations.

## Best Practices

- Lazy-load large images; provide width/height to avoid CLS.
- Use IntersectionObserver to trigger animations once per section.
- Hide sections with no items; avoid rendering empty containers.
- Memoize derived lists (amenities grid, connectivity rows) for performance.
