import { Container } from '../layout/Container';

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
                className={`text-xl md:text-2xl font-bold font-heading text-gray-300 hover:${source.color} hover:scale-110 hover:shadow-glow transition-all duration-300 cursor-default px-8`}
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
                className={`text-xl md:text-2xl font-bold font-heading text-gray-300 hover:${source.color} hover:scale-110 hover:shadow-glow transition-all duration-300 cursor-default px-8`}
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
