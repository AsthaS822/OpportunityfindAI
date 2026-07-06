const fs = require('fs');
const path = require('path');

const srcDir = path.join(__dirname, 'src');

const indexCssPath = path.join(srcDir, 'styles', 'index.css');
let indexCss = fs.readFileSync(indexCssPath, 'utf8');

if (!indexCss.includes('animate-marquee')) {
  indexCss += `
@layer utilities {
  .shadow-glow {
    box-shadow: 0 0 20px rgba(249, 115, 22, 0.15);
  }
}

@keyframes marquee {
  0% { transform: translateX(0%); }
  100% { transform: translateX(-50%); }
}

.animate-marquee {
  animation: marquee 30s linear infinite;
}
`;
  fs.writeFileSync(indexCssPath, indexCss);
}

const appTsxPath = path.join(srcDir, 'App.tsx');
let appTsx = fs.readFileSync(appTsxPath, 'utf8');
appTsx = appTsx.replace(
  "import { Container } from './components/layout/Container';",
  "import { Container } from './components/layout/Container';\nimport { Home } from './pages/Home';"
);
appTsx = appTsx.replace(
  `<Route path="/" element={<PlaceholderPage title="Home (Placeholder)" />} />`,
  `<Route path="/" element={<Home />} />`
);
// Also the Layout currently has pt-24 which might interfere with the hero section since it's 100vh and the navbar is absolute/fixed. 
// We should remove pt-24 from layout for the Home page or in general, since Navbar is fixed and hero has its own padding.
appTsx = appTsx.replace(
  `className="min-h-screen flex flex-col pt-24"`,
  `className="min-h-screen flex flex-col"`
);
fs.writeFileSync(appTsxPath, appTsx);

console.log("Updated App.tsx and index.css");
