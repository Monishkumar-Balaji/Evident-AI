import { motion } from 'framer-motion';
import { IoAnalytics } from 'react-icons/io5';
import ConfidenceGauge from './ConfidenceGauge';
import RetrievalBar from './RetrievalBar';
import VerificationBadge from './VerificationBadge';
import EvidenceBars from './EvidenceBars';
import SourceCards from './SourceCards';

export default function AnalyticsPanel({ message, isOpen, onClose }) {
  const hasData = message && message.role === 'assistant' && !message.isError;

  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div className="fixed inset-0 bg-black/30 z-40 lg:hidden" onClick={onClose} />
      )}

      <motion.div
        initial={false}
        animate={{ x: isOpen || window.innerWidth >= 1024 ? 0 : '100%' }}
        className={`fixed right-0 top-0 h-full w-80 lg:relative lg:w-full lg:translate-x-0 z-50 lg:z-auto
          bg-card border-l border-border overflow-y-auto`}
      >
        <div className="p-4 border-b border-border flex items-center gap-2">
          <IoAnalytics className="text-primary text-lg" />
          <h2 className="text-sm font-semibold text-text">Analytics</h2>
          <button
            onClick={onClose}
            className="lg:hidden ml-auto text-muted hover:text-text text-sm cursor-pointer"
          >
            ✕
          </button>
        </div>

        <div className="p-4 space-y-6">
          {!hasData ? (
            <div className="text-center py-12">
              <IoAnalytics className="text-4xl text-border mx-auto mb-3" />
              <p className="text-sm text-muted">
                Ask a question to see analytics
              </p>
            </div>
          ) : (
            <>
              {/* Confidence Gauge */}
              <div className="bg-background rounded-xl p-4 text-center">
                <h3 className="text-xs font-semibold text-muted uppercase tracking-wider mb-3">
                  Confidence
                </h3>
                <ConfidenceGauge confidence={message.confidence} />
              </div>

              {/* Retrieval Quality */}
              <div className="bg-background rounded-xl p-4">
                <RetrievalBar retrievalQuality={message.retrieval_quality} />
              </div>

              {/* Verification */}
              <div className="bg-background rounded-xl p-4">
                <VerificationBadge verification={message.verification} />
              </div>

              {/* Evidence Bars */}
              <div className="bg-background rounded-xl p-4">
                <EvidenceBars evidence={message.evidence} />
              </div>

              {/* Sources */}
              <div className="bg-background rounded-xl p-4">
                <SourceCards sources={message.sources} />
              </div>
            </>
          )}
        </div>
      </motion.div>
    </>
  );
}
