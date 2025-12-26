import React, { useState, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import './ChatWidget.css';

const ChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState(null);
  const [showSelectionButton, setShowSelectionButton] = useState(false);
  const [selectionButtonPosition, setSelectionButtonPosition] = useState({ x: 0, y: 0 });

  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
  const chatPanelRef = useRef(null);

  // Backend API URL - Updated for your Railway deployment
  // For local development, use localhost
  const BACKEND_URL = process.env.NODE_ENV === 'production'
    ? 'https://project-physical-ai-text-book-production.up.railway.app'
    : 'http://127.0.0.1:8000';

  // Scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Handle text selection
  useEffect(() => {
    const handleSelection = () => {
      const selection = window.getSelection();
      const selectedText = selection.toString().trim();

      if (selectedText.length > 0) {
        const range = selection.getRangeAt(0);
        const rect = range.getBoundingClientRect();

        setSelectionButtonPosition({
          x: rect.left + window.scrollX,
          y: rect.top + window.scrollY - 40 // Position above the selection
        });

        setSelectedText(selectedText);
        setShowSelectionButton(true);
      } else {
        setShowSelectionButton(false);
        setSelectedText(null);
      }
    };

    document.addEventListener('mouseup', handleSelection);

    return () => {
      document.removeEventListener('mouseup', handleSelection);
    };
  }, []);

  // Close selection button when clicking elsewhere
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (showSelectionButton && !event.target.closest('.chat-selection-button')) {
        setShowSelectionButton(false);
      }
    };

    document.addEventListener('click', handleClickOutside);
    return () => document.removeEventListener('click', handleClickOutside);
  }, [showSelectionButton]);

  const handleAskAboutSelection = () => {
    if (selectedText) {
      setIsOpen(true);
      setInputValue(`Explain this: "${selectedText}"`);
      setShowSelectionButton(false);
    }
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = { id: Date.now(), text: inputValue, sender: 'user' };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Prepare the query - if we have selected text, include it in context
      let query = inputValue;
      if (selectedText && !inputValue.includes(selectedText)) {
        query = `Based on this text: "${selectedText}". ${inputValue}`;
      }

      const response = await fetch(`${BACKEND_URL}/rag`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: query,
          source_url: window.location.pathname // Optional: send current page URL
        }),
      });

      if (!response.ok) {
        throw new Error(`Backend error: ${response.status}`);
      }

      const data = await response.json();

      const botMessage = {
        id: Date.now() + 1,
        text: data.answer,
        sender: 'bot',
        sources: data.sources || []
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, I encountered an error. Please try again.',
        sender: 'bot'
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      setSelectedText(null);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
    if (!isOpen) {
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  };

  return (
    <>
      {/* Selection button - appears when text is selected */}
      {showSelectionButton && (
        <button
          className="chat-selection-button"
          style={{
            position: 'fixed',
            left: `${selectionButtonPosition.x}px`,
            top: `${selectionButtonPosition.y}px`,
            zIndex: 10000,
            fontSize: '14px',
            padding: '4px 8px',
            backgroundColor: '#3b82f6',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
            boxShadow: '0 2px 8px rgba(0,0,0,0.2)',
          }}
          onClick={handleAskAboutSelection}
        >
          Ask AI
        </button>
      )}

      {/* Chat widget */}
      <div className={`chat-widget ${isOpen ? 'open' : ''}`} ref={chatPanelRef}>
        {/* Floating button */}
        {!isOpen && (
          <button className="chat-toggle" onClick={toggleChat}>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2C6.48 2 2 6.48 2 12C2 13.54 2.36 15.01 3.02 16.32L2 22L7.68 20.98C8.99 21.64 10.46 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM9 17C8.45 17 8 16.55 8 16C8 15.45 8.45 15 9 15C9.55 15 10 15.45 10 16C10 16.55 9.55 17 9 17ZM12 17C11.45 17 11 16.55 11 16C11 15.45 11.45 15 12 15C12.55 15 13 15.45 13 16C13 16.55 12.55 17 12 17ZM15 17C14.45 17 14 16.55 14 16C14 15.45 14.45 15 15 15C15.55 15 16 15.45 16 16C16 16.55 15.55 17 15 17Z" fill="currentColor"/>
            </svg>
          </button>
        )}

        {/* Chat panel */}
        {isOpen && (
          <div className="chat-panel">
            <div className="chat-header">
              <h3>AI Assistant</h3>
              <button className="chat-close" onClick={toggleChat}>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M19 6.41L17.59 5L12 10.59L6.41 5L5 6.41L10.59 12L5 17.59L6.41 19L12 13.41L17.59 19L19 17.59L13.41 12L19 6.41Z" fill="currentColor"/>
                </svg>
              </button>
            </div>

            <div className="chat-messages">
              {messages.length === 0 ? (
                <div className="chat-welcome">
                  <p>Hello! I'm your AI assistant for the Physical AI textbook.</p>
                  <p>Ask me anything about the content, or select text on the page and click "Ask AI" to get explanations.</p>
                </div>
              ) : (
                messages.map((message) => (
                  <div key={message.id} className={`chat-message ${message.sender}`}>
                    <div className="chat-message-content">
                      {message.sender === 'bot' && message.sources && message.sources.length > 0 && (
                        <div className="chat-sources">
                          <small>Sources:</small>
                          {message.sources.map((source, index) => (
                            <a
                              key={index}
                              href={source.startsWith('http') ? source : `/${source}`}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="source-link"
                            >
                              {source}
                            </a>
                          ))}
                        </div>
                      )}
                      <ReactMarkdown>{message.text}</ReactMarkdown>
                    </div>
                  </div>
                ))
              )}
              {isLoading && (
                <div className="chat-message bot">
                  <div className="chat-message-content">
                    <div className="typing-indicator">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            <div className="chat-input-area">
              <textarea
                ref={inputRef}
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask a question about the textbook..."
                className="chat-input"
                rows="1"
              />
              <button
                onClick={handleSendMessage}
                disabled={isLoading || !inputValue.trim()}
                className="chat-send-button"
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M2.01 21L23 12L2.01 3L2 10L17 12L2 14L2.01 21Z" fill="currentColor"/>
                </svg>
              </button>
            </div>
          </div>
        )}
      </div>
    </>
  );
};

export default ChatWidget;