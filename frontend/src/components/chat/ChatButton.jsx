import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';
import { useChatbot } from '../../hooks/useChatbot';
import { FiMessageSquare } from 'react-icons/fi';
import ErrorBoundary from '../ui/ErrorBoundary';

export default function ChatButton({ extractionReady, context }) {
  const bot = useChatbot();
  const [hover, setHover] = useState(false);

  useEffect(() => {
    bot.setReady(!!extractionReady);
  }, [extractionReady]);

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {bot.isReady && (
        <div className="relative">
          {hover && (
            <div className="absolute -top-10 right-0 bg-slate-800 text-white text-sm px-3 py-1 rounded shadow">
              Ask about project details
            </div>
          )}
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.98 }}
            onMouseEnter={() => setHover(true)}
            onMouseLeave={() => setHover(false)}
            onClick={() => {
              bot.toggle();
              bot.greetIfFirstOpen();
            }}
            className="rounded-full p-4 bg-gradient-to-r from-indigo-500 to-purple-600 text-white shadow-lg"
          >
            <FiMessageSquare size={22} />
          </motion.button>
          {bot.open && (
            <div className="absolute bottom-16 right-0">
              <ErrorBoundary>
                <ChatWindow bot={bot} context={context} />
              </ErrorBoundary>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function ChatWindow({ bot, context }) {
  // lightweight wrapper to lazy import window
  const [Comp, setComp] = useState(null);
  useEffect(() => {
    import('./ChatWindow').then((m) => setComp(() => m.default));
  }, []);
  if (!Comp) return null;
  return <Comp bot={bot} context={context} />;
}
