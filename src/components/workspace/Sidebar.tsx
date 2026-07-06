import { motion } from 'framer-motion';
import { Plus, Heart, Calendar, Clock, Settings } from 'lucide-react';

const recentChats = [
  { emoji: '🇩🇪', title: 'Germany Scholarship' },
  { emoji: '🎓', title: 'MCA Career' },
  { emoji: '💰', title: 'Education Loan' },
  { emoji: '🏛', title: 'PM Scholarship' },
  { emoji: '🌍', title: 'Erasmus' },
];

export const Sidebar = () => {
  return (
    <aside className="fixed top-[64px] left-0 bottom-0 w-[280px] bg-white/70 backdrop-blur-xl border-r border-gray-100 flex flex-col z-40 hidden lg:flex overflow-hidden">
      <div className="flex-1 flex flex-col p-4 gap-4 overflow-y-auto scrollbar-hide">
        <button className="flex items-center justify-center gap-2 w-full h-[44px] rounded-xl bg-gradient-to-r from-primary to-orange-400 text-white font-semibold text-[13px] shadow-sm hover:shadow-md hover:scale-[1.02] transition-all">
          <Plus className="w-4 h-4" /> New Chat
        </button>

        <div className="space-y-1">
          <p className="text-[11px] font-bold text-gray-400 uppercase tracking-widest mb-2">Recent Conversations</p>
          {recentChats.map((chat, i) => (
            <motion.button
              key={i}
              whileHover={{ x: 3 }}
              className="flex items-center gap-2.5 w-full px-3 py-2.5 rounded-xl text-[13px] text-text-secondary hover:text-text-primary hover:bg-gray-50 transition-all text-left"
            >
              <span className="text-[15px]">{chat.emoji}</span>
              <span className="truncate">{chat.title}</span>
            </motion.button>
          ))}
        </div>

        <div className="mt-auto pt-4 border-t border-gray-100 space-y-0.5">
          <SidebarItem icon={Heart} label="Saved Opportunities" />
          <SidebarItem icon={Calendar} label="Application Tracker" />
          <SidebarItem icon={Clock} label="Deadlines" />
          <SidebarItem icon={Settings} label="Settings" />
        </div>

        {/* User Profile Card */}
        <div className="pt-3 border-t border-gray-100">
          <div className="bg-white border border-gray-100 rounded-xl p-3.5 shadow-sm">
            <div className="flex items-center gap-2.5 mb-2.5">
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-primary to-orange-400 flex items-center justify-center text-white font-bold text-[12px]">
                AS
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-[13px] font-semibold text-text-primary">Astha Singh</p>
                <p className="text-[10px] text-text-secondary">Online</p>
              </div>
              <span className="w-2 h-2 rounded-full bg-emerald-500" />
            </div>
            <div className="space-y-1 text-[11px] text-text-secondary">
              <div className="flex items-center gap-2">
                <span className="text-gray-400 w-16">Education</span>
                <span className="font-medium text-text-primary">MCA</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-gray-400 w-16">Country</span>
                <span className="font-medium text-text-primary">India</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-gray-400 w-16">Interest</span>
                <span className="font-medium text-text-primary">AI · Study Abroad</span>
              </div>
            </div>
            <button className="w-full mt-2.5 py-1.5 rounded-lg border border-gray-200 text-[11px] font-medium text-text-secondary hover:bg-gray-50 hover:text-text-primary transition-all">
              Edit Profile
            </button>
          </div>
        </div>
      </div>
    </aside>
  );
};

const SidebarItem = ({ icon: Icon, label }: { icon: any; label: string }) => (
  <button className="flex items-center gap-2.5 w-full px-3 py-2 rounded-xl text-[12px] text-text-secondary hover:text-text-primary hover:bg-gray-50 transition-all">
    <Icon className="w-3.5 h-3.5 text-gray-400 flex-shrink-0" />
    <span>{label}</span>
  </button>
);
