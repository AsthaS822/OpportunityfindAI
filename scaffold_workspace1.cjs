const fs = require('fs');
const path = require('path');

const srcDir = path.join(__dirname, 'src');
const workspaceDir = path.join(srcDir, 'components', 'workspace');

if (!fs.existsSync(workspaceDir)) {
  fs.mkdirSync(workspaceDir, { recursive: true });
}

const files = {
  'components/workspace/Sidebar.tsx': `import { motion } from 'framer-motion';
import { Plus, MessageSquare, Pin, Globe, Trash2, HelpCircle } from 'lucide-react';
import { useTranslation } from '../../contexts/LanguageContext';

export const Sidebar = () => {
  const { language, setLanguage } = useTranslation();

  return (
    <div className="w-[300px] h-screen fixed left-0 top-0 bg-white border-r border-gray-100 flex flex-col pt-6 pb-6 px-4 z-40 hidden lg:flex">
      {/* Logo Area */}
      <div className="flex items-center gap-2 px-2 mb-8">
        <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-primary to-orange-400 flex items-center justify-center text-white font-bold text-xl">
          O
        </div>
        <span className="font-heading text-lg font-bold tracking-tight text-text-primary">OpportunityOS</span>
      </div>

      <button className="flex items-center justify-center gap-2 w-full h-[44px] rounded-xl bg-orange-50 text-primary font-medium hover:bg-orange-100 transition-colors mb-6">
        <Plus className="w-4 h-4" /> New Discovery
      </button>

      <div className="flex-1 overflow-y-auto scrollbar-hide space-y-6">
        <div>
          <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-wider px-2 mb-3">Pinned</h3>
          <div className="space-y-1">
            <SidebarItem icon={<Pin className="w-4 h-4 text-secondary" />} text="MBA Scholarships in UK" active />
          </div>
        </div>
        
        <div>
          <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-wider px-2 mb-3">Recent</h3>
          <div className="space-y-1">
            <SidebarItem icon={<MessageSquare className="w-4 h-4" />} text="Govt schemes for tech startups" />
            <SidebarItem icon={<MessageSquare className="w-4 h-4" />} text="Education loans SBI vs HDFC" />
            <SidebarItem icon={<MessageSquare className="w-4 h-4" />} text="DAAD Scholarship requirements" />
          </div>
        </div>
      </div>

      <div className="pt-4 border-t border-gray-50 space-y-1">
        <button 
          onClick={() => setLanguage(language === 'en' ? 'hi' : 'en')}
          className="flex items-center gap-3 w-full px-2 py-2.5 rounded-xl text-text-secondary hover:bg-gray-50 hover:text-text-primary transition-colors text-sm"
        >
          <Globe className="w-4 h-4" /> {language === 'en' ? 'Switch to Hindi' : 'Switch to English'}
        </button>
        <button className="flex items-center gap-3 w-full px-2 py-2.5 rounded-xl text-text-secondary hover:bg-gray-50 hover:text-text-primary transition-colors text-sm">
          <Trash2 className="w-4 h-4" /> Clear Session
        </button>
        <button className="flex items-center gap-3 w-full px-2 py-2.5 rounded-xl text-text-secondary hover:bg-gray-50 hover:text-text-primary transition-colors text-sm">
          <HelpCircle className="w-4 h-4" /> Help & Support
        </button>
      </div>
    </div>
  );
};

const SidebarItem = ({ icon, text, active }: { icon: React.ReactNode, text: string, active?: boolean }) => {
  return (
    <motion.button 
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      className={\`flex items-center gap-3 w-full px-2 py-2.5 rounded-xl transition-all duration-300 text-sm truncate \${active ? 'bg-orange-50/50 text-primary border border-orange-100 shadow-sm' : 'text-text-secondary hover:bg-gray-50 hover:text-text-primary border border-transparent'}\`}
    >
      <span className="flex-shrink-0">{icon}</span>
      <span className="truncate">{text}</span>
    </motion.button>
  );
};
`,
  'components/workspace/AnalysisPanel.tsx': `import { motion } from 'framer-motion';
import { Target, CheckCircle2, ChevronRight, BarChart3, Download } from 'lucide-react';
import { Button } from '../ui/Button';

export const AnalysisPanel = ({ active }: { active: boolean }) => {
  return (
    <div className="w-[24%] max-w-[360px] h-screen fixed right-0 top-0 bg-white border-l border-gray-100 pt-6 pb-6 px-6 z-40 hidden xl:flex flex-col">
      <div className="flex items-center gap-2 mb-8">
        <BarChart3 className="w-5 h-5 text-secondary" />
        <span className="font-heading font-semibold text-text-primary">Live Analysis</span>
      </div>

      {!active ? (
        <div className="flex-1 flex flex-col items-center justify-center text-center opacity-60">
          <div className="w-24 h-24 mb-4 rounded-full bg-gradient-to-tr from-blue-50 to-orange-50 flex items-center justify-center">
             <Target className="w-10 h-10 text-gray-300" />
          </div>
          <p className="text-text-secondary text-sm max-w-[200px]">Analysis will appear here once you start exploring.</p>
        </div>
      ) : (
        <motion.div 
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="flex-1 flex flex-col"
        >
          {/* Profile Summary */}
          <div className="mb-6">
            <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">Profile Summary</h3>
            <div className="space-y-2">
              <SummaryItem label="Goal" value="Master's Scholarship" />
              <SummaryItem label="Country" value="Germany" />
              <SummaryItem label="Education" value="B.Tech (8.6 CGPA)" />
              <SummaryItem label="Budget" value="Fully Funded Required" />
            </div>
          </div>

          {/* Current Match */}
          <div className="mb-8">
            <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">Current Matches</h3>
            <div className="bg-emerald-50 rounded-2xl p-4 border border-emerald-100">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium text-emerald-800">Top Match Rate</span>
                <span className="text-lg font-bold text-emerald-600">94%</span>
              </div>
              <div className="text-xs text-emerald-600/80">3 highly relevant opportunities found across 4 verified sources.</div>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="mt-auto space-y-3">
            <button className="w-full flex items-center justify-between bg-white border border-gray-200 rounded-xl p-3 hover:border-primary/40 hover:shadow-sm transition-all group">
              <span className="text-sm font-medium text-text-primary">Compare Matches</span>
              <ChevronRight className="w-4 h-4 text-gray-400 group-hover:text-primary transition-colors" />
            </button>
            <button className="w-full flex items-center justify-between bg-white border border-gray-200 rounded-xl p-3 hover:border-primary/40 hover:shadow-sm transition-all group">
              <span className="text-sm font-medium text-text-primary">Decision Report</span>
              <ChevronRight className="w-4 h-4 text-gray-400 group-hover:text-primary transition-colors" />
            </button>
            <Button variant="secondary" className="w-full h-[44px] gap-2">
              <Download className="w-4 h-4" /> Export Plan
            </Button>
          </div>
        </motion.div>
      )}
    </div>
  );
};

const SummaryItem = ({ label, value }: { label: string, value: string }) => (
  <div className="flex items-center justify-between bg-gray-50 rounded-xl p-3 border border-gray-100">
    <span className="text-xs text-text-secondary">{label}</span>
    <span className="text-sm font-medium text-text-primary">{value}</span>
  </div>
);
`,
  'components/workspace/ChatInput.tsx': `import { useState } from 'react';
import { motion } from 'framer-motion';
import { ArrowUp, Paperclip, Mic } from 'lucide-react';
import { GlassPanel } from '../ui/GlassPanel';

export const ChatInput = ({ onSend }: { onSend: (val: string) => void }) => {
  const [val, setVal] = useState('');
  const [focused, setFocused] = useState(false);

  const handleSubmit = (e?: React.FormEvent) => {
    e?.preventDefault();
    if (val.trim()) {
      onSend(val);
      setVal('');
    }
  };

  return (
    <div className="fixed bottom-0 left-0 lg:left-[300px] right-0 xl:right-[24%] p-6 bg-gradient-to-t from-white via-white to-transparent z-30 flex justify-center">
      <motion.div 
        className="w-full max-w-[800px] relative"
        animate={{ scale: focused ? 1.01 : 1 }}
        transition={{ duration: 0.2 }}
      >
        <div className={\`absolute inset-0 bg-primary/20 rounded-[28px] blur-xl transition-opacity duration-500 pointer-events-none \${focused ? 'opacity-100' : 'opacity-0'}\`} />
        
        <form onSubmit={handleSubmit} className="relative">
          <GlassPanel className={\`h-[70px] rounded-[28px] p-2 flex items-center shadow-[0_8px_30px_rgb(0,0,0,0.06)] border transition-colors \${focused ? 'border-primary/40 bg-white/90' : 'border-gray-200 bg-white/70'}\`}>
            
            <button type="button" className="p-3 text-gray-400 hover:text-text-primary transition-colors rounded-full hover:bg-gray-100">
              <Paperclip className="w-5 h-5" />
            </button>

            <input 
              type="text"
              value={val}
              onChange={e => setVal(e.target.value)}
              onFocus={() => setFocused(true)}
              onBlur={() => setFocused(false)}
              placeholder="Describe your goals... (e.g. Master's in Germany)"
              className="flex-1 bg-transparent border-none outline-none text-text-primary placeholder:text-gray-400 py-3 px-2 text-[15px]"
            />
            
            <button type="button" className="p-3 text-gray-400 hover:text-text-primary transition-colors rounded-full hover:bg-gray-100 mr-1">
              <Mic className="w-5 h-5" />
            </button>

            <button 
              type="submit"
              disabled={!val.trim()}
              className="w-12 h-12 rounded-2xl bg-gradient-to-br from-primary to-orange-500 text-white flex items-center justify-center shadow-md disabled:opacity-50 disabled:grayscale transition-all hover:scale-105 active:scale-95"
            >
              <ArrowUp className="w-5 h-5" />
            </button>
          </GlassPanel>
        </form>
      </motion.div>
    </div>
  );
};
`
};

for (const [relPath, content] of Object.entries(files)) {
  const fullPath = path.join(srcDir, relPath);
  const dir = path.dirname(fullPath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  fs.writeFileSync(fullPath, content);
}
console.log("Scaffolded Workspace Sidebars and Input");
