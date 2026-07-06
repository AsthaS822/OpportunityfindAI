import { motion } from 'framer-motion';
import { useTranslation } from 'react-i18next';

export const MessageEmptyState = ({ onSelect }: { onSelect: (text: string) => void }) => {
  const { t } = useTranslation();

  const chips = [
    { key: 'workspace.prompt_germany', raw: 'Study in Germany' },
    { key: 'workspace.prompt_mba', raw: 'MBA Scholarships' },
    { key: 'workspace.prompt_loans', raw: 'Education Loan' },
    { key: 'workspace.prompt_abroad', raw: 'Study Abroad' },
    { key: 'workspace.prompt_schemes', raw: 'Government Schemes' },
    { key: 'workspace.prompt_startup', raw: 'Startup Grants' },
  ];

  return (
    <div className="flex-1 flex flex-col items-center justify-center text-center px-6 min-h-[60vh]">
      <motion.div
        initial={{ opacity: 0, y: 24 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, ease: 'easeOut' }}
        className="max-w-[540px] w-full"
      >
        <h2 className="text-[42px] font-heading font-bold text-text-primary mb-3 leading-tight">{t('workspace.empty_greeting')}</h2>
        <p className="text-[18px] text-text-secondary mb-12 max-w-[400px] mx-auto">{t('workspace.empty_desc')}</p>

        <div className="flex flex-wrap justify-center gap-3">
          {chips.map(({ key }, i) => (
            <motion.button
              key={i}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 + i * 0.06, duration: 0.35 }}
              whileHover={{ scale: 1.04, y: -3 }}
              whileTap={{ scale: 0.97 }}
              onClick={() => onSelect(t(key))}
              className="px-5 py-3 bg-white/70 backdrop-blur-sm border border-gray-200 rounded-2xl text-[14px] font-medium text-text-secondary hover:text-primary hover:border-primary/40 hover:shadow-[0_8px_24px_rgba(249,115,22,0.15)] transition-all shadow-sm cursor-pointer"
            >
              {t(key)}
            </motion.button>
          ))}
        </div>
      </motion.div>
    </div>
  );
};
