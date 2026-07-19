import { IoDocumentText } from 'react-icons/io5';

export default function SourceCards({ sources }) {
  if (!sources || sources.length === 0) return null;

  return (
    <div className="space-y-2">
      <span className="text-xs font-semibold text-text">Sources</span>

      <div className="space-y-2">
        {sources.map((src, i) => (
          <div
            key={i}
            className="bg-accent/50 border border-border rounded-lg p-3 hover:border-primary/30 transition-colors"
          >
            <div className="flex items-center gap-2 mb-1">
              <IoDocumentText className="text-primary text-sm" />
              <span className="text-xs font-semibold text-text">{src.source}</span>
            </div>
            <div className="flex flex-wrap gap-x-3 gap-y-1 text-xs text-muted">
              <span>Page {src.page}</span>
              <span>Distance {src.distance}</span>
              {src.filter_score > 0 && <span>Filter {src.filter_score}</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
