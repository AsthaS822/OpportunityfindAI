function Navbar() {
  const { t, language, setLanguage } = useLanguage()
  const [open, setOpen] = useState(false)
  const [sc, setSc] = useState(false)
  useEffect(() => {
    const f = () => setSc(window.scrollY > 30)
    window.addEventListener('scroll', f, { passive: true })
    return () => window.removeEventListener('scroll', f)
  }, [])
  return (
    <header className={cn('fixed top-0 inset-x-0 z-50 transition-all duration-300',
      sc ? 'bg-black/60 backdrop-blur-2xl border-b border-white/10' : 'bg-transparent')}>
      <div className="max-w-[1200px] mx-auto px-6 h-16 flex items-center justify-between">
        <a href="/" className="flex items-center gap-2.5 shrink-0">
          <div className="w-8 h-8 rounded-[10px] bg-[#4F46E5] flex items-center justify-center shadow-[0_0_20px_rgba(79,70,229,0.6)]">
            <Sparkles className="w-4 h-4 text-white" />
          </div>
          <span className="font-display font-bold text-white text-[15px] tracking-tight">OpportunityOS</span>
          <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-[#4F46E5]/25 text-[#818CF8] border border-[#4F46E5]/40">AI</span>
        </a>
        <nav className="hidden md:flex items-center gap-7">
          {['Discover','How it Works','Features','About'].map(l => (
            <a key={l} href="#" className="text-sm text-white/60 hover:text-white transition-colors">{l}</a>
          ))}
        </nav>
        <div className="hidden md:flex items-center gap-3">
          <div className="flex items-center bg-white/08 rounded-full p-0.5 border border-white/10">
            <button onClick={() => setLanguage('en')} className={cn('px-3 py-1 text-xs font-medium rounded-full transition-all', language === 'en' ? 'bg-white/20 text-white' : 'text-white/40')}>EN</button>
            <button onClick={() => setLanguage('hi')} className={cn('px-3 py-1 text-xs font-medium rounded-full transition-all', language === 'hi' ? 'bg-white/20 text-white' : 'text-white/40')}>हिंदी</button>
          </div>
          <Button variant="ghost" size="sm" className="text-white/70 hover:text-white">{t('auth.signIn')}</Button>
          <Button variant="primary" size="sm">{t('nav.getStarted')}</Button>
        </div>
        <button className="md:hidden text-white/70" onClick={() => setOpen(!open)}>
          {open ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
        </button>
      </div>
      <AnimatePresence>
        {open && (
          <motion.div initial={{ opacity: 0, y: -8 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -8 }}
            className="md:hidden bg-black/80 backdrop-blur-xl border-t border-white/10 px-6 py-4 flex flex-col gap-3">
            {['Discover','How it Works','Features','About'].map(l => (
              <a key={l} href="#" className="text-sm text-white/60 py-1">{l}</a>
            ))}
            <div className="flex gap-2 pt-2">
              <Button variant="secondary" size="sm" className="flex-1">{t('auth.signIn')}</Button>
              <Button variant="primary" size="sm" className="flex-1">{t('nav.getStarted')}</Button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  )
}
