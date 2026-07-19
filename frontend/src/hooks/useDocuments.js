import { useState, useCallback } from 'react';
import { getDocuments, uploadDocuments, deleteDocument } from '../services/api';

export function useDocuments() {
  const [documents, setDocuments] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(null);
  const [error, setError] = useState(null);

  const fetchDocuments = useCallback(async () => {
    try {
      const data = await getDocuments();
      setDocuments(data.documents || []);
    } catch (err) {
      setError('Failed to fetch documents');
    }
  }, []);

  const upload = useCallback(async (files) => {
    setUploading(true);
    setUploadProgress('uploading');
    setError(null);

    try {
      setUploadProgress('indexing');
      const data = await uploadDocuments(files);
      setUploadProgress('ready');

      await fetchDocuments();

      setTimeout(() => {
        setUploading(false);
        setUploadProgress(null);
      }, 1500);

      return data;
    } catch (err) {
      setError(err.response?.data?.message || 'Upload failed');
      setUploading(false);
      setUploadProgress(null);
      throw err;
    }
  }, [fetchDocuments]);

  const remove = useCallback(async (name) => {
    try {
      await deleteDocument(name);
      await fetchDocuments();
    } catch (err) {
      setError('Failed to delete document');
    }
  }, [fetchDocuments]);

  return {
    documents,
    uploading,
    uploadProgress,
    error,
    fetchDocuments,
    upload,
    remove,
    setError,
  };
}
