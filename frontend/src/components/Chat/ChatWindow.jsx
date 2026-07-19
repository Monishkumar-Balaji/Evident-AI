import { useRef, useEffect } from 'react';
import { AnimatePresence } from 'framer-motion';
import MessageBubble from './MessageBubble';
import TypingIndicator from './TypingIndicator';
import ChatInput from './ChatInput';
import { IoShieldCheckmark } from 'react-icons/io5';

export default function ChatWindow({
  messages,
  loading,
  hasDocuments,
  onSend,
  onAttach,
  onShowAnalysis,
  onRegenerate,
}) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  return (
    <div className="flex flex-col h-full">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-6 py-4">
        {messages.length === 0 && !loading ? (
          <div className="h-full flex flex-col items-center justify-center text-center">
            <div className="w-16 h-16 bg-accent rounded-2xl flex items-center justify-center mb-4">
              <IoShieldCheckmark className="text-primary text-3xl" />
            </div>
            <h2 className="text-xl font-semibold text-text mb-2">
              Start a conversation
            </h2>
            <p className="text-sm text-muted max-w-sm">
              Ask questions about your uploaded documents. Every answer comes with confidence scoring and evidence tracking.
            </p>
          </div>
        ) : (
          <>
            {messages.map((msg, i) => (
              <MessageBubble
                key={msg.id}
                message={msg}
                isLast={i === messages.length - 1 && msg.role === 'assistant'}
                onShowAnalysis={onShowAnalysis}
                onRegenerate={i === messages.length - 1 && msg.role === 'assistant' ? onRegenerate : null}
              />
            ))}

            <AnimatePresence>
              {loading && <TypingIndicator />}
            </AnimatePresence>
          </>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <ChatInput
        onSend={onSend}
        onAttach={onAttach}
        disabled={loading}
        hasDocuments={hasDocuments}
      />
    </div>
  );
}
