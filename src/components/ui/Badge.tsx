import type { ReactNode } from 'react';

export const Badge = ({ children, className = '' }: { children: ReactNode, className?: string }) => (
  <span className={`inline-flex items-center rounded-full bg-primary/10 px-3 py-1 text-sm font-medium text-primary ${className}`}>
    {children}
  </span>
);
