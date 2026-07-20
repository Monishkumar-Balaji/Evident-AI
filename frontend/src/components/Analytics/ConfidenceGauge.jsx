import { motion } from 'framer-motion';
import { PieChart, Pie, Cell } from 'recharts';
import { useEffect, useState } from 'react';

function getColor(score) {
  if (score >= 85) return '#5CB85C';
  if (score >= 70) return '#F0AD4E';
  if (score >= 50) return '#E88B3A';
  return '#D9534F';
}

function getTrackColor(score) {
  if (score >= 85) return '#E8F5E8';
  if (score >= 70) return '#FFF8EC';
  if (score >= 50) return '#FFF0E0';
  return '#FDE8E8';
}

export default function ConfidenceGauge({ confidence }) {
  const [animatedScore, setAnimatedScore] = useState(0);
  const score = confidence?.score || 0;
  const level = confidence?.level || 'NONE';
  const color = getColor(score);
  const trackColor = getTrackColor(score);

  useEffect(() => {
    const timer = setTimeout(() => setAnimatedScore(score), 200);
    return () => clearTimeout(timer);
  }, [score]);

  const data = [
    { value: animatedScore },
    { value: 100 - animatedScore },
  ];

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      className="flex flex-col items-center"
    >
      <div className="relative w-32 h-32">
        <PieChart width={128} height={128}>
          <Pie
            data={data}
            cx={59}
            cy={59}
            innerRadius={42}
            outerRadius={56}
            startAngle={90}
            endAngle={-270}
            dataKey="value"
            strokeWidth={0}
          >
            <Cell fill={color} />
            <Cell fill={trackColor} />
          </Pie>
        </PieChart>

        {/* Center text */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-2xl font-bold" style={{ color }}>{Math.round(animatedScore)}%</span>
          <span className="text-xs font-semibold text-muted">{level}</span>
        </div>
      </div>

      <div className="text-sm text-left mt-4 w-full flex flex-col gap-1.5 px-2">
        {confidence?.explanation ? confidence.explanation.split('\n').map((line, idx) => {
          let colorClass = 'text-muted';
          if (line.includes('✓')) colorClass = 'text-green-600 font-medium';
          if (line.includes('⚠')) colorClass = 'text-orange-600 font-medium';
          return (
            <div key={idx} className={`leading-snug ${colorClass}`}>
              {line}
            </div>
          );
        }) : <div className="text-center text-muted">No data available</div>}
      </div>
    </motion.div>
  );
}
