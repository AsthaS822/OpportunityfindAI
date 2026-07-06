import { useState, useEffect, useImperativeHandle, forwardRef } from 'react';
import { ArrowUp } from 'lucide-react';

const PLACEHOLDERS = [
  'What can I do after MCA?',
  'Find scholarships in Germany',
  'Compare DAAD vs Erasmus',
  'Can I study abroad with 7 CGPA?',
  'Government schemes for women entrepreneurs',
  'Career roadmap after BCA',
  'How to get into AI Research?',
];

export interface ChatInputHandle {
  setValue: (val: string) => void;
}

export const ChatInput = forwardRef<ChatInputHandle, { onSend: (val: string) => void }>(({ onSend }, ref) => {
  const [val, setVal] = useState('');
  const [focused, setFocused] = useState(false);
  const [placeholderIdx, setPlaceholderIdx] = useState(0);

  useImperativeHandle(ref, () => ({ setValue: (v: string) => setVal(v) }));

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
    <div className="border-t border-gray-200 px-4 py-3 bg-white">
      <div className="max-w-[720px] mx-auto">
        <form onSubmit={handleSubmit}>
          <div className={`flex items-center rounded-xl px-3 border transition-all ${
            focused ? 'border-orange-400 shadow-sm' : 'border-gray-300 hover:border-gray-400'
          }`}>
            <input
              type="text"
              value={val}
              onChange={e => setVal(e.target.value)}
              onFocus={() => setFocused(true)}
              onBlur={() => setFocused(false)}
              onKeyDown={handleKey}
              placeholder={PLACEHOLDERS[placeholderIdx]}
              className="flex-1 bg-transparent border-none outline-none text-gray-800 placeholder:text-gray-400 py-3 px-1 text-[14px]"
            />
            <button
              type="submit"
              disabled={!val.trim()}
              className="h-8 w-8 rounded-lg bg-orange-500 text-white flex items-center justify-center disabled:opacity-30 hover:bg-orange-600 transition-all flex-shrink-0"
            >
              <ArrowUp className="w-4 h-4" />
            </button>
          </div>
        </form>
      </div>
    </div>
  );
});

ChatInput.displayName = 'ChatInput';
