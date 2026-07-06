import { Container } from '../layout/Container';
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
              <div className={`w-14 h-14 rounded-2xl ${cat.bg} ${cat.color} flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}>
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
