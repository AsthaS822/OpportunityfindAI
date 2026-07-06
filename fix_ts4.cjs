const fs = require('fs');
const path = require('path');

const srcDir = path.join(__dirname, 'src');

const heroPath = path.join(srcDir, 'components', 'landing', 'HeroSection.tsx');
let hero = fs.readFileSync(heroPath, 'utf8');
hero = hero.replace("import { Link, useNavigate } from 'react-router-dom';", "import { Link } from 'react-router-dom';");
fs.writeFileSync(heroPath, hero);

const panelPath = path.join(srcDir, 'components', 'workspace', 'AnalysisPanel.tsx');
let panel = fs.readFileSync(panelPath, 'utf8');
panel = panel.replace("import { Target, CheckCircle2, ChevronRight, BarChart3, Download } from 'lucide-react';", "import { Target, ChevronRight, BarChart3, Download } from 'lucide-react';");
fs.writeFileSync(panelPath, panel);

console.log("Fixed unused imports");
