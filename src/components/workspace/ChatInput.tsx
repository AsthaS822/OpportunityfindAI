import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { ArrowUp, Mic, Paperclip } from 'lucide-react';

const PLACEHOLDERS = [
  'What can I do after MCA?',
  'Find scholarships in Germany',
  'Compare DAAD vs Erasmus',
  'Can I study abroad with 7 CGPA?',
  'Government schemes for women entrepreneurs',
  'Career roadmap after BCA',
  'How to get into AI Research?',
];

export const ChatInput = ({ onSend }: { onSend: (val: string) => void }) => {
  const [val, setVal] = useState('');
  const [focused, setFocused] = useState(false);
  const [placeholderIdx, setPlaceholderIdx] = useState(0);

  useEffect(() => {
    if (focused) return;
    const interval = setInterval(() => setPlaceholderIdx(i => (i + 1) % PLACEHOLDERS.length), 3500);
    return () => clearInterval(interval);
  }, [focused]);

  const handleSubmit = (e?: React.FormEvent) => {
    e?.preventDefault();
    if (val.trim()) { onSend(val); setVal(''); }
  };

  const handleKey = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSubmit(); }
  };

  return (
    <div className="sticky bottom-0 left-0 right-0 pb-6 pt-4 bg-gradient-to-t from-white via-white/90 to-transparent flex justify-center px-4">
      <motion.div
        className="w-full max-w-[720px] relative"
        animate={{ scale: focused ? 1.01 : 1, y: focused ? -2 : 0 }}
        transition={{ duration: 0.2, ease: 'easeOut' }}
      >
        <div className={`absolute inset-0 bg-primary/10 rounded-[20px] blur-3xl transition-opacity duration-500 pointer-events-none ${focused ? 'opacity-100' : 'opacity-0'}`} />

        <form onSubmit={handleSubmit} className="relative">
          <div className={`flex items-center h-[56px] rounded-[16px] px-3 border transition-all duration-300 shadow-[0_4px_20px_rgba(0,0,0,0.06)] ${
            focused
              ? 'bg-white border-primary/40 shadow-[0_0_20px_rgba(255,122,0,0.12)]'
              : 'bg-white/90 backdrop-blur-xl border-gray-200 hover:border-gray-300'
          }`}>
            <button type="button" className="w-8 h-8 rounded-lg flex items-center justify-center text-gray-400 hover:text-text-primary hover:bg-gray-100 transition-all flex-shrink-0">
              <Paperclip className="w-4 h-4" />
            </button>

            <input
              type="text"
              value={val}
              onChange={e => setVal(e.target.value)}
              onFocus={() => setFocused(true)}
              onBlur={() => setFocused(false)}
              onKeyDown={handleKey}
              placeholder={PLACEHOLDERS[placeholderIdx]}
              className="flex-1 bg-transparent border-none outline-none text-text-primary placeholder:text-gray-400 py-3 px-2 text-[14px]"
            />

            <button type="button" className="w-8 h-8 rounded-lg flex items-center justify-center text-gray-400 hover:text-text-primary hover:bg-gray-100 transition-all flex-shrink-0">
              <Mic className="w-4 h-4" />
            </button>

            <div className="w-px h-6 bg-gray-200 mx-1" />

            <button
              type="submit"
              disabled={!val.trim()}
              className="h-[38px] w-[38px] rounded-xl bg-gradient-to-br from-primary to-orange-500 text-white flex items-center justify-center shadow-sm disabled:opacity-30 disabled:grayscale hover:scale-105 active:scale-95 transition-all"
            >
              <ArrowUp className="w-4 h-4" />
            </button>
          </div>
        </form>
      </motion.div>
    </div>
  );
};
