import React, { useState, useEffect } from 'react';
import { translateToUrdu } from './translator';
import styles from './LanguageToggle.module.css';

const LanguageToggle = () => {
  const [currentLang, setCurrentLang] = useState('en');
  const [isTranslating, setIsTranslating] = useState(false);
  const [translationProgress, setTranslationProgress] = useState(0);

  const toggleLanguage = async () => {
    if (currentLang === 'en') {
      // Switch to Urdu
      setIsTranslating(true);
      setTranslationProgress(0);

      // Simulate translation progress
      const interval = setInterval(() => {
        setTranslationProgress(prev => {
          if (prev >= 95) {
            clearInterval(interval);
            return 95;
          }
          return prev + 5;
        });
      }, 100);

      // After translation simulation, apply the translated content
      setTimeout(() => {
        translatePageToUrdu();
        setTranslationProgress(100);
        setCurrentLang('ur');
        setIsTranslating(false);
        clearInterval(interval);
      }, 1500);
    } else {
      // Switch back to English
      setCurrentLang('en');
      // Revert to original content
      window.location.reload();
    }
  };

  const translatePageToUrdu = () => {
    // Translate main content
    const elements = document.querySelectorAll('h1, h2, h3, h4, h5, h6, p, li, .markdown');
    elements.forEach(element => {
      if (element.classList.contains('notranslate')) return;

      const originalText = element.getAttribute('data-original') || element.textContent;
      element.setAttribute('data-original', originalText);

      // Get translated text from our translation function
      const translatedText = translateToUrdu(originalText);
      element.textContent = translatedText;
    });

    // Translate navigation items
    const navItems = document.querySelectorAll('.navbar__item, .menu__link');
    navItems.forEach(item => {
      if (item.classList.contains('notranslate')) return;

      const originalText = item.getAttribute('data-original') || item.textContent;
      item.setAttribute('data-original', originalText);

      const translatedText = translateToUrdu(originalText);
      item.textContent = translatedText;
    });
  };

  return (
    <div className={styles.languageToggle}>
      <button
        className={`${styles.translateButton} ${currentLang === 'ur' ? styles.active : ''}`}
        onClick={toggleLanguage}
        disabled={isTranslating}
        title={currentLang === 'en' ? 'Translate to Urdu' : 'Switch to English'}
      >
        {isTranslating ? (
          <div className={styles.loadingContainer}>
            <div className={styles.spinner}></div>
            <span className={styles.progressText}>
              Translating... {translationProgress}%
            </span>
          </div>
        ) : (
          <span>
            {currentLang === 'en' ? '🇺🇦 Urdu' : '🇬🇧 English'}
          </span>
        )}
      </button>
    </div>
  );
};

export default LanguageToggle;