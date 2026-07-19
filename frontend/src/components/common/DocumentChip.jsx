import { IoDocumentText, IoCheckmarkCircle, IoClose } from 'react-icons/io5';

export default function DocumentChip({ filename, pages, chunks, onRemove }) {
  return (
    <div className="inline-flex items-center gap-2 bg-accent border border-border rounded-lg px-3 py-1.5 text-sm group">
      <IoCheckmarkCircle className="text-primary text-base" />
      <IoDocumentText className="text-muted text-sm" />
      <span className="font-medium text-text">{filename}</span>
      {pages > 0 && (
        <span className="text-xs text-muted">
          {pages}p · {chunks}ch
        </span>
      )}
      {onRemove && (
        <button
          onClick={() => onRemove(filename)}
          className="opacity-0 group-hover:opacity-100 transition-opacity text-muted hover:text-danger cursor-pointer"
          title="Remove document"
        >
          <IoClose className="text-sm" />
        </button>
      )}
    </div>
  );
}
