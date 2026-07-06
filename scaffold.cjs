const fs = require('fs');
const path = require('path');

const srcDir = path.join(__dirname, 'src');

const files = {
  'styles/index.css': `@import "tailwindcss";
@import "tw-animate-css";

@theme inline {
  /* Colors */
  --color-primary: #F97316;
  --color-secondary: #2563EB;
  --color-accent: #10B981;
  
  --color-background: #FFFFFF;
  --color-background-alt-1: #FFF8F3;
  --color-background-alt-2: #F7F9FC;
  
  --color-border: #EAEAEA;
  --color-text-primary: #111827;
  --color-text-secondary: #6B7280;

  /* Typography */
  --font-heading: "Plus Jakarta Sans", sans-serif;
  --font-body: "Inter", sans-serif;

  /* Spacing */
  --spacing-section: 120px;
  --spacing-section-lg: 140px;
  --spacing-card-p: 28px;
  --spacing-card-p-lg: 36px;
  --spacing-gap: 24px;
  --spacing-gap-lg: 32px;
  --container-max-w: 1280px;

  /* Radius */
  --radius-card: 24px;
}

@layer base {
  body {
    @apply font-body bg-background text-text-primary antialiased;
  }
  h1, h2, h3, h4, h5, h6 {
    @apply font-heading tracking-tight;
  }
}

@layer utilities {
  .glass-panel {
    @apply bg-white/70 backdrop-blur-[16px] border border-white/40;
  }
  .card-shadow {
    @apply shadow-[0_8px_30px_rgb(0,0,0,0.04)];
  }
}
`,
  'translations/en.json': `{
  "welcome": "Welcome to OpportunityOS AI",
  "start": "Start Exploring",
  "analyze": "Analyze"
}`,
  'translations/hi.json': `{
  "welcome": "OpportunityOS AI में आपका स्वागत है",
  "start": "खोजना शुरू करें",
  "analyze": "विश्लेषण करें"
}`,
  'contexts/LanguageContext.tsx': `import React, { createContext, useContext, useState, ReactNode } from 'react';
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
import { motion } from 'framer-motion';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost';
  children: React.ReactNode;
}

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
    
    return (
      <motion.button 
        ref={ref}
        className={\`\${baseClass} \${variantClass} \${className}\`}
        whileTap={{ scale: 0.98 }}
        {...props}
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
  'components/ui/Badge.tsx': `import React from 'react';

export const Badge = ({ children, className = '' }: { children: React.ReactNode, className?: string }) => (
  <span className={\`inline-flex items-center rounded-full bg-primary/10 px-3 py-1 text-sm font-medium text-primary \${className}\`}>
    {children}
  </span>
);
`,
  'components/ui/GlassPanel.tsx': `import React from 'react';

export const GlassPanel = ({ children, className = '' }: { children: React.ReactNode, className?: string }) => (
  <div className={\`glass-panel rounded-[24px] \${className}\`}>
    {children}
  </div>
);
`,
  'components/layout/Container.tsx': `import React from 'react';

export const Container = ({ children, className = '' }: { children: React.ReactNode, className?: string }) => (
  <div className={\`mx-auto w-full max-w-[1280px] px-6 md:px-8 \${className}\`}>
    {children}
  </div>
);
`,
  'components/layout/Section.tsx': `import React from 'react';

export const Section = ({ children, className = '', id }: { children: React.ReactNode, className?: string, id?: string }) => (
  <section id={id} className={\`py-[120px] md:py-[140px] \${className}\`}>
    {children}
  </section>
);
`,
  'components/layout/Navbar.tsx': `import React from 'react';
import { GlassPanel } from '../ui/GlassPanel';
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
  'components/layout/Footer.tsx': `import React from 'react';
import { Container } from './Container';

export const Footer = () => (
  <footer className="border-t border-border bg-background py-12 text-center text-text-secondary">
    <Container>
      <p>&copy; {new Date().getFullYear()} OpportunityOS AI. All rights reserved.</p>
    </Container>
  </footer>
);
`,
  'components/motion/LoadingSkeleton.tsx': `import React from 'react';
import { motion } from 'framer-motion';

export const LoadingSkeleton = ({ className = '' }: { className?: string }) => (
  <motion.div
    className={\`bg-gray-200 rounded-xl \${className}\`}
    animate={{ opacity: [0.5, 1, 0.5] }}
    transition={{ duration: 1.5, repeat: Infinity, ease: "easeInOut" }}
  />
);
`,
  'components/motion/PageTransition.tsx': `import React from 'react';
import { motion } from 'framer-motion';

export const PageTransition = ({ children }: { children: React.ReactNode }) => (
  <motion.div
    initial={{ opacity: 0, y: 10 }}
    animate={{ opacity: 1, y: 0 }}
    exit={{ opacity: 0, y: -10 }}
    transition={{ duration: 0.3, ease: 'easeOut' }}
  >
    {children}
  </motion.div>
);
`,
  'App.tsx': `import React from 'react';
import { BrowserRouter, Routes, Route, Outlet } from 'react-router-dom';
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
  'main.tsx': `import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';
import './styles/index.css';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>
);
`
};

for (const [relPath, content] of Object.entries(files)) {
  const fullPath = path.join(srcDir, relPath);
  const dir = path.dirname(fullPath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  fs.writeFileSync(fullPath, content);
}
console.log("Done scaffolding files.");
