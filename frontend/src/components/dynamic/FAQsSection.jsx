import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

export default function FAQsSection({ faqs = [] }) {
  if (!faqs || faqs.length === 0) return null;
  return (
    <section id="faqs" className="max-w-3xl mx-auto px-6 py-12">
      <motion.h2 initial={{ opacity: 0, y: 10 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} className="text-2xl font-semibold text-slate-900">FAQs</motion.h2>
      <div className="mt-6 space-y-3">
        {faqs.map((f, idx) => (
          <FAQItem key={idx} q={f.question} a={f.answer} />
        ))}
      </div>
    </section>
  );
}

function FAQItem({ q = '', a = '' }) {
  const [open, setOpen] = useState(false);
  return (
    <div className="border border-slate-200 rounded-xl bg-white overflow-hidden">
      <button onClick={() => setOpen((v) => !v)} className="w-full text-left px-4 py-3 font-medium text-slate-800 hover:bg-slate-50">
        {q}
      </button>
      <AnimatePresence initial={false}>
        {open && (
          <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} exit={{ height: 0, opacity: 0 }} transition={{ duration: 0.2 }} className="px-4 pb-4 text-slate-700">
            {a}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
