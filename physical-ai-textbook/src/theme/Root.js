import React from 'react';
import { TranslationProvider } from '../contexts/TranslationContext';
import ChatWidget from '../components/ChatWidget/ChatWidget';

const Root = ({ children }) => {
  return (
    <TranslationProvider>
      {children}
      <ChatWidget />
    </TranslationProvider>
  );
};

export default Root;