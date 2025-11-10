import { useCallback, useMemo, useRef, useState } from 'react';
import axios from 'axios';

const MAX_QUESTION = 500;
const FALLBACK = 'No idea based on brochure.';

export function useChatbot() {
  const [isReady, setReady] = useState(false); // set to true after extraction complete
  const [open, setOpen] = useState(false);
  const [typing, setTyping] = useState(false);
  const [error, setError] = useState('');
  const [messages, setMessages] = useState([]); // {role:'user'|'assistant',content}
  const inputRef = useRef(null);

  const truncate = (q) => (q?.length > MAX_QUESTION ? q.slice(0, MAX_QUESTION) : q || '');

  const toggle = useCallback(() => {
    if (!isReady) return;
    setOpen((v) => !v);
  }, [isReady]);

  const greetIfFirstOpen = useCallback(() => {
    if (!messages.length) {
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: 'Hi 👋 I can help you with details from the brochure!' },
      ]);
    }
  }, [messages.length]);

  const ask = useCallback(async (question, context) => {
    if (!question) return;
    setError('');
    const q = truncate(question);
    if (q.length !== question.length) {
      setError('Your message was truncated to 500 characters.');
    }
    setMessages((prev) => [...prev, { role: 'user', content: q }]);
    setTyping(true);
    try {
      const res = await axios.post('/chatbot/query', { question: q, context: context || {} });
      const answer = res?.data?.answer ?? FALLBACK;
      setMessages((prev) => [...prev, { role: 'assistant', content: answer }]);
    } catch (e) {
      setMessages((prev) => [...prev, { role: 'assistant', content: FALLBACK }]);
    } finally {
      setTyping(false);
    }
  }, []);

  return useMemo(
    () => ({
      // state
      isReady,
      open,
      typing,
      error,
      messages,
      // actions
      setReady,
      toggle,
      greetIfFirstOpen,
      ask,
      inputRef,
    }),
    [isReady, open, typing, error, messages, toggle, greetIfFirstOpen, ask]
  );
}
