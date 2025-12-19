import React, { createContext, useContext, useState } from 'react';
import UrduTranslation from '../components/UrduTranslation/UrduTranslation';

const TranslationContext = createContext();

export const TranslationProvider = ({ children }) => {
  const [isUrdu, setIsUrdu] = useState(false);

  const toggleLanguage = () => {
    setIsUrdu(!isUrdu);
  };

  const value = {
    isUrdu,
    toggleLanguage,
    setIsUrdu
  };

  return (
    <TranslationContext.Provider value={value}>
      <UrduTranslation>
        {children}
      </UrduTranslation>
    </TranslationContext.Provider>
  );
};

export const useTranslation = () => {
  const context = useContext(TranslationContext);
  if (!context) {
    throw new Error('useTranslation must be used within a TranslationProvider');
  }
  return context;
};