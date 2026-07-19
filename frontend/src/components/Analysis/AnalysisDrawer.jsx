import { motion, AnimatePresence } from 'framer-motion';
import { IoClose, IoAnalytics } from 'react-icons/io5';
import AnalysisContent from './AnalysisContent';

export default function AnalysisDrawer({ isOpen, message, onClose }) {
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Overlay */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/30 z-50"
            onClick={onClose}
          />

          {/* Drawer */}
          <motion.div
            initial={{ x: '100%' }}
            animate={{ x: 0 }}
            exit={{ x: '100%' }}
            transition={{ type: 'spring', stiffness: 300, damping: 30 }}
            className="fixed right-0 top-0 h-full w-full max-w-lg bg-card border-l border-border z-50 flex flex-col shadow-2xl"
          >
            {/* Header */}
            <div className="flex items-center justify-between p-4 border-b border-border">
              <div className="flex items-center gap-2">
                <IoAnalytics className="text-primary text-lg" />
                <h2 className="text-base font-semibold text-text">Full Analysis</h2>
              </div>
              <button
                onClick={onClose}
                className="p-2 text-muted hover:text-text hover:bg-accent rounded-lg transition-all cursor-pointer"
              >
                <IoClose className="text-lg" />
              </button>
            </div>

            {/* Content */}
            <div className="flex-1 overflow-y-auto p-4">
              <AnalysisContent message={message} />
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
