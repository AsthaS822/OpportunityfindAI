const fs = require('fs');
const path = require('path');

const srcDir = path.join(__dirname, 'src');

// Fix HeroSection
const heroPath = path.join(srcDir, 'components', 'landing', 'HeroSection.tsx');
let hero = fs.readFileSync(heroPath, 'utf8');
hero = hero.replace('ease: [0.22, 1, 0.36, 1]', 'ease: "easeOut"');
fs.writeFileSync(heroPath, hero);

// Fix Navbar
const navPath = path.join(srcDir, 'components', 'layout', 'Navbar.tsx');
let nav = fs.readFileSync(navPath, 'utf8');
nav = nav.replace("import { motion } from 'framer-motion';\n", "");
fs.writeFileSync(navPath, nav);

console.log("Fixed TS errors");
