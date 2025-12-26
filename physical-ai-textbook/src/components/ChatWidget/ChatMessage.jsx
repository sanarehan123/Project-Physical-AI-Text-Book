/**
 * ChatMessage React component for RAG Chatbot Integration - Spec 4
 * T015: Create ChatMessage component in `physical-ai-textbook/src/components/ChatWidget/ChatMessage.jsx`
 */
import React from 'react';
import styles from './ChatWidget.module.css';

const ChatMessage = ({ message }) => {
  const { role, content, sources } = message;

  const getMessageClass = () => {
    switch (role) {
      case 'user':
        return styles['chat-widget-message-user'];
      case 'assistant':
        return styles['chat-widget-message-assistant'];
      case 'error':
        return styles['chat-widget-message-error'];
      default:
        return styles['chat-widget-message'];
    }
  };

  return (
    <div className={`${styles['chat-widget-message']} ${getMessageClass()}`}>
      <div className={styles['chat-widget-message-content']}>
        {content}
      </div>

      {/* Render sources for assistant messages */}
      {role === 'assistant' && sources && sources.length > 0 && (
        <div className={styles['chat-widget-sources']}>
          <strong>Sources:</strong>
          <ul>
            {sources.map((source, index) => (
              <li key={index}>
                <a
                  href={source.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  onClick={(e) => e.stopPropagation()}
                >
                  {source.text.substring(0, 100)}{source.text.length > 100 ? '...' : ''}
                </a>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default ChatMessage;