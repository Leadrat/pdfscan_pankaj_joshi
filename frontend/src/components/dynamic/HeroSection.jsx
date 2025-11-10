import { motion, useScroll, useTransform } from 'framer-motion';

export default function HeroSection({ overview, onKnowMoreId = 'amenities' }) {
  if (!overview) return null;
  const { scrollY } = useScroll();
  const y = useTransform(scrollY, [0, 400], [0, -60]);

  return (
    <section id="overview" className="relative overflow-hidden">
      <motion.div style={{ y }} className="absolute inset-0 pointer-events-none bg-gradient-to-b from-indigo-50 to-white" />
      <div className="relative max-w-6xl mx-auto px-6 py-16 grid grid-cols-1 md:grid-cols-2 items-center gap-8">
        <div>
          <motion.h1 initial={{ opacity: 0, y: 10 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.5 }} className="text-3xl sm:text-4xl md:text-5xl font-bold text-slate-900">
            {overview.project_name || 'Project'}
          </motion.h1>
          <motion.p initial={{ opacity: 0, y: 10 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.6, delay: 0.1 }} className="mt-3 text-slate-700">
            {overview.developer_name ? `${overview.developer_name} · ` : ''}{overview.location || ''}
          </motion.p>
          <motion.p initial={{ opacity: 0, y: 10 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.6, delay: 0.15 }} className="mt-1 text-slate-600">
            {overview.possession_date ? `Possession: ${overview.possession_date}` : ''}
          </motion.p>
          <motion.button onClick={() => document.getElementById(onKnowMoreId)?.scrollIntoView({ behavior: 'smooth' })} initial={{ opacity: 0, y: 10 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.6, delay: 0.2 }} className="mt-6 inline-flex items-center px-5 py-3 rounded-lg text-white bg-indigo-600 hover:bg-indigo-700 shadow">
            Know More
          </motion.button>
        </div>
        <motion.div initial={{ opacity: 0, scale: 0.98 }} whileInView={{ opacity: 1, scale: 1 }} viewport={{ once: true }} transition={{ duration: 0.6, delay: 0.1 }} className="w-full h-64 md:h-80 rounded-2xl bg-gradient-to-r from-indigo-500 to-purple-600 shadow-lg">
          {overview.hero_image && (
            <img src={overview.hero_image} alt="Project" className="w-full h-full object-cover rounded-2xl" />
          )}
        </motion.div>
      </div>
    </section>
  );
}
