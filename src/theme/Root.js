import React from 'react';
import { TranslationProvider } from '../contexts/TranslationContext';

const Root = ({ children }) => {
  return (
    <TranslationProvider>
      {children}
    </TranslationProvider>
  );
};

export default Root;