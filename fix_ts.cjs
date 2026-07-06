const fs = require('fs');
const path = require('path');

const srcDir = path.join(__dirname, 'src');

const files = {
  'App.tsx': `import { BrowserRouter, Routes, Route, Outlet } from 'react-router-dom';
import { TranslationProvider } from './contexts/LanguageContext';
import { Navbar } from './components/layout/Navbar';
import { Footer } from './components/layout/Footer';
import { PageTransition } from './components/motion/PageTransition';
import { Container } from './components/layout/Container';

const Layout = () => (
  <div className="min-h-screen flex flex-col pt-24">
    <Navbar />
    <main className="flex-1">
      <Outlet />
    </main>
    <Footer />
  </div>
);

const PlaceholderPage = ({ title }: { title: string }) => (
  <PageTransition>
    <Container className="py-20 text-center">
      <h1 className="text-4xl font-heading font-bold">{title}</h1>
      <p className="mt-4 text-text-secondary">This page has not been built yet.</p>
    </Container>
  </PageTransition>
);

export default function App() {
  return (
    <TranslationProvider>
      <BrowserRouter>
        <Routes>
          <Route element={<Layout />}>
            <Route path="/" element={<PlaceholderPage title="Home (Placeholder)" />} />
            <Route path="/discover" element={<PlaceholderPage title="Discover" />} />
            <Route path="/report" element={<PlaceholderPage title="Report" />} />
            <Route path="/opportunity/:id" element={<PlaceholderPage title="Opportunity Detail" />} />
            <Route path="/compare" element={<PlaceholderPage title="Compare" />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </TranslationProvider>
  );
}
`,
  'components/layout/Footer.tsx': `import { Container } from './Container';

export const Footer = () => (
  <footer className="border-t border-border bg-background py-12 text-center text-text-secondary">
    <Container>
      <p>&copy; {new Date().getFullYear()} OpportunityOS AI. All rights reserved.</p>
    </Container>
  </footer>
);
`,
  'components/layout/Navbar.tsx': `import { GlassPanel } from '../ui/GlassPanel';
import { Container } from './Container';

export const Navbar = () => (
  <header className="fixed top-4 left-0 right-0 z-50">
    <Container>
      <GlassPanel className="flex h-16 items-center justify-between px-6">
        <div className="font-heading text-xl font-bold">OpportunityOS AI</div>
        <nav>
          {/* Navigation items will go here */}
        </nav>
      </GlassPanel>
    </Container>
  </header>
);
`,
  'components/motion/LoadingSkeleton.tsx': `import { motion } from 'framer-motion';

export const LoadingSkeleton = ({ className = '' }: { className?: string }) => (
  <motion.div
    className={\`bg-gray-200 rounded-xl \${className}\`}
    animate={{ opacity: [0.5, 1, 0.5] }}
    transition={{ duration: 1.5, repeat: Infinity, ease: "easeInOut" }}
  />
);
`,
  'contexts/LanguageContext.tsx': `import { createContext, useContext, useState } from 'react';
import type { ReactNode } from 'react';
import en from '../translations/en.json';
import hi from '../translations/hi.json';

type Language = 'en' | 'hi';
type Translations = typeof en;

interface LanguageContextType {
  language: Language;
  setLanguage: (lang: Language) => void;
  t: (key: keyof Translations) => string;
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export const TranslationProvider = ({ children }: { children: ReactNode }) => {
  const [language, setLanguage] = useState<Language>('en');
  
  const translations = language === 'en' ? en : hi;
  
  const t = (key: keyof Translations) => {
    return translations[key] || key;
  };

  return (
    <LanguageContext.Provider value={{ language, setLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useTranslation = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useTranslation must be used within a TranslationProvider');
  }
  return context;
};
`,
  'components/ui/Button.tsx': `import React from 'react';
import { motion, HTMLMotionProps } from 'framer-motion';

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
        className={\`\${baseClass} \${variantClass} \${className}\`}
        whileTap={{ scale: 0.98 }}
        {...motionProps}
      >
        {children}
      </motion.button>
    );
  }
);
Button.displayName = 'Button';
`,
  'components/ui/Card.tsx': `import React from 'react';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
}

export const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className = '', children, ...props }, ref) => {
    return (
      <div 
        ref={ref}
        className={\`bg-white rounded-[24px] p-[28px] md:p-[36px] border border-[#f3f4f6] card-shadow hover:-translate-y-1 transition-transform duration-300 \${className}\`}
        {...props}
      >
        {children}
      </div>
    );
  }
);
Card.displayName = 'Card';
`,
  'components/ui/Input.tsx': `import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className = '', ...props }, ref) => {
    return (
      <input
        ref={ref}
        className={\`h-[52px] w-full rounded-2xl border border-border bg-white px-4 text-text-primary focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all \${className}\`}
        {...props}
      />
    );
  }
);
Input.displayName = 'Input';
`,
  'components/ui/Badge.tsx': `import type { ReactNode } from 'react';

export const Badge = ({ children, className = '' }: { children: ReactNode, className?: string }) => (
  <span className={\`inline-flex items-center rounded-full bg-primary/10 px-3 py-1 text-sm font-medium text-primary \${className}\`}>
    {children}
  </span>
);
`,
  'components/ui/GlassPanel.tsx': `import type { ReactNode } from 'react';

export const GlassPanel = ({ children, className = '' }: { children: ReactNode, className?: string }) => (
  <div className={\`glass-panel rounded-[24px] \${className}\`}>
    {children}
  </div>
);
`,
  'components/layout/Container.tsx': `import type { ReactNode } from 'react';

export const Container = ({ children, className = '' }: { children: ReactNode, className?: string }) => (
  <div className={\`mx-auto w-full max-w-[1280px] px-6 md:px-8 \${className}\`}>
    {children}
  </div>
);
`,
  'components/layout/Section.tsx': `import type { ReactNode } from 'react';

export const Section = ({ children, className = '', id }: { children: ReactNode, className?: string, id?: string }) => (
  <section id={id} className={\`py-[120px] md:py-[140px] \${className}\`}>
    {children}
  </section>
);
`,
  'components/motion/PageTransition.tsx': `import type { ReactNode } from 'react';
import { motion } from 'framer-motion';

export const PageTransition = ({ children }: { children: ReactNode }) => (
  <motion.div
    initial={{ opacity: 0, y: 10 }}
    animate={{ opacity: 1, y: 0 }}
    exit={{ opacity: 0, y: -10 }}
    transition={{ duration: 0.3, ease: 'easeOut' }}
  >
    {children}
  </motion.div>
);
`
};

for (const [relPath, content] of Object.entries(files)) {
  const fullPath = path.join(srcDir, relPath);
  fs.writeFileSync(fullPath, content);
}
console.log("Fixes applied.");
