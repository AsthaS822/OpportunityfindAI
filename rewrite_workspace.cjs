const fs = require('fs');
const path = require('path');
const srcDir = path.join(__dirname, 'src');

const files = {

// ─────────────────────────────────────────────────────────────────────────────
// NAVBAR — fixed 80px, proper z-index, no overlap
// ─────────────────────────────────────────────────────────────────────────────
'components/layout/Navbar.tsx': `import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Container } from './Container';
import { Button } from '../ui/Button';
import { GlassPanel } from '../ui/GlassPanel';
import { useTranslation } from '../../contexts/LanguageContext';

export const Navbar = () => {
  const [scrolled, setScrolled] = useState(false);
  const { language, setLanguage, t } = useTranslation();

  useEffect(() => {
    const fn = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', fn);
    return () => window.removeEventListener('scroll', fn);
  }, []);

  return (
    <header className="fixed top-0 left-0 right-0 z-[100] h-[80px] flex items-center">
      <Container>
        <GlassPanel
          className={\`flex items-center justify-between px-6 h-[64px] transition-all duration-300 \${
            scrolled ? 'bg-white/90 backdrop-blur-2xl shadow-sm' : 'bg-white/50 backdrop-blur-md'
          }\`}
        >
          <Link to="/" className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-primary to-orange-400 flex items-center justify-center text-white font-bold text-sm">O</div>
            <span className="font-heading text-lg font-bold tracking-tight text-text-primary">OpportunityOS</span>
          </Link>

          <nav className="hidden md:flex items-center gap-8 text-[15px] font-medium text-text-secondary">
            <a href="#how-it-works" className="hover:text-primary transition-colors">{t('nav.howItWorks')}</a>
            <a href="#features" className="hover:text-primary transition-colors">{t('nav.features')}</a>
            <a href="#opportunities" className="hover:text-primary transition-colors">{t('nav.opportunities')}</a>
            <a href="#about" className="hover:text-primary transition-colors">{t('nav.about')}</a>
          </nav>

          <div className="flex items-center gap-3">
            <button
              onClick={() => setLanguage(language === 'en' ? 'hi' : 'en')}
              className="text-[13px] font-medium px-3 py-1.5 rounded-full border border-gray-200 hover:border-primary/40 hover:bg-orange-50 transition-all text-text-secondary"
            >
              {t('nav.switchLang')}
            </button>
            <Link to="/discover">
              <Button className="h-[42px] px-5 text-[14px]">{t('nav.start')}</Button>
            </Link>
          </div>
        </GlassPanel>
      </Container>
    </header>
  );
};
`,

// ─────────────────────────────────────────────────────────────────────────────
// SIDEBAR — proper width, breathing room, realistic history
// ─────────────────────────────────────────────────────────────────────────────
'components/workspace/Sidebar.tsx': `import { motion } from 'framer-motion';
import { Plus, MessageSquare, Globe, Trash2, HelpCircle } from 'lucide-react';
import { useTranslation } from '../../contexts/LanguageContext';

export const Sidebar = () => {
  const { language, setLanguage, t } = useTranslation();

  const history = {
    today: ['MS Germany', 'Fulbright AI'],
    yesterday: ['Education Loan', 'Japan MEXT'],
    lastWeek: ['Research Funding', 'DAAD Scholarship'],
  };

  return (
    <aside className="fixed top-[80px] left-0 bottom-0 w-[280px] bg-white border-r border-black/[0.04] flex flex-col z-40 hidden lg:flex overflow-hidden">
      <div className="flex-1 flex flex-col p-8 gap-6 overflow-y-auto scrollbar-hide">
        <button className="flex items-center justify-center gap-2 w-full h-[44px] rounded-2xl bg-gradient-to-r from-primary to-orange-400 text-white font-semibold text-[14px] shadow-sm hover:shadow-md hover:scale-[1.02] transition-all">
          <Plus className="w-4 h-4" /> {t('workspace.newDiscovery')}
        </button>

        <div className="space-y-6">
          <HistoryGroup label={t('workspace.today')} items={history.today} />
          <HistoryGroup label={t('workspace.yesterday')} items={history.yesterday} />
          <HistoryGroup label={t('workspace.lastWeek')} items={history.lastWeek} />
        </div>
      </div>

      <div className="px-6 pb-8 pt-4 border-t border-black/[0.04] space-y-1">
        <SidebarAction
          icon={<Globe className="w-4 h-4" />}
          label={language === 'en' ? t('workspace.switchLang') : 'Switch to English'}
          onClick={() => setLanguage(language === 'en' ? 'hi' : 'en')}
        />
        <SidebarAction icon={<Trash2 className="w-4 h-4" />} label={t('workspace.clearSession')} />
        <SidebarAction icon={<HelpCircle className="w-4 h-4" />} label={t('workspace.help')} />
      </div>
    </aside>
  );
};

const HistoryGroup = ({ label, items }: { label: string; items: string[] }) => (
  <div>
    <p className="text-[11px] font-bold text-gray-400 uppercase tracking-widest mb-2 px-2">{label}</p>
    <div className="space-y-0.5">
      {items.map((item, i) => (
        <motion.button
          key={i}
          whileHover={{ x: 3 }}
          className="flex items-center gap-3 w-full px-3 py-2.5 rounded-xl text-[14px] text-text-secondary hover:text-text-primary hover:bg-gray-50 transition-all truncate text-left group"
        >
          <MessageSquare className="w-3.5 h-3.5 flex-shrink-0 text-gray-300 group-hover:text-primary transition-colors" />
          <span className="truncate">{item}</span>
        </motion.button>
      ))}
    </div>
  </div>
);

const SidebarAction = ({ icon, label, onClick }: { icon: React.ReactNode; label: string; onClick?: () => void }) => (
  <button
    onClick={onClick}
    className="flex items-center gap-3 w-full px-3 py-2.5 rounded-xl text-[14px] text-text-secondary hover:bg-gray-50 hover:text-text-primary transition-all"
  >
    {icon} {label}
  </button>
);
`,

// ─────────────────────────────────────────────────────────────────────────────
// RIGHT ANALYSIS PANEL — alive from start, transforms after query
// ─────────────────────────────────────────────────────────────────────────────
'components/workspace/AnalysisPanel.tsx': `import { motion } from 'framer-motion';
import { ChevronRight, Download, Sparkles } from 'lucide-react';
import { Button } from '../ui/Button';
import { useTranslation } from '../../contexts/LanguageContext';

export const AnalysisPanel = ({ active }: { active: boolean }) => {
  const { t } = useTranslation();

  return (
    <aside className="fixed top-[80px] right-0 bottom-0 w-[280px] bg-white border-l border-black/[0.04] hidden xl:flex flex-col z-40 overflow-hidden">
      <div className="flex-1 flex flex-col p-6 overflow-y-auto scrollbar-hide">
        <div className="flex items-center gap-2 mb-6">
          <Sparkles className="w-4 h-4 text-secondary" />
          <span className="font-heading font-semibold text-[15px] text-text-primary">{t('workspace.analysis')}</span>
        </div>

        {!active ? (
          <div className="flex-1 flex flex-col">
            {/* Stats cards — visible even before query */}
            <div className="mb-8">
              <p className="text-[12px] font-semibold text-gray-400 uppercase tracking-widest mb-4">{t('workspace.assistant')}</p>
              <p className="text-[13px] text-text-secondary leading-relaxed mb-6">{t('workspace.assistantDesc')}</p>
              <div className="grid grid-cols-3 gap-2">
                <StatCard value="200+" label={t('workspace.verifiedSources')} color="text-primary" bg="bg-orange-50" />
                <StatCard value="65" label={t('workspace.countries')} color="text-secondary" bg="bg-blue-50" />
                <StatCard value="12K+" label={t('workspace.programs')} color="text-accent" bg="bg-emerald-50" />
              </div>
            </div>
            <div className="flex-1 flex items-center justify-center">
              <p className="text-[13px] text-gray-400 text-center max-w-[160px]">{t('workspace.analysisEmpty')}</p>
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
              <p className="text-[11px] font-bold text-gray-400 uppercase tracking-widest mb-3">{t('workspace.profileSummary')}</p>
              <div className="space-y-2">
                <SummaryItem label={t('workspace.goal')} value="Master's Scholarship" />
                <SummaryItem label={t('workspace.country')} value="Germany" />
                <SummaryItem label={t('workspace.education')} value="B.Tech (8.6 CGPA)" />
                <SummaryItem label={t('workspace.budget')} value="Fully Funded" />
              </div>
            </div>

            <div>
              <p className="text-[11px] font-bold text-gray-400 uppercase tracking-widest mb-3">{t('workspace.currentMatches')}</p>
              <div className="bg-gradient-to-br from-emerald-50 to-teal-50 rounded-2xl p-4 border border-emerald-100">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-[13px] font-semibold text-emerald-800">{t('workspace.topMatch')}</span>
                  <span className="text-xl font-bold text-emerald-600">94%</span>
                </div>
                <p className="text-[12px] text-emerald-600/80">{t('workspace.matchDesc')}</p>
              </div>
            </div>

            <div className="mt-auto space-y-2 pt-4 border-t border-gray-50">
              <PanelAction label={t('workspace.compare')} />
              <PanelAction label={t('workspace.decisionReport')} />
              <Button variant="secondary" className="w-full h-[40px] text-[13px] gap-2">
                <Download className="w-4 h-4" /> {t('workspace.export')}
              </Button>
            </div>
          </motion.div>
        )}
      </div>
    </aside>
  );
};

const StatCard = ({ value, label, color, bg }: any) => (
  <div className={\`\${bg} rounded-xl p-3 text-center border border-white\`}>
    <div className={\`text-lg font-bold \${color}\`}>{value}</div>
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
`,

// ─────────────────────────────────────────────────────────────────────────────
// EMPTY STATE — better greeting, emoji chips
// ─────────────────────────────────────────────────────────────────────────────
'components/workspace/MessageEmptyState.tsx': `import { motion } from 'framer-motion';
import { useTranslation } from '../../contexts/LanguageContext';

export const MessageEmptyState = ({ onSelect }: { onSelect: (text: string) => void }) => {
  const { t } = useTranslation();

  const chips = [
    { key: 'chat.chip1' as const, raw: 'Scholarships' },
    { key: 'chat.chip2' as const, raw: 'Germany' },
    { key: 'chat.chip3' as const, raw: 'PhD' },
    { key: 'chat.chip4' as const, raw: 'Loans' },
    { key: 'chat.chip5' as const, raw: 'Study Abroad' },
    { key: 'chat.chip6' as const, raw: 'Startup Grants' },
  ];

  return (
    <div className="flex-1 flex flex-col items-center justify-center text-center px-6 min-h-[60vh]">
      <motion.div
        initial={{ opacity: 0, y: 24 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, ease: 'easeOut' }}
        className="max-w-[540px] w-full"
      >
        <h2 className="text-[42px] font-heading font-bold text-text-primary mb-3 leading-tight">{t('chat.greeting')}</h2>
        <p className="text-[18px] text-text-secondary mb-12 max-w-[400px] mx-auto">{t('chat.greetingSub')}</p>

        <div className="flex flex-wrap justify-center gap-3">
          {chips.map(({ key, raw }, i) => (
            <motion.button
              key={i}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 + i * 0.06, duration: 0.35 }}
              whileHover={{ scale: 1.04, y: -3 }}
              whileTap={{ scale: 0.97 }}
              onClick={() => onSelect(raw)}
              className="px-5 py-3 bg-white border border-gray-200 rounded-2xl text-[14px] font-medium text-text-secondary hover:text-primary hover:border-primary/30 hover:shadow-[0_8px_24px_rgba(249,115,22,0.1)] transition-all shadow-sm cursor-pointer"
            >
              {t(key)}
            </motion.button>
          ))}
        </div>
      </motion.div>
    </div>
  );
};
`,

// ─────────────────────────────────────────────────────────────────────────────
// CHAT INPUT — properly floating, glass, glows
// ─────────────────────────────────────────────────────────────────────────────
'components/workspace/ChatInput.tsx': `import { useState } from 'react';
import { motion } from 'framer-motion';
import { ArrowUp, Paperclip, Mic } from 'lucide-react';
import { useTranslation } from '../../contexts/LanguageContext';

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
    <div className="sticky bottom-0 left-0 right-0 pb-6 pt-4 bg-gradient-to-t from-white via-white/95 to-transparent flex justify-center px-4">
      <motion.div
        className="w-full max-w-[720px] relative"
        animate={{ scale: focused ? 1.01 : 1 }}
        transition={{ duration: 0.2, ease: 'easeOut' }}
      >
        {/* Glow halo */}
        <div className={\`absolute inset-0 bg-primary/15 rounded-[28px] blur-2xl transition-opacity duration-500 pointer-events-none \${focused ? 'opacity-100' : 'opacity-0'}\`} />

        <form onSubmit={handleSubmit} className="relative">
          <div className={\`flex items-center h-[70px] rounded-[28px] px-2 border transition-all duration-300 shadow-[0_8px_30px_rgba(0,0,0,0.06)] \${
            focused
              ? 'bg-white border-primary/40 shadow-[0_12px_40px_rgba(249,115,22,0.12)]'
              : 'bg-white/80 backdrop-blur-sm border-gray-200'
          }\`}>
            <button type="button" className="p-3 text-gray-300 hover:text-gray-500 transition-colors rounded-full">
              <Paperclip className="w-5 h-5" />
            </button>

            <input
              type="text"
              value={val}
              onChange={e => setVal(e.target.value)}
              onFocus={() => setFocused(true)}
              onBlur={() => setFocused(false)}
              onKeyDown={handleKey}
              placeholder={t('chat.placeholder')}
              className="flex-1 bg-transparent border-none outline-none text-text-primary placeholder:text-gray-400 py-3 px-2 text-[15px]"
            />

            <button type="button" className="p-3 text-gray-300 hover:text-gray-500 transition-colors rounded-full mr-1">
              <Mic className="w-5 h-5" />
            </button>

            <button
              type="submit"
              disabled={!val.trim()}
              className="w-12 h-12 rounded-2xl bg-gradient-to-br from-primary to-orange-500 text-white flex items-center justify-center shadow-md disabled:opacity-30 disabled:grayscale hover:scale-105 active:scale-95 transition-all"
            >
              <ArrowUp className="w-5 h-5" />
            </button>
          </div>
        </form>
      </motion.div>
    </div>
  );
};
`,

// ─────────────────────────────────────────────────────────────────────────────
// MESSAGE SEQUENCE — Perplexity-style cards, no bubble wall
// ─────────────────────────────────────────────────────────────────────────────
'components/workspace/MessageSequence.tsx': `import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle2, ChevronDown, Check, ExternalLink, Star } from 'lucide-react';
import { Button } from '../ui/Button';
import { useTranslation } from '../../contexts/LanguageContext';

export const MessageSequence = ({ query }: { query: string }) => {
  const [step, setStep] = useState(0);
  const { t } = useTranslation();

  useEffect(() => {
    let timer: ReturnType<typeof setTimeout>;
    if (step < 7) timer = setTimeout(() => setStep(p => p + 1), step === 0 ? 400 : 500);
    return () => clearTimeout(timer);
  }, [step]);

  const thinkingSteps = [
    t('ai.step1'), t('ai.step2'), t('ai.step3'),
    t('ai.step4'), t('ai.step5'), t('ai.step6'),
  ];

  return (
    <div className="w-full max-w-[720px] mx-auto flex flex-col gap-8 py-6">
      {/* User message — right aligned, no bubble wall */}
      <motion.div
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        className="self-end max-w-[520px] bg-orange-50/80 border border-orange-100 px-6 py-4 rounded-3xl rounded-tr-lg"
      >
        <p className="text-[15px] text-text-primary leading-relaxed">{query}</p>
        <span className="text-[11px] text-gray-400 block mt-1">{t('chat.just_now')}</span>
      </motion.div>

      {/* AI — no bubble, just cards */}
      <div className="self-start w-full flex flex-col gap-6">
        {/* Thinking checklist */}
        <AnimatePresence>
          {step < 7 && (
            <motion.div
              exit={{ opacity: 0, height: 0, overflow: 'hidden' }}
              transition={{ duration: 0.3 }}
              className="bg-gray-50/80 border border-gray-100 rounded-2xl px-5 py-4 w-fit"
            >
              <div className="flex items-center gap-2 text-[13px] font-medium text-text-secondary mb-3">
                <span className="relative flex h-2 w-2">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-primary"></span>
                </span>
                {t('ai.thinking')}
              </div>
              <div className="space-y-2">
                {thinkingSteps.map((stepText, i) => (
                  <ThinkStep key={i} show={step >= i + 1} text={stepText} />
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Results — staggered reveal */}
        {step >= 7 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex flex-col gap-8 w-full"
          >
            {/* Summary chips */}
            <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} className="flex flex-wrap gap-2">
              <Chip label={\`94% \${t('card.match')}\`} bg="bg-emerald-50" text="text-emerald-700" border="border-emerald-100" dot="bg-emerald-500" />
              <Chip label={t('card.fullFunding')} bg="bg-blue-50" text="text-blue-700" border="border-blue-100" />
              <Chip label="4 Sources Checked" bg="bg-gray-50" text="text-text-secondary" border="border-gray-200" />
            </motion.div>

            {/* Opportunity Cards */}
            <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.15 }} className="space-y-4">
              <OpCard
                flag="🇩🇪" name="DAAD EPOS Scholarship" match="94"
                funding={t('card.fullFunding')} deadline="20 Nov 2026" difficulty="High"
              />
              <OpCard
                flag="🇩🇪" name="Heinrich Böll Foundation" match="88"
                funding={t('card.partialFunding')} deadline="01 Sep 2026" difficulty="Medium"
              />
            </motion.div>

            {/* Eligibility */}
            <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}
              className="bg-white rounded-[24px] p-6 border border-gray-100 shadow-[0_8px_30px_rgba(0,0,0,0.04)]"
            >
              <div className="flex items-center justify-between cursor-pointer mb-4">
                <h3 className="font-heading font-bold text-lg text-text-primary">{t('eligibility.title')}</h3>
                <ChevronDown className="w-5 h-5 text-gray-300" />
              </div>
              <div className="space-y-3 pt-4 border-t border-gray-50">
                <EligReason text={t('eligibility.reason1')} />
                <EligReason text={t('eligibility.reason2')} />
              </div>
            </motion.div>

            {/* Sources */}
            <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.45 }}>
              <p className="text-[11px] font-bold text-gray-400 uppercase tracking-widest mb-3">{t('card.officialSource')}</p>
              <div className="flex flex-wrap gap-2">
                {['DAAD', 'Fulbright', 'AICTE'].map(src => (
                  <div key={src} className="flex items-center gap-2 bg-white border border-gray-100 rounded-xl px-3 py-2 text-[13px] shadow-sm hover:border-gray-300 cursor-pointer transition-all group">
                    <span className="font-bold text-text-primary">{src}</span>
                    <span className="text-gray-300 group-hover:text-primary transition-colors"><ExternalLink className="w-3 h-3" /></span>
                  </div>
                ))}
              </div>
            </motion.div>

            {/* Follow-ups */}
            <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.6 }}
              className="pt-4 border-t border-gray-100"
            >
              <p className="text-[12px] text-text-secondary mb-3 font-semibold uppercase tracking-widest">{t('followup.label')}</p>
              <div className="flex flex-wrap gap-2">
                <FollowUp label={t('followup.full')} />
                <FollowUp label={t('followup.alt')} />
                <FollowUp label={t('followup.loans')} />
              </div>
            </motion.div>
          </motion.div>
        )}
      </div>
    </div>
  );
};

const ThinkStep = ({ show, text }: { show: boolean; text: string }) => (
  <AnimatePresence>
    {show && (
      <motion.div
        initial={{ opacity: 0, x: -8, height: 0 }}
        animate={{ opacity: 1, x: 0, height: 'auto' }}
        className="flex items-center gap-2 text-[13px] text-text-secondary overflow-hidden"
      >
        <CheckCircle2 className="w-3.5 h-3.5 text-accent flex-shrink-0" /> {text}
      </motion.div>
    )}
  </AnimatePresence>
);

const Chip = ({ label, bg, text, border, dot }: any) => (
  <span className={\`inline-flex items-center gap-1.5 \${bg} \${text} \${border} border px-3 py-1.5 rounded-xl text-[13px] font-semibold\`}>
    {dot && <span className={\`w-1.5 h-1.5 rounded-full \${dot}\`} />}
    {label}
  </span>
);

const EligReason = ({ text }: { text: string }) => (
  <div className="flex items-start gap-3">
    <div className="mt-0.5 w-5 h-5 rounded-full bg-emerald-100 flex items-center justify-center flex-shrink-0">
      <Check className="w-3 h-3 text-emerald-600" />
    </div>
    <p className="text-[15px] text-text-secondary">{text}</p>
  </div>
);

const FollowUp = ({ label }: { label: string }) => (
  <button className="text-[13px] bg-gray-50 hover:bg-orange-50 hover:text-primary text-text-secondary px-4 py-2 rounded-full transition-all border border-gray-200 hover:border-primary/20">
    {label}
  </button>
);

const OpCard = ({ flag, name, match, funding, deadline, difficulty }: any) => {
  const { t } = useTranslation();
  return (
    <motion.div
      whileHover={{ y: -4, boxShadow: '0 16px 40px rgba(249,115,22,0.08)' }}
      className="bg-white rounded-[24px] p-6 border border-gray-100 shadow-[0_8px_30px_rgba(0,0,0,0.04)] transition-all duration-300 cursor-pointer group hover:border-primary/20"
    >
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <span className="text-3xl">{flag}</span>
          <div>
            <h3 className="font-heading font-bold text-[17px] text-text-primary">{name}</h3>
            <div className="flex items-center gap-1 mt-1">
              {[1,2,3,4,5].map(s => <Star key={s} className="w-3 h-3 fill-amber-400 text-amber-400" />)}
              <span className="text-[11px] text-gray-400 ml-1 flex items-center gap-1">
                <CheckCircle2 className="w-3 h-3 text-emerald-500" /> {t('card.verified')}
              </span>
            </div>
          </div>
        </div>
        <div className="bg-emerald-100 text-emerald-700 text-[12px] font-bold px-3 py-1 rounded-full">{match}% {t('card.match')}</div>
      </div>

      <div className="grid grid-cols-3 gap-2 mb-5">
        <InfoCell label={t('card.funding')} value={funding} />
        <InfoCell label={t('card.deadline')} value={deadline} />
        <InfoCell label={t('card.difficulty')} value={difficulty} />
      </div>

      <div className="flex items-center gap-3">
        <Button className="h-[40px] px-5 text-[13px] flex-1">{t('card.viewDetails')}</Button>
        <Button variant="secondary" className="h-[40px] px-5 text-[13px]">{t('card.compare')}</Button>
      </div>
    </motion.div>
  );
};

const InfoCell = ({ label, value }: { label: string; value: string }) => (
  <div className="bg-gray-50 rounded-xl px-3 py-2.5 border border-black/[0.04]">
    <div className="text-[10px] text-gray-400 uppercase tracking-wider mb-0.5">{label}</div>
    <div className="text-[13px] font-semibold text-text-primary">{value}</div>
  </div>
);
`,

// ─────────────────────────────────────────────────────────────────────────────
// CHAT AREA — only scrolls centre, navbar offset correct
// ─────────────────────────────────────────────────────────────────────────────
'components/workspace/ChatArea.tsx': `import { useRef } from 'react';
import { useState } from 'react';
import { ChatInput } from './ChatInput';
import { MessageEmptyState } from './MessageEmptyState';
import { MessageSequence } from './MessageSequence';

export const ChatArea = ({ onAnalysisActive }: { onAnalysisActive: (v: boolean) => void }) => {
  const [messages, setMessages] = useState<string[]>([]);
  const bottomRef = useRef<HTMLDivElement>(null);

  const handleSend = (text: string) => {
    setMessages(prev => [...prev, text]);
    onAnalysisActive(true);
    setTimeout(() => bottomRef.current?.scrollIntoView({ behavior: 'smooth' }), 100);
  };

  return (
    <div className="fixed top-[80px] bottom-0 left-[280px] right-[280px] flex flex-col hidden lg:flex xl:flex overflow-hidden">
      {/* Soft background blobs */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden z-0">
        <div className="absolute top-[-10%] left-[-5%] w-[400px] h-[400px] bg-primary/4 rounded-full blur-[100px]" />
        <div className="absolute bottom-[-10%] right-[-5%] w-[400px] h-[400px] bg-secondary/4 rounded-full blur-[100px]" />
      </div>

      {/* Scrollable conversation */}
      <div className="flex-1 overflow-y-auto px-8 py-6 relative z-10 scrollbar-hide">
        {messages.length === 0 ? (
          <MessageEmptyState onSelect={handleSend} />
        ) : (
          <div className="flex flex-col">
            {messages.map((m, i) => (
              <MessageSequence key={i} query={m} />
            ))}
            <div ref={bottomRef} />
          </div>
        )}
      </div>

      {/* Pinned input */}
      <div className="relative z-10">
        <ChatInput onSend={handleSend} />
      </div>
    </div>
  );
};
`,

// ─────────────────────────────────────────────────────────────────────────────
// DISCOVERY PAGE — clean three-col layout, no overlaps
// ─────────────────────────────────────────────────────────────────────────────
'pages/Discovery.tsx': `import { useState } from 'react';
import { Sidebar } from '../components/workspace/Sidebar';
import { AnalysisPanel } from '../components/workspace/AnalysisPanel';
import { ChatArea } from '../components/workspace/ChatArea';
import { Navbar } from '../components/layout/Navbar';
import { PageTransition } from '../components/motion/PageTransition';

export const Discovery = () => {
  const [analysisActive, setAnalysisActive] = useState(false);

  return (
    <PageTransition>
      <div className="w-full min-h-screen bg-white relative">
        {/* Fixed Navbar — full width, 80px */}
        <Navbar />

        {/* Three-column layout starting below 80px navbar */}
        <Sidebar />
        <ChatArea onAnalysisActive={setAnalysisActive} />
        <AnalysisPanel active={analysisActive} />

        {/* Mobile fallback — full-width chat on small screens */}
        <div className="lg:hidden flex flex-col min-h-screen pt-[80px]">
          <div className="flex-1 overflow-y-auto px-4 py-6">
            <div className="text-center text-text-secondary pt-20 text-[16px]">
              AI Workspace is optimized for desktop. Please use a larger screen for the best experience.
            </div>
          </div>
        </div>
      </div>
    </PageTransition>
  );
};
`,

};

for (const [relPath, content] of Object.entries(files)) {
  const fullPath = path.join(srcDir, relPath);
  const dir = path.dirname(fullPath);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(fullPath, content);
}
console.log("All workspace components rewritten!");
