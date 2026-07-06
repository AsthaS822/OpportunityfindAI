import { MessageSquare, Plus, Sparkles, Menu, X } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export const Sidebar = ({ sidebarOpen, onToggleSidebar }: { sidebarOpen: boolean; onToggleSidebar: () => void }) => {
  const navigate = useNavigate();

  const chatHistory = [
    { id: '1', title: 'Loan opportunities for higher studies...', active: true },
    { id: '2', title: 'PhD in Computer Science Europe', active: false },
    { id: '3', title: 'Scholarships after MCA', active: false },
    { id: '4', title: 'Study in Germany without IELTS', active: false },
  ];

  return (
    <>
      <button
        onClick={onToggleSidebar}
        className="fixed top-4 left-4 z-50 p-2 rounded-lg bg-[#1E293B] border border-gray-700/50 text-gray-400 hover:text-white hover:border-[#FF7A00]/30 transition-all duration-200"
      >
        {sidebarOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
      </button>

      <div
        className={`${
          sidebarOpen ? 'translate-x-0' : '-translate-x-full'
        } fixed left-0 top-0 h-full w-72 bg-[#1E293B]/95 backdrop-blur-xl border-r border-gray-800/50 transition-transform duration-300 ease-in-out z-40`}
      >
        <div className="flex flex-col h-full pt-16 px-3">
          {/* Logo */}
          <div className="flex items-center gap-2.5 px-2 py-4 mb-2">
            <div className="w-7 h-7 rounded-lg bg-gradient-to-br from-[#FF7A00] to-[#FF9A3D] flex items-center justify-center text-white font-bold text-[11px] shadow-sm">
              F
            </div>
            <span className="font-heading text-[15px] font-bold tracking-tight text-white">FutureOS</span>
          </div>

          {/* New Chat */}
          <button
            onClick={() => navigate('/discover')}
            className="flex items-center gap-2.5 px-3 py-2.5 rounded-lg text-gray-400 hover:text-white hover:bg-gray-700/30 transition-all text-sm mb-4"
          >
            <Plus className="w-4 h-4" />
            <span>New Chat</span>
          </button>

          {/* Navigation */}
          <div className="mb-4 px-2">
            <p className="text-[10px] font-semibold uppercase tracking-widest text-gray-500 mb-2">Navigation</p>
            <button
              onClick={() => navigate('/')}
              className="flex items-center gap-2.5 px-3 py-2 rounded-lg text-gray-400 hover:text-white hover:bg-gray-700/30 transition-all text-sm w-full text-left"
            >
              <Sparkles className="w-4 h-4" />
              <span>Home</span>
            </button>
          </div>

          {/* Divider */}
          <div className="border-t border-gray-700/30 mb-4" />

          {/* Chat History */}
          <div className="flex-1 overflow-y-auto space-y-1 px-1">
            <p className="text-[10px] font-semibold uppercase tracking-widest text-gray-500 mb-2 px-1">Recent Chats</p>
            {chatHistory.map((chat) => (
              <button
                key={chat.id}
                className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm transition-all text-left ${
                  chat.active
                    ? 'bg-[#FF7A00]/10 text-[#FF7A00] border border-[#FF7A00]/20'
                    : 'text-gray-400 hover:text-white hover:bg-gray-700/30'
                }`}
              >
                <MessageSquare className="w-3.5 h-3.5 flex-shrink-0" />
                <span className="truncate">{chat.title}</span>
              </button>
            ))}
          </div>
        </div>
      </div>
    </>
  );
};
