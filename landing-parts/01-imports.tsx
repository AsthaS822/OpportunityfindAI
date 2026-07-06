/* eslint-disable */
import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  Sparkles, Shield, CheckCircle2, ArrowRight,
  BookOpen, Building2, CreditCard, Award, Rocket, Globe2,
  Brain, GitCompare, Target, Bell, MessageCircle, FileText,
  Menu, X, Check, Loader2, ChevronDown,
  DollarSign, Calendar, GraduationCap, Star, Zap, Trophy
} from 'lucide-react'
import { useLanguage } from '@/contexts/LanguageContext'
import { Button } from '@/components/ui/button'
import { Accordion, AccordionItem, AccordionTrigger, AccordionContent } from '@/components/ui/accordion'
import { cn } from '@/lib/utils'

const fUp  = { hidden:{opacity:0,y:28}, visible:{opacity:1,y:0,transition:{duration:0.6,ease:[0.22,1,0.36,1]}} }
const stag = { hidden:{}, visible:{transition:{staggerChildren:0.1}} }
const stagF = { hidden:{}, visible:{transition:{staggerChildren:0.06}} }

const STEPS = [
  'Searching 5,200+ verified opportunities…',
  'Checking your eligibility criteria…',
  'Analyzing profile match strength…',
  'Comparing funding & deadlines…',
  'Generating your personal roadmap…',
]
const RESULTS = [
  { title:'Fulbright-Nehru Fellowship', match:92, funding:'₹35L', flag:'🇺🇸', type:'Fellowship' },
  { title:'DAAD Research Scholarship',  match:87, funding:'₹28L', flag:'🇩🇪', type:'Scholarship' },
  { title:'PM Research Fellowship',     match:85, funding:'₹8.4L/yr', flag:'🇮🇳', type:'Fellowship' },
]
const FAQS = [
  { q:'How does the AI match me?', a:'Our AI evaluates your academic profile, income, and goals against official eligibility criteria from verified sources. Each opportunity gets a precise match score.' },
  { q:'Is OpportunityOS free?', a:'Yes, completely free. Every student deserves access to opportunity information without a paywall.' },
  { q:'Does it apply on my behalf?', a:'No — we guide you with checklists and document guidance, but you apply directly on official portals.' },
  { q:'What types of opportunities?', a:'Scholarships, govt schemes, education loans, fellowships, internships, research grants, study abroad, and startup grants.' },
  { q:'How accurate is the eligibility check?', a:'Our rule engine uses official criteria updated monthly. Match scores are indicative — always verify on the official source.' },
]
