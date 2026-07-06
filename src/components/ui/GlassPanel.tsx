import type { ReactNode } from 'react';

export const GlassPanel = ({ children, className = '' }: { children: ReactNode, className?: string }) => (
  <div className={`glass-panel rounded-[24px] ${className}`}>
    {children}
  </div>
);
