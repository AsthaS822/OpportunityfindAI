const fs = require('fs');
const path = require('path');

const srcDir = path.join(__dirname, 'src');

// Update App.tsx
const appTsxPath = path.join(srcDir, 'App.tsx');
let appTsx = fs.readFileSync(appTsxPath, 'utf8');
if (!appTsx.includes('import { Discovery } from')) {
  appTsx = appTsx.replace(
    "import { Home } from './pages/Home';",
    "import { Home } from './pages/Home';\nimport { Discovery } from './pages/Discovery';"
  );
  appTsx = appTsx.replace(
    `<Route path="/discover" element={<PlaceholderPage title="Discover" />} />`,
    `<Route path="/discover" element={<Discovery />} />`
  );
  fs.writeFileSync(appTsxPath, appTsx);
}

// Update Navbar.tsx to use react-router-dom Link for routing
const navPath = path.join(srcDir, 'components', 'layout', 'Navbar.tsx');
let nav = fs.readFileSync(navPath, 'utf8');
if (!nav.includes('import { Link } from')) {
  nav = nav.replace("import { GlassPanel } from '../ui/GlassPanel';", "import { GlassPanel } from '../ui/GlassPanel';\nimport { Link } from 'react-router-dom';");
  
  // Replace the Start Exploring button with a Link wrapper
  nav = nav.replace(
    `<Button className="h-[44px] px-6 text-[15px]">{t('start')}</Button>`,
    `<Link to="/discover"><Button className="h-[44px] px-6 text-[15px]">{t('start')}</Button></Link>`
  );
  
  // Link the Logo back to home
  nav = nav.replace(
    `<div className="flex items-center gap-2">`,
    `<Link to="/" className="flex items-center gap-2">`
  );
  nav = nav.replace(
    `<span className="font-heading text-xl font-bold tracking-tight">OpportunityOS</span>\n          </div>`,
    `<span className="font-heading text-xl font-bold tracking-tight">OpportunityOS</span>\n          </Link>`
  );

  fs.writeFileSync(navPath, nav);
}

// Update HeroSection.tsx to also link to discover
const heroPath = path.join(srcDir, 'components', 'landing', 'HeroSection.tsx');
let hero = fs.readFileSync(heroPath, 'utf8');
if (!hero.includes('import { Link } from')) {
  hero = hero.replace("import { Button } from '../ui/Button';", "import { Button } from '../ui/Button';\nimport { Link, useNavigate } from 'react-router-dom';");
  
  // We need to inject useNavigate hook. This is a bit tricky with string replace, so we'll just link the button.
  hero = hero.replace(
    `<Button className="h-[48px] px-6 ml-2 group/btn">\n                Analyze`,
    `<Link to="/discover"><Button type="button" className="h-[48px] px-6 ml-2 group/btn">\n                Analyze`
  );
  hero = hero.replace(
    `Analyze\n                <ArrowRight className="w-4 h-4 ml-2 group-hover/btn:translate-x-1 transition-transform" />\n              </Button>`,
    `Analyze\n                <ArrowRight className="w-4 h-4 ml-2 group-hover/btn:translate-x-1 transition-transform" />\n              </Button></Link>`
  );

  fs.writeFileSync(heroPath, hero);
}

// Update FinalCTA to link to discover
const ctaPath = path.join(srcDir, 'components', 'landing', 'FinalCTA.tsx');
let cta = fs.readFileSync(ctaPath, 'utf8');
if (!cta.includes('import { Link } from')) {
  cta = cta.replace("import { ArrowRight } from 'lucide-react';", "import { ArrowRight } from 'lucide-react';\nimport { Link } from 'react-router-dom';");
  cta = cta.replace(
    `<Button className="h-[56px] px-10 text-lg shadow-lg shadow-primary/20 hover:shadow-primary/30 group">`,
    `<Link to="/discover"><Button className="h-[56px] px-10 text-lg shadow-lg shadow-primary/20 hover:shadow-primary/30 group">`
  );
  cta = cta.replace(
    `<ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />\n            </Button>`,
    `<ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />\n            </Button></Link>`
  );
  fs.writeFileSync(ctaPath, cta);
}

console.log("Updated routing");
