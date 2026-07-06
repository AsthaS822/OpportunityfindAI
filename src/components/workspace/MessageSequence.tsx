import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle2, ChevronDown, Check, ExternalLink, Star } from 'lucide-react';
import { Button } from '../ui/Button';
import { useTranslation } from 'react-i18next';

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
      {/* User message */}
      <motion.div
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        className="self-end max-w-[520px] bg-orange-50/80 border border-orange-100 px-6 py-4 rounded-3xl rounded-tr-lg shadow-sm"
      >
        <p className="text-[15px] text-text-primary leading-relaxed">{query}</p>
        <span className="text-[11px] text-gray-400 block mt-1">{t('chat.just_now')}</span>
      </motion.div>

      {/* AI */}
      <div className="self-start w-full flex flex-col gap-6">
        {/* Thinking checklist */}
        <AnimatePresence>
          {step < 7 && (
            <motion.div
              exit={{ opacity: 0, height: 0, overflow: 'hidden' }}
              transition={{ duration: 0.3 }}
              className="bg-white/70 backdrop-blur-md border border-gray-100 rounded-2xl px-5 py-4 w-fit shadow-sm"
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

        {/* Results */}
        {step >= 7 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex flex-col gap-8 w-full"
          >
            {/* Summary chips */}
            <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} className="flex flex-wrap gap-2">
              <Chip label={`94% ${t('card.match')}`} bg="bg-emerald-50" text="text-emerald-700" border="border-emerald-100" dot="bg-emerald-500" />
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
  <span className={`inline-flex items-center gap-1.5 ${bg} ${text} ${border} border px-3 py-1.5 rounded-xl text-[13px] font-semibold`}>
    {dot && <span className={`w-1.5 h-1.5 rounded-full ${dot}`} />}
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
