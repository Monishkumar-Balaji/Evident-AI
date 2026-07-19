import { useState, useRef, useEffect } from 'react';
import { IoSend, IoAttach } from 'react-icons/io5';

export default function ChatInput({ onSend, onAttach, disabled, hasDocuments }) {
  const [text, setText] = useState('');
  const textareaRef = useRef(null);

  const isDisabled = disabled || !hasDocuments;

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 150) + 'px';
    }
  }, [text]);

  const handleSend = () => {
    const trimmed = text.trim();
    if (!trimmed || isDisabled) return;
    onSend(trimmed);
    setText('');
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="border-t border-border bg-card p-4">
      <div className={`flex items-end gap-3 bg-background border border-border rounded-2xl px-4 py-3 transition-all
        ${isDisabled ? 'opacity-50' : 'focus-within:border-primary/50 focus-within:shadow-sm'}
      `}>
        <button
          onClick={onAttach}
          disabled={disabled}
          className="text-muted hover:text-primary transition-colors pb-0.5 cursor-pointer disabled:cursor-not-allowed"
          title="Attach PDF"
          id="attach-pdf-btn"
        >
          <IoAttach className="text-xl" />
        </button>

        <textarea
          ref={textareaRef}
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={
            hasDocuments
              ? 'Ask anything about your uploaded documents...'
              : 'Upload a document first to start asking questions...'
          }
          disabled={isDisabled}
          rows={1}
          className="flex-1 resize-none bg-transparent text-text text-sm placeholder:text-muted focus:outline-none disabled:cursor-not-allowed max-h-[150px]"
          id="chat-input"
        />

        <button
          onClick={handleSend}
          disabled={isDisabled || !text.trim()}
          className={`p-2 rounded-xl transition-all cursor-pointer
            ${text.trim() && !isDisabled
              ? 'bg-primary text-white hover:bg-primary-dark shadow-sm'
              : 'bg-border text-muted cursor-not-allowed'
            }`}
          title="Send message"
          id="send-btn"
        >
          <IoSend className="text-sm" />
        </button>
      </div>

      {!hasDocuments && (
        <p className="text-xs text-muted text-center mt-2">
          Upload at least one document to start asking questions
        </p>
      )}
    </div>
  );
}
