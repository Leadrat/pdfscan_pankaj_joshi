# Gallery Implementation Context

## Technology Stack
- **Frontend**: React 18+ with Vite
- **UI Library**: React 18, Framer Motion
- **Styling**: TailwindCSS with custom theme
- **Image Handling**: react-medium-image-zoom
- **State Management**: React Context + useReducer
- **Performance**: React.lazy, Suspense, WebP with fallbacks

## Key Components
- `Gallery`: Main container component
- `GalleryCard`: Individual image card with hover/focus states
- `ImageModal`: Full-screen modal with zoom/pan
- `CarouselControls`: Navigation controls for the carousel
- `LoadingSkeleton`: Loading state placeholder
- `ErrorBoundary`: Error handling wrapper

## Performance Considerations
- Lazy loading with Intersection Observer
- WebP format with JPEG/PNG fallbacks
- Optimized image loading with placeholders
- Code splitting with React.lazy
- Memoized components with React.memo

## Accessibility Features
- ARIA labels and roles
- Keyboard navigation
- Reduced motion support
- Focus management
- Screen reader support
