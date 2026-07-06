import { Sparkles } from 'lucide-react';

export const AnalysisPanel = ({ active }: { active: boolean }) => {
  return (
    <aside className="fixed top-[64px] right-0 bottom-0 w-[280px] bg-white/70 backdrop-blur-xl border-l border-gray-100 hidden xl:flex flex-col z-40 overflow-hidden">
      <div className="flex-1 flex flex-col p-5 overflow-y-auto scrollbar-hide">
        <div className="flex items-center gap-2 mb-6">
          <div className="w-5 h-5 rounded-lg bg-gradient-to-br from-primary to-orange-400 flex items-center justify-center">
            <Sparkles className="w-3 h-3 text-white" />
          </div>
          <span className="font-heading font-semibold text-[14px] text-text-primary">OpportunityOS AI</span>
        </div>

        {!active && (
          <div className="text-center text-[13px] text-text-secondary py-10">
            Your analysis will appear here once you start a conversation.
          </div>
        )}

        {active && (
          <div className="space-y-5">
            <div>
              <p className="text-[11px] font-bold text-gray-400 uppercase tracking-widest mb-2">Analysis</p>
              <div className="bg-gradient-to-br from-orange-50 to-amber-50 rounded-xl p-4 border border-orange-100">
                <p className="text-[12px] text-text-secondary">Analysis panel shows real-time insights as you explore opportunities.</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </aside>
  );
};
