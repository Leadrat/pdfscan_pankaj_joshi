import { motion } from 'framer-motion';
import { normalizeConnectivity } from './utils/normalizeConnectivity';

export default function ConnectivitySection({ connectivity }) {
  const items = normalizeConnectivity(connectivity);
  if (!items || items.length === 0) return null;
  return (
    <section id="connectivity" className="max-w-6xl mx-auto px-6 py-12">
      <motion.h2 initial={{ opacity: 0, y: 10 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} className="text-2xl font-semibold text-slate-900">Connectivity</motion.h2>
      <div className="mt-6 overflow-x-auto">
        <table className="min-w-full text-left bg-white border border-slate-200 rounded-xl overflow-hidden">
          <thead className="bg-slate-50 text-slate-700">
            <tr>
              <th className="px-4 py-3">Type</th>
              <th className="px-4 py-3">Name</th>
              <th className="px-4 py-3">Distance</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200">
            {items.map((it, idx) => (
              <tr key={idx} className="hover:bg-slate-50">
                <td className="px-4 py-3 text-slate-800">{it.type || ''}</td>
                <td className="px-4 py-3 text-slate-800">{it.label || ''}</td>
                <td className="px-4 py-3 text-slate-600">{it.distance || ''}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
