import React from 'react';
import { motion } from 'framer-motion';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost';
  children: React.ReactNode;
}

// Framer motion's button type can conflict with React's button type sometimes,
// so we cast or omit conflicting properties.
export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ variant = 'primary', className = '', children, ...props }, ref) => {
    const baseClass = "inline-flex items-center justify-center rounded-full font-medium transition-all duration-300 h-[52px] px-8";
    
    let variantClass = "";
    if (variant === 'primary') {
      variantClass = "bg-gradient-to-r from-primary to-[#fb923c] text-white hover:scale-[1.02] shadow-md hover:shadow-lg";
    } else if (variant === 'secondary') {
      variantClass = "bg-white text-text-primary border border-border hover:bg-gray-50 hover:scale-[1.02]";
    } else {
      variantClass = "bg-transparent text-text-secondary hover:text-text-primary";
    }
    
    // Omit event handlers that conflict between react and motion
    const motionProps: any = { ...props, ref };
    
    return (
      <motion.button 
        className={`${baseClass} ${variantClass} ${className}`}
        whileTap={{ scale: 0.98 }}
        {...motionProps}
      >
        {children}
      </motion.button>
    );
  }
);
Button.displayName = 'Button';
