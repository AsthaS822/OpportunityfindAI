import { motion } from 'framer-motion';
import { Plus, HelpCircle, Info } from 'lucide-react';
import { useTranslation } from 'react-i18next';

export const Sidebar = () => {
  const { t } = useTranslation();

  return (
    <aside className="fixed top-[80px] left-0 bottom-0 w-[280px] bg-white border-r border-black/[0.04] flex flex-col z-40 hidden lg:flex overflow-hidden">
      <div className="flex-1 flex flex-col p-8 gap-6 overflow-y-auto scrollbar-hide">
        <button className="flex items-center justify-center gap-2 w-full h-[44px] rounded-2xl bg-gradient-to-r from-primary to-orange-400 text-white font-semibold text-[14px] shadow-sm hover:shadow-md hover:scale-[1.02] transition-all">
          <Plus className="w-4 h-4" /> {t('workspace.newDiscovery')}
        </button>

        <div className="space-y-2">
          <p className="text-[11px] font-bold text-gray-400 uppercase tracking-widest mb-4 px-2">{t('workspace.quickPrompts')}</p>
          <PromptItem label={t('workspace.prompt_scholarships')} />
          <PromptItem label={t('workspace.prompt_schemes')} />
          <PromptItem label={t('workspace.prompt_abroad')} />
          <PromptItem label={t('workspace.prompt_loans')} />
          <PromptItem label={t('workspace.prompt_startup')} />
        </div>
      </div>

      <div className="px-6 pb-8 pt-4 space-y-1">
        <SidebarAction icon={<HelpCircle className="w-4 h-4" />} label={t('workspace.help')} />
        <SidebarAction icon={<Info className="w-4 h-4" />} label={t('workspace.about')} />
      </div>
    </aside>
  );
};

const PromptItem = ({ label }: { label: string }) => (
  <motion.button
    whileHover={{ x: 3 }}
    className="flex items-center gap-3 w-full px-3 py-2.5 rounded-xl text-[14px] text-text-secondary hover:text-text-primary hover:bg-gray-50 transition-all truncate text-left"
  >
    <span className="truncate">{label}</span>
  </motion.button>
);

const SidebarAction = ({ icon, label, onClick }: { icon: React.ReactNode; label: string; onClick?: () => void }) => (
  <button
    onClick={onClick}
    className="flex items-center gap-3 w-full px-3 py-2.5 rounded-xl text-[14px] text-text-secondary hover:bg-gray-50 hover:text-text-primary transition-all"
  >
    {icon} {label}
  </button>
);
