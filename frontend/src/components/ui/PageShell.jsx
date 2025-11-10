import { motion } from 'framer-motion';
import { MotionTokens, prefersReducedMotion } from '../../theme/motion';

const base = MotionTokens.variants.page;

export default function PageShell({ children }) {
  const reduced = prefersReducedMotion();
  const variants = reduced
    ? { hidden: { opacity: 1, y: 0 }, show: { opacity: 1, y: 0 } }
    : { ...base, show: { ...base.show, transition: { duration: 0.2, ease: 'easeOut' } } };
  return (
    <motion.div variants={variants} initial="hidden" animate="show">
      {children}
    </motion.div>
  );
}
