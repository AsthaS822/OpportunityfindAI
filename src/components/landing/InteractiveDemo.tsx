import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Container } from '../layout/Container';
import { Section } from '../layout/Section';
import { CheckCircle2, ArrowRight, ExternalLink } from 'lucide-react';

export const InteractiveDemo = () => {
  const [step, setStep] = useState(0);

  // Auto-play the demo sequence
  useEffect(() => {
    let timer: any;
    if (step < 7) {
      timer = setTimeout(() => {
        setStep(prev => prev + 1);
      }, step === 0 ? 1500 : step < 5 ? 800 : 2000);
    } else {
      // Reset after a long pause
      timer = setTimeout(() => setStep(0), 10000);
    }
    return () => clearTimeout(timer);
  }, [step]);

  return (
    <Section id="demo" className="bg-[#FFF8F3]">
      <Container>
        <div className="text-center max-w-[620px] mx-auto mb-16">
          <h2 className="text-4xl md:text-[48px] font-heading font-bold text-text-primary mb-6 tracking-tight">
            See the magic in action.
          </h2>
          <p className="text-[18px] text-text-secondary">
            No complex filters or endless scrolling. Just tell the AI what you need.
          </p>
        </div>

        <div className="max-w-[800px] mx-auto bg-white rounded-[32px] shadow-[0_20px_60px_rgb(0,0,0,0.06)] border border-orange-100 overflow-hidden relative min-h-[600px]">
          {/* Header */}
          <div className="px-8 py-6 border-b border-gray-100 flex items-center gap-4 bg-gray-50/50">
            <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center text-primary font-bold">U</div>
            <div className="text-[16px] font-medium text-text-primary bg-white px-5 py-3 rounded-2xl rounded-tl-none shadow-sm border border-gray-100">
              Find fully funded master's scholarships in Germany for Indian students.
            </div>
          </div>

          <div className="p-8">
            <AnimatePresence>
              {step >= 1 && (
                <motion.div 
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="mb-8"
                >
                  <div className="flex items-center gap-3 mb-4 text-text-secondary text-sm font-medium">
                    <span className="relative flex h-3 w-3">
                      <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
                      <span className="relative inline-flex rounded-full h-3 w-3 bg-primary"></span>
                    </span>
                    FutureOS is thinking...
                  </div>
                  
                  <div className="space-y-3 pl-6">
                    <CheckItem show={step >= 1} text="Understanding requirements" />
                    <CheckItem show={step >= 2} text="Searching global scholarship database" />
                    <CheckItem show={step >= 3} text="Checking eligibility criteria for Indian citizens" />
                    <CheckItem show={step >= 4} text="Filtering for fully funded options" />
                  </div>
                </motion.div>
              )}
            </AnimatePresence>

            <AnimatePresence>
              {step >= 5 && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.5, ease: "easeOut" }}
                  className="bg-white rounded-2xl p-6 border-2 border-primary/20 shadow-lg hover:shadow-xl hover:border-primary/40 transition-all cursor-pointer relative group"
                >
                  <div className="absolute top-4 right-4 bg-emerald-100 text-emerald-700 text-xs font-bold px-3 py-1 rounded-full">
                    94% Match
                  </div>
                  
                  <h4 className="text-xl font-heading font-bold text-text-primary mb-2 flex items-center gap-2">
                    🇩🇪 DAAD EPOS Scholarship
                  </h4>
                  <div className="text-text-secondary text-[15px] mb-4 max-w-[500px]">
                    Development-Related Postgraduate Courses for developing countries. Covers full tuition, monthly stipend, and travel.
                  </div>
                  
                  <div className="flex gap-4 mb-6">
                    <div className="bg-gray-50 px-4 py-2 rounded-xl text-sm border border-gray-100">
                      <span className="block text-gray-400 text-xs mb-1">Funding</span>
                      <span className="font-semibold text-text-primary">Fully Funded</span>
                    </div>
                    <div className="bg-gray-50 px-4 py-2 rounded-xl text-sm border border-gray-100">
                      <span className="block text-gray-400 text-xs mb-1">Deadline</span>
                      <span className="font-semibold text-text-primary">Oct 15, 2026</span>
                    </div>
                  </div>

                  <div className="flex items-center justify-between mt-4 pt-4 border-t border-gray-100">
                    <div className="text-sm font-medium text-gray-500 flex items-center gap-2">
                      <ExternalLink className="w-4 h-4" /> Official Source
                    </div>
                    <button className="text-primary font-medium text-sm flex items-center group-hover:translate-x-1 transition-transform">
                      View Details <ArrowRight className="w-4 h-4 ml-1" />
                    </button>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>

            <AnimatePresence>
              {step >= 6 && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.4 }}
                  className="mt-6 bg-blue-50/50 rounded-2xl p-6 border border-blue-100"
                >
                  <div className="text-sm font-semibold text-secondary mb-2">Decision Summary</div>
                  <p className="text-[15px] text-text-secondary">
                    You meet all 5 primary eligibility criteria for the DAAD EPOS program. You have 3 months left to prepare your application. I recommend starting with your Motivation Letter.
                  </p>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>
      </Container>
    </Section>
  );
};

const CheckItem = ({ show, text }: { show: boolean; text: string }) => {
  return (
    <motion.div 
      initial={{ opacity: 0, x: -10 }}
      animate={show ? { opacity: 1, x: 0 } : { opacity: 0, x: -10 }}
      className="flex items-center gap-2 text-sm text-text-secondary"
    >
      <CheckCircle2 className="w-4 h-4 text-accent" />
      {text}
    </motion.div>
  );
};
