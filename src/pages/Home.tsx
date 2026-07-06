import { BackgroundSystem } from '../components/landing/BackgroundSystem';
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
