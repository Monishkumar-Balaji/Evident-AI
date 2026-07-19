import { motion } from 'framer-motion';

function getColor(score) {
  if (score >= 75) return 'bg-green-500';
  if (score >= 50) return 'bg-yellow-500';
  if (score >= 30) return 'bg-orange-500';
  return 'bg-red-500';
}

function getTrack(score) {
  if (score >= 75) return 'bg-green-100';
  if (score >= 50) return 'bg-yellow-100';
  if (score >= 30) return 'bg-orange-100';
  return 'bg-red-100';
}

export default function RetrievalBar({ retrievalQuality }) {
  if (!retrievalQuality) return null;

  const score = retrievalQuality.score || 0;
  const level = retrievalQuality.level || 'NONE';

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        <span className="text-xs font-semibold text-text">Retrieval Quality</span>
        <span className="text-xs font-bold text-primary">{level}</span>
      </div>

      <div className={`w-full h-2.5 rounded-full ${getTrack(score)} overflow-hidden`}>
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${score}%` }}
          transition={{ duration: 0.8, ease: 'easeOut' }}
          className={`h-full rounded-full ${getColor(score)}`}
        />
      </div>

      <div className="flex justify-between text-xs text-muted">
        <span>{score.toFixed(1)}%</span>
        <span>{retrievalQuality.strong_chunk_count || 0} strong chunks</span>
      </div>
    </div>
  );
}
