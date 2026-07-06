const fs = require('fs'), path = require('path')
const out = path.join(__dirname, 'src/pages/Landing.tsx')
let code = ''
code += `/* eslint-disable */\n`
code += `import { useState, useEffect } from 'react'\n`
code += `import { motion, AnimatePresence } from 'framer-motion'\n`
code += `import { Sparkles, Shield, CheckCircle2, ArrowRight, BookOpen, Building2, CreditCard, Award, Rocket, Globe2, Brain, GitCompare, Target, Bell, MessageCircle, FileText, Menu, X, Check, Loader2, ChevronDown, DollarSign, Calendar, GraduationCap, Star, Zap, Trophy } from 'lucide-react'\n`
code += `import { useLanguage } from '@/contexts/LanguageContext'\n`
code += `import { Button } from '@/components/ui/button'\n`
code += `import { Accordion, AccordionItem, AccordionTrigger, AccordionContent } from '@/components/ui/accordion'\n`
code += `import { cn } from '@/lib/utils'\n\n`
code += `const fUp = { hidden:{opacity:0,y:28}, visible:{opacity:1,y:0,transition:{duration:0.6,ease:[0.22,1,0.36,1]}} }\n`
code += `const fIn = { hidden:{opacity:0}, visible:{opacity:1,transition:{duration:0.5}} }\n`
code += `const stag = { hidden:{}, visible:{transition:{staggerChildren:0.1}} }\n`
code += `const stagF = { hidden:{}, visible:{transition:{staggerChildren:0.06}} }\n\n`
code += `const STEPS = [\n`
code += `  { label:'Searching 5,200+ opportunities…' },\n`
code += `  { label:'Verifying eligibility criteria…' },\n`
code += `  { label:'Analyzing your profile match…' },\n`
code += `  { label:'Comparing funding options…' },\n`
code += `  { label:'Generating your roadmap…' },\n`
code += `]\n`
code += `const RESULTS = [\n`
code += `  { title:'Fulbright-Nehru Fellowship', match:92, funding:'₹35L', flag:'🇺🇸', type:'Fellowship' },\n`
code += `  { title:'DAAD Research Scholarship',  match:87, funding:'₹28L', flag:'🇩🇪', type:'Scholarship' },\n`
code += `  { title:'PM Research Fellowship',     match:85, funding:'₹8.4L/yr', flag:'🇮🇳', type:'Fellowship' },\n`
code += `]\n\n`
fs.writeFileSync(out, code)
console.log('part1 ok')

// Navbar
code += `function Navbar() {\n`
code += `  const { t, language, setLanguage } = useLanguage()\n`
code += `  const [open, setOpen] = useState(false)\n`
code += `  const [sc, setSc] = useState(false)\n`
code += `  useEffect(() => { const f = () => setSc(window.scrollY > 30); window.addEventListener('scroll',f,{passive:true}); return ()=>window.removeEventListener('scroll',f) }, [])\n`
code += `  return (\n`
code += `    <header className={cn('fixed top-0 inset-x-0 z-50 transition-all duration-300', sc ? 'bg-black/60 backdrop-blur-2xl border-b border-white/10' : 'bg-transparent')}>\n`
code += `      <div className="max-w-[1200px] mx-auto px-6 h-16 flex items-center justify-between">\n`
code += `        <a href="/" className="flex items-center gap-2.5">\n`
code += `          <div className="w-8 h-8 rounded-[10px] bg-[#4F46E5] flex items-center justify-center shadow-[0_0_20px_rgba(79,70,229,0.6)]"><Sparkles className="w-4 h-4 text-white"/></div>\n`
code += `          <span className="font-display font-bold text-white text-[15px]">OpportunityOS</span>\n`
code += `          <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-[#4F46E5]/25 text-[#818CF8] border border-[#4F46E5]/40">AI</span>\n`
code += `        </a>\n`
code += `        <nav className="hidden md:flex items-center gap-7">\n`
code += `          {['Discover','How it Works','Features','About'].map(l=><a key={l} href="#" className="text-sm text-white/60 hover:text-white transition-colors">{l}</a>)}\n`
code += `        </nav>\n`
code += `        <div className="hidden md:flex items-center gap-3">\n`
code += `          <div className="flex items-center bg-white/08 rounded-full p-0.5 border border-white/10">\n`
code += `            <button onClick={()=>setLanguage('en')} className={cn('px-3 py-1 text-xs font-medium rounded-full transition-all', language==='en'?'bg-white/20 text-white':'text-white/40')}>EN</button>\n`
code += `            <button onClick={()=>setLanguage('hi')} className={cn('px-3 py-1 text-xs font-medium rounded-full transition-all', language==='hi'?'bg-white/20 text-white':'text-white/40')}>हिंदी</button>\n`
code += `          </div>\n`
code += `          <Button variant="ghost" size="sm" className="text-white/70 hover:text-white">{t('auth.signIn')}</Button>\n`
code += `          <Button variant="primary" size="sm">{t('nav.getStarted')}</Button>\n`
code += `        </div>\n`
code += `        <button className="md:hidden text-white/70" onClick={()=>setOpen(!open)}>{open?<X className="w-5 h-5"/>:<Menu className="w-5 h-5"/>}</button>\n`
code += `      </div>\n`
code += `      <AnimatePresence>{open&&<motion.div initial={{opacity:0,y:-8}} animate={{opacity:1,y:0}} exit={{opacity:0,y:-8}} className="md:hidden bg-black/80 backdrop-blur-xl border-t border-white/10 px-6 py-4 flex flex-col gap-3"><{['Discover','How it Works','Features','About'].map(l=><a key={l} href="#" className="text-sm text-white/60 py-1">{l}</a>)}<div className="flex gap-2 pt-2"><Button variant="secondary" size="sm" className="flex-1">{t('auth.signIn')}</Button><Button variant="primary" size="sm" className="flex-1">{t('nav.getStarted')}</Button></div></motion.div>}</AnimatePresence>\n`
code += `    </header>\n`
code += `  )\n`
code += `}\n\n`
fs.appendFileSync(out, code.split('/* eslint-disable */\n')[1] || '')
// reset code for next chunk
code = ''
console.log('navbar ok')
