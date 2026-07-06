import { motion } from 'framer-motion';
import { ChevronRight, Sparkles } from 'lucide-react';
import { useTranslation } from 'react-i18next';

export const AnalysisPanel = ({ active }: { active: boolean }) => {
  const { t } = useTranslation();

  return (
    <aside className="fixed top-[80px] right-0 bottom-0 w-[280px] bg-white border-l border-black/[0.04] hidden xl:flex flex-col z-40 overflow-hidden">
      <div className="flex-1 flex flex-col p-6 overflow-y-auto scrollbar-hide">
        <div className="flex items-center gap-2 mb-6">
          <Sparkles className="w-4 h-4 text-secondary" />
          <span className="font-heading font-semibold text-[15px] text-text-primary">AI Assistant</span>
        </div>

        {!active ? (
          <div className="flex-1 flex flex-col">
            <div className="space-y-3 mb-8">
              <PanelAction label={t('panel.discover')} />
              <PanelAction label={t('panel.compare')} />
              <PanelAction label={t('panel.explain')} />
              <PanelAction label={t('panel.plan')} />
            </div>
            
            <div className="mt-auto border-t border-gray-50 pt-6">
              <p className="text-[12px] font-semibold text-gray-400 uppercase tracking-widest mb-4 text-center">{t('panel.verified_sources')}</p>
              <div className="grid grid-cols-2 gap-2">
                <StatCard value="200+" label={t('panel.countries')} color="text-primary" bg="bg-orange-50" />
                <StatCard value="65+" label={t('panel.programs')} color="text-secondary" bg="bg-blue-50" />
                <StatCard value="12000+" label="Sources" color="text-accent" bg="bg-emerald-50" />
              </div>
            </div>
          </div>
        ) : (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
            className="flex-1 flex flex-col gap-5"
          >
            <div>
              <p className="text-[11px] font-bold text-gray-400 uppercase tracking-widest mb-3">Current Goal</p>
              <div className="space-y-2">
                <SummaryItem label="Funding" value="Master's" />
                <SummaryItem label="Countries" value="Germany" />
              </div>
            </div>

            <div>
              <p className="text-[11px] font-bold text-gray-400 uppercase tracking-widest mb-3">Overall Match</p>
              <div className="bg-gradient-to-br from-emerald-50 to-teal-50 rounded-2xl p-4 border border-emerald-100">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-[13px] font-semibold text-emerald-800">Top Match</span>
                  <span className="text-xl font-bold text-emerald-600">94%</span>
                </div>
              </div>
            </div>

            <div className="mt-auto space-y-2 pt-4 border-t border-gray-50">
              <PanelAction label="Compare" />
              <PanelAction label="Decision Report" />
            </div>
          </motion.div>
        )}
      </div>
    </aside>
  );
};

const StatCard = ({ value, label, color, bg }: any) => (
  <div className={`${bg} rounded-xl p-3 text-center border border-white`}>
    <div className={`text-lg font-bold ${color}`}>{value}</div>
    <div className="text-[10px] text-gray-500 mt-0.5 leading-tight">{label}</div>
  </div>
);

const SummaryItem = ({ label, value }: { label: string; value: string }) => (
  <div className="flex items-center justify-between bg-gray-50 rounded-xl px-3 py-2.5 border border-black/[0.04]">
    <span className="text-[12px] text-text-secondary">{label}</span>
    <span className="text-[13px] font-semibold text-text-primary">{value}</span>
  </div>
);

const PanelAction = ({ label }: { label: string }) => (
  <button className="w-full flex items-center justify-between bg-white border border-gray-100 rounded-xl px-4 py-3 hover:border-primary/30 hover:shadow-sm transition-all group text-[13px] font-medium text-text-primary">
    {label}
    <ChevronRight className="w-4 h-4 text-gray-300 group-hover:text-primary transition-colors" />
  </button>
);
