import { useState, useCallback, useRef } from 'react';
import { askQuestion } from '../services/api';

function generateId() {
  return Date.now().toString(36) + Math.random().toString(36).slice(2, 7);
}

function getDateLabel(date) {
  const now = new Date();
  const d = new Date(date);
  const diffDays = Math.floor((now - d) / (1000 * 60 * 60 * 24));
  if (diffDays === 0) return 'Today';
  if (diffDays === 1) return 'Yesterday';
  if (diffDays < 7) return `${diffDays} days ago`;
  return d.toLocaleDateString();
}

export function useChat() {
  const [conversations, setConversations] = useState([]);
  const [activeConversationId, setActiveConversationId] = useState(null);
  const [loading, setLoading] = useState(false);
  const abortRef = useRef(null);

  const activeConversation = conversations.find(c => c.id === activeConversationId);
  const messages = activeConversation?.messages || [];

  const startNewChat = useCallback(() => {
    const newConv = {
      id: generateId(),
      title: 'New Chat',
      messages: [],
      createdAt: new Date().toISOString(),
    };
    setConversations(prev => [newConv, ...prev]);
    setActiveConversationId(newConv.id);
    return newConv.id;
  }, []);

  const sendMessage = useCallback(async (question) => {
    let convId = activeConversationId;

    if (!convId) {
      const newConv = {
        id: generateId(),
        title: question.slice(0, 50),
        messages: [],
        createdAt: new Date().toISOString(),
      };
      setConversations(prev => [newConv, ...prev]);
      setActiveConversationId(newConv.id);
      convId = newConv.id;
    }

    const userMessage = {
      id: generateId(),
      role: 'user',
      content: question,
      timestamp: new Date().toISOString(),
    };

    setConversations(prev =>
      prev.map(c => {
        if (c.id !== convId) return c;
        const updated = {
          ...c,
          messages: [...c.messages, userMessage],
          title: c.messages.length === 0 ? question.slice(0, 50) : c.title,
        };
        return updated;
      })
    );

    setLoading(true);

    try {
      const data = await askQuestion(question);

      const assistantMessage = {
        id: generateId(),
        role: 'assistant',
        content: data.answer,
        confidence: data.confidence,
        retrieval_quality: data.retrieval_quality,
        verification: data.verification,
        sources: data.sources,
        evidence: data.evidence,
        analysis: data.analysis,
        time_taken: data.time_taken,
        timestamp: new Date().toISOString(),
      };

      setConversations(prev =>
        prev.map(c => {
          if (c.id !== convId) return c;
          return { ...c, messages: [...c.messages, assistantMessage] };
        })
      );
    } catch (err) {
      const errorMessage = {
        id: generateId(),
        role: 'assistant',
        content: 'Sorry, an error occurred while processing your question. Please try again.',
        isError: true,
        timestamp: new Date().toISOString(),
      };

      setConversations(prev =>
        prev.map(c => {
          if (c.id !== convId) return c;
          return { ...c, messages: [...c.messages, errorMessage] };
        })
      );
    } finally {
      setLoading(false);
    }
  }, [activeConversationId]);

  const selectConversation = useCallback((id) => {
    setActiveConversationId(id);
  }, []);

  const clearConversation = useCallback(() => {
    if (!activeConversationId) return;
    setConversations(prev => prev.filter(c => c.id !== activeConversationId));
    setActiveConversationId(null);
  }, [activeConversationId]);

  const groupedHistory = conversations.reduce((groups, conv) => {
    const label = getDateLabel(conv.createdAt);
    if (!groups[label]) groups[label] = [];
    groups[label].push(conv);
    return groups;
  }, {});

  return {
    messages,
    conversations,
    activeConversationId,
    activeConversation,
    loading,
    groupedHistory,
    sendMessage,
    startNewChat,
    selectConversation,
    clearConversation,
  };
}
