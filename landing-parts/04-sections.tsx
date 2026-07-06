// ── Trusted Logos ─────────────────────────────────────────────────────────────
function TrustedLogos() {
  const logos = ['myScheme','DAAD','NSP','Fulbright','AICTE','MEXT','Chevening','Erasmus+','UGC','Vidya Lakshmi']
  return (
    <section className="bg-[#09090B] py-16 border-t border-white/06">
      <div className="max-w-[1200px] mx-auto px-6">
        <p className="text-center text-xs font-semibold uppercase tracking-widest text-white/30 mb-8">Official verified sources</p>
        <div className="flex flex-wrap justify-center gap-3">
          {logos.map(l => (
            <div key={l} className="px-5 py-2.5 rounded-full bg-white/05 border border-white/08 text-white/50 text-sm font-medium hover:bg-white/10 hover:text-white transition-all cursor-default">{l}</div>
          ))}
        </div>
      </div>
    </section>
  )
}

// ── Opportunity Pills / Categories ────────────────────────────────────────────
function Categories() {
  const cats = [
    { icon: BookOpen,  label:'Scholarships',   count:'2,400+', c:'#818CF8', bg:'rgba(129,140,248,0.12)' },
    { icon: Building2, label:'Govt Schemes',   count:'850+',   c:'#10B981', bg:'rgba(16,185,129,0.12)' },
    { icon: CreditCard,label:'Education Loans',count:'320+',   c:'#F97316', bg:'rgba(249,115,22,0.12)' },
    { icon: Award,     label:'Fellowships',    count:'480+',   c:'#818CF8', bg:'rgba(129,140,248,0.12)' },
    { icon: Rocket,    label:'Startup Grants', count:'190+',   c:'#F97316', bg:'rgba(249,115,22,0.12)' },
    { icon: Globe2,    label:'Study Abroad',   count:'290+',   c:'#10B981', bg:'rgba(16,185,129,0.12)' },
    { icon: Trophy,    label:'Competitions',   count:'670+',   c:'#818CF8', bg:'rgba(129,140,248,0.12)' },
    { icon: GraduationCap, label:'Internships',count:'1,100+', c:'#F97316', bg:'rgba(249,115,22,0.12)' },
  ]
  return (
    <section className="bg-[#09090B] py-28 px-6">
      <div className="max-w-[1200px] mx-auto">
        <motion.div variants={stag} initial="hidden" whileInView="visible" viewport={{ once: true }} className="mb-14">
          <motion.p variants={fUp} className="text-[#4F46E5] text-sm font-bold uppercase tracking-widest mb-3">Opportunity Types</motion.p>
          <motion.h2 variants={fUp} className="font-display font-black text-[clamp(36px,5vw,52px)] text-white tracking-[-0.02em] leading-tight">
            Everything in<br /><span className="text-white/40">one platform.</span>
          </motion.h2>
        </motion.div>
        <div className="flex flex-wrap gap-3">
          {cats.map((c, i) => (
            <motion.div key={c.label}
              variants={fUp} initial="hidden" whileInView="visible" viewport={{ once: true }}
              style={{ transitionDelay: `${i * 0.04}s` }}
              className="group flex items-center gap-3 px-5 py-3.5 rounded-full border border-white/10 cursor-pointer hover:-translate-y-1 transition-all duration-200"
              whileHover={{ scale: 1.03 }}>
              <div className="w-7 h-7 rounded-full flex items-center justify-center shrink-0" style={{ background: c.bg }}>
                <c.icon className="w-3.5 h-3.5" style={{ color: c.c }} />
              </div>
              <span className="text-white text-sm font-semibold">{c.label}</span>
              <span className="text-xs font-bold px-2 py-0.5 rounded-full" style={{ background: c.bg, color: c.c }}>{c.count}</span>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}

// ── Feature Showcase ──────────────────────────────────────────────────────────
function Features() {
  const feats = [
    { tag:'AI Intelligence', title:'Eligibility checked\nin seconds.', desc:'Match score + reason.', c:'#4F46E5', stat1:'200+ criteria', stat2:'98% accurate' },
    { tag:'Decision Center', title:'Your personal\nroadmap.', desc:'Compare. Decide. Apply.', c:'#F97316', stat1:'Up to 4 compared', stat2:'-80% decision time' },
    { tag:'AI Chat', title:'Ask anything,\nget answers.', desc:'No forms. Just ask.', c:'#10B981', stat1:'EN + हिंदी', stat2:'<2s response' },
  ]
  return (
    <section className="bg-[#09090B] py-28 px-6 border-t border-white/06">
      <div className="max-w-[1200px] mx-auto">
        <motion.div variants={stag} initial="hidden" whileInView="visible" viewport={{ once: true }} className="mb-16">
          <motion.p variants={fUp} className="text-[#F97316] text-sm font-bold uppercase tracking-widest mb-3">Features</motion.p>
          <motion.h2 variants={fUp} className="font-display font-black text-[clamp(36px,5vw,52px)] text-white tracking-[-0.02em] leading-tight">
            Built for serious<br /><span className="text-white/40">opportunity seekers.</span>
          </motion.h2>
        </motion.div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          {feats.map((f, i) => (
            <motion.div key={f.tag}
              variants={fUp} initial="hidden" whileInView="visible" viewport={{ once: true }}
              style={{ transitionDelay: `${i * 0.1}s` }}
              className="group relative rounded-3xl bg-white/04 border border-white/08 p-7 overflow-hidden hover:border-white/16 transition-all duration-300 hover:-translate-y-1">
              <div className="absolute top-0 right-0 w-48 h-48 rounded-full blur-[60px] opacity-0 group-hover:opacity-30 transition-opacity duration-500"
                style={{ background: f.c, transform: 'translate(30%,-30%)' }} />
              <span className="text-xs font-bold uppercase tracking-wider px-3 py-1 rounded-full inline-block mb-5" style={{ background:`${f.c}20`, color:f.c, border:`1px solid ${f.c}30` }}>{f.tag}</span>
              <h3 className="font-display font-black text-2xl text-white leading-tight mb-2 whitespace-pre-line">{f.title}</h3>
              <p className="text-white/40 text-sm mb-6">{f.desc}</p>
              <div className="grid grid-cols-2 gap-3">
                {[f.stat1, f.stat2].map(s => (
                  <div key={s} className="rounded-2xl px-4 py-3" style={{ background:`${f.c}10`, border:`1px solid ${f.c}20` }}>
                    <p className="text-white text-sm font-bold">{s}</p>
                  </div>
                ))}
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}

// ── Dashboard Preview ─────────────────────────────────────────────────────────
function DashboardPreview() {
  return (
    <section className="bg-[#09090B] py-28 px-6 border-t border-white/06">
      <div className="max-w-[1200px] mx-auto">
        <motion.div variants={stag} initial="hidden" whileInView="visible" viewport={{ once: true }} className="mb-14 text-center flex flex-col items-center gap-3">
          <motion.p variants={fUp} className="text-[#10B981] text-sm font-bold uppercase tracking-widest">Dashboard</motion.p>
          <motion.h2 variants={fUp} className="font-display font-black text-[clamp(36px,5vw,52px)] text-white tracking-[-0.02em]">Your opportunity<br />command center.</motion.h2>
        </motion.div>
        <motion.div variants={fUp} initial="hidden" whileInView="visible" viewport={{ once: true }}
          className="rounded-3xl bg-white/04 border border-white/08 p-6 overflow-hidden">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            {[
              { label:'Opportunity Score', value:'84/100', color:'#10B981' },
              { label:'Funding Potential', value:'₹18.5L', color:'#F97316' },
              { label:'Matched', value:'18 found', color:'#818CF8' },
              { label:'Next Deadline', value:'Aug 31', color:'#F97316' },
            ].map(s => (
              <div key={s.label} className="rounded-2xl bg-white/05 border border-white/08 p-4 text-center">
                <p className="font-display font-black text-2xl" style={{ color: s.color }}>{s.value}</p>
                <p className="text-white/40 text-xs mt-1">{s.label}</p>
              </div>
            ))}
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {[
              { title:'Fulbright-Nehru Fellowship', match:92, flag:'🇺🇸', funding:'₹35L' },
              { title:'DAAD Research Scholarship', match:87, flag:'🇩🇪', funding:'₹28L' },
              { title:'PM Research Fellowship', match:85, flag:'🇮🇳', funding:'₹8.4L/yr' },
            ].map(o => (
              <div key={o.title} className="rounded-2xl bg-white/05 border border-white/08 p-4 flex items-center gap-3">
                <span className="text-2xl">{o.flag}</span>
                <div className="flex-1 min-w-0">
                  <p className="text-white text-sm font-semibold truncate">{o.title}</p>
                  <p className="text-[#F97316] text-xs font-bold">{o.funding}</p>
                </div>
                <span className="text-xs px-2.5 py-1 rounded-full bg-[#10B981]/15 text-[#10B981] font-bold shrink-0">{o.match}%</span>
              </div>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  )
}

// ── Testimonials ─────────────────────────────────────────────────────────────
function Testimonials() {
  const tms = [
    { name:'Priya S.', inst:'IIT Delhi', text:'Found the Fulbright match in 30 seconds. Would have taken me weeks.', flag:'🇺🇸' },
    { name:'Rohan M.', inst:'NIT Trichy', text:'The AI eligibility check saved me from applying to 4 scholarships I wasn\'t eligible for.', flag:'🇩🇪' },
    { name:'Ananya K.', inst:'BITS Pilani', text:'The decision center helped me compare DAAD vs Chevening side by side. Incredible.', flag:'🇬🇧' },
  ]
  return (
    <section className="bg-[#09090B] py-28 px-6 border-t border-white/06">
      <div className="max-w-[1200px] mx-auto">
        <motion.div variants={stag} initial="hidden" whileInView="visible" viewport={{ once: true }} className="mb-14 text-center flex flex-col items-center gap-3">
          <motion.p variants={fUp} className="text-[#818CF8] text-sm font-bold uppercase tracking-widest">Students love it</motion.p>
          <motion.h2 variants={fUp} className="font-display font-black text-[clamp(36px,5vw,52px)] text-white tracking-[-0.02em]">Real results.</motion.h2>
        </motion.div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          {tms.map((tm, i) => (
            <motion.div key={tm.name} variants={fUp} initial="hidden" whileInView="visible" viewport={{ once: true }}
              style={{ transitionDelay: `${i * 0.1}s` }}
              className="rounded-3xl bg-white/04 border border-white/08 p-7 flex flex-col gap-4">
              <div className="flex gap-1">{[...Array(5)].map((_,j) => <Star key={j} className="w-4 h-4 text-[#F59E0B] fill-[#F59E0B]"/>)}</div>
              <p className="text-white/80 text-sm leading-relaxed">&ldquo;{tm.text}&rdquo;</p>
              <div className="flex items-center gap-2 mt-auto pt-2 border-t border-white/08">
                <div className="w-8 h-8 rounded-full bg-[#4F46E5]/20 flex items-center justify-center text-sm">{tm.name[0]}</div>
                <div><p className="text-white text-xs font-semibold">{tm.name}</p><p className="text-white/40 text-[10px]">{tm.inst}</p></div>
                <span className="ml-auto text-xl">{tm.flag}</span>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}

// ── FAQ ────────────────────────────────────────────────────────────────────────
function FAQSection() {
  return (
    <section className="bg-[#09090B] py-24 px-6 border-t border-white/06">
      <div className="max-w-[800px] mx-auto">
        <motion.div variants={stag} initial="hidden" whileInView="visible" viewport={{ once: true }} className="text-center mb-12 flex flex-col items-center gap-3">
          <motion.p variants={fUp} className="text-[#818CF8] text-sm font-bold uppercase tracking-widest">FAQ</motion.p>
          <motion.h2 variants={fUp} className="font-display font-black text-[clamp(32px,4vw,48px)] text-white tracking-[-0.02em]">Questions? Answered.</motion.h2>
        </motion.div>
        <Accordion type="single" collapsible className="flex flex-col gap-2">
          {FAQS.map((f, i) => (
            <AccordionItem key={i} value={`f${i}`} className="rounded-2xl bg-white/04 border border-white/08 px-5 overflow-hidden">
              <AccordionTrigger className="text-white hover:text-white text-left py-4 [&[data-state=open]]:text-[#818CF8]">{f.q}</AccordionTrigger>
              <AccordionContent className="text-white/50 pb-4">{f.a}</AccordionContent>
            </AccordionItem>
          ))}
        </Accordion>
      </div>
    </section>
  )
}

// ── CTA ────────────────────────────────────────────────────────────────────────
function CTA() {
  return (
    <section className="bg-[#09090B] py-28 px-6 border-t border-white/06">
      <div className="max-w-[1200px] mx-auto">
        <motion.div variants={fUp} initial="hidden" whileInView="visible" viewport={{ once: true }}
          className="relative rounded-3xl overflow-hidden text-center py-20 px-8"
          style={{ background:'linear-gradient(135deg,#1E1B4B,#312E81,#1E1B4B)' }}>
          <div className="absolute inset-0" style={{ background:'radial-gradient(ellipse at center, rgba(79,70,229,0.5) 0%, transparent 70%)' }} />
          <div className="absolute top-[-20%] right-[-5%] w-80 h-80 rounded-full blur-[80px] opacity-25" style={{ background:'#F97316' }} />
          <div className="relative z-10 flex flex-col items-center gap-6">
            <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/10 border border-white/20 text-xs text-white/70">
              <span className="w-1.5 h-1.5 rounded-full bg-[#10B981] animate-pulse" /> Free forever · No sign-up required to explore
            </span>
            <h2 className="font-display font-black text-[clamp(36px,6vw,64px)] text-white leading-tight tracking-[-0.03em]">
              Your next opportunity<br />is waiting.
            </h2>
            <p className="text-white/50 text-lg max-w-md">Start with AI. Discover in seconds. Apply with confidence.</p>
            <div className="flex flex-col sm:flex-row gap-3 mt-2">
              <Button variant="primary" size="xl">Get Started Free <ArrowRight className="w-5 h-5" /></Button>
              <Button variant="secondary" size="xl">Explore Dashboard</Button>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}

// ── Footer ─────────────────────────────────────────────────────────────────────
function Footer() {
  const { language, setLanguage } = useLanguage()
  const cols = [
    { title:'Product', links:['Dashboard','Discover','Decision Center','AI Chat','Compare'] },
    { title:'Resources', links:['Help Center','Docs','API','Changelog'] },
    { title:'Company', links:['About','Blog','Careers','Press'] },
    { title:'Legal', links:['Privacy','Terms','Cookies'] },
  ]
  return (
    <footer className="bg-[#09090B] border-t border-white/06 px-6 pt-16 pb-10">
      <div className="max-w-[1200px] mx-auto">
        <div className="grid grid-cols-2 md:grid-cols-5 gap-10 pb-12 border-b border-white/06">
          <div className="col-span-2 md:col-span-1 flex flex-col gap-4">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-[10px] bg-[#4F46E5] flex items-center justify-center"><Sparkles className="w-4 h-4 text-white"/></div>
              <span className="font-display font-bold text-white text-[15px]">OpportunityOS</span>
            </div>
            <p className="text-sm text-white/30 leading-relaxed">AI Decision Intelligence for students seeking educational opportunities.</p>
            <div className="flex gap-2">
              <span className="text-[10px] px-2.5 py-1 rounded-full border border-white/10 text-white/30">v2.0 Beta</span>
              <span className="text-[10px] px-2.5 py-1 rounded-full bg-[#4F46E5]/15 text-[#818CF8] border border-[#4F46E5]/25">AI-Powered</span>
            </div>
          </div>
          {cols.map(col => (
            <div key={col.title} className="flex flex-col gap-3">
              <h4 className="text-[10px] font-bold uppercase tracking-widest text-white/25">{col.title}</h4>
              {col.links.map(l => <a key={l} href="#" className="text-sm text-white/40 hover:text-white transition-colors">{l}</a>)}
            </div>
          ))}
        </div>
        <div className="pt-8 flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-xs text-white/25">© 2026 OpportunityOS AI. All rights reserved.</p>
          <div className="flex items-center bg-white/05 rounded-full p-0.5 border border-white/08">
            <button onClick={() => setLanguage('en')} className={cn('px-3 py-1 text-xs font-medium rounded-full transition-all', language==='en'?'bg-white/15 text-white':'text-white/30')}>EN</button>
            <button onClick={() => setLanguage('hi')} className={cn('px-3 py-1 text-xs font-medium rounded-full transition-all', language==='hi'?'bg-white/15 text-white':'text-white/30')}>हिंदी</button>
          </div>
        </div>
      </div>
    </footer>
  )
}
