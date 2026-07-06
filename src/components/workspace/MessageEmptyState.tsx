import { motion } from 'framer-motion';

const examples = [
  { label: 'Scholarships after MCA', query: 'Scholarships after MCA' },
  { label: 'Study in Germany', query: 'I want to study in Germany' },
  { label: 'Career roadmap after BCA', query: 'Career options after BCA' },
  { label: 'Government schemes for startups', query: 'Government schemes for startups' },
  { label: 'PhD opportunities in Europe', query: 'PhD opportunities in Europe' },
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
        <div className="text-4xl mb-5">🌍</div>

        <h2 className="text-2xl font-bold text-gray-900 mb-2">Hello!</h2>
        <p className="text-sm text-gray-500 leading-relaxed mb-8">
          I'm FutureOS. Ask me about scholarships, careers, universities, government schemes, fellowships, internships, research, education loans, or studying abroad.
        </p>

        <div className="border-t border-gray-200 pt-6 w-full max-w-[400px] mx-auto">
          <p className="text-[11px] font-bold text-gray-400 uppercase tracking-widest mb-3">Examples</p>
          <div className="flex flex-col gap-1.5">
            {examples.map((ex, i) => (
              <motion.button
                key={i}
                initial={{ opacity: 0, x: -8 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.1 + i * 0.05, duration: 0.3 }}
                whileHover={{ x: 4 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => onSelect(ex.query)}
                className="flex items-center gap-2.5 px-4 py-2.5 bg-white border border-gray-200 rounded-xl text-sm text-gray-700 font-medium hover:border-orange-300 hover:text-orange-600 transition-all text-left shadow-sm"
              >
                <span>{ex.label}</span>
              </motion.button>
            ))}
          </div>
        </div>
      </motion.div>
    </div>
  );
};
