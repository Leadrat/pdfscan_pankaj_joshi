# Quickstart: Global UI/UX Refresh

## Scope
Apply a unified glassmorphism + gradient theme, smooth motion (Framer Motion), and Lottie animations across:
- Upload page
- Results dashboard
- Chatbot window
- Dynamic landing page

## Theme & Motion Tokens
Use tokens from `data-model.md`:
- ThemeTokens: gradients, glass backgrounds, radii, shadows
- MotionTokens: durations/easings/variants, reduced-motion handling
- LottieAssets: uploadSuccess, loading, pageTransition

## Implementation Hints
- Wrap top-level routes/pages with a Motion layout component using page variants
- Add section reveal (whileInView or IntersectionObserver) and hover micro-interactions
- Add glass styles to major panels: `backdrop-blur-lg bg-white/15 border border-white/20 shadow-xl`
- Keep contrast by using `text-slate-900` and `text-slate-600` on frosted cards

## Lottie Usage (example with lottie-react)
```jsx
import Lottie from 'lottie-react';
import uploadSuccess from '/lottie/upload_success.json';

export default function UploadSuccessBanner() {
  return (
    <div className="rounded-2xl backdrop-blur-lg bg-white/15 border border-white/20 p-4">
      <Lottie animationData={uploadSuccess} loop={false} autoplay={true} style={{ height: 120 }} />
    </div>
  );
}
```

## Page Transition (Framer Motion)
```jsx
import { motion } from 'framer-motion';
const page = { hidden: { opacity: 0, y: 8 }, show: { opacity: 1, y: 0, transition: { duration: 0.2, ease: 'easeOut' } } };

export default function PageShell({ children }) {
  return (
    <motion.div variants={page} initial="hidden" animate="show">
      {children}
    </motion.div>
  );
}
```

## Reduced Motion
Respect user preferences:
- Check `window.matchMedia('(prefers-reduced-motion: reduce)')`
- Use conditional variants or minimal transitions

## Testing
- Verify responsiveness on mobile/tablet/desktop
- Ensure transitions finish in 150–300ms; no jank
- Trigger Lottie on upload success and long operations
- Check contrast/readability on glass backgrounds
