import { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Container } from './Container';
import { Button } from '../ui/Button';
import { GlassPanel } from '../ui/GlassPanel';
import { useTranslation } from 'react-i18next';

export const Navbar = () => {
  const [scrolled, setScrolled] = useState(false);
  const { t, i18n } = useTranslation();
  const location = useLocation();

  const isWorkspace = location.pathname.startsWith('/discover');

  useEffect(() => {
    const fn = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', fn);
    return () => window.removeEventListener('scroll', fn);
  }, []);


  return (
    <header className="fixed top-0 left-0 right-0 z-[100] h-[80px] flex items-center">
      <Container className={isWorkspace ? 'max-w-full px-6' : undefined}>
        <GlassPanel
          className={`flex items-center justify-between px-6 h-[64px] transition-all duration-300 ${
            scrolled ? 'bg-white/90 backdrop-blur-2xl shadow-sm' : 'bg-white/60 backdrop-blur-md'
          }`}
        >
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2 flex-shrink-0">
            <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-primary to-orange-400 flex items-center justify-center text-white font-bold text-sm">
              O
            </div>
            <span className="font-heading text-lg font-bold tracking-tight text-text-primary">OpportunityOS</span>
          </Link>

          {/* Right actions */}
          <div className="flex items-center gap-6">
            {!isWorkspace && (
              <a href="#about" className="hidden md:block text-[15px] font-medium text-text-secondary hover:text-primary transition-colors">
                {t('landing.nav_about')}
              </a>
            )}
            
            <div className="text-[14px] font-medium text-text-secondary flex gap-2">
              <button 
                onClick={() => i18n.changeLanguage('en')}
                className={`hover:text-primary transition-colors ${i18n.language === 'en' ? 'text-primary font-bold' : ''}`}
              >
                English
              </button>
              <span>|</span>
              <button 
                onClick={() => i18n.changeLanguage('hi')}
                className={`hover:text-primary transition-colors ${i18n.language === 'hi' ? 'text-primary font-bold' : ''}`}
              >
                हिन्दी
              </button>
            </div>

            {!isWorkspace && (
              <Link to="/discover">
                <Button className="h-[42px] px-5 text-[14px]">Launch →</Button>
              </Link>
            )}
          </div>
        </GlassPanel>
      </Container>
    </header>
  );
};
