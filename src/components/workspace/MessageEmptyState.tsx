import { motion } from 'framer-motion';

const chips = [
  '🎓 Scholarships',
  '🌍 Study Abroad',
  '💼 Career Advice',
  '🏛 Government Schemes',
  '💰 Loans',
  '🚀 Startup Grants',
  '📖 Research',
  '🎯 Internships',
];

export const MessageEmptyState = ({ onSelect }: { onSelect: (text: string) => void }) => {
  return (
    <div className="flex-1 flex flex-col items-center justify-center text-center px-6 min-h-[60vh]">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, ease: 'easeOut' }}
        className="max-w-[520px] w-full"
      >
        <motion.div
          animate={{ y: [0, -6, 0] }}
          transition={{ duration: 3, repeat: Infinity, ease: 'easeInOut' }}
          className="text-4xl mb-5"
        >
          🌍
        </motion.div>

        <h2 className="text-[28px] font-heading font-bold text-text-primary mb-1">Hello 👋</h2>
        <p className="text-[16px] text-text-secondary mb-8">What would you like to explore today?</p>

        <div className="flex flex-wrap justify-center gap-2 max-w-[400px] mx-auto">
          {chips.map((chip, i) => (
            <motion.button
              key={i}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.1 + i * 0.04, duration: 0.3 }}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => onSelect(chip.replace(/^[^\s]+\s/, ''))}
              className="px-4 py-2.5 bg-white border border-gray-200 rounded-xl text-[13px] text-text-primary font-medium hover:border-primary/40 hover:bg-orange-50 hover:text-primary transition-all shadow-sm"
            >
              {chip}
            </motion.button>
          ))}
        </div>

        <p className="text-[12px] text-text-secondary mt-10 opacity-60">Every opportunity starts with one question.</p>
      </motion.div>
    </div>
  );
};
