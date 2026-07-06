import { useLocation, useNavigate } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';

export const Navbar = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const isWorkspace = location.pathname.startsWith('/discover');

  return (
    <header className="fixed top-0 left-0 right-0 z-[100] h-[64px] flex items-center bg-white/70 backdrop-blur-xl border-b border-gray-100">
      <div className={`flex items-center justify-between px-6 w-full ${isWorkspace ? '' : 'max-w-[1400px] mx-auto'}`}>
        <div className="flex items-center gap-3">
          {isWorkspace && (
            <button onClick={() => navigate('/')} className="w-7 h-7 rounded-lg bg-gray-100 hover:bg-gray-200 flex items-center justify-center transition-colors flex-shrink-0">
              <ArrowLeft className="w-3.5 h-3.5 text-text-secondary" />
            </button>
          )}
          <div className="flex items-center gap-2.5">
            <div className="w-7 h-7 rounded-lg bg-gradient-to-br from-primary to-orange-400 flex items-center justify-center text-white font-bold text-[11px] shadow-sm">
              O
            </div>
            <div>
              <span className="font-heading text-[15px] font-bold tracking-tight text-text-primary">OpportunityOS AI</span>
              <p className="text-[10px] text-text-secondary leading-none">Your AI Opportunity Advisor</p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <span className="hidden sm:flex items-center gap-1.5 px-2.5 py-1 bg-emerald-50 border border-emerald-200 rounded-full text-[10px] font-medium text-emerald-700">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
            Verified Sources Enabled
          </span>
        </div>
      </div>
    </header>
  );
};
