import { useState, useEffect, useRef } from 'react';
import { useDocuments } from './hooks/useDocuments';
import { useChat } from './hooks/useChat';
import Landing from './components/Landing/Landing';
import Sidebar from './components/Sidebar/Sidebar';
import ChatWindow from './components/Chat/ChatWindow';
import AnalyticsPanel from './components/Analytics/AnalyticsPanel';
import AnalysisDrawer from './components/Analysis/AnalysisDrawer';
import UploadArea from './components/Upload/UploadArea';
import UploadProgress from './components/Upload/UploadProgress';
import Toast from './components/common/Toast';
import { IoMenu } from 'react-icons/io5';
import { AnimatePresence, motion } from 'framer-motion';

export default function App() {
  const {
    documents,
    uploading,
    uploadProgress,
    error: uploadError,
    fetchDocuments,
    upload,
    remove,
    setError: setUploadError,
  } = useDocuments();

  const {
    messages,
    conversations,
    activeConversationId,
    loading,
    groupedHistory,
    sendMessage,
    startNewChat,
    selectConversation,
    clearConversation,
  } = useChat();

  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [analyticsOpen, setAnalyticsOpen] = useState(false);
  const [analysisDrawerOpen, setAnalysisDrawerOpen] = useState(false);
  const [analysisMessage, setAnalysisMessage] = useState(null);
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [toast, setToast] = useState(null);

  const uploadInputRef = useRef(null);

  // Fetch documents on mount
  useEffect(() => {
    fetchDocuments();
  }, [fetchDocuments]);

  // Show toast on upload error
  useEffect(() => {
    if (uploadError) {
      setToast({ message: uploadError, type: 'error' });
      setUploadError(null);
    }
  }, [uploadError, setUploadError]);

  const hasDocuments = documents.length > 0;

  // Get the latest assistant message for the analytics panel
  const lastAssistantMessage = [...messages].reverse().find(m => m.role === 'assistant' && !m.isError);

  const handleUpload = async (files) => {
    try {
      const result = await upload(files);
      setShowUploadModal(false);
      setToast({ message: `${result.documents?.length || 0} document(s) indexed successfully`, type: 'success' });
    } catch {
      // Error already handled by hook
    }
  };

  const handleShowAnalysis = (msg) => {
    setAnalysisMessage(msg);
    setAnalysisDrawerOpen(true);
  };

  const handleRegenerate = () => {
    const lastUserMsg = [...messages].reverse().find(m => m.role === 'user');
    if (lastUserMsg) {
      sendMessage(lastUserMsg.content);
    }
  };

  const handleAttach = () => {
    setShowUploadModal(true);
  };

  const handleDownloadChat = () => {
    if (messages.length === 0) return;
    const text = messages
      .map(m => `[${m.role.toUpperCase()}] ${m.content}`)
      .join('\n\n---\n\n');
    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'evident-ai-chat.txt';
    a.click();
    URL.revokeObjectURL(url);
  };

  // Landing page when no documents are uploaded
  if (!hasDocuments && !uploading) {
    return (
      <>
        <Landing
          documents={documents}
          uploading={uploading}
          uploadProgress={uploadProgress}
          onUpload={handleUpload}
          onRemove={remove}
        />
        <AnimatePresence>
          {toast && (
            <Toast
              message={toast.message}
              type={toast.type}
              onClose={() => setToast(null)}
            />
          )}
        </AnimatePresence>
      </>
    );
  }

  // Main three-column chat layout
  return (
    <div className="h-screen flex bg-[#EAEEE8] p-4 lg:p-6 pb-6 lg:pb-8">
      <div className="w-full h-full flex bg-background rounded-2xl lg:rounded-3xl shadow-xl border border-border relative overflow-hidden">
        {/* Mobile header */}
        <div className="absolute top-0 left-0 right-0 h-14 bg-card border-b border-border flex items-center px-4 z-30 md:hidden">
          <button
            onClick={() => setSidebarOpen(true)}
            className="p-2 text-muted hover:text-text cursor-pointer"
          >
            <IoMenu className="text-xl" />
          </button>
          <span className="text-sm font-semibold text-primary ml-2">Evident AI</span>
          <button
            onClick={() => setAnalyticsOpen(true)}
            className="ml-auto p-2 text-muted hover:text-text text-xs cursor-pointer"
          >
            Analytics
          </button>
        </div>

        {/* Sidebar */}
        <div className="hidden md:block w-1/4 min-w-[240px] max-w-[300px]">
          <Sidebar
            documents={documents}
            groupedHistory={groupedHistory}
            activeConversationId={activeConversationId}
            onNewChat={startNewChat}
            onSelectConversation={selectConversation}
            onClearConversation={clearConversation}
            onUploadClick={() => setShowUploadModal(true)}
            onRemoveDocument={remove}
            isOpen={true}
            onClose={() => {}}
          />
        </div>

        {/* Mobile sidebar */}
        <div className="md:hidden">
          <Sidebar
            documents={documents}
            groupedHistory={groupedHistory}
            activeConversationId={activeConversationId}
            onNewChat={() => { startNewChat(); setSidebarOpen(false); }}
            onSelectConversation={(id) => { selectConversation(id); setSidebarOpen(false); }}
            onClearConversation={clearConversation}
            onUploadClick={() => { setShowUploadModal(true); setSidebarOpen(false); }}
            onRemoveDocument={remove}
            isOpen={sidebarOpen}
            onClose={() => setSidebarOpen(false)}
          />
        </div>

        {/* Chat Window */}
        <div className="flex-1 flex flex-col min-w-0 md:border-x border-border mt-14 md:mt-0">
          <ChatWindow
            messages={messages}
            loading={loading}
            hasDocuments={hasDocuments}
            onSend={sendMessage}
            onAttach={handleAttach}
            onShowAnalysis={handleShowAnalysis}
            onRegenerate={handleRegenerate}
          />
        </div>

        {/* Analytics Panel (desktop) */}
        <div className="hidden lg:block w-1/4 min-w-[260px] max-w-[320px]">
          <AnalyticsPanel
            message={lastAssistantMessage}
            isOpen={true}
            onClose={() => {}}
          />
        </div>

        {/* Analytics Panel (mobile) */}
        <div className="lg:hidden">
          <AnalyticsPanel
            message={lastAssistantMessage}
            isOpen={analyticsOpen}
            onClose={() => setAnalyticsOpen(false)}
          />
        </div>
      </div>

      {/* Analysis Drawer */}
      <AnalysisDrawer
        isOpen={analysisDrawerOpen}
        message={analysisMessage}
        onClose={() => setAnalysisDrawerOpen(false)}
      />

      {/* Upload Modal */}
      <AnimatePresence>
        {showUploadModal && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 bg-black/40 z-50"
              onClick={() => !uploading && setShowUploadModal(false)}
            />
            <motion.div
              initial={{ opacity: 0, scale: 0.95, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: 20 }}
              className="fixed inset-0 z-50 flex items-center justify-center p-4"
            >
              <div className="bg-card rounded-2xl shadow-2xl p-6 w-full max-w-md">
                <h2 className="text-lg font-semibold text-text mb-4">Upload Documents</h2>
                {uploading ? (
                  <UploadProgress progress={uploadProgress} />
                ) : (
                  <UploadArea onUpload={handleUpload} disabled={uploading} />
                )}
                {!uploading && (
                  <button
                    onClick={() => setShowUploadModal(false)}
                    className="mt-4 w-full text-sm text-muted hover:text-text py-2 transition-colors cursor-pointer"
                  >
                    Cancel
                  </button>
                )}
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>

      {/* Toast */}
      <AnimatePresence>
        {toast && (
          <Toast
            message={toast.message}
            type={toast.type}
            onClose={() => setToast(null)}
          />
        )}
      </AnimatePresence>
    </div>
  );
}
