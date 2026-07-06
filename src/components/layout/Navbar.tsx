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
              <span className="font-heading text-[15px] font-bold tracking-tight text-text-primary">FutureOS</span>
              <p className="text-[10px] text-text-secondary leading-none">Your AI Career Advisor</p>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};
