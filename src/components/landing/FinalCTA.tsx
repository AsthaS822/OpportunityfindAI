import { Container } from '../layout/Container';
import { Section } from '../layout/Section';
import { Button } from '../ui/Button';
import { ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';

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
            <Link to="/discover"><Button className="h-[56px] px-10 text-lg shadow-lg shadow-primary/20 hover:shadow-primary/30 group">
              Start Exploring 
              <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
            </Button></Link>
          </div>
        </div>
      </Container>
    </Section>
  );
};
