import { motion, AnimatePresence } from 'framer-motion';
import { IoShieldCheckmark, IoAdd, IoCloudUpload, IoChatbubbleEllipses, IoTrash, IoClose } from 'react-icons/io5';
import DocumentChip from '../common/DocumentChip';

export default function Sidebar({
  documents,
  groupedHistory,
  activeConversationId,
  onNewChat,
  onSelectConversation,
  onClearConversation,
  onUploadClick,
  onRemoveDocument,
  isOpen,
  onClose,
}) {
  return (
    <>
      {/* Mobile overlay */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/30 z-40 md:hidden"
            onClick={onClose}
          />
        )}
      </AnimatePresence>

      <motion.aside
        initial={false}
        animate={{ x: isOpen ? 0 : '-100%' }}
        transition={{ type: 'spring', stiffness: 300, damping: 30 }}
        className={`fixed md:relative md:translate-x-0 z-50 md:z-auto
          w-72 h-full bg-card border-r border-border flex flex-col
          md:flex md:w-full`}
      >
        {/* Header */}
        <div className="p-4 border-b border-border">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-gradient-to-br from-primary to-secondary rounded-lg flex items-center justify-center">
                <IoShieldCheckmark className="text-white text-sm" />
              </div>
              <span className="text-lg font-bold text-primary">Evident AI</span>
            </div>
            <button onClick={onClose} className="md:hidden text-muted hover:text-text cursor-pointer">
              <IoClose className="text-xl" />
            </button>
          </div>

          <div className="space-y-3 mt-2">
            <button
              onClick={onNewChat}
              className="w-full flex items-center gap-2 px-3 py-2.5 bg-primary text-white rounded-xl text-sm font-medium hover:bg-primary-dark transition-colors cursor-pointer"
              id="new-chat-btn"
            >
              <IoAdd className="text-base" />
              New Chat
            </button>
            <button
              onClick={onUploadClick}
              className="w-full flex items-center gap-2 px-3 py-2.5 bg-accent text-primary rounded-xl text-sm font-medium hover:bg-secondary/30 transition-colors cursor-pointer"
              id="upload-docs-btn"
            >
              <IoCloudUpload className="text-base" />
              Upload Documents
            </button>
          </div>
        </div>

        {/* Documents */}
        {documents.length > 0 && (
          <div className="px-4 py-3 border-b border-border">
            <h3 className="text-xs font-semibold text-muted uppercase tracking-wider mb-2">Documents</h3>
            <div className="flex flex-wrap gap-1.5">
              {documents.map(doc => (
                <DocumentChip
                  key={doc.filename}
                  filename={doc.filename}
                  pages={doc.pages}
                  chunks={doc.chunks}
                  onRemove={onRemoveDocument}
                />
              ))}
            </div>
          </div>
        )}

        {/* History */}
        <div className="flex-1 overflow-y-auto px-4 py-3">
          <h3 className="text-xs font-semibold text-muted uppercase tracking-wider mb-2">History</h3>

          {Object.keys(groupedHistory).length === 0 ? (
            <p className="text-xs text-muted mt-2">No conversations yet</p>
          ) : (
            Object.entries(groupedHistory).map(([label, convs]) => (
              <div key={label} className="mb-3">
                <p className="text-xs text-muted font-medium mb-1">{label}</p>
                <div className="space-y-1">
                  {convs.map(conv => (
                    <button
                      key={conv.id}
                      onClick={() => onSelectConversation(conv.id)}
                      className={`w-full text-left flex items-center gap-2 px-3 py-2 rounded-lg text-sm transition-all cursor-pointer
                        ${conv.id === activeConversationId
                          ? 'bg-accent text-primary font-medium'
                          : 'text-text hover:bg-accent/50'
                        }`}
                    >
                      <IoChatbubbleEllipses className="text-xs flex-shrink-0 text-muted" />
                      <span className="truncate">{conv.title}</span>
                    </button>
                  ))}
                </div>
              </div>
            ))
          )}
        </div>

        {/* Footer */}
        {activeConversationId && (
          <div className="p-4 border-t border-border">
            <button
              onClick={onClearConversation}
              className="w-full flex items-center justify-center gap-2 px-3 py-2 text-sm text-danger hover:bg-red-50 rounded-lg transition-colors cursor-pointer"
              id="clear-chat-btn"
            >
              <IoTrash className="text-sm" />
              Clear Conversation
            </button>
          </div>
        )}
      </motion.aside>
    </>
  );
}
