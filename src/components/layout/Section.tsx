import type { ReactNode } from 'react';

export const Section = ({ children, className = '', id }: { children: ReactNode, className?: string, id?: string }) => (
  <section id={id} className={`py-[120px] md:py-[140px] ${className}`}>
    {children}
  </section>
);
