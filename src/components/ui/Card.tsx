import React from 'react';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
}

export const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className = '', children, ...props }, ref) => {
    return (
      <div 
        ref={ref}
        className={`bg-white rounded-[24px] p-[28px] md:p-[36px] border border-[#f3f4f6] card-shadow hover:-translate-y-1 transition-transform duration-300 ${className}`}
        {...props}
      >
        {children}
      </div>
    );
  }
);
Card.displayName = 'Card';
