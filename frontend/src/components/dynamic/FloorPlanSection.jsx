import { motion } from 'framer-motion';
import { useCallback, useState } from 'react';

const PLACEHOLDER = '/src/assets/placeholder-floorplan.svg';

export default function FloorPlanSection({ floor_plans = [] }) {
  const [open, setOpen] = useState(false);
  const [img, setImg] = useState('');
  if (!Array.isArray(floor_plans) || floor_plans.length === 0) return null;

  const openLightbox = useCallback((src) => {
    setImg(src || PLACEHOLDER);
    setOpen(true);
  }, []);

  return (
    <section id="floor-plans" className="max-w-6xl mx-auto px-6 py-12">
      <motion.h2 initial={{ opacity: 0, y: 10 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} className="text-2xl font-semibold text-slate-900">Floor Plans</motion.h2>
      <div className="mt-6 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        {floor_plans.map((fp, idx) => (
          <motion.div key={idx} initial={{ opacity: 0, y: 10 }} whileInView={{ opacity: 1, y: 0 }} whileHover={{ scale: 1.01 }} viewport={{ once: true }} className="rounded-xl border border-slate-200 bg-white shadow-sm overflow-hidden">
            <div className="h-40 bg-slate-100 overflow-hidden">
              {/* eslint-disable-next-line jsx-a11y/img-redundant-alt */}
              <img
                src={fp.image || PLACEHOLDER}
                alt={`Floor plan image`}
                onError={(e) => {
                  e.currentTarget.src = PLACEHOLDER;
                }}
                className="w-full h-full object-cover"
              />
            </div>
            <div className="p-4">
              <div className="font-medium text-slate-900">{fp.tower_name || 'Tower'}</div>
              <div className="text-slate-700 text-sm mt-1">{fp.bhk_type || ''}{fp.area ? ` · ${fp.area}` : ''}</div>
              <button onClick={() => openLightbox(fp.image)} className="mt-3 inline-flex items-center px-3 py-1.5 rounded-md text-white bg-indigo-600 hover:bg-indigo-700">
                View
              </button>
            </div>
          </motion.div>
        ))}
      </div>

      {open && (
        <div className="fixed inset-0 z-50 bg-black/70 flex items-center justify-center" onClick={() => setOpen(false)}>
          <div className="max-w-4xl max-h-[85vh] p-2 bg-white rounded-lg" onClick={(e) => e.stopPropagation()}>
            {/* eslint-disable-next-line jsx-a11y/img-redundant-alt */}
            <img src={img || PLACEHOLDER} alt="Floor plan zoom" className="w-full h-full object-contain" onError={(e) => { e.currentTarget.src = PLACEHOLDER; }} />
            <div className="text-right mt-2">
              <button onClick={() => setOpen(false)} className="px-3 py-1.5 rounded-md bg-slate-800 text-white">Close</button>
            </div>
          </div>
        </div>
      )}
    </section>
  );
}
