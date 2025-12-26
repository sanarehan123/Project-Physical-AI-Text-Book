/**
 * ChatWidget React component for RAG Chatbot Integration - Spec 4
 * T014: Create ChatWidget React component in `physical-ai-textbook/src/components/ChatWidget/ChatWidget.jsx`
 * T017: Implement API communication logic in ChatWidget to call backend /chat endpoint
 * T018: Add loading states and error handling to ChatWidget
 * T019: Implement source citation rendering with clickable links to book URLs
 */
import React, { useState, useRef } from 'react';
import ChatMessage from './ChatMessage';
import styles from './ChatWidget.module.css';

const ChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);

  // Scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  React.useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Get backend URL from environment variable or default to localhost
  const BACKEND_URL = 'http://127.0.0.1:8002';

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    try {
      setIsLoading(true);
      setError(null);

      // Add user message to chat
      const userMessage = {
        id: Date.now(),
        content: inputValue,
        role: 'user',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, userMessage]);
      const currentInput = inputValue;
      setInputValue('');

      // Call backend API
      const response = await fetch(`${BACKEND_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: currentInput,
          context: null // Optional context can be added here
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Add assistant message with sources
      const assistantMessage = {
        id: Date.now() + 1,
        content: data.answer,
        role: 'assistant',
        sources: data.sources || [],
        timestamp: new Date()
      };

      setMessages(prev => [...prev, assistantMessage]);

    } catch (err) {
      console.error('Error in chat:', err);
      console.error('Full error details:', err);
      setError(err.message || 'An error occurred while processing your request');

      // Add error message to chat with more specific information
      const errorMessage = {
        id: Date.now(),
        content: `Error: ${err.message || 'Failed to get response'}`,
        role: 'error',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const closeChat = () => {
    setIsOpen(false);
  };

  return (
    <>
      {/* Floating button to open chat */}
      {!isOpen && (
        <button
          className={styles['chat-widget-toggle']}
          onClick={toggleChat}
          aria-label="Open chat"
          title="Ask about the book"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
          </svg>
        </button>
      )}

      {/* Chat widget */}
      {isOpen && (
        <div className={styles['chat-widget-container']}>
          <div className={styles['chat-widget-header']}>
            <h3>Book Assistant</h3>
            <button
              className={styles['chat-widget-close']}
              onClick={closeChat}
              aria-label="Close chat"
            >
              ×
            </button>
          </div>

          <div className={styles['chat-widget-messages']}>
            {messages.length === 0 ? (
              <div className={styles['chat-widget-welcome']}>
                <p>Ask me anything about the Physical AI & Humanoid Robotics book!</p>
                <p>I can help explain concepts and find relevant information.</p>
              </div>
            ) : (
              messages.map((message) => (
                <ChatMessage key={message.id} message={message} />
              ))
            )}

            {isLoading && (
              <div className={`${styles['chat-widget-message']} ${styles['chat-widget-message-assistant']}`}>
                <div className={styles['chat-widget-typing-indicator']}>
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {error && (
            <div className={styles['chat-widget-error']}>
              Error: {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className={styles['chat-widget-input-form']}>
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Ask a question about the book..."
              disabled={isLoading}
              className={styles['chat-widget-input']}
              aria-label="Type your question"
            />
            <button
              type="submit"
              disabled={!inputValue.trim() || isLoading}
              className={styles['chat-widget-send-button']}
              aria-label="Send message"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="22" y1="2" x2="11" y2="13"></line>
                <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
              </svg>
            </button>
          </form>
        </div>
      )}
    </>
  );
};

export default ChatWidget;