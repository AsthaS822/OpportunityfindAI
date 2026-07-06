const fs = require('fs');
const path = require('path');

const srcDir = path.join(__dirname, 'src');

const files = {
  'components/workspace/MessageEmptyState.tsx': `import { motion } from 'framer-motion';

export const MessageEmptyState = ({ onSelect }: { onSelect: (text: string) => void }) => {
  const suggestions = [
    "Study in Germany",
    "Scholarships in Japan",
    "Education Loan",
    "Government Schemes",
    "Research Funding",
    "Startup Grants"
  ];

  return (
    <div className="flex-1 flex flex-col items-center justify-center pt-[10vh] pb-32 px-4 text-center">
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, ease: "easeOut" }}
      >
        <h2 className="text-[32px] md:text-[40px] font-heading font-bold text-text-primary mb-2">Hello 👋</h2>
        <p className="text-xl text-text-secondary mb-12">What opportunity are you looking for today?</p>
      </motion.div>

      <motion.div 
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5, delay: 0.2 }}
        className="flex flex-wrap justify-center gap-3 max-w-[600px]"
      >
        {suggestions.map((s, i) => (
          <motion.button
            key={i}
            whileHover={{ scale: 1.03, y: -2 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => onSelect(s)}
            className="px-5 py-3 bg-white border border-gray-200 rounded-[20px] text-[15px] font-medium text-text-secondary hover:text-primary hover:border-primary/40 hover:shadow-[0_8px_20px_rgba(249,115,22,0.1)] transition-all shadow-sm"
          >
            {s}
          </motion.button>
        ))}
      </motion.div>
    </div>
  );
};
`,
  'components/workspace/MessageSequence.tsx': `import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle2, ChevronDown, Check, ExternalLink } from 'lucide-react';
import { Button } from '../ui/Button';

export const MessageSequence = ({ query }: { query: string }) => {
  const [step, setStep] = useState(0);

  useEffect(() => {
    let timer: any;
    if (step < 7) {
      timer = setTimeout(() => {
        setStep(prev => prev + 1);
      }, step === 0 ? 500 : 800);
    }
    return () => clearTimeout(timer);
  }, [step]);

  return (
    <div className="w-full max-w-[800px] mx-auto py-8 flex flex-col gap-8 pb-32">
      {/* User Message */}
      <motion.div 
        initial={{ opacity: 0, y: 10, scale: 0.95 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        className="self-end max-w-[700px] bg-orange-50 text-text-primary px-6 py-4 rounded-3xl rounded-tr-lg border border-orange-100 shadow-sm"
      >
        <p className="text-[16px] leading-relaxed">{query}</p>
        <span className="text-[11px] text-gray-400 block mt-2 font-medium">Just now</span>
      </motion.div>

      {/* AI Response Area */}
      <div className="flex flex-col gap-6 self-start w-full">
        {/* Thinking Sequence */}
        <AnimatePresence>
          {step < 7 && (
            <motion.div 
              exit={{ opacity: 0, height: 0, marginBottom: 0 }}
              className="bg-gray-50 rounded-2xl p-4 w-fit border border-gray-100 overflow-hidden"
            >
              <div className="flex items-center gap-2 text-sm font-medium text-text-secondary mb-3">
                <span className="relative flex h-2 w-2">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-primary"></span>
                </span>
                Researching opportunities...
              </div>
              <div className="space-y-2 pl-4">
                <CheckItem show={step >= 1} text="Understanding your profile" />
                <CheckItem show={step >= 2} text="Extracting important details" />
                <CheckItem show={step >= 3} text="Searching verified sources" />
                <CheckItem show={step >= 4} text="Applying eligibility rules" />
                <CheckItem show={step >= 5} text="Comparing opportunities" />
                <CheckItem show={step >= 6} text="Creating personalized roadmap" />
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Results */}
        <AnimatePresence>
          {step >= 7 && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, staggerChildren: 0.15 }}
              className="flex flex-col gap-8 w-full"
            >
              {/* Summary Card */}
              <motion.div 
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="flex flex-wrap gap-3"
              >
                <div className="bg-emerald-50 text-emerald-700 px-4 py-2 rounded-xl text-sm font-semibold flex items-center gap-2 border border-emerald-100">
                  <CheckCircle2 className="w-4 h-4" /> 94% Top Match
                </div>
                <div className="bg-blue-50 text-blue-700 px-4 py-2 rounded-xl text-sm font-semibold border border-blue-100">
                  Fully Funded
                </div>
                <div className="bg-gray-50 text-text-secondary px-4 py-2 rounded-xl text-sm font-medium border border-gray-200">
                  4 Sources Checked
                </div>
              </motion.div>

              {/* Opportunity Cards */}
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-4">
                <OpportunityCard 
                  title="DAAD EPOS Scholarship" 
                  flag="🇩🇪"
                  match="94%" 
                  funding="Full Funding" 
                  deadline="20 Nov 2026"
                  difficulty="High"
                />
                <OpportunityCard 
                  title="Heinrich Böll Foundation" 
                  flag="🇩🇪"
                  match="88%" 
                  funding="Partial Funding" 
                  deadline="01 Sep 2026"
                  difficulty="Medium"
                />
              </motion.div>

              {/* Eligibility Expandable */}
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="bg-white border border-gray-200 rounded-[24px] p-6 shadow-sm">
                <div className="flex items-center justify-between cursor-pointer">
                  <h3 className="font-heading font-bold text-lg text-text-primary">Why are you eligible?</h3>
                  <ChevronDown className="w-5 h-5 text-gray-400" />
                </div>
                <div className="mt-4 space-y-3 pt-4 border-t border-gray-50">
                  <div className="flex items-start gap-3">
                    <div className="mt-0.5 w-5 h-5 rounded-full bg-emerald-100 flex items-center justify-center flex-shrink-0 text-emerald-600">
                      <Check className="w-3 h-3" />
                    </div>
                    <p className="text-[15px] text-text-secondary">Your B.Tech degree matches the postgraduate course prerequisite.</p>
                  </div>
                  <div className="flex items-start gap-3">
                    <div className="mt-0.5 w-5 h-5 rounded-full bg-emerald-100 flex items-center justify-center flex-shrink-0 text-emerald-600">
                      <Check className="w-3 h-3" />
                    </div>
                    <p className="text-[15px] text-text-secondary">Your 8.6 CGPA is well above the minimum requirement of 7.5.</p>
                  </div>
                </div>
              </motion.div>

              {/* Verified Sources */}
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                <h4 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-3">Verified Sources</h4>
                <div className="flex flex-wrap gap-3">
                  <div className="flex items-center gap-2 bg-white border border-gray-200 rounded-xl px-3 py-2 text-sm shadow-sm hover:border-gray-300 cursor-pointer transition-colors group">
                    <span className="font-bold text-sky-600">DAAD</span>
                    <span className="text-gray-400 group-hover:text-primary transition-colors"><ExternalLink className="w-3 h-3" /></span>
                  </div>
                </div>
              </motion.div>

              {/* Suggested Follow-ups */}
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="pt-4 border-t border-gray-100">
                <p className="text-sm text-text-secondary mb-3 font-medium">Suggested Questions</p>
                <div className="flex flex-wrap gap-2">
                  <button className="text-[13px] bg-gray-50 hover:bg-orange-50 hover:text-primary text-text-secondary px-3 py-1.5 rounded-full transition-colors border border-gray-200">
                    Show only full scholarships
                  </button>
                  <button className="text-[13px] bg-gray-50 hover:bg-orange-50 hover:text-primary text-text-secondary px-3 py-1.5 rounded-full transition-colors border border-gray-200">
                    Find alternatives
                  </button>
                  <button className="text-[13px] bg-gray-50 hover:bg-orange-50 hover:text-primary text-text-secondary px-3 py-1.5 rounded-full transition-colors border border-gray-200">
                    Education loans
                  </button>
                </div>
              </motion.div>

            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

const CheckItem = ({ show, text }: { show: boolean, text: string }) => (
  <motion.div 
    initial={{ opacity: 0, height: 0 }}
    animate={show ? { opacity: 1, height: "auto" } : { opacity: 0, height: 0 }}
    className="flex items-center gap-2 text-[13px] text-text-secondary overflow-hidden"
  >
    <CheckCircle2 className="w-3.5 h-3.5 text-accent" />
    {text}
  </motion.div>
);

const OpportunityCard = ({ title, flag, match, funding, deadline, difficulty }: any) => {
  return (
    <div className="w-full max-w-[500px] bg-white rounded-[24px] p-6 shadow-[0_8px_20px_rgb(0,0,0,0.03)] border border-gray-200 hover:-translate-y-1 hover:shadow-glow hover:border-primary/30 transition-all duration-300">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <span className="text-2xl">{flag}</span>
          <div>
            <h3 className="font-heading font-bold text-lg text-text-primary leading-tight">{title}</h3>
            <span className="text-xs text-gray-400 flex items-center gap-1 mt-1">
              <CheckCircle2 className="w-3 h-3 text-emerald-500" /> Verified
            </span>
          </div>
        </div>
        <div className="bg-emerald-100 text-emerald-700 text-xs font-bold px-2.5 py-1 rounded-full whitespace-nowrap">
          {match} Match
        </div>
      </div>

      <div className="grid grid-cols-3 gap-2 mb-5">
        <div className="bg-gray-50 p-2 rounded-xl border border-gray-100">
          <div className="text-[10px] text-gray-400 uppercase tracking-wider mb-0.5">Funding</div>
          <div className="text-sm font-semibold text-text-primary">{funding}</div>
        </div>
        <div className="bg-gray-50 p-2 rounded-xl border border-gray-100">
          <div className="text-[10px] text-gray-400 uppercase tracking-wider mb-0.5">Deadline</div>
          <div className="text-sm font-semibold text-text-primary">{deadline}</div>
        </div>
        <div className="bg-gray-50 p-2 rounded-xl border border-gray-100">
          <div className="text-[10px] text-gray-400 uppercase tracking-wider mb-0.5">Difficulty</div>
          <div className="text-sm font-semibold text-text-primary">{difficulty}</div>
        </div>
      </div>

      <div className="flex items-center gap-3">
        <Button className="h-[40px] px-4 text-sm flex-1">View Details</Button>
        <Button variant="secondary" className="h-[40px] px-4 text-sm">Compare</Button>
      </div>
    </div>
  );
};
`,
  'components/workspace/ChatArea.tsx': `import { useState } from 'react';
import { BackgroundSystem } from '../landing/BackgroundSystem';
import { ChatInput } from './ChatInput';
import { MessageEmptyState } from './MessageEmptyState';
import { MessageSequence } from './MessageSequence';
import { Navbar } from '../layout/Navbar';

export const ChatArea = ({ onAnalysisActive }: { onAnalysisActive: (v: boolean) => void }) => {
  const [messages, setMessages] = useState<string[]>([]);

  const handleSend = (text: string) => {
    setMessages(prev => [...prev, text]);
    onAnalysisActive(true);
    
    // In a real app we'd scroll to bottom here.
    window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
  };

  return (
    <div className="flex-1 lg:ml-[300px] xl:mr-[24%] min-h-screen relative flex flex-col pt-[80px]">
      <BackgroundSystem />
      <Navbar />
      
      <div className="flex-1 overflow-y-auto px-4 md:px-8 flex flex-col">
        {messages.length === 0 ? (
          <MessageEmptyState onSelect={handleSend} />
        ) : (
          <div className="flex flex-col gap-6 w-full pb-32">
            {messages.map((m, i) => (
              <MessageSequence key={i} query={m} />
            ))}
          </div>
        )}
      </div>

      <ChatInput onSend={handleSend} />
    </div>
  );
};
`,
  'pages/Discovery.tsx': `import { useState } from 'react';
import { Sidebar } from '../components/workspace/Sidebar';
import { AnalysisPanel } from '../components/workspace/AnalysisPanel';
import { ChatArea } from '../components/workspace/ChatArea';
import { PageTransition } from '../components/motion/PageTransition';

export const Discovery = () => {
  const [analysisActive, setAnalysisActive] = useState(false);

  return (
    <PageTransition>
      <div className="flex min-h-screen w-full bg-white relative">
        <Sidebar />
        <ChatArea onAnalysisActive={setAnalysisActive} />
        <AnalysisPanel active={analysisActive} />
      </div>
    </PageTransition>
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
console.log("Scaffolded Workspace Area Components");
