import { useState } from 'react';
import { Sidebar } from '../components/workspace/Sidebar';
import { AnalysisPanel } from '../components/workspace/AnalysisPanel';
import { ChatArea } from '../components/workspace/ChatArea';
import { Navbar } from '../components/layout/Navbar';
import { PageTransition } from '../components/motion/PageTransition';

export const Discovery = () => {
  const [analysisActive, setAnalysisActive] = useState(false);

  return (
    <PageTransition>
      <div className="w-full h-screen overflow-hidden relative" style={{ backgroundColor: '#f8fafc' }}>
        {/* Chat background */}
        <div className="absolute inset-0 bg-cover bg-center opacity-[0.12] pointer-events-none" style={{ backgroundImage: "url('/bgcchat.png')", backgroundAttachment: 'fixed' }} />
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-white/40 pointer-events-none" />

        {/* Fixed Navbar — full width, 80px */}
        <Navbar />

        {/* Three-column layout starting below 80px navbar */}
        <Sidebar />
        <ChatArea onAnalysisActive={setAnalysisActive} />
        <AnalysisPanel active={analysisActive} />

        {/* Mobile fallback — full-width chat on small screens */}
        <div className="lg:hidden flex flex-col min-h-screen pt-[64px]">
          <div className="flex-1 overflow-y-auto px-4 py-6">
            <div className="text-center text-text-secondary pt-20 text-[16px]">
              AI Workspace is optimized for desktop. Please use a larger screen for the best experience.
            </div>
          </div>
        </div>
      </div>
    </PageTransition>
  );
};
