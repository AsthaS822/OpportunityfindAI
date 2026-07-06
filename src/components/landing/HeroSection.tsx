import { motion } from 'framer-motion';
import { ArrowRight, Search, Sparkles, GraduationCap, Building2, Globe2 } from 'lucide-react';
import { Button } from '../ui/Button';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

export const HeroSection = () => {
  const { t } = useTranslation();
  const containerVariants: any = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.15, delayChildren: 0.1 }
    }
  };

  const itemVariants: any = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.6, ease: "easeOut" } }
  };

  return (
    <section className="relative min-h-screen flex items-center pt-24 overflow-hidden">
      <div className="mx-auto w-full max-w-[1280px] px-6 md:px-8 grid grid-cols-12 gap-8 items-center">
        
        {/* Left Column (42%) */}
        <motion.div 
          className="col-span-12 lg:col-span-5 z-10 flex flex-col justify-center"
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          <motion.div variants={itemVariants} className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-orange-50 border border-orange-100 text-primary text-sm font-medium mb-8 w-fit shadow-sm">
            <Sparkles className="w-4 h-4" />
            <span>{t('landing.hero_title')}</span>
          </motion.div>
          
          <motion.h1 variants={itemVariants} className="text-[72px] leading-[1.05] font-bold font-heading text-text-primary tracking-tight mb-6" dangerouslySetInnerHTML={{ __html: t('landing.hero_subtitle').replace('.', '.<br/><span class="bg-clip-text text-transparent bg-gradient-to-r from-primary to-orange-400">').replace('।', '।</span>') + (t('landing.hero_subtitle').includes('।') ? '' : '</span>') }}>
          </motion.h1>
          
          <motion.p variants={itemVariants} className="text-[18px] text-text-secondary leading-relaxed mb-10 max-w-[480px]">
            {t('landing.hero_desc')}
          </motion.p>
          
          <motion.div variants={itemVariants} className="relative group max-w-[500px] mb-6">
            <div className="absolute inset-0 bg-primary/20 rounded-[24px] blur-xl opacity-0 group-focus-within:opacity-100 transition-opacity duration-500" />
            <div className="relative glass-panel rounded-[24px] p-2 flex items-center shadow-lg border border-white/60 bg-white/70">
              <div className="pl-4 pr-2 text-gray-400">
                <Search className="w-5 h-5" />
              </div>
              <input 
                type="text"
                placeholder={t('landing.ask_placeholder')}
                className="flex-1 bg-transparent border-none outline-none text-text-primary placeholder:text-gray-400 py-3"
              />
              <Link to="/discover"><Button type="button" className="h-[48px] w-[48px] flex items-center justify-center p-0 ml-2 group/btn rounded-2xl">
                <ArrowRight className="w-5 h-5 group-hover/btn:translate-x-0.5 transition-transform" />
              </Button></Link>
            </div>
          </motion.div>
          
          <motion.div variants={itemVariants} className="flex flex-wrap gap-3 items-center mb-8">
            <span className="text-sm text-text-secondary mr-2">{t('landing.suggestions')}:</span>
            <button className="text-sm px-4 py-2 rounded-full bg-white border border-border hover:border-primary/30 hover:bg-orange-50 transition-colors shadow-sm">
              {t('workspace.prompt_germany')}
            </button>
            <button className="text-sm px-4 py-2 rounded-full bg-white border border-border hover:border-primary/30 hover:bg-orange-50 transition-colors shadow-sm">
              {t('workspace.prompt_mba')}
            </button>
            <button className="text-sm px-4 py-2 rounded-full bg-white border border-border hover:border-primary/30 hover:bg-orange-50 transition-colors shadow-sm">
              {t('workspace.prompt_loans')}
            </button>
          </motion.div>
          
          <motion.a variants={itemVariants} href="#demo" className="text-sm font-medium text-text-secondary hover:text-primary transition-colors flex items-center gap-1 w-fit">
            {t('landing.see_demo')} <ArrowRight className="w-3 h-3" />
          </motion.a>
        </motion.div>
        
        {/* Right Column (58%) */}
        <div className="col-span-12 lg:col-span-7 relative h-full min-h-[600px] hidden lg:block">
          <div className="absolute inset-0 bg-gradient-to-l from-transparent via-white/50 to-background z-10 pointer-events-none" />
          
          <motion.div 
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 1.2, ease: "easeOut" }}
            className="absolute inset-0 flex items-center justify-end"
          >
            <div className="relative w-[120%] h-[120%] -right-[10%] rounded-full bg-gradient-to-br from-blue-50 to-orange-50 overflow-hidden mix-blend-multiply opacity-80 filter blur-3xl"></div>
            <div className="absolute right-0 top-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-[url('https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=2564&auto=format&fit=crop')] bg-cover bg-center opacity-40 mix-blend-luminosity mask-image-gradient-left pointer-events-none" style={{ WebkitMaskImage: 'linear-gradient(to right, transparent, black 30%)' }} />
          </motion.div>

          {/* Floating Cards */}
          <motion.div 
            animate={{ y: [-10, 10, -10] }}
            transition={{ duration: 5, repeat: Infinity, ease: "easeInOut" }}
            className="absolute top-[20%] right-[60%] glass-panel rounded-2xl p-4 flex items-center gap-3 shadow-xl z-20"
          >
            <div className="w-10 h-10 rounded-full bg-orange-100 flex items-center justify-center text-primary">
              <GraduationCap className="w-5 h-5" />
            </div>
            <div>
              <div className="text-sm font-bold text-text-primary">{t('workspace.prompt_scholarships').replace('🎓 ', '')}</div>
              <div className="text-xs text-text-secondary">10,000+ matched</div>
            </div>
          </motion.div>

          <motion.div 
            animate={{ y: [15, -15, 15] }}
            transition={{ duration: 6, repeat: Infinity, ease: "easeInOut", delay: 1 }}
            className="absolute top-[50%] right-[20%] glass-panel rounded-2xl p-4 flex items-center gap-3 shadow-xl z-20"
          >
            <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center text-secondary">
              <Building2 className="w-5 h-5" />
            </div>
            <div>
              <div className="text-sm font-bold text-text-primary">{t('workspace.prompt_schemes').replace('🏛 ', '')}</div>
              <div className="text-xs text-text-secondary">Verified sources</div>
            </div>
          </motion.div>

          <motion.div 
            animate={{ y: [-12, 12, -12] }}
            transition={{ duration: 5.5, repeat: Infinity, ease: "easeInOut", delay: 2 }}
            className="absolute bottom-[20%] right-[45%] glass-panel rounded-2xl p-4 flex items-center gap-3 shadow-xl z-20"
          >
            <div className="w-10 h-10 rounded-full bg-emerald-100 flex items-center justify-center text-accent">
              <Globe2 className="w-5 h-5" />
            </div>
            <div>
              <div className="text-sm font-bold text-text-primary">{t('workspace.prompt_abroad').replace('🌍 ', '')}</div>
              <div className="text-xs text-text-secondary">Study abroad</div>
            </div>
          </motion.div>

        </div>
      </div>
    </section>
  );
};
