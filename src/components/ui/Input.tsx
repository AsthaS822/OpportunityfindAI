import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className = '', ...props }, ref) => {
    return (
      <input
        ref={ref}
        className={`h-[52px] w-full rounded-2xl border border-border bg-white px-4 text-text-primary focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all ${className}`}
        {...props}
      />
    );
  }
);
Input.displayName = 'Input';
