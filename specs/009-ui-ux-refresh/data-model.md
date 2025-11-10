# Data Model: Global UI/UX Refresh

## ThemeTokens
- colors:
  - primaryGradient: "from-indigo-500 to-purple-600"
  - secondaryGradient: "from-sky-500 to-teal-500"
  - glassBg: "bg-white/15"
  - glassBorder: "border-white/20"
  - textPrimary: "text-slate-900"
  - textSecondary: "text-slate-600"
- radii:
  - card: "rounded-2xl"
  - button: "rounded-xl"
- shadows:
  - card: "shadow-xl"
  - hover: "shadow-2xl"
- blur:
  - panel: "backdrop-blur-lg"
- spacing:
  - base: Tailwind spacing scale (4, 6, 8, 12)

## MotionTokens
- durations:
  - enter: 0.2
  - exit: 0.18
  - hover: 0.15
- easings:
  - enter: "easeOut"
  - exit: "easeIn"
- variants:
  - page: { hidden: { opacity: 0, y: 8 }, show: { opacity: 1, y: 0 } }
  - section: { hidden: { opacity: 0, y: 10 }, show: { opacity: 1, y: 0 } }
  - hover: { whileHover: { scale: 1.02 } }
- reducedMotion:
  - disableTransitions: true when `prefers-reduced-motion`

## LottieAssets
- uploadSuccess: "/lottie/upload_success.json"
- loading: "/lottie/loading.json"
- pageTransition: "/lottie/page_transition.json"

## Validation Rules
- ThemeTokens MUST be applied consistently across major screens.
- MotionTokens MUST be used for page transitions and section reveals; honor reduced motion.
- LottieAssets SHOULD have fallbacks (skeleton/spinner) when unavailable.
