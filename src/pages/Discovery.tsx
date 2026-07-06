import { ArrowLeft } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { ChatArea } from '../components/workspace/ChatArea';

export default function Discovery() {
  const navigate = useNavigate();

  return (
    <div className="flex h-screen bg-[#0F172A] overflow-hidden">
      <button
        onClick={() => navigate('/')}
        className="fixed top-4 left-4 z-50 p-2 rounded-lg bg-[#1E293B] border border-gray-700/50 text-gray-400 hover:text-white hover:border-[#FF7A00]/30 transition-all duration-200"
      >
        <ArrowLeft className="w-5 h-5" />
      </button>
      <ChatArea />
    </div>
  );
}
