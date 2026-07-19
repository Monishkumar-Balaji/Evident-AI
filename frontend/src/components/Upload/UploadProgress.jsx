import { motion } from 'framer-motion';
import { IoCheckmarkCircle } from 'react-icons/io5';

const steps = [
  { key: 'uploading', label: 'Uploading files...' },
  { key: 'indexing', label: 'Indexing documents...' },
  { key: 'embedding', label: 'Creating embeddings...' },
  { key: 'ready', label: 'Ready!' },
];

function getStepIndex(progress) {
  if (!progress) return -1;
  if (progress === 'uploading') return 0;
  if (progress === 'indexing') return 1;
  if (progress === 'embedding') return 2;
  if (progress === 'ready') return 3;
  return -1;
}

export default function UploadProgress({ progress }) {
  const currentIndex = getStepIndex(progress);

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-card rounded-xl border border-border p-6 shadow-sm"
    >
      <div className="space-y-3">
        {steps.map((step, i) => {
          const isComplete = i < currentIndex;
          const isCurrent = i === currentIndex;

          return (
            <div key={step.key} className="flex items-center gap-3">
              <div className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold transition-all duration-500
                ${isComplete ? 'bg-primary text-white' : isCurrent ? 'bg-secondary text-primary' : 'bg-border text-muted'}
              `}>
                {isComplete ? (
                  <IoCheckmarkCircle className="text-base" />
                ) : (
                  <span>{i + 1}</span>
                )}
              </div>
              <span className={`text-sm transition-colors duration-300 ${
                isComplete ? 'text-primary font-medium' : isCurrent ? 'text-text font-medium' : 'text-muted'
              }`}>
                {step.label}
              </span>
              {isCurrent && !isComplete && step.key !== 'ready' && (
                <div className="ml-auto">
                  <div className="w-4 h-4 border-2 border-primary border-t-transparent rounded-full animate-spin" />
                </div>
              )}
            </div>
          );
        })}
      </div>

      {currentIndex >= 0 && (
        <div className="mt-4 w-full bg-border rounded-full h-2 overflow-hidden">
          <motion.div
            className="h-full bg-gradient-to-r from-primary to-secondary rounded-full"
            initial={{ width: '0%' }}
            animate={{ width: `${((currentIndex + 1) / steps.length) * 100}%` }}
            transition={{ duration: 0.8, ease: 'easeInOut' }}
          />
        </div>
      )}
    </motion.div>
  );
}
