export const MotionTokens = {
  durations: { enter: 0.2, exit: 0.18, hover: 0.15 },
  easings: { enter: 'easeOut', exit: 'easeIn' },
  variants: {
    page: { hidden: { opacity: 0, y: 8 }, show: { opacity: 1, y: 0 } },
    section: { hidden: { opacity: 0, y: 10 }, show: { opacity: 1, y: 0 } },
    hover: { whileHover: { scale: 1.02 } },
  },
};

export function prefersReducedMotion() {
  if (typeof window === 'undefined') return false;
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}
