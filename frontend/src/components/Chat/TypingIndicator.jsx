import { motion } from 'framer-motion';
import { IoCheckmarkCircle } from 'react-icons/io5';
import { useState, useEffect } from 'react';

const thinkingSteps = [
  'Searching documents...',
  'Finding relevant chunks...',
  'Removing weak context...',
  'Generating answer...',
  'Verifying response...',
];

export default function TypingIndicator() {
  const [currentStep, setCurrentStep] = useState(0);
  const [completedSteps, setCompletedSteps] = useState([]);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentStep(prev => {
        if (prev < thinkingSteps.length - 1) {
          setCompletedSteps(completed => [...completed, prev]);
          return prev + 1;
        }
        return prev;
      });
    }, 1200);

    return () => clearInterval(interval);
  }, []);

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      className="flex justify-start mb-4"
    >
      <div className="bg-card border border-border rounded-2xl rounded-tl-sm px-5 py-4 shadow-sm max-w-md">
        <div className="flex items-center gap-2 mb-3">
          <div className="flex gap-1">
            {[0, 1, 2].map(i => (
              <motion.div
                key={i}
                className="w-2 h-2 bg-primary rounded-full"
                animate={{ opacity: [0.3, 1, 0.3], scale: [0.8, 1, 0.8] }}
                transition={{ duration: 1, repeat: Infinity, delay: i * 0.2 }}
              />
            ))}
          </div>
          <span className="text-sm font-medium text-primary">Thinking...</span>
        </div>

        <div className="space-y-2">
          {thinkingSteps.map((step, i) => {
            const isCompleted = completedSteps.includes(i);
            const isCurrent = i === currentStep;
            const isPending = i > currentStep;

            if (isPending) return null;

            return (
              <motion.div
                key={i}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.1 }}
                className="flex items-center gap-2"
              >
                {isCompleted ? (
                  <IoCheckmarkCircle className="text-primary text-sm flex-shrink-0" />
                ) : (
                  <div className="w-3.5 h-3.5 border-2 border-primary border-t-transparent rounded-full animate-spin flex-shrink-0" />
                )}
                <span className={`text-xs ${isCompleted ? 'text-muted' : 'text-text font-medium'}`}>
                  {step}
                </span>
              </motion.div>
            );
          })}
        </div>
      </div>
    </motion.div>
  );
}
