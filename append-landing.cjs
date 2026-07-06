const fs = require('fs')
const path = require('path')

const file = path.join(__dirname, 'src/pages/Landing.tsx')
const current = fs.readFileSync(file, 'utf8')

// Only append if export default not already present
if (current.includes('export default function Landing')) {
  console.log('Already complete, skipping.')
  process.exit(0)
}

const rest = `
function HeroOrb() {
  return (
    <div className="relative w-[420px] h-[420px] shrink-0 hidden lg:block">
      <div className="absolute inset-0 rounded-full border border-[#6366F1]/20 animate-spin-slow" />
      <div className="absolute inset-[28px] rounded-full border border-[#F97316]/15 animate-spin-slow" style={{animationDirection:'reverse',animationDuration:'15s'}} />
      <div className="absolute inset-[56px] rounded-full bg-gradient-to-br from-[#4338CA] via-[#6366F1] to-[#818CF8] animate-pulse-glow flex items-center justify-center shadow-[0_0_80px_rgba(99,102,241,0.6)]">
        <div className="w-20 h-20 rounded-full bg-white/15 backdrop-blur-sm flex items-center justify-center border border-white/20">
          <Sparkles className="w-9 h-9 text-white" />
        </div>
      </div>
      <motion.div animate={{y:[0,-12,0]}} transition={{duration:3.5,repeat:Infinity,ease:'easeInOut'}}
        className="absolute top-2 right-[-8px] glass rounded-2xl p-3 flex items-center gap-2.5 border border-white/10 min-w-[150px]">
        <div className="w-7 h-7 rounded-lg bg-[#10B981]/20 flex items-center justify-center shrink-0">
          <CheckCircle2 className="w-4 h-4 text-[#10B981]" />
        </div>
        <div><p className="text-white text-xs font-semibold">92% Match</p><p className="text-[#71717A] text-[10px]">Fulbright Fellowship</p></div>
      </motion.div>
      <motion.div animate={{y:[0,10,0]}} transition={{duration:4,repeat:Infinity,ease:'easeInOut',delay:0.8}}
        className="absolute bottom-14 left-[-8px] glass rounded-2xl p-3 flex items-center gap-2.5 border border-white/10 min-w-[145px]">
        <div className="w-7 h-7 rounded-lg bg-[#F59E0B]/20 flex items-center justify-center shrink-0">
          <DollarSign className="w-4 h-4 text-[#F59E0B]" />
        </div>
        <div><p className="text-white text-xs font-semibold">₹35L Funding</p><p className="text-[#71717A] text-[10px]">Full scholarship</p></div>
      </motion.div>
      <motion.div animate={{y:[0,-8,0]}} transition={{duration:4.5,repeat:Infinity,ease:'easeInOut',delay:1.5}}
        className="absolute top-28 left-[-24px] glass rounded-2xl p-3 flex items-center gap-2.5 border border-white/10 min-w-[138px]">
        <div className="w-7 h-7 rounded-lg bg-[#6366F1]/20 flex items-center justify-center shrink-0">
          <Calendar className="w-4 h-4 text-[#818CF8]" />
        </div>
        <div><p className="text-white text-xs font-semibold">Aug 31</p><p className="text-[#71717A] text-[10px]">DAAD Deadline</p></div>
      </motion.div>
      <motion.div animate={{y:[0,10,0]}} transition={{duration:3,repeat:Infinity,ease:'easeInOut',delay:2.2}}
        className="absolute bottom-0 right-4 glass rounded-2xl p-3 flex items-center gap-2.5 border border-white/10 min-w-[145px]">
        <div className="w-7 h-7 rounded-lg bg-[#EC4899]/20 flex items-center justify-center shrink-0">
          <GraduationCap className="w-4 h-4 text-[#EC4899]" />
        </div>
        <div><p className="text-white text-xs font-semibold">48 Countries</p><p className="text-[#71717A] text-[10px]">Study destinations</p></div>
      </motion.div>
    </div>
  )
}
`

fs.writeFileSync(file, current + rest)
console.log('Step 1 done — HeroOrb added')
