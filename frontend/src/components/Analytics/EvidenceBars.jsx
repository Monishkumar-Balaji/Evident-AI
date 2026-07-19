import { motion } from 'framer-motion';

function getBarColor(score) {
  if (score >= 80) return 'bg-green-500';
  if (score >= 60) return 'bg-yellow-500';
  if (score >= 40) return 'bg-orange-500';
  return 'bg-red-400';
}

export default function EvidenceBars({ evidence }) {
  if (!evidence || evidence.length === 0) return null;

  return (
    <div className="space-y-2">
      <span className="text-xs font-semibold text-text">Evidence Strength</span>

      <div className="space-y-2.5">
        {evidence.map((item, i) => {
          const bestScore = item.sentences?.[0]?.score
            ? Math.round(item.sentences[0].score * 100)
            : 0;

          return (
            <div key={i} className="space-y-1">
              <div className="flex items-center justify-between">
                <span className="text-xs text-muted">
                  {item.source || 'Source'} · Page {item.page}
                </span>
                <span className="text-xs font-semibold text-text">{bestScore}%</span>
              </div>

              <div className="w-full h-2 bg-border rounded-full overflow-hidden">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${bestScore}%` }}
                  transition={{ duration: 0.6, ease: 'easeOut', delay: i * 0.1 }}
                  className={`h-full rounded-full ${getBarColor(bestScore)}`}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
