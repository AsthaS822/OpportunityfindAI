import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import type { DiscoverResponse } from '../../lib/api';
import { discoverOpportunities } from '../../lib/api';
import {
  MapPin, CheckCircle2, ExternalLink,
  Sparkles, Target, BookOpen, Award,
  Building2, DollarSign, Globe, Briefcase,
  ChevronDown, ChevronUp,
  BarChart3, Heart, Share2, FileText, MessageSquare,
  GraduationCap
} from 'lucide-react';

function getCategoryIcon(category: string) {
  const c = category?.toLowerCase() || '';
  if (c.includes('scholar') || c.includes('merit')) return Award;
  if (c.includes('grant') || c.includes('fund') || c.includes('startup')) return DollarSign;
  if (c.includes('loan') || c.includes('finance')) return Building2;
  if (c.includes('abroad') || c.includes('global') || c.includes('overseas')) return Globe;
  if (c.includes('intern') || c.includes('job')) return Briefcase;
  return BookOpen;
}

function getCategoryColor(category: string) {
  const c = category?.toLowerCase() || '';
  if (c.includes('scholar') || c.includes('merit')) return 'bg-orange-50 text-orange-600';
  if (c.includes('intern') || c.includes('job')) return 'bg-violet-50 text-violet-600';
  if (c.includes('grant') || c.includes('fund')) return 'bg-rose-50 text-rose-600';
  if (c.includes('loan') || c.includes('finance')) return 'bg-emerald-50 text-emerald-600';
  if (c.includes('abroad') || c.includes('global') || c.includes('overseas')) return 'bg-blue-50 text-blue-600';
  return 'bg-gray-100 text-gray-600';
}

function formatDeadline(deadline?: string): string {
  if (!deadline || deadline === 'Invalid Date' || deadline === 'Unknown') return '';
  const d = new Date(deadline);
  if (isNaN(d.getTime())) return '';
  const now = new Date();
  if (d > now) {
    const diff = Math.ceil((d.getTime() - now.getTime()) / (1000 * 60 * 60 * 24));
    if (diff <= 30) return `${d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })} — ${diff} days left`;
    return d.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });
  }
  return '';
}

function formatProvider(provider?: string): string {
  if (!provider || provider === 'Unknown' || provider === 'Unknown Provider' || provider === 'N/A' || provider === 'Official source') return '';
  return provider;
}

function stars(score?: number): string {
  if (!score || score < 20) return '☆☆☆☆☆';
  if (score < 40) return '★☆☆☆☆';
  if (score < 60) return '★★☆☆☆';
  if (score < 80) return '★★★☆☆';
  if (score < 90) return '★★★★☆';
  return '★★★★★';
}

function starLabel(score?: number): string {
  if (!score || score < 20) return 'Possible match';
  if (score < 40) return 'Fair match';
  if (score < 60) return 'Good match';
  if (score < 80) return 'Excellent match';
  return 'Highly recommended';
}

function starReasons(score?: number): string[] {
  const reasons = [];
  if (score && score > 40) reasons.push('Your academic background aligns');
  if (score && score > 60) reasons.push('Strong eligibility match');
  if (score && score > 30) reasons.push('Indian applicants welcome');
  return reasons;
}

function deduplicate<T>(items: T[], key: (item: T) => string): T[] {
  const seen = new Set<string>();
  return items.filter(item => {
    const k = key(item).toLowerCase().trim();
    if (seen.has(k)) return false;
    seen.add(k);
    return true;
  });
}

function isLoanRelated(category?: string, title?: string): boolean {
  const txt = `${category || ''} ${title || ''}`.toLowerCase();
  return txt.includes('loan') || txt.includes('vidyalaxmi') || txt.includes('vidyarthi') || txt.includes('buddy4study');
}

const LOADING_STEPS = [
  { emoji: '🌍', text: 'Looking across official sources...' },
  { emoji: '📚', text: 'Comparing eligibility...' },
  { emoji: '🤖', text: 'Preparing personalized recommendations...' },
];

function SkeletonBlock() {
  const [step, setStep] = useState(0);
  useEffect(() => {
    const interval = setInterval(() => setStep(s => Math.min(s + 1, LOADING_STEPS.length - 1)), 2000);
    return () => clearInterval(interval);
  }, []);
  return (
    <div className="space-y-3">
      {LOADING_STEPS.map((s, i) => (
        <motion.div
          key={i}
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: i <= step ? 1 : 0.3, y: 0 }}
          transition={{ duration: 0.4 }}
          className="flex items-center gap-2.5 text-[13px] text-text-secondary"
        >
          <span className="text-base">{s.emoji}</span>
          <span>{s.text}</span>
        </motion.div>
      ))}
    </div>
  );
}

export const MessageSequence = ({ query }: { query: string }) => {
  const [result, setResult] = useState<DiscoverResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState('');
  const [expandedCard, setExpandedCard] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true); setErr(''); setResult(null); setExpandedCard(null);
    discoverOpportunities(query)
      .then((data: DiscoverResponse) => { setResult(data); setLoading(false); })
      .catch((e: Error) => { setErr(e instanceof Error ? e.message : 'Connection issue'); setLoading(false); });
  }, [query]);

  const opportunities = result?.opportunities ? deduplicate(result.opportunities, o => o.title) : [];
  const relevant = opportunities.filter(o => !isLoanRelated(o.category, o.title));
  const loans = opportunities.filter(o => isLoanRelated(o.category, o.title));

  return (
    <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} className="mb-10 last:mb-0">
      {/* User query bubble */}
      <div className="flex items-start gap-2.5 mb-8">
        <div className="w-7 h-7 rounded-full bg-gradient-to-br from-primary to-orange-400 flex items-center justify-center flex-shrink-0">
          <GraduationCap className="w-3.5 h-3.5 text-white" />
        </div>
        <div className="bg-gray-100 px-4 py-2.5 rounded-2xl rounded-tl-none text-[14px] text-text-primary max-w-[80%]">
          {query}
        </div>
      </div>

      {/* AI Response */}
      <div className="ml-0">
        {/* AI Header */}
        <div className="flex items-center gap-2 mb-4">
          <Sparkles className="w-4 h-4 text-primary" />
          <span className="text-[13px] font-semibold text-text-primary">OpportunityOS AI</span>
          <span className="text-[10px] text-text-secondary bg-gray-100 px-2 py-0.5 rounded-full">Advisor</span>
        </div>

        {/* Natural Loading */}
        {loading && <SkeletonBlock />}

        {/* Error */}
        {err && (
          <div className="bg-red-50 border border-red-200 rounded-xl p-5 flex items-start gap-3">
            <div className="w-5 h-5 rounded-full bg-red-100 flex items-center justify-center flex-shrink-0 mt-0.5">
              <span className="text-red-500 text-xs font-bold">!</span>
            </div>
            <div>
              <p className="text-[14px] font-semibold text-red-700 mb-1">Could not complete your request</p>
              <p className="text-[13px] text-red-600">{err}</p>
            </div>
          </div>
        )}

        {/* Results */}
        {result && !loading && (
          <div className="space-y-6">
            {/* MCA career paths */}
            {query.toLowerCase().includes('mca') && (
              <div className="bg-gradient-to-br from-orange-50 via-amber-50 to-white border border-orange-100 rounded-2xl p-5">
                <h3 className="text-[16px] font-heading font-bold text-text-primary mb-1">Opportunities after MCA</h3>
                <p className="text-[12px] text-text-secondary mb-4">Career paths, study abroad options, and funding based on your MCA background.</p>
                <div className="mb-4">
                  <h4 className="text-[11px] font-bold text-text-secondary uppercase tracking-wider mb-2">Career Paths</h4>
                  <div className="flex flex-wrap gap-1.5">
                    {['Software Engineer', 'Data Scientist', 'AI/ML Engineer', 'Cloud Architect', 'DevOps', 'Cyber Security', 'Full Stack', 'Research'].map((p, i) => (
                      <span key={i} className="px-2.5 py-1 bg-white border border-gray-200 rounded-lg text-[11px] font-medium text-text-primary">{p}</span>
                    ))}
                  </div>
                </div>
                <div>
                  <h4 className="text-[11px] font-bold text-text-secondary uppercase tracking-wider mb-2">Study Abroad</h4>
                  <div className="grid grid-cols-2 sm:grid-cols-3 gap-1.5">
                    {['Germany', 'Canada', 'Ireland', 'Finland', 'Sweden'].map((c, i) => (
                      <div key={i} className="bg-white/70 rounded-lg px-3 py-2 border border-gray-100 text-center">
                        <span className="text-[12px] font-semibold text-text-primary">{c}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* Recommendation */}
            {result.summary && result.summary !== 'No verified opportunities found.' && !result.summary.startsWith('Found') && (
              <div className="bg-gradient-to-br from-orange-50 to-amber-50 border border-orange-100 rounded-2xl p-4">
                <div className="flex items-center gap-1.5 mb-1.5">
                  <Target className="w-3.5 h-3.5 text-primary" />
                  <h4 className="text-[13px] font-bold text-text-primary">Recommendation</h4>
                </div>
                <p className="text-[13px] text-text-secondary leading-relaxed">{result.summary}</p>
              </div>
            )}

            {/* Best Matches */}
            {relevant.length > 0 && (
              <div>
                <h3 className="text-[16px] font-heading font-bold text-text-primary mb-1 flex items-center gap-2">
                  <Target className="w-4 h-4 text-primary" />
                  Best Matches
                </h3>
                <p className="text-[12px] text-text-secondary mb-3">We found {relevant.length} opportunities matching your profile.</p>
                <div className="space-y-2.5">
                  {relevant.map((opp, i) => {
                    const CatIcon = getCategoryIcon(opp.category);
                    const catColor = getCategoryColor(opp.category);
                    const isExpanded = expandedCard === opp.id || expandedCard === `r-${i}`;
                    const provider = formatProvider(opp.provider);
                    const deadline = formatDeadline(opp.deadline);
                    const score = opp.match_score ?? 0;

                    return (
                      <motion.div
                        key={opp.id || `r-${i}`}
                        initial={{ opacity: 0, y: 12 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: i * 0.06 }}
                        className="bg-white border border-gray-100 rounded-2xl overflow-hidden hover:border-gray-200 transition-all"
                      >
                        <div className="p-4 cursor-pointer" onClick={() => setExpandedCard(isExpanded ? null : (opp.id || `r-${i}`))}>
                          <div className="flex items-start gap-3">
                            <div className={`w-10 h-10 rounded-xl ${catColor} flex items-center justify-center flex-shrink-0`}>
                              <CatIcon className="w-4.5 h-4.5" />
                            </div>

                            <div className="flex-1 min-w-0">
                              <div className="flex items-start justify-between gap-2">
                                <div className="min-w-0 flex-1">
                                  <h4 className="text-[14px] font-bold text-text-primary">{opp.title}</h4>
                                  <div className="flex flex-wrap items-center gap-x-2 gap-y-0.5 mt-0.5">
                                    {opp.country && (
                                      <span className="flex items-center gap-1 text-[11px] text-text-secondary">
                                        <MapPin className="w-2.5 h-2.5" />{opp.country}
                                      </span>
                                    )}
                                    {provider && (
                                      <span className="flex items-center gap-1 text-[11px] text-text-secondary">
                                        <Building2 className="w-2.5 h-2.5" />{provider}
                                      </span>
                                    )}
                                  </div>
                                </div>

                                <div className="flex-shrink-0 text-right">
                                  <div className="text-[11px] tracking-wider text-amber-500">{stars(score)}</div>
                                  <div className="text-[10px] font-medium text-text-secondary mt-0.5">{starLabel(score)}</div>
                                </div>
                              </div>

                              <div className="flex flex-wrap items-center gap-x-3 gap-y-1 mt-2 text-[11px]">
                                <span className="flex items-center gap-1 text-emerald-600 font-medium">
                                  <CheckCircle2 className="w-3 h-3" />
                                  Open
                                </span>
                                {deadline && <span className="text-text-secondary">{deadline}</span>}
                              </div>

                              {/* Why */}
                              {score > 0 && (
                                <div className="flex flex-wrap gap-1 mt-2 pt-2 border-t border-gray-50">
                                  {starReasons(score).map((r, ri) => (
                                    <span key={ri} className="text-[10px] px-2 py-0.5 rounded-full bg-green-50 text-green-700 flex items-center gap-0.5">
                                      <CheckCircle2 className="w-2 h-2" /> {r}
                                    </span>
                                  ))}
                                  {opp.eligibility && (
                                    <span className="text-[10px] px-2 py-0.5 rounded-full bg-blue-50 text-blue-700">
                                      {opp.eligibility.split(/[,;]/)[0]?.trim()?.substring(0, 40)}
                                    </span>
                                  )}
                                </div>
                              )}

                              <div className="flex items-center gap-3 mt-2">
                                {opp.official_url && (
                                  <a href={opp.official_url} target="_blank" rel="noopener noreferrer" onClick={e => e.stopPropagation()}
                                    className="inline-flex items-center gap-1 text-[11px] font-medium text-primary hover:text-orange-600 transition-colors">
                                    <ExternalLink className="w-2.5 h-2.5" /> View Details →
                                  </a>
                                )}
                                <span className="text-[10px] text-gray-400 flex items-center gap-1">
                                  {isExpanded ? <ChevronUp className="w-2.5 h-2.5" /> : <ChevronDown className="w-2.5 h-2.5" />}
                                  {isExpanded ? 'Less' : 'More'}
                                </span>
                              </div>
                            </div>
                          </div>
                        </div>

                        {/* Expanded */}
                        {isExpanded && (
                          <motion.div
                            initial={{ height: 0, opacity: 0 }}
                            animate={{ height: 'auto', opacity: 1 }}
                            className="border-t border-gray-50 px-4 py-3 bg-gray-50/30 space-y-2.5"
                          >
                            {opp.eligibility && (
                              <div>
                                <h5 className="text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-0.5">Eligibility</h5>
                                <p className="text-[12px] text-text-secondary">{opp.eligibility}</p>
                              </div>
                            )}
                            {opp.degree && (
                              <div>
                                <h5 className="text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-0.5">Degree Level</h5>
                                <p className="text-[12px] text-text-secondary">{opp.degree}</p>
                              </div>
                            )}
                            {score > 0 && (
                              <div>
                                <h5 className="text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-0.5">Match Assessment</h5>
                                <div className="flex items-center gap-2">
                                  <div className="flex-1 h-1.5 bg-gray-200 rounded-full overflow-hidden">
                                    <motion.div
                                      initial={{ width: 0 }}
                                      animate={{ width: `${score}%` }}
                                      transition={{ duration: 1, ease: 'easeOut' }}
                                      className="h-full bg-gradient-to-r from-primary to-orange-400 rounded-full"
                                    />
                                  </div>
                                  <span className="text-[11px] font-semibold text-text-primary">{score}%</span>
                                </div>
                              </div>
                            )}
                          </motion.div>
                        )}
                      </motion.div>
                    );
                  })}
                </div>

                {/* Floating Actions */}
                <div className="flex flex-wrap gap-1.5 mt-4">
                  {[
                    { icon: BarChart3, label: 'Compare' },
                    { icon: Heart, label: 'Save' },
                    { icon: Share2, label: 'Share' },
                    { icon: FileText, label: 'Application Plan' },
                    { icon: MessageSquare, label: 'Ask Follow-up' },
                  ].map((action, i) => (
                    <button key={i} className="flex items-center gap-1 px-3 py-1.5 bg-white border border-gray-200 rounded-lg text-[11px] text-text-secondary hover:text-primary hover:border-primary/30 hover:bg-orange-50 transition-all shadow-sm">
                      <action.icon className="w-3 h-3" />
                      {action.label}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* No results */}
            {relevant.length === 0 && loans.length === 0 && (
              <div className="bg-gray-50 border border-gray-200 rounded-2xl p-6 text-center">
                <div className="w-12 h-12 rounded-2xl bg-gray-100 flex items-center justify-center mx-auto mb-3">
                  <BookOpen className="w-5 h-5 text-gray-400" />
                </div>
                <h4 className="text-[15px] font-bold text-text-primary mb-1">Exploring your options</h4>
                <p className="text-[13px] text-text-secondary max-w-[400px] mx-auto">
                  Couldn't find active scholarships matching your exact criteria. Try telling me more about your interests.
                </p>
              </div>
            )}

            {/* Loans */}
            {loans.length > 0 && (
              <div>
                <h4 className="text-[13px] font-bold text-text-primary mb-2 flex items-center gap-1.5">
                  <DollarSign className="w-3.5 h-3.5 text-primary" />
                  Need financial support?
                </h4>
                <div className="space-y-1">
                  {loans.slice(0, 3).map((opp, i) => (
                    <div key={`l-${i}`} className="flex items-center justify-between px-3.5 py-2.5 bg-white border border-gray-100 rounded-xl">
                      <div className="flex items-center gap-2.5 min-w-0">
                        <div className="w-6 h-6 rounded-lg bg-emerald-50 flex items-center justify-center flex-shrink-0">
                          <Building2 className="w-3 h-3 text-emerald-600" />
                        </div>
                        <span className="text-[12px] font-medium text-text-primary truncate">{opp.title}</span>
                      </div>
                      {opp.official_url && (
                        <a href={opp.official_url} target="_blank" rel="noopener noreferrer" className="text-[10px] text-primary hover:text-orange-600 transition-colors flex-shrink-0 ml-2">
                          View →
                        </a>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Follow-ups */}
            {result.follow_up_questions && result.follow_up_questions.length > 0 && (
              <div className="pt-2">
                <h4 className="text-[12px] font-bold text-text-secondary mb-2.5">Continue Exploring</h4>
                <div className="flex flex-wrap gap-1.5">
                  {[
                    'Compare with Erasmus',
                    'Estimate my chances',
                    'Show easier scholarships',
                    'Create application roadmap',
                    'Find universities',
                    'Find internships',
                  ].map((q, i) => (
                    <span key={i} className="px-3 py-1.5 bg-gray-100 border border-gray-200 rounded-lg text-[11px] text-text-secondary hover:bg-gray-200 hover:text-text-primary transition-all cursor-pointer shadow-sm">
                      {q}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </motion.div>
  );
};
