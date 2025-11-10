import { motion } from 'framer-motion';

export default function AmenitiesSection({ amenities = [] }) {
  if (!amenities || amenities.length === 0) return null;
  return (
    <section id="amenities" className="max-w-6xl mx-auto px-6 py-12">
      <motion.h2 initial={{ opacity: 0, y: 10 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} className="text-2xl font-semibold text-slate-900">Amenities</motion.h2>
      <div className="mt-6 grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
        {amenities.map((name, idx) => (
          <motion.div
            key={idx}
            initial={{ opacity: 0, y: 10 }}
            whileInView={{ opacity: 1, y: 0 }}
            whileHover={{ scale: 1.02 }}
            viewport={{ once: true }}
            className="rounded-xl border border-slate-200 bg-white shadow-sm p-4"
          >
            <div className="text-slate-800 font-medium">{String(name)}</div>
          </motion.div>
        ))}
      </div>
    </section>
  );
}
