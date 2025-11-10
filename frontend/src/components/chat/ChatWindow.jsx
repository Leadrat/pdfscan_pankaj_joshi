import { motion } from 'framer-motion';
import ChatMessage from './ChatMessage';
import { useEffect, useRef, useState } from 'react';

export default function ChatWindow({ bot, context }) {
  const [input, setInput] = useState('');
  const listRef = useRef(null);

  useEffect(() => {
    if (listRef.current) {
      listRef.current.scrollTop = listRef.current.scrollHeight;
    }
  }, [bot.messages, bot.typing]);

  const onSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || bot.typing) return;
    const q = input.trim();
    setInput('');
    await bot.ask(q, context);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 20 }}
      className="w-80 sm:w-96 bg-white rounded-xl shadow-2xl overflow-hidden border border-slate-200"
    >
      <div className="bg-gradient-to-r from-indigo-500 to-purple-600 text-white px-4 py-3">
        <div className="font-semibold">Project Chatbot</div>
        <div className="text-xs opacity-80">Answers based on brochure only</div>
      </div>
      <div ref={listRef} className="h-80 overflow-y-auto p-3 space-y-2 bg-slate-50">
        {bot.messages.map((m, idx) => (
          <ChatMessage key={idx} role={m.role} content={m.content} />
        ))}
        {bot.typing && (
          <div className="text-slate-500 text-sm">Typing…</div>
        )}
        {bot.error && (
          <div className="text-amber-600 text-xs">{bot.error}</div>
        )}
      </div>
      <form onSubmit={onSend} className="p-3 bg-white border-t border-slate-200 flex gap-2">
        <input
          ref={bot.inputRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about the project…"
          className="flex-1 px-3 py-2 rounded-md border border-slate-300 focus:outline-none focus:ring-2 focus:ring-indigo-400"
        />
        <button
          type="submit"
          disabled={bot.typing}
          className="px-3 py-2 rounded-md bg-indigo-600 text-white disabled:opacity-50"
        >
          Send
        </button>
      </form>
    </motion.div>
  );
}
