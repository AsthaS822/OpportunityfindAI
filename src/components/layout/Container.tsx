import type { ReactNode } from 'react';

interface ContainerProps {
  children: ReactNode;
  className?: string;
  /** Override max-width (default is max-w-[1280px]) */
  maxWidth?: string;
}

export const Container = ({ children, className = '', maxWidth = 'max-w-[1280px]' }: ContainerProps) => (
  <div className={`mx-auto w-full ${maxWidth} px-6 md:px-8 ${className}`}>
    {children}
  </div>
);
