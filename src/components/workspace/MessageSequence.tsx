import { useState, useEffect } from 'react';
import { ChevronDown, ChevronRight } from 'lucide-react';
import { discoverOpportunities, type DiscoverResponse } from '../../lib/api';

function clusterDuplicates(opps: DiscoverResponse['opportunities']): DiscoverResponse['opportunities'] {
  const seen = new Set<string>();
  return opps.filter((opp) => {
    const key = (opp.title || opp.provider || '').toLowerCase().slice(0, 30);
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

export const MessageSequence = ({ query }: { query: string }) => {
  const [result, setResult] = useState<DiscoverResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showReasoning, setShowReasoning] = useState(false);

  useEffect(() => {
    let mounted = true;
    setLoading(true);
    setError(null);

    discoverOpportunities(query)
      .then((data) => {
        if (mounted) setResult(data);
      })
      .catch((err) => {
        if (mounted) setError(err.message);
      })
      .finally(() => {
        if (mounted) setLoading(false);
      });

    return () => { mounted = false; };
  }, [query]);

  if (loading) {
    return (
      <div className="flex items-start gap-4 p-6 border-b border-gray-100">
        <div className="w-8 h-8 rounded-full bg-gradient-to-r from-orange-500 to-orange-400 flex items-center justify-center text-white text-sm font-bold flex-shrink-0">
          F
        </div>
        <div className="flex-1 space-y-3">
          <div className="h-4 bg-gray-200 rounded animate-pulse w-3/4" />
          <div className="h-4 bg-gray-200 rounded animate-pulse w-1/2" />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-start gap-4 p-6 border-b border-gray-100">
        <div className="w-8 h-8 rounded-full bg-gradient-to-r from-orange-500 to-orange-400 flex items-center justify-center text-white text-sm font-bold flex-shrink-0">
          F
        </div>
        <div className="flex-1">
          <p className="text-red-500">Connection error. Please try again.</p>
        </div>
      </div>
    );
  }

  if (!result) return null;

  const topOpps = clusterDuplicates(result.opportunities).slice(0, 3);

  return (
    <div className="border-b border-gray-100">
      <div className="flex items-start gap-4 p-6">
        <div className="w-8 h-8 rounded-full bg-gradient-to-r from-orange-500 to-orange-400 flex items-center justify-center text-white text-sm font-bold flex-shrink-0">
          F
        </div>
        <div className="flex-1 space-y-4">
          {/* Summary / Answer */}
          <p className="text-gray-800 leading-relaxed text-sm">{result.summary}</p>

          {/* Recommended Programs */}
          {topOpps.length > 0 && (
            <div className="space-y-2">
              <h4 className="text-xs font-semibold text-gray-400 uppercase tracking-wider">Recommended Programs</h4>
              {topOpps.map((opp, i) => (
                <div key={i} className="bg-gray-50 rounded-lg px-4 py-3 border border-gray-100">
                  <div className="flex items-start justify-between gap-2">
                    <div className="flex-1 min-w-0">
                      <h3 className="text-gray-900 font-medium text-sm">{opp.title}</h3>
                      <div className="flex flex-wrap gap-x-2 text-xs text-gray-500 mt-0.5">
                        {opp.provider && <span>{opp.provider}</span>}
                        {opp.country && <span>• {opp.country}</span>}
                        {opp.deadline && opp.deadline !== 'Unknown' && <span>• {opp.deadline}</span>}
                      </div>
                    </div>
                    {opp.match_score && (
                      <span className={`text-[10px] font-medium px-1.5 py-0.5 rounded flex-shrink-0 ${
                        opp.match_score >= 70 ? 'bg-green-100 text-green-700' :
                        opp.match_score >= 40 ? 'bg-blue-100 text-blue-700' :
                        'bg-gray-100 text-gray-500'
                      }`}>
                        {opp.match_score >= 70 ? 'Best' : opp.match_score >= 40 ? 'Good' : 'Fair'}
                      </span>
                    )}
                  </div>
                  {opp.eligibility && <p className="text-xs text-gray-500 mt-1.5 leading-relaxed">{opp.eligibility.slice(0, 120)}</p>}
                  {opp.official_url && opp.official_url !== 'Unknown' && (
                    <a href={opp.official_url} target="_blank" rel="noopener noreferrer"
                       className="inline-block text-xs text-orange-600 hover:underline mt-1.5">
                      Official link →
                    </a>
                  )}
                </div>
              ))}
            </div>
          )}

          {/* Next Steps */}
          {result.groq_reasoning?.roadmap && result.groq_reasoning.roadmap.length > 0 && (
            <div className="bg-gray-50 rounded-lg px-4 py-3 border border-gray-100">
              <h4 className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Next Steps</h4>
              <ol className="list-decimal list-inside space-y-1">
                {result.groq_reasoning.roadmap.map((step, i) => (
                  <li key={i} className="text-sm text-gray-600">{step}</li>
                ))}
              </ol>
            </div>
          )}

          {/* Toggle reasoning */}
          {result.groq_reasoning?.reasoning && result.groq_reasoning.reasoning.length > 0 && (
            <div>
              <button
                onClick={() => setShowReasoning(!showReasoning)}
                className="flex items-center gap-1 text-xs text-gray-400 hover:text-gray-600 transition-colors"
              >
                {showReasoning ? <ChevronDown className="w-3 h-3" /> : <ChevronRight className="w-3 h-3" />}
                How I found these
              </button>
              {showReasoning && (
                <div className="mt-2 bg-gray-50 rounded-lg px-4 py-3 border border-gray-100 space-y-1">
                  {result.groq_reasoning.reasoning.map((step, i) => (
                    <p key={i} className="text-xs text-gray-500">{step}</p>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
