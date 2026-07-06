import { useRef } from 'react';
import { useState } from 'react';
import { ChatInput } from './ChatInput';
import { MessageEmptyState } from './MessageEmptyState';
import { MessageSequence } from './MessageSequence';

export const ChatArea = ({ onAnalysisActive }: { onAnalysisActive: (v: boolean) => void }) => {
  const [messages, setMessages] = useState<string[]>([]);
  const bottomRef = useRef<HTMLDivElement>(null);

  const handleSend = (text: string) => {
    setMessages(prev => [...prev, text]);
    onAnalysisActive(true);
    setTimeout(() => bottomRef.current?.scrollIntoView({ behavior: 'smooth' }), 100);
  };

  return (
    <div className="fixed top-[80px] bottom-0 left-[280px] right-0 xl:right-[280px] flex flex-col hidden lg:flex xl:flex overflow-hidden">
      {/* Soft background blobs */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden z-0">
        <div className="absolute top-[-10%] left-[-5%] w-[400px] h-[400px] bg-primary/4 rounded-full blur-[100px]" />
        <div className="absolute bottom-[-10%] right-[-5%] w-[400px] h-[400px] bg-secondary/4 rounded-full blur-[100px]" />
      </div>

      {/* Scrollable conversation */}
      <div className="flex-1 overflow-y-auto px-8 py-6 relative z-10 scrollbar-hide">
        {messages.length === 0 ? (
          <MessageEmptyState onSelect={handleSend} />
        ) : (
          <div className="flex flex-col">
            {messages.map((m, i) => (
              <MessageSequence key={i} query={m} />
            ))}
            <div ref={bottomRef} />
          </div>
        )}
      </div>

      {/* Pinned input */}
      <div className="relative z-10">
        <ChatInput onSend={handleSend} />
      </div>
    </div>
  );
};
