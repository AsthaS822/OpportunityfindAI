import { motion } from 'framer-motion';
import { ArrowRight, Search, Sparkles, GraduationCap, Building2, Globe2 } from 'lucide-react';
import { Link } from 'react-router-dom';

export const HeroSection = () => {
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
      {/* Background image with dark overlay and Ken Burns effect */}
      <div className="absolute inset-0 z-0">
        <motion.div
          className="absolute inset-0 bg-cover bg-center"
          style={{ backgroundImage: "url('/bg.jpg')" }}
          initial={{ scale: 1 }}
          animate={{ scale: 1.08 }}
          transition={{ duration: 12, ease: "easeOut", repeat: Infinity, repeatType: "mirror" }}
        />
        <div className="absolute inset-0 bg-black/50" />
        <div className="absolute inset-0 bg-gradient-to-r from-black/30 to-transparent" />
      </div>

      <div className="mx-auto w-full max-w-[1280px] px-6 md:px-8 grid grid-cols-12 gap-8 items-center relative z-10">
        
        {/* Left Column (42%) */}
        <motion.div 
          className="col-span-12 lg:col-span-5 z-10 flex flex-col justify-center"
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          <motion.div variants={itemVariants} className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-white/10 backdrop-blur-md border border-white/20 text-orange-300 text-sm font-medium mb-8 w-fit shadow-sm">
            <Sparkles className="w-4 h-4" />
            <span>AI-Powered Opportunity Discovery</span>
          </motion.div>
          
          <motion.h1 variants={itemVariants} className="text-[72px] leading-[1.05] font-bold font-heading text-white tracking-tight mb-6">
            Your Future<br/>
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-orange-300 to-orange-400">Starts Here</span>
          </motion.h1>
          
          <motion.p variants={itemVariants} className="text-[18px] text-white/80 leading-relaxed mb-10 max-w-[480px]">
            Discover scholarships, fellowships, government schemes, education loans, and career opportunities tailored to your profile using AI-powered analysis.
          </motion.p>
          
          <motion.div variants={itemVariants} className="relative group max-w-[500px] mb-6">
            <div className="absolute inset-0 bg-primary/30 rounded-[24px] blur-xl opacity-0 group-focus-within:opacity-100 transition-opacity duration-500" />
            <Link to="/discover" className="relative rounded-[24px] p-2 flex items-center shadow-lg border border-white/30 bg-white/10 backdrop-blur-xl">
              <div className="pl-4 pr-2 text-white/50">
                <Search className="w-5 h-5" />
              </div>
              <span className="flex-1 text-white/40 py-3 text-[15px]">Ask anything about your education, career, funding, or study abroad...</span>
              <button type="button" className="h-[48px] w-[48px] flex items-center justify-center p-0 ml-2 group/btn rounded-2xl bg-gradient-to-r from-[#FF7A00] to-[#FF9A3D] text-white">
                <ArrowRight className="w-5 h-5 group-hover/btn:translate-x-0.5 transition-transform" />
              </button>
            </Link>
          </motion.div>
          
          <motion.div variants={itemVariants} className="space-y-3 mb-8">
            <p className="text-sm text-white/50 font-medium">Try asking...</p>
            <div className="flex flex-wrap gap-2">
              <Link to="/discover" className="text-[13px] px-4 py-2 rounded-full bg-white/10 backdrop-blur-md text-white/80 border border-white/20 hover:bg-white/20 hover:border-orange-400/50 transition-colors">
                "I completed MCA. What should I do next?"
              </Link>
              <Link to="/discover" className="text-[13px] px-4 py-2 rounded-full bg-white/10 backdrop-blur-md text-white/80 border border-white/20 hover:bg-white/20 hover:border-orange-400/50 transition-colors">
                "Can I study in Germany without IELTS?"
              </Link>
              <Link to="/discover" className="text-[13px] px-4 py-2 rounded-full bg-white/10 backdrop-blur-md text-white/80 border border-white/20 hover:bg-white/20 hover:border-orange-400/50 transition-colors">
                "Which scholarships fit my profile?"
              </Link>
              <Link to="/discover" className="text-[13px] px-4 py-2 rounded-full bg-white/10 backdrop-blur-md text-white/80 border border-white/20 hover:bg-white/20 hover:border-orange-400/50 transition-colors">
                "What careers are best after BCA?"
              </Link>
              <Link to="/discover" className="text-[13px] px-4 py-2 rounded-full bg-white/10 backdrop-blur-md text-white/80 border border-white/20 hover:bg-white/20 hover:border-orange-400/50 transition-colors">
                "What government schemes can help me?"
              </Link>
            </div>
          </motion.div>
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
            <div className="relative w-[120%] h-[120%] -right-[10%] rounded-full bg-gradient-to-br from-blue-900/30 to-orange-900/30 overflow-hidden mix-blend-screen opacity-60 filter blur-3xl"></div>
            <div className="absolute right-0 top-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-[url('https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=2564&auto=format&fit=crop')] bg-cover bg-center opacity-20 mix-blend-luminosity mask-image-gradient-left pointer-events-none" style={{ WebkitMaskImage: 'linear-gradient(to right, transparent, black 30%)' }} />
          </motion.div>

          {/* Floating Cards */}
          <motion.div 
            animate={{ y: [-10, 10, -10] }}
            transition={{ duration: 5, repeat: Infinity, ease: "easeInOut" }}
            className="absolute top-[20%] right-[60%] rounded-2xl p-4 flex items-center gap-3 shadow-xl z-20 bg-white/10 backdrop-blur-xl border border-white/20"
          >
            <div className="w-10 h-10 rounded-full bg-orange-500/30 flex items-center justify-center text-orange-300">
              <GraduationCap className="w-5 h-5" />
            </div>
            <div>
              <div className="text-sm font-bold text-white">Scholarships</div>
              <div className="text-xs text-white/60">10,000+ matched</div>
            </div>
          </motion.div>

          <motion.div 
            animate={{ y: [15, -15, 15] }}
            transition={{ duration: 6, repeat: Infinity, ease: "easeInOut", delay: 1 }}
            className="absolute top-[50%] right-[20%] rounded-2xl p-4 flex items-center gap-3 shadow-xl z-20 bg-white/10 backdrop-blur-xl border border-white/20"
          >
            <div className="w-10 h-10 rounded-full bg-blue-500/30 flex items-center justify-center text-blue-300">
              <Building2 className="w-5 h-5" />
            </div>
            <div>
              <div className="text-sm font-bold text-white">Government Schemes</div>
              <div className="text-xs text-white/60">Verified sources</div>
            </div>
          </motion.div>

          <motion.div 
            animate={{ y: [-12, 12, -12] }}
            transition={{ duration: 5.5, repeat: Infinity, ease: "easeInOut", delay: 2 }}
            className="absolute bottom-[20%] right-[45%] rounded-2xl p-4 flex items-center gap-3 shadow-xl z-20 bg-white/10 backdrop-blur-xl border border-white/20"
          >
            <div className="w-10 h-10 rounded-full bg-emerald-500/30 flex items-center justify-center text-emerald-300">
              <Globe2 className="w-5 h-5" />
            </div>
            <div>
              <div className="text-sm font-bold text-white">Study Abroad</div>
              <div className="text-xs text-white/60">Explore destinations</div>
            </div>
          </motion.div>

        </div>
      </div>
    </section>
  );
};
