function Hero() {
  const { t } = useLanguage()
  const [query, setQuery] = useState('')
  const [phase, setPhase] = useState<'idle'|'thinking'|'done'>('idle')
  const [stepIdx, setStepIdx] = useState(0)

  function analyze() {
    if (!query.trim()) return
    setPhase('thinking'); setStepIdx(0)
    let i = 0
    const tick = () => { i++; setStepIdx(i); if (i < STEPS.length) setTimeout(tick, 650); else setTimeout(() => setPhase('done'), 500) }
    setTimeout(tick, 300)
  }

  return (
    <section className="relative min-h-screen flex flex-col items-center justify-center overflow-hidden">
      {/* Fantasy background image */}
      <div className="absolute inset-0 z-0">
        <img src="/bg.jpg" alt="" className="w-full h-full object-cover scale-105 blur-[3px]" />
        <div className="absolute inset-0 bg-black/55" />
        <div className="absolute inset-0 bg-gradient-to-b from-black/30 via-black/20 to-[#09090B]" />
      </div>

      {/* Floating ambient orbs */}
      <div className="absolute inset-0 z-[1] pointer-events-none">
        <div className="absolute top-[15%] left-[10%] w-[300px] h-[300px] rounded-full bg-[#4F46E5]/20 blur-[80px]" />
        <div className="absolute top-[25%] right-[12%] w-[250px] h-[250px] rounded-full bg-[#F97316]/15 blur-[70px]" />
        <div className="absolute bottom-[20%] left-[35%] w-[200px] h-[200px] rounded-full bg-[#10B981]/10 blur-[60px]" />
      </div>

      {/* Content */}
      <div className="relative z-10 max-w-[1200px] mx-auto px-6 pt-24 pb-16 flex flex-col items-center gap-8 text-center">

        {/* Badge */}
        <motion.div variants={fUp} initial="hidden" animate="visible">
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/10 backdrop-blur-md border border-white/20 text-xs font-medium text-white/80">
            <span className="w-1.5 h-1.5 rounded-full bg-[#10B981] animate-pulse" />
            AI-Powered · 5,200+ Verified Opportunities · Free Forever
          </span>
        </motion.div>

        {/* Headline */}
        <motion.h1 variants={fUp} initial="hidden" animate="visible"
          className="font-display font-black text-[clamp(48px,8vw,80px)] leading-[1.0] tracking-[-0.03em] text-white max-w-4xl">
          Your AI Guide to<br />
          <span style={{background:'linear-gradient(135deg,#818CF8,#4F46E5,#F97316)',WebkitBackgroundClip:'text',WebkitTextFillColor:'transparent',backgroundClip:'text'}}>
            Every Opportunity.
          </span>
        </motion.h1>

        <motion.p variants={fUp} initial="hidden" animate="visible"
          className="text-white/60 text-lg max-w-lg leading-relaxed">
          Scholarships · Government schemes · Education loans · Fellowships
        </motion.p>

        {/* AI Search box — glass card */}
        <motion.div variants={fUp} initial="hidden" animate="visible" className="w-full max-w-2xl">
          <div className={cn(
            'rounded-3xl p-5 transition-all duration-300',
            'bg-white/10 backdrop-blur-2xl border border-white/20',
            phase !== 'idle' && 'border-[#4F46E5]/60 shadow-[0_0_60px_rgba(79,70,229,0.25)]'
          )}>
            {/* AI label */}
            <div className="flex items-center gap-2 mb-3">
              <div className="w-6 h-6 rounded-lg bg-[#4F46E5] flex items-center justify-center">
                <Sparkles className="w-3.5 h-3.5 text-white" />
              </div>
              <span className="text-white/80 text-sm font-semibold">OpportunityOS AI</span>
              <span className="ml-auto text-xs text-[#10B981] flex items-center gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-[#10B981] animate-pulse" /> Online
              </span>
            </div>

            <textarea
              value={query}
              onChange={e => setQuery(e.target.value)}
              onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); analyze() } }}
              placeholder="Tell me what you want to achieve… e.g. I'm a B.Tech CSE student from Karnataka, ₹4L income, want MS in Germany"
              rows={3}
              className="w-full bg-transparent text-white text-sm placeholder:text-white/30 outline-none resize-none leading-relaxed"
            />

            {/* Chips */}
            <div className="flex flex-wrap gap-2 mt-3 mb-4">
              {[['🎓','Scholarships'],['🏦','Education Loans'],['🌍','Study Abroad'],['🏛','Govt Schemes'],['🔬','Fellowships']].map(([icon, label]) => (
                <button key={label} onClick={() => setQuery(`${icon} ${label}`)}
                  className="flex items-center gap-1 px-3 py-1 rounded-full bg-white/10 border border-white/15 text-white/70 text-xs hover:bg-white/20 hover:text-white transition-all">
                  {icon} {label}
                </button>
              ))}
            </div>

            <div className="flex items-center justify-between border-t border-white/10 pt-3">
              <span className="flex items-center gap-1.5 text-xs text-[#10B981]">
                <Shield className="w-3.5 h-3.5" /> Verified sources only
              </span>
              <Button variant="primary" size="md" onClick={analyze} disabled={!query.trim()}>
                <Sparkles className="w-4 h-4" /> Analyze with AI
              </Button>
            </div>

            {/* Analysis steps */}
            <AnimatePresence>
              {phase !== 'idle' && (
                <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }} className="overflow-hidden mt-3 pt-3 border-t border-white/10">
                  {phase === 'thinking' && (
                    <div className="flex flex-col gap-2">
                      {STEPS.map((s, i) => (
                        <div key={i} className={cn('flex items-center gap-2 text-xs transition-all', i < stepIdx ? 'text-[#10B981]' : 'text-white/30')}>
                          {i < stepIdx ? <Check className="w-3.5 h-3.5 shrink-0" /> : i === stepIdx - 1 ? <Loader2 className="w-3.5 h-3.5 shrink-0 animate-spin" /> : <span className="w-3.5 h-3.5 rounded-full border border-white/20 shrink-0" />}
                          {s}
                        </div>
                      ))}
                    </div>
                  )}
                  {phase === 'done' && (
                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex flex-col gap-2">
                      <p className="text-xs text-white/50 mb-1">✓ Found 12 matches · Top results:</p>
                      {RESULTS.map((r, i) => (
                        <div key={i} className="flex items-center justify-between px-3 py-2 rounded-xl bg-white/08 border border-white/10">
                          <div className="flex items-center gap-2">
                            <span>{r.flag}</span>
                            <div><p className="text-white text-xs font-medium">{r.title}</p><p className="text-white/40 text-[10px]">{r.type}</p></div>
                          </div>
                          <div className="flex items-center gap-3">
                            <span className="text-[#F97316] text-xs font-bold">{r.funding}</span>
                            <span className="text-[10px] px-2 py-0.5 rounded-full bg-[#10B981]/20 text-[#10B981] font-semibold">{r.match}%</span>
                          </div>
                        </div>
                      ))}
                    </motion.div>
                  )}
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </motion.div>

        {/* Floating glass stat cards */}
        <div className="hidden lg:flex items-center gap-4 mt-2">
          {[
            { label:'Match Score', value:'94%', sub:'Fulbright', color:'#10B981' },
            { label:'Total Funding', value:'₹18.5L', sub:'Across 3 schemes', color:'#F97316' },
            { label:'Deadlines', value:'Aug 31', sub:'DAAD next', color:'#818CF8' },
            { label:'Countries', value:'48+', sub:'Study destinations', color:'#10B981' },
          ].map(card => (
            <motion.div key={card.label}
              animate={{ y: [0, -6, 0] }}
              transition={{ duration: 3 + Math.random() * 2, repeat: Infinity, ease: 'easeInOut' }}
              className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-2xl px-5 py-3 text-center min-w-[120px]">
              <p className="font-display font-black text-2xl" style={{ color: card.color }}>{card.value}</p>
              <p className="text-white text-xs font-semibold mt-0.5">{card.label}</p>
              <p className="text-white/40 text-[10px] mt-0.5">{card.sub}</p>
            </motion.div>
          ))}
        </div>
      </div>

      <motion.div animate={{ y: [0, 8, 0] }} transition={{ repeat: Infinity, duration: 2 }}
        className="absolute bottom-8 left-1/2 -translate-x-1/2 z-10 text-white/30">
        <ChevronDown className="w-5 h-5" />
      </motion.div>
    </section>
  )
}
