import { IoCheckmarkCircle, IoCloseCircle } from 'react-icons/io5';

export default function AnalysisContent({ message }) {
  if (!message) return null;

  const analysis = message.analysis || {};
  const evidence = message.evidence || [];
  const verification = message.verification || {};
  const retrieval = message.retrieval_quality || {};

  return (
    <div className="space-y-6">
      {/* Retrieval Quality */}
      <section>
        <h3 className="text-sm font-bold text-text mb-2 flex items-center gap-2">
          <span className="w-2 h-2 bg-primary rounded-full" />
          Retrieval Quality
        </h3>
        <div className="bg-background rounded-lg p-3 text-xs space-y-1">
          <div className="flex justify-between">
            <span className="text-muted">Score</span>
            <span className="font-semibold text-text">{retrieval.score}%</span>
          </div>
          <div className="flex justify-between">
            <span className="text-muted">Level</span>
            <span className="font-semibold text-text">{retrieval.level}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-muted">Best Distance</span>
            <span className="font-semibold text-text">{retrieval.best_distance?.toFixed(3) ?? 'N/A'}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-muted">Strong Chunks</span>
            <span className="font-semibold text-text">{retrieval.strong_chunk_count || 0}</span>
          </div>
          <p className="text-muted pt-1 border-t border-border mt-1">{retrieval.reason}</p>
        </div>
      </section>

      {/* Chunk Filtering */}
      <section>
        <h3 className="text-sm font-bold text-text mb-2 flex items-center gap-2">
          <span className="w-2 h-2 bg-secondary rounded-full" />
          Chunk Filtering
        </h3>
        <div className="bg-background rounded-lg p-3 text-xs space-y-1">
          <div className="flex justify-between">
            <span className="text-muted">Retrieved</span>
            <span className="font-semibold text-text">{analysis.retrieved_chunks}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-muted">Kept</span>
            <span className="font-semibold text-text">{analysis.kept_chunks}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-muted">Weak Removed</span>
            <span className="font-semibold text-text">{analysis.weak_removed}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-muted">Duplicates Removed</span>
            <span className="font-semibold text-text">{analysis.duplicates_removed}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-muted">Low Score Removed</span>
            <span className="font-semibold text-text">{analysis.low_score_removed}</span>
          </div>
          <p className="text-muted pt-1 border-t border-border mt-1">{analysis.chunk_filter_reason}</p>
        </div>

        {/* Kept Chunk Details */}
        {analysis.kept_chunk_details?.length > 0 && (
          <div className="mt-2 space-y-1.5">
            {analysis.kept_chunk_details.map((chunk, i) => (
              <div key={i} className="bg-accent/50 rounded-lg p-2.5 text-xs">
                <div className="font-semibold text-text mb-1">
                  {chunk.source || 'Source'} · Page {chunk.page}
                </div>
                <div className="flex flex-wrap gap-x-3 gap-y-0.5 text-muted">
                  <span>Filter: {chunk.filter_score}</span>
                  <span>Retrieval: {chunk.retrieval_score}</span>
                  <span>Evidence: {chunk.evidence_score}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>

      {/* Evidence */}
      <section>
        <h3 className="text-sm font-bold text-text mb-2 flex items-center gap-2">
          <span className="w-2 h-2 bg-primary rounded-full" />
          Evidence
        </h3>
        <div className="space-y-3">
          {evidence.map((item, i) => (
            <div key={i} className="bg-background rounded-lg p-3">
              <div className="text-xs font-semibold text-text mb-2">
                {item.source || 'Source'} · Page {item.page} · Distance {item.distance}
              </div>
              <div className="space-y-1.5">
                {item.sentences?.map((s, j) => (
                  <div key={j} className="text-xs flex gap-2">
                    <span className="font-mono text-muted flex-shrink-0 w-12">{s.strength}</span>
                    <span className="text-muted flex-shrink-0 w-10">({s.score})</span>
                    <span className="text-text">{s.text}</span>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Verification Details */}
      {verification.details?.length > 0 && (
        <section>
          <h3 className="text-sm font-bold text-text mb-2 flex items-center gap-2">
            <span className="w-2 h-2 bg-secondary rounded-full" />
            Verification Details
          </h3>
          <div className="space-y-2">
            {verification.details.map((item, i) => (
              <div key={i} className="bg-background rounded-lg p-3 text-xs">
                <div className="flex items-center gap-2 mb-1">
                  {item.verified ? (
                    <IoCheckmarkCircle className="text-green-600" />
                  ) : (
                    <IoCloseCircle className="text-red-500" />
                  )}
                  <span className="font-semibold text-text">
                    {item.verified ? 'VERIFIED' : 'UNSUPPORTED'}
                  </span>
                  <span className="text-muted ml-auto">Similarity: {item.score}</span>
                </div>
                <p className="text-muted">{item.sentence}</p>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Audit Trail */}
      {analysis.audit_trail?.length > 0 && (
        <section>
          <h3 className="text-sm font-bold text-text mb-2 flex items-center gap-2">
            <span className="w-2 h-2 bg-primary rounded-full" />
            Audit Trail
          </h3>
          <div className="space-y-2">
            {analysis.audit_trail.map((item, i) => (
              <div key={i} className="bg-background rounded-lg p-3 text-xs space-y-1.5">
                <div>
                  <span className="text-muted">Claim: </span>
                  <span className="text-text">{item.claim}</span>
                </div>
                <div>
                  <span className="text-muted">Support: </span>
                  <span className="text-text">{item.support_quote}</span>
                </div>
                <div className="flex gap-3 text-muted">
                  <span>{item.source} · Page {item.page}</span>
                  <span>Similarity: {item.similarity}</span>
                  <span className={item.supported ? 'text-green-600' : 'text-red-500'}>
                    {item.supported ? 'SUPPORTED' : 'UNSUPPORTED'}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
