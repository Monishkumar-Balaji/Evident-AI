import { useState, useRef } from 'react';
import { motion } from 'framer-motion';
import { IoCloudUpload, IoDocumentText } from 'react-icons/io5';

export default function UploadArea({ onUpload, disabled }) {
  const [dragActive, setDragActive] = useState(false);
  const [selectedFiles, setSelectedFiles] = useState([]);
  const inputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const files = Array.from(e.dataTransfer.files).filter(f =>
      f.name.toLowerCase().endsWith('.pdf') || f.name.toLowerCase().endsWith('.docx')
    );
    if (files.length > 0) {
      setSelectedFiles(files);
      onUpload(files);
    }
  };

  const handleChange = (e) => {
    const files = Array.from(e.target.files);
    if (files.length > 0) {
      setSelectedFiles(files);
      onUpload(files);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.3 }}
      className={`relative border-2 border-dashed rounded-2xl p-10 text-center transition-all duration-300 cursor-pointer
        ${dragActive
          ? 'border-primary bg-accent scale-[1.02]'
          : 'border-border bg-card hover:border-primary/50 hover:bg-accent/30'
        }
        ${disabled ? 'opacity-50 pointer-events-none' : ''}
      `}
      onDragEnter={handleDrag}
      onDragLeave={handleDrag}
      onDragOver={handleDrag}
      onDrop={handleDrop}
      onClick={() => inputRef.current?.click()}
    >
      <input
        ref={inputRef}
        type="file"
        multiple
        accept=".pdf,.docx"
        onChange={handleChange}
        className="hidden"
        id="file-upload-input"
      />

      <motion.div
        animate={{ y: dragActive ? -5 : 0 }}
        transition={{ type: 'spring', stiffness: 300 }}
      >
        <IoCloudUpload className="text-5xl text-primary mx-auto mb-4" />
        <h3 className="text-lg font-semibold text-text mb-2">
          {dragActive ? 'Drop your files here' : 'Upload Documents'}
        </h3>
        <p className="text-sm text-muted mb-4">
          Drag and drop PDF or DOCX files, or click to browse
        </p>
        <div className="inline-flex items-center gap-2 px-4 py-2 bg-primary text-white rounded-xl text-sm font-medium hover:bg-primary-dark transition-colors">
          <IoDocumentText />
          Choose Files
        </div>
      </motion.div>

      {selectedFiles.length > 0 && !disabled && (
        <div className="mt-4 flex flex-wrap gap-2 justify-center">
          {selectedFiles.map((f, i) => (
            <span key={i} className="text-xs bg-accent text-primary px-3 py-1 rounded-full font-medium">
              {f.name}
            </span>
          ))}
        </div>
      )}
    </motion.div>
  );
}
