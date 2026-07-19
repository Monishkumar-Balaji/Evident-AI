import { IoCheckmarkCircle, IoAlertCircle, IoCloseCircle, IoHelpCircle } from 'react-icons/io5';

const badges = {
  VERIFIED: {
    icon: <IoCheckmarkCircle className="text-base" />,
    bg: 'bg-green-100 text-green-700 border-green-200',
    label: 'Verified',
  },
  PARTIALLY_VERIFIED: {
    icon: <IoAlertCircle className="text-base" />,
    bg: 'bg-yellow-100 text-yellow-700 border-yellow-200',
    label: 'Partially Verified',
  },
  UNSUPPORTED: {
    icon: <IoCloseCircle className="text-base" />,
    bg: 'bg-red-100 text-red-700 border-red-200',
    label: 'Unsupported',
  },
  NO_DATA: {
    icon: <IoHelpCircle className="text-base" />,
    bg: 'bg-gray-100 text-gray-600 border-gray-200',
    label: 'No Data',
  },
};

export default function VerificationBadge({ verification }) {
  if (!verification) return null;

  const status = verification.status || 'NO_DATA';
  const badge = badges[status] || badges.NO_DATA;

  return (
    <div className="space-y-2">
      <span className="text-xs font-semibold text-text">Verification</span>

      <div className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border text-sm font-semibold ${badge.bg}`}>
        {badge.icon}
        {badge.label}
      </div>

      {verification.score > 0 && (
        <p className="text-xs text-muted">
          Score: {verification.score}%
        </p>
      )}
    </div>
  );
}
