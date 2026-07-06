const fs = require('fs');
const path = require('path');

const srcDir = path.join(__dirname, 'src');
const componentsDir = path.join(srcDir, 'components', 'landing');

if (!fs.existsSync(componentsDir)) {
  fs.mkdirSync(componentsDir, { recursive: true });
}

const files = {
  'utils/cn.ts': `import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
`,
  'components/layout/Navbar.tsx': `import { useState, useEffect } from 'react';
import { Container } from './Container';
import { Button } from '../ui/Button';
import { GlassPanel } from '../ui/GlassPanel';
import { useTranslation } from '../../contexts/LanguageContext';
import { motion } from 'framer-motion';

export const Navbar = () => {
  const [scrolled, setScrolled] = useState(false);
  const { language, setLanguage, t } = useTranslation();

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <header className={\`fixed top-0 left-0 right-0 z-50 transition-all duration-300 \${scrolled ? 'py-4' : 'py-6'}\`}>
      <Container>
        <GlassPanel className={\`flex items-center justify-between px-6 transition-all duration-300 \${scrolled ? 'h-[70px] bg-white/80 backdrop-blur-2xl' : 'h-[80px] bg-white/40 backdrop-blur-md'}\`}>
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-primary to-orange-400 flex items-center justify-center text-white font-bold text-xl">
              O
            </div>
            <span className="font-heading text-xl font-bold tracking-tight">OpportunityOS</span>
          </div>
          
          <nav className="hidden md:flex items-center gap-8 text-[15px] font-medium text-text-secondary">
            <a href="#how-it-works" className="hover:text-primary transition-colors">How it Works</a>
            <a href="#features" className="hover:text-primary transition-colors">Features</a>
            <a href="#opportunities" className="hover:text-primary transition-colors">Opportunities</a>
            <a href="#about" className="hover:text-primary transition-colors">About</a>
          </nav>
          
          <div className="flex items-center gap-4">
            <button 
              onClick={() => setLanguage(language === 'en' ? 'hi' : 'en')}
              className="text-sm font-medium px-3 py-1.5 rounded-full hover:bg-gray-100 transition-colors"
            >
              {language === 'en' ? 'हिन्दी' : 'English'}
            </button>
            <Button className="h-[44px] px-6 text-[15px]">{t('start')}</Button>
          </div>
        </GlassPanel>
      </Container>
    </header>
  );
};
`,
  'components/landing/BackgroundSystem.tsx': `import { motion } from 'framer-motion';

export const BackgroundSystem = () => {
  return (
    <div className="fixed inset-0 z-[-1] overflow-hidden pointer-events-none opacity-40">
      {/* Soft mesh gradient base */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top_left,_var(--tw-gradient-stops))] from-orange-50/40 via-white to-blue-50/30" />
      
      {/* Light Blobs */}
      <motion.div 
        animate={{
          x: [0, 100, -50, 0],
          y: [0, -50, 100, 0],
        }}
        transition={{ duration: 30, repeat: Infinity, ease: "linear" }}
        className="absolute top-[10%] left-[20%] w-[600px] h-[600px] bg-primary/5 rounded-full blur-[100px]"
      />
      <motion.div 
        animate={{
          x: [0, -100, 50, 0],
          y: [0, 100, -50, 0],
        }}
        transition={{ duration: 25, repeat: Infinity, ease: "linear" }}
        className="absolute top-[40%] right-[10%] w-[500px] h-[500px] bg-secondary/5 rounded-full blur-[100px]"
      />
      <motion.div 
        animate={{
          x: [0, 50, -100, 0],
          y: [0, 50, -50, 0],
        }}
        transition={{ duration: 35, repeat: Infinity, ease: "linear" }}
        className="absolute bottom-[10%] left-[30%] w-[700px] h-[700px] bg-accent/5 rounded-full blur-[120px]"
      />
      
      {/* Subtle Noise Texture */}
      <div 
        className="absolute inset-0 opacity-[0.015] mix-blend-overlay"
        style={{ backgroundImage: 'url("data:image/svg+xml,%3Csvg viewBox=%220 0 200 200%22 xmlns=%22http://www.w3.org/2000/svg%22%3E%3Cfilter id=%22noiseFilter%22%3E%3CfeTurbulence type=%22fractalNoise%22 baseFrequency=%220.65%22 numOctaves=%223%22 stitchTiles=%22stitch%22/%3E%3C/filter%3E%3Crect width=%22100%25%22 height=%22100%25%22 filter=%22url(%23noiseFilter)%22/%3E%3C/svg%3E")' }}
      />
    </div>
  );
};
`,
  'components/landing/HeroSection.tsx': `import { motion } from 'framer-motion';
import { ArrowRight, Search, Sparkles, GraduationCap, Building2, Globe2 } from 'lucide-react';
import { Button } from '../ui/Button';

export const HeroSection = () => {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.15, delayChildren: 0.1 }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.6, ease: [0.22, 1, 0.36, 1] } }
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
            <span>Discover every opportunity</span>
          </motion.div>
          
          <motion.h1 variants={itemVariants} className="text-[72px] leading-[1.05] font-bold font-heading text-text-primary tracking-tight mb-6">
            One AI.<br/>
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-primary to-orange-400">
              Every Opportunity.
            </span>
          </motion.h1>
          
          <motion.p variants={itemVariants} className="text-[18px] text-text-secondary leading-relaxed mb-10 max-w-[480px]">
            Scholarships, government schemes, education loans, and fellowships — discovered, matched, and explained by AI in seconds.
          </motion.p>
          
          <motion.div variants={itemVariants} className="relative group max-w-[500px] mb-6">
            <div className="absolute inset-0 bg-primary/20 rounded-[24px] blur-xl opacity-0 group-focus-within:opacity-100 transition-opacity duration-500" />
            <div className="relative glass-panel rounded-[24px] p-2 flex items-center shadow-lg border border-white/60 bg-white/70">
              <div className="pl-4 pr-2 text-gray-400">
                <Search className="w-5 h-5" />
              </div>
              <input 
                type="text"
                placeholder="Ask OpportunityOS AI..."
                className="flex-1 bg-transparent border-none outline-none text-text-primary placeholder:text-gray-400 py-3"
              />
              <Button className="h-[48px] px-6 ml-2 group/btn">
                Analyze
                <ArrowRight className="w-4 h-4 ml-2 group-hover/btn:translate-x-1 transition-transform" />
              </Button>
            </div>
          </motion.div>
          
          <motion.div variants={itemVariants} className="flex flex-wrap gap-3 items-center mb-8">
            <span className="text-sm text-text-secondary mr-2">Suggestions:</span>
            <button className="text-sm px-4 py-2 rounded-full bg-white border border-border hover:border-primary/30 hover:bg-orange-50 transition-colors shadow-sm">
              Study in Germany
            </button>
            <button className="text-sm px-4 py-2 rounded-full bg-white border border-border hover:border-primary/30 hover:bg-orange-50 transition-colors shadow-sm">
              MBA Scholarships
            </button>
            <button className="text-sm px-4 py-2 rounded-full bg-white border border-border hover:border-primary/30 hover:bg-orange-50 transition-colors shadow-sm">
              Education Loan
            </button>
          </motion.div>
          
          <motion.a variants={itemVariants} href="#demo" className="text-sm font-medium text-text-secondary hover:text-primary transition-colors flex items-center gap-1 w-fit">
            See Demo <ArrowRight className="w-3 h-3" />
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
            {/* The user mentioned an uploaded underwater illustration. We'll simulate a beautiful placeholder for it */}
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
              <div className="text-sm font-bold text-text-primary">Scholarships</div>
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
              <div className="text-sm font-bold text-text-primary">Govt Schemes</div>
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
              <div className="text-sm font-bold text-text-primary">Global Programs</div>
              <div className="text-xs text-text-secondary">Study abroad</div>
            </div>
          </motion.div>

        </div>
      </div>
    </section>
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
console.log("Scaffolded hero and utils.");
