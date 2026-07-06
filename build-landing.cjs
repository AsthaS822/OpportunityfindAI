const fs = require('fs')
const p = require('path')
const out = p.join(__dirname, 'src/pages/Landing.tsx')

// Read all section files and concatenate
const sections = [
  'landing-parts/01-imports.tsx',
  'landing-parts/02-navbar.tsx',
  'landing-parts/03-hero.tsx',
  'landing-parts/04-sections.tsx',
  'landing-parts/05-export.tsx',
]

const content = sections.map(f => {
  const full = p.join(__dirname, f)
  if (!fs.existsSync(full)) { console.error('MISSING:', f); process.exit(1) }
  return fs.readFileSync(full, 'utf8')
}).join('\n\n')

fs.writeFileSync(out, content)
console.log('Landing.tsx written —', content.length, 'chars')
