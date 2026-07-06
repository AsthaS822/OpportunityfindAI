import { useRef, useState, useEffect } from 'react';
import { ChatInput, type ChatInputHandle } from './ChatInput';
import { MessageSequence } from './MessageSequence';
import { MessageEmptyState } from './MessageEmptyState';

export const ChatArea = () => {
  const [messages, setMessages] = useState<string[]>([]);
  const inputRef = useRef<ChatInputHandle>(null);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: 'smooth' });
  }, [messages]);

  const handleSend = (query: string) => {
    setMessages(prev => [...prev, query]);
  };

  const handleSelectExample = (text: string) => {
    inputRef.current?.setValue(text);
  };

  if (messages.length === 0) {
    return (
      <div className="flex-1 flex flex-col h-full bg-white">
        <div className="flex-1 overflow-y-auto" ref={scrollRef}>
          <MessageEmptyState onSelect={handleSelectExample} />
        </div>
        <ChatInput ref={inputRef} onSend={handleSend} />
      </div>
    );
  }

  return (
    <div className="flex-1 flex flex-col h-full bg-white">
      <div className="flex-1 overflow-y-auto" ref={scrollRef}>
        {messages.map((msg, i) => (
          <MessageSequence key={i} query={msg} />
        ))}
      </div>
      <ChatInput ref={inputRef} onSend={handleSend} />
    </div>
  );
};
