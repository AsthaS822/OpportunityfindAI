import { motion } from 'framer-motion';
import { ArrowRight, Bot, Target, FileCheck } from 'lucide-react';
import { Container } from '../layout/Container';

export const FeatureStrip = () => {
  return (
    <div className="pt-[140px]">
      <Container>
        <motion.div 
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{ duration: 0.6, ease: "easeOut" }}
          className="bg-white rounded-[32px] p-8 md:p-12 shadow-[0_8px_40px_rgb(0,0,0,0.04)] border border-gray-100"
        >
          <div className="grid grid-cols-1 md:grid-cols-3 gap-12 divide-y md:divide-y-0 md:divide-x divide-gray-100">
            {/* Feature 1 */}
            <div className="group flex flex-col items-start md:pr-12 cursor-pointer pt-0">
              <div className="w-14 h-14 rounded-2xl bg-orange-50 text-primary flex items-center justify-center mb-6 group-hover:scale-110 group-hover:bg-primary group-hover:text-white transition-all duration-300 shadow-sm">
                <Bot className="w-7 h-7" />
              </div>
              <h3 className="font-heading text-2xl font-bold text-text-primary mb-3">AI Discovery</h3>
              <p className="text-text-secondary text-[16px] leading-relaxed mb-6 max-w-[280px]">
                Tell our AI about yourself and find every hidden opportunity instantly.
              </p>
              <div className="mt-auto flex items-center text-primary font-medium text-sm group-hover:translate-x-1 transition-transform">
                Learn more <ArrowRight className="w-4 h-4 ml-1" />
              </div>
            </div>

            {/* Feature 2 */}
            <div className="group flex flex-col items-start md:px-12 cursor-pointer pt-12 md:pt-0">
              <div className="w-14 h-14 rounded-2xl bg-blue-50 text-secondary flex items-center justify-center mb-6 group-hover:scale-110 group-hover:bg-secondary group-hover:text-white transition-all duration-300 shadow-sm">
                <Target className="w-7 h-7" />
              </div>
              <h3 className="font-heading text-2xl font-bold text-text-primary mb-3">Eligibility Check</h3>
              <p className="text-text-secondary text-[16px] leading-relaxed mb-6 max-w-[280px]">
                Instantly verify if you meet the requirements before applying.
              </p>
              <div className="mt-auto flex items-center text-secondary font-medium text-sm group-hover:translate-x-1 transition-transform">
                Learn more <ArrowRight className="w-4 h-4 ml-1" />
              </div>
            </div>

            {/* Feature 3 */}
            <div className="group flex flex-col items-start md:pl-12 cursor-pointer pt-12 md:pt-0">
              <div className="w-14 h-14 rounded-2xl bg-emerald-50 text-accent flex items-center justify-center mb-6 group-hover:scale-110 group-hover:bg-accent group-hover:text-white transition-all duration-300 shadow-sm">
                <FileCheck className="w-7 h-7" />
              </div>
              <h3 className="font-heading text-2xl font-bold text-text-primary mb-3">Decision Report</h3>
              <p className="text-text-secondary text-[16px] leading-relaxed mb-6 max-w-[280px]">
                Get a personalized roadmap with deadlines and requirements.
              </p>
              <div className="mt-auto flex items-center text-accent font-medium text-sm group-hover:translate-x-1 transition-transform">
                Learn more <ArrowRight className="w-4 h-4 ml-1" />
              </div>
            </div>
          </div>
        </motion.div>
      </Container>
    </div>
  );
};
