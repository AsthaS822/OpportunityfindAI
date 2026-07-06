const fs = require('fs'), path = require('path')
const file = path.join(__dirname, 'src/pages/Landing.tsx')
const cur = fs.readFileSync(file, 'utf8')
if (cur.includes('function Hero()')) { console.log('skip'); process.exit(0) }

const hero = `
function Hero() {
  const { t } = useLanguage()
  const [query, setQuery] = React.useState('')
  const [phase, setPhase] = React.useState('idle')
  const [stepIdx, setStepIdx] = React.useState(0)
  function handleAnalyze() {
    if (!query.trim()) return
    setPhase('thinking'); setStepIdx(0)
    let i = 0
    const tick = () => { i++; setStepIdx(i); if (i < AI_STEPS.length) setTimeout(tick, 700); else setTimeout(() => setPhase('done'), 500) }
    setTimeout(tick, 400)
  }
  return (
    <section className="relative min-h-screen flex items-center overflow-hidden bg-[#09090B] pt-16">
      <div className="absolute inset-0 pointer-events-none" aria-hidden>
        <div className="absolute top-[-20%] left-[-10%] w-[700px] h-[700px] glow-indigo opacity-60" />
        <div className="absolute bottom-[-10%] right-[-5%] w-[500px] h-[500px] glow-orange opacity-40" />
        <div className="absolute top-[40%] left-[40%] w-[400px] h-[400px] glow-emerald opacity-30" />
        <div className="absolute inset-0" style={{backgroundImage:'linear-gradient(rgba(255,255,255,0.03) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,0.03) 1px,transparent 1px)',backgroundSize:'64px 64px'}} />
      </div>
      <div className="relative max-w-7xl mx-auto px-5 py-20 w-full flex items-center gap-16 justify-between">
        <div className="flex-1 max-w-2xl">
          <motion.div variants={stagger} initial="hidden" animate="visible" className="flex flex-col gap-7">
            <motion.div variants={fadeUp}>
              <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full glass border border-white/10 text-xs font-medium text-[#A1A1AA]">
                <span className="w-1.5 h-1.5 rounded-full bg-[#10B981] animate-pulse" />
                5,200+ verified opportunities · Free forever
              </span>
            </motion.div>
            <motion.h1 variants={fadeUp} className="font-display font-black text-5xl md:text-6xl xl:text-7xl leading-[1.05] tracking-[-0.03em] text-white">
              Your AI guide to<br /><span className="gradient-text">every opportunity.</span>
            </motion.h1>
            <motion.p variants={fadeUp} className="text-[#71717A] text-lg leading-relaxed max-w-lg">
              Scholarships, government schemes, education loans, fellowships — discovered, matched, and explained by AI in seconds.
            </motion.p>
            <motion.div variants={fadeUp} className="w-full">
              <div className={"relative rounded-2xl transition-all duration-300 glass border " + (phase !== 'idle' ? "border-[#6366F1]/40 shadow-[0_0_40px_rgba(99,102,241,0.15)]" : "border-white/10")}>
                <textarea value={query} onChange={e => setQuery(e.target.value)}
                  onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleAnalyze() } }}
                  placeholder="I'm a B.Tech student from Karnataka with ₹4L income. I want MS in Germany…"
                  rows={3} className="w-full bg-transparent text-white text-sm placeholder:text-[#52525B] outline-none resize-none p-4 pb-2 leading-relaxed" />
                <div className="flex items-center justify-between px-4 pb-4 pt-2 border-t border-white/06">
                  <span className="flex items-center gap-1.5 text-xs text-[#10B981]">
                    <Shield className="w-3.5 h-3.5" /> Verified sources only
                  </span>
                  <Button variant="primary" size="md" onClick={handleAnalyze} disabled={!query.trim()}>
                    <Sparkles className="w-4 h-4" /> Analyze with AI
                  </Button>
                </div>
                <AnimatePresence>
                  {phase !== 'idle' && (
                    <motion.div initial={{opacity:0,height:0}} animate={{opacity:1,height:'auto'}} exit={{opacity:0,height:0}}
                      className="border-t border-white/06 px-4 py-3 overflow-hidden">
                      {phase === 'thinking' && (
                        <div className="flex flex-col gap-2">
                          {AI_STEPS.map((s,i) => (
                            <div key={i} className={"flex items-center gap-2.5 text-xs transition-all duration-300 " + (i < stepIdx ? "text-[#10B981]" : "text-[#3F3F46]")}>
                              {i < stepIdx ? <Check className="w-3.5 h-3.5 shrink-0"/> : i === stepIdx-1 ? <Loader2 className="w-3.5 h-3.5 shrink-0 animate-spin"/> : <div className="w-3.5 h-3.5 rounded-full border border-[#3F3F46] shrink-0"/>}
                              {s.label}
                            </div>
                          ))}
                        </div>
                      )}
                      {phase === 'done' && (
                        <motion.div initial={{opacity:0}} animate={{opacity:1}} className="flex flex-col gap-2">
                          <p className="text-xs text-[#A1A1AA] mb-1">Top matches found</p>
                          {MOCK_RESULTS.map((r,i) => (
                            <div key={i} className="flex items-center justify-between py-1.5 px-3 rounded-xl bg-white/04 border border-white/06">
                              <div className="flex items-center gap-2">
                                <span className="text-base">{r.flag}</span>
                                <div><p className="text-white text-xs font-medium">{r.title}</p><p className="text-[#71717A] text-[10px]">{r.type}</p></div>
                              </div>
                              <div className="flex items-center gap-3 shrink-0">
                                <span className="text-[#F59E0B] text-xs font-semibold">{r.funding}</span>
                                <span className="text-[10px] px-2 py-0.5 rounded-full bg-[#10B981]/15 text-[#10B981] font-medium">{r.match}%</span>
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
            <motion.div variants={staggerFast} initial="hidden" animate="visible" className="flex flex-wrap gap-2">
              {['🇩🇪 Study in Germany','🇯🇵 Japan Scholarships','💰 Education Loans','🎓 PhD Fellowships','🏛 Govt Schemes','🚀 Startup Grants'].map(c => (
                <motion.button key={c} variants={fadeUp} onClick={() => setQuery(c)}
                  className="px-3 py-1.5 text-xs rounded-full glass border border-white/10 text-[#A1A1AA] hover:border-[#6366F1]/50 hover:text-white transition-all duration-200">
                  {c}
                </motion.button>
              ))}
            </motion.div>
          </motion.div>
        </div>
        <HeroOrb />
      </div>
      <motion.div animate={{y:[0,8,0]}} transition={{repeat:Infinity,duration:2}} className="absolute bottom-8 left-1/2 -translate-x-1/2 text-[#3F3F46]">
        <ChevronDown className="w-5 h-5" />
      </motion.div>
    </section>
  )
}
`
fs.writeFileSync(file, cur + hero)
console.log('Hero added')
