import { motion } from 'framer-motion';
import { IoShieldCheckmark } from 'react-icons/io5';
import UploadArea from '../Upload/UploadArea';
import UploadProgress from '../Upload/UploadProgress';
import DocumentChip from '../common/DocumentChip';

export default function Landing({ documents, uploading, uploadProgress, onUpload, onRemove }) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-background px-4">
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: 'easeOut' }}
        className="w-full max-w-xl text-center"
      >
        {/* Logo */}
        <motion.div
          initial={{ scale: 0.8 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.1, type: 'spring', stiffness: 200 }}
          className="mb-8"
        >
          <div className="inline-flex items-center gap-3 mb-4">
            <div className="w-12 h-12 bg-gradient-to-br from-primary to-secondary rounded-xl flex items-center justify-center shadow-lg">
              <IoShieldCheckmark className="text-white text-2xl" />
            </div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-primary to-primary-light bg-clip-text text-transparent">
              Evident AI
            </h1>
          </div>
          <p className="text-muted text-lg font-light">
            Trustworthy AI for your Documents
          </p>
        </motion.div>

        {/* Upload Area */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3, duration: 0.5 }}
        >
          {uploading ? (
            <UploadProgress progress={uploadProgress} />
          ) : (
            <UploadArea onUpload={onUpload} disabled={uploading} />
          )}
        </motion.div>

        {/* Document Chips */}
        {documents.length > 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2 }}
            className="mt-6 flex flex-wrap gap-2 justify-center"
          >
            {documents.map((doc) => (
              <DocumentChip
                key={doc.filename}
                filename={doc.filename}
                pages={doc.pages}
                chunks={doc.chunks}
                onRemove={onRemove}
              />
            ))}
          </motion.div>
        )}

        {/* Features */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="mt-10 grid grid-cols-3 gap-4"
        >
          {[
            { label: 'Confidence Scoring', desc: 'Know how reliable each answer is' },
            { label: 'Evidence Tracking', desc: 'See exactly where answers come from' },
            { label: 'Hallucination Detection', desc: 'Every claim is verified' },
          ].map((feature, i) => (
            <div key={i} className="bg-card border border-border rounded-xl p-4 text-center hover:border-primary/30 hover:shadow-sm transition-all duration-300">
              <h3 className="text-sm font-semibold text-text mb-1">{feature.label}</h3>
              <p className="text-xs text-muted">{feature.desc}</p>
            </div>
          ))}
        </motion.div>
      </motion.div>
    </div>
  );
}
