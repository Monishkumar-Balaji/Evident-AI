import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { IoCopy, IoAnalytics, IoRefresh, IoTime, IoDocumentText, IoCheckmarkCircle } from 'react-icons/io5';

function ConfidenceBadge({ confidence }) {
  if (!confidence) return null;

  const score = confidence.score || 0;
  const level = confidence.level || 'NONE';

  let color = 'bg-red-100 text-red-700';
  if (score >= 85) color = 'bg-green-100 text-green-700';
  else if (score >= 70) color = 'bg-yellow-100 text-yellow-700';
  else if (score >= 50) color = 'bg-orange-100 text-orange-700';

  return (
    <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-semibold ${color}`}>
      {score}% {level}
    </span>
  );
}

function TypingText({ text }) {
  const [displayed, setDisplayed] = useState('');
  const [done, setDone] = useState(false);

  useEffect(() => {
    if (!text) return;
    let i = 0;
    setDisplayed('');
    setDone(false);

    const interval = setInterval(() => {
      if (i < text.length) {
        setDisplayed(text.slice(0, i + 1));
        i++;
      } else {
        setDone(true);
        clearInterval(interval);
      }
    }, 12);

    return () => clearInterval(interval);
  }, [text]);

  return (
    <span>
      {displayed}
      {!done && <span className="typing-cursor" />}
    </span>
  );
}

export default function MessageBubble({ message, isLast, onShowAnalysis, onRegenerate }) {
  const isUser = message.role === 'user';
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(message.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={`flex mb-4 ${isUser ? 'justify-end' : 'justify-start'}`}
    >
      <div className={`max-w-[80%] ${isUser ? '' : 'w-full max-w-2xl'}`}>
        <div
          className={`rounded-2xl px-5 py-3.5 ${
            isUser
              ? 'bg-primary text-white rounded-tr-sm'
              : message.isError
                ? 'bg-red-50 border border-danger/30 text-danger rounded-tl-sm'
                : 'bg-card border border-border shadow-sm rounded-tl-sm'
          }`}
        >
          {/* Message content */}
          <div className={`text-base leading-relaxed ${isUser ? 'text-white' : 'text-text'}`}>
            {!isUser && isLast && !message.isError ? (
              <TypingText text={message.content} />
            ) : (
              message.content
            )}
          </div>
        </div>

        {/* Assistant message footer */}
        {!isUser && !message.isError && (
          <div className="mt-3 flex flex-col gap-3">
            <div className="flex flex-wrap items-center gap-2">
              {/* Confidence */}
              {message.confidence && (
                <ConfidenceBadge confidence={message.confidence} />
              )}

              {/* Sources */}
              {message.sources?.map((src, i) => (
                <span key={i} className="inline-flex items-center gap-1 text-xs text-muted bg-accent px-2 py-0.5 rounded-full">
                  <IoDocumentText className="text-primary" />
                  {src.source} p.{src.page}
                </span>
              ))}

              {/* Time */}
              {message.time_taken && (
                <span className="inline-flex items-center gap-1 text-xs text-muted">
                  <IoTime /> {message.time_taken}s
                </span>
              )}
            </div>

            {/* Action buttons */}
            <div className="flex items-center gap-3">
              <button
                onClick={handleCopy}
                className="flex items-center gap-1.5 px-3 py-1.5 text-muted hover:text-primary hover:bg-accent rounded-lg transition-all cursor-pointer text-sm font-medium border border-transparent hover:border-border"
                title="Copy answer"
              >
                {copied ? <IoCheckmarkCircle className="text-primary text-base" /> : <IoCopy className="text-base" />}
                <span>Copy</span>
              </button>

              {message.analysis && (
                <button
                  onClick={() => onShowAnalysis?.(message)}
                  className="flex items-center gap-1.5 px-3 py-1.5 text-muted hover:text-primary hover:bg-accent rounded-lg transition-all cursor-pointer text-sm font-medium border border-transparent hover:border-border"
                  title="Show Analysis"
                >
                  <IoAnalytics className="text-base" />
                  <span>Show Analysis</span>
                </button>
              )}

              {isLast && onRegenerate && (
                <button
                  onClick={onRegenerate}
                  className="flex items-center gap-1.5 px-3 py-1.5 text-muted hover:text-primary hover:bg-accent rounded-lg transition-all cursor-pointer text-sm font-medium border border-transparent hover:border-border"
                  title="Regenerate"
                >
                  <IoRefresh className="text-base" />
                  <span>Regenerate</span>
                </button>
              )}
            </div>
          </div>
        )}
      </div>
    </motion.div>
  );
}
