import { motion, AnimatePresence } from 'framer-motion';
import { useEffect } from 'react';
import { IoCheckmarkCircle, IoCloseCircle, IoInformationCircle } from 'react-icons/io5';

const icons = {
  success: <IoCheckmarkCircle className="text-success text-xl flex-shrink-0" />,
  error: <IoCloseCircle className="text-danger text-xl flex-shrink-0" />,
  info: <IoInformationCircle className="text-primary text-xl flex-shrink-0" />,
};

const bgColors = {
  success: 'bg-green-50 border-success',
  error: 'bg-red-50 border-danger',
  info: 'bg-accent border-primary',
};

export default function Toast({ message, type = 'info', onClose, duration = 4000 }) {
  useEffect(() => {
    const timer = setTimeout(onClose, duration);
    return () => clearTimeout(timer);
  }, [onClose, duration]);

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0, y: -20, scale: 0.95 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        exit={{ opacity: 0, y: -20, scale: 0.95 }}
        className={`fixed top-5 right-5 z-50 flex items-center gap-3 px-5 py-3 rounded-xl border shadow-lg ${bgColors[type]} max-w-sm`}
      >
        {icons[type]}
        <span className="text-sm font-medium text-text">{message}</span>
        <button
          onClick={onClose}
          className="ml-2 text-muted hover:text-text transition-colors cursor-pointer"
        >
          ✕
        </button>
      </motion.div>
    </AnimatePresence>
  );
}
