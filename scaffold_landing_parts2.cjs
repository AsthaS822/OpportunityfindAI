const fs = require('fs');
const path = require('path');

const srcDir = path.join(__dirname, 'src');

const files = {
  'components/landing/TrustedSources.tsx': `import { Container } from '../layout/Container';

export const TrustedSources = () => {
  const sources = [
    { name: 'NSP', color: 'text-orange-600' },
    { name: 'myScheme', color: 'text-blue-600' },
    { name: 'UGC', color: 'text-indigo-600' },
    { name: 'AICTE', color: 'text-emerald-600' },
    { name: 'Fulbright', color: 'text-red-600' },
    { name: 'DAAD', color: 'text-sky-600' },
    { name: 'Chevening', color: 'text-purple-600' },
    { name: 'MEXT', color: 'text-rose-600' },
    { name: 'Vidya Lakshmi', color: 'text-amber-600' },
    { name: 'Erasmus+', color: 'text-cyan-600' },
  ];

  return (
    <section className="py-[140px] border-y border-gray-50 bg-white overflow-hidden">
      <Container>
        <div className="text-center mb-12">
          <p className="text-sm font-medium text-text-secondary uppercase tracking-widest">
            Powered by verified sources
          </p>
        </div>
      </Container>
      
      <div className="relative w-full group">
        <div className="absolute left-0 top-0 bottom-0 w-32 bg-gradient-to-r from-white to-transparent z-10" />
        <div className="absolute right-0 top-0 bottom-0 w-32 bg-gradient-to-l from-white to-transparent z-10" />
        
        <div className="flex animate-marquee group-hover:[animation-play-state:paused] w-[200%]">
          {/* First set */}
          <div className="flex flex-1 justify-around items-center">
            {sources.map((source, i) => (
              <div 
                key={i} 
                className={\`text-xl md:text-2xl font-bold font-heading text-gray-300 hover:\${source.color} hover:scale-110 hover:shadow-glow transition-all duration-300 cursor-default px-8\`}
              >
                {source.name}
              </div>
            ))}
          </div>
          {/* Duplicated set for seamless loop */}
          <div className="flex flex-1 justify-around items-center">
            {sources.map((source, i) => (
              <div 
                key={i + sources.length} 
                className={\`text-xl md:text-2xl font-bold font-heading text-gray-300 hover:\${source.color} hover:scale-110 hover:shadow-glow transition-all duration-300 cursor-default px-8\`}
              >
                {source.name}
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};
`,
  'components/landing/OpportunityCategories.tsx': `import { Container } from '../layout/Container';
import { Section } from '../layout/Section';
import { GraduationCap, Landmark, Banknote, Globe2, Lightbulb, Trophy, Briefcase, Rocket } from 'lucide-react';

export const OpportunityCategories = () => {
  const categories = [
    { icon: <GraduationCap />, name: 'Scholarships', bg: 'bg-orange-50', color: 'text-primary' },
    { icon: <Landmark />, name: 'Government Schemes', bg: 'bg-blue-50', color: 'text-secondary' },
    { icon: <Banknote />, name: 'Education Loans', bg: 'bg-emerald-50', color: 'text-accent' },
    { icon: <Globe2 />, name: 'Study Abroad', bg: 'bg-sky-50', color: 'text-sky-600' },
    { icon: <Lightbulb />, name: 'Research Grants', bg: 'bg-purple-50', color: 'text-purple-600' },
    { icon: <Briefcase />, name: 'Internships', bg: 'bg-rose-50', color: 'text-rose-600' },
    { icon: <Trophy />, name: 'Competitions', bg: 'bg-amber-50', color: 'text-amber-600' },
    { icon: <Rocket />, name: 'Startup Grants', bg: 'bg-indigo-50', color: 'text-indigo-600' },
  ];

  return (
    <Section id="opportunities" className="bg-[#F7F9FC]">
      <Container>
        <div className="text-center max-w-[620px] mx-auto mb-16">
          <h2 className="text-4xl md:text-[48px] font-heading font-bold text-text-primary mb-6 tracking-tight">
            Everything you need. <br />In one place.
          </h2>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 md:gap-8">
          {categories.map((cat, i) => (
            <div 
              key={i}
              className="bg-white rounded-[24px] p-6 flex flex-col items-center justify-center text-center cursor-pointer border border-transparent hover:border-gray-100 hover:shadow-[0_12px_40px_rgb(0,0,0,0.06)] hover:-translate-y-2 transition-all duration-300 group"
            >
              <div className={\`w-14 h-14 rounded-2xl \${cat.bg} \${cat.color} flex items-center justify-center mb-4 group-hover:scale-110 transition-transform\`}>
                {cat.icon}
              </div>
              <h3 className="font-heading font-semibold text-text-primary text-lg">
                {cat.name}
              </h3>
            </div>
          ))}
        </div>
      </Container>
    </Section>
  );
};
`,
  'components/landing/FinalCTA.tsx': `import { Container } from '../layout/Container';
import { Section } from '../layout/Section';
import { Button } from '../ui/Button';
import { ArrowRight } from 'lucide-react';

export const FinalCTA = () => {
  return (
    <Section className="bg-white">
      <Container>
        <div className="bg-[#FFF8F3] rounded-[48px] px-6 py-24 text-center max-w-[1000px] mx-auto border border-orange-50 relative overflow-hidden">
          {/* Subtle decoration */}
          <div className="absolute top-0 right-0 w-64 h-64 bg-white rounded-full opacity-40 blur-[80px]" />
          <div className="absolute bottom-0 left-0 w-64 h-64 bg-primary/10 rounded-full blur-[80px]" />
          
          <div className="relative z-10">
            <h2 className="text-4xl md:text-[56px] font-heading font-bold text-text-primary mb-6 tracking-tight">
              Ready to find your <br className="hidden md:block"/> next opportunity?
            </h2>
            <p className="text-[18px] text-text-secondary max-w-[500px] mx-auto mb-10">
              Join thousands of students and professionals using AI to unlock their future.
            </p>
            <Button className="h-[56px] px-10 text-lg shadow-lg shadow-primary/20 hover:shadow-primary/30 group">
              Start Exploring 
              <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
            </Button>
          </div>
        </div>
      </Container>
    </Section>
  );
};
`,
  'pages/Home.tsx': `import { BackgroundSystem } from '../components/landing/BackgroundSystem';
import { HeroSection } from '../components/landing/HeroSection';
import { FeatureStrip } from '../components/landing/FeatureStrip';
import { InteractiveDemo } from '../components/landing/InteractiveDemo';
import { TrustedSources } from '../components/landing/TrustedSources';
import { OpportunityCategories } from '../components/landing/OpportunityCategories';
import { FinalCTA } from '../components/landing/FinalCTA';
import { PageTransition } from '../components/motion/PageTransition';

export const Home = () => {
  return (
    <PageTransition>
      <div className="relative w-full">
        <BackgroundSystem />
        <HeroSection />
        <FeatureStrip />
        <InteractiveDemo />
        <TrustedSources />
        <OpportunityCategories />
        <FinalCTA />
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
console.log("Scaffolded landing parts 2");
