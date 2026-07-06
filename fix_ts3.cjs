const fs = require('fs');
const path = require('path');

const srcDir = path.join(__dirname, 'src');

const heroPath = path.join(srcDir, 'components', 'landing', 'HeroSection.tsx');
let hero = fs.readFileSync(heroPath, 'utf8');

// Cast itemVariants as any
hero = hero.replace('const itemVariants = {', 'const itemVariants: any = {');
hero = hero.replace('const containerVariants = {', 'const containerVariants: any = {');

fs.writeFileSync(heroPath, hero);
console.log("Fixed Hero TS variants error");
