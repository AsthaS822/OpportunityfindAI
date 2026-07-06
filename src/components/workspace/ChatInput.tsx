import { useState } from 'react';
import { motion } from 'framer-motion';
import { ArrowUp, Paperclip, Mic } from 'lucide-react';
import { useTranslation } from 'react-i18next';

export const ChatInput = ({ onSend }: { onSend: (val: string) => void }) => {
  const [val, setVal] = useState('');
  const [focused, setFocused] = useState(false);
  const { t } = useTranslation();

  const handleSubmit = (e?: React.FormEvent) => {
    e?.preventDefault();
    if (val.trim()) { onSend(val); setVal(''); }
  };

  const handleKey = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSubmit(); }
  };

  return (
    <div className="sticky bottom-0 left-0 right-0 pb-8 pt-4 bg-transparent flex justify-center px-4">
      <motion.div
        className="w-full max-w-[720px] relative"
        animate={{ scale: focused ? 1.01 : 1, y: focused ? -2 : 0 }}
        transition={{ duration: 0.2, ease: 'easeOut' }}
      >
        {/* Glow halo */}
        <div className={`absolute inset-0 bg-primary/20 rounded-[28px] blur-3xl transition-opacity duration-500 pointer-events-none ${focused ? 'opacity-100' : 'opacity-0'}`} />

        <form onSubmit={handleSubmit} className="relative">
          <div className={`flex items-center h-[70px] rounded-[28px] px-2 border transition-all duration-300 shadow-[0_8px_30px_rgba(0,0,0,0.06)] ${
            focused
              ? 'bg-white/80 backdrop-blur-xl border-orange-500/50 shadow-[0_0_15px_rgba(249,115,22,0.3)]'
              : 'bg-white/50 backdrop-blur-md border-gray-200/50 hover:bg-white/70'
          }`}>
            <button type="button" className="p-3 text-gray-400 hover:text-gray-600 transition-colors rounded-full">
              <Paperclip className="w-5 h-5" />
            </button>

            <input
              type="text"
              value={val}
              onChange={e => setVal(e.target.value)}
              onFocus={() => setFocused(true)}
              onBlur={() => setFocused(false)}
              onKeyDown={handleKey}
              placeholder={t('workspace.input_placeholder')}
              className="flex-1 bg-transparent border-none outline-none text-text-primary placeholder:text-gray-500 py-3 px-2 text-[15px]"
            />

            <button type="button" className="p-3 text-gray-400 hover:text-gray-600 transition-colors rounded-full mr-1">
              <Mic className="w-5 h-5" />
            </button>

            <button
              type="submit"
              disabled={!val.trim()}
              className="w-[100px] h-12 rounded-2xl bg-gradient-to-br from-primary to-orange-500 text-white flex items-center justify-center gap-1 shadow-md disabled:opacity-30 disabled:grayscale hover:scale-105 active:scale-95 transition-all font-medium text-sm"
            >
              {t('workspace.analyze_btn').replace(' →', '')} <ArrowUp className="w-4 h-4 ml-1" />
            </button>
          </div>
        </form>
      </motion.div>
    </div>
  );
};
