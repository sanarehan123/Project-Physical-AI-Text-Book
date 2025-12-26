import React, { useState, useEffect } from 'react';
import clsx from 'clsx';
import styles from './UrduTranslation.module.css';

const UrduTranslation = ({ children, className = '' }) => {
  const [isUrdu, setIsUrdu] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  // Comprehensive Urdu translation mappings
  const translationMap = {
    // Module titles and chapter titles
    'Module 1 - Foundations of Physical AI & Embodied Intelligence': 'ماڈیول 1 - جسمانی مصنوعی ذہانت اور لیسانی مصنوعی ذہانت کی بنیادیں',
    'Module 2 - The Robotic Nervous System (ROS 2)': 'ماڈیول 2 - روبوٹک اعصابی نظام (ROS 2)',
    'Module 3 - Digital Twins & AI-Robot Brains': 'ماڈیول 3 - ڈیجیٹل جڑواں اور AI-روبوٹ دماغ',
    'Module 4 - Vision-Language-Action & Capstone': 'ماڈیول 4 - بینائش-زبان-عمل اور کیپسٹون',

    // Chapter titles
    'Introduction to Physical AI': 'جسمانی مصنوعی ذہانت کا تعارف',
    'Humanoid Robotics Landscape': 'ہیومنوائڈ روبوٹکس کا منظر نامہ',
    'Sensors as Perception Organs': 'ادراک کے عضو کے طور پر سینسرز',
    'Physical Constraints Reality Gaps': 'جسمانی پابندیاں اور حقیقت کے فاصلے',
    'ROS 2 Architecture': 'ROS 2 کی تعمیر',
    'Python Agents with ROS 2': 'ROS 2 کے ساتھ پائی تھون ایجنٹس',
    'Robot Description URDF': 'روبوٹ کی تفصیل URDF',
    'ROS 2 Systems Engineering': 'ROS 2 نظام ہائے انجینئرنگ',
    'Gazebo Physics Simulation': 'گزیبو طبیعیات تقلید',
    'Unity Human Robot Interaction': 'یونٹی انسان روبوٹ مداخلت',
    'NVIDIA Isaac Sim': 'این وی ڈی ائی اے آئزیک سیم',
    'Isaac ROS Navigation': 'آئزیک ROS ہدایت',
    'Vision for Humanoid Robots': 'ہیومنوائڈ روبوٹس کے لیے بینائش',
    'Language Control Interface': 'زبان کنٹرول انٹرفیس',
    'Vision Language Action': 'بینائش زبان عمل',
    'Autonomous Humanoid Capstone': 'خود مختار ہیومنوائڈ کیپسٹون',

    // Technical concepts
    'Physical AI': 'جسمانی مصنوعی ذہانت',
    'Humanoid Robotics': 'ہیومنوائڈ روبوٹکس',
    'Embodied Intelligence': 'لیسانی مصنوعی ذہانت',
    'AI Systems': 'مصنوعی ذہانت کے نظام',
    'ROS 2': 'ROS 2',
    'Simulation': 'تقلید',
    'Vision-Language-Action': 'بینائش-زبان-عمل',
    'Digital Twins': 'ڈیجیٹل جڑواں',
    'AI-Robot Brains': 'مصنوعی ذہانت-روبوٹ دماغ',
    'Sensors': 'سینسرز',
    'Perception': 'ادراک',
    'Reality Gaps': 'حقیقت کے فاصلے',
    'Architecture': 'تعمیر',
    'Agents': 'ایجنٹس',
    'URDF': 'URDF',
    'Navigation': 'ہدایت',
    'Physics Simulation': 'طبیعیات تقلید',
    'Human Robot Interaction': 'انسان روبوٹ مداخلت',

    // Educational terms
    'Welcome to the Physical AI & Humanoid Robotics textbook': 'جسمانی مصنوعی ذہانت اور ہیومنوائڈ روبوٹکس کے دستور میں خوش آمدید',
    'where we explore the intersection of artificial intelligence and physical systems': 'جہاں ہم مصنوعی ذہانت اور جسمانی نظام کے تقاطع کو دریافت کرتے ہیں',
    'This comprehensive resource covers the foundations': 'یہ جامع وسیلہ بنیادیں کو احاطہ کرتا ہے',
    'Guide you through the essential concepts': 'ضروری تصورات کے ذریعے آپ کی رہنمائی کریں',
    'From foundational principles to advanced implementations': 'ادار کے اصولوں سے لے کر اعلی درجے کے نفاذ تک',
    'Begin your journey by exploring the modules': 'ماڈیولز کو دریافت کرکے اپنا سفر شروع کریں',
    'Each module contains comprehensive chapters': 'ہر ماڈیول میں جامع ابواب ہیں',

    // Navigation and common terms
    'Textbook': 'دستور',
    'Resources': 'وسائل',
    'GitHub': 'گیٹ ہب',
    'Docusaurus': 'ڈوکوسورس',
    'ROS': 'ROS',
    'Gazebo': 'گزیبو',
    'NVIDIA': 'این وی ڈی ائی اے',
    'Isaac': 'آئزیک',
    'Unity': 'یونٹی',
    'Module 1': 'ماڈیول 1',
    'Module 2': 'ماڈیول 2',
    'Module 3': 'ماڈیول 3',
    'Module 4': 'ماڈیول 4',
    'Foundations': 'ادار',
    'Landscape': 'منظر نامہ',
    'Perception Organs': 'ادراک کے عضو',
    'Constraints': 'پابندیاں',
    'Architecture': 'تعمیر',
    'Python': 'پائی تھون',
    'Robot': 'روبوٹ',
    'Systems': 'نظام',
    'Physics': 'طبیعیات',
    'Human': 'انسان',
    'Vision': 'بینائش',
    'Language': 'زبان',
    'Action': 'عمل',
    'Capstone': 'کیپسٹون',
    'Autonomous': 'خود مختار',

    // General terms
    'Welcome': 'خوش آمدید',
    'Getting Started': 'شروع کریں',
    'About This Textbook': 'اس دستور کے بارے میں',
    'This textbook is designed to guide you': 'یہ دستور آپ کی رہنمائی کے لیے ڈیزائن کیا گیا ہے',
    'Learn about': 'متعلق سیکھیں',
    'Begin your journey': 'اپنا سفر شروع کریں',
    'Explore': 'دریافت کریں',
    'Learn': 'سیکھیں',
    'Understand': 'سمجھیں',
    'Implement': 'نافذ کریں',
    'Design': 'ڈیزائن',
    'Develop': 'ترقی دیں',
    'Build': 'تعمیر کریں',
    'Create': 'تخلیق کریں',
    'Master': 'مہارت',
    'Advanced': 'اعلی درجے کی',
    'Practical': 'عملی',
    'Comprehensive': 'جامع',
    'Essential': 'ضروری',
    'Concepts': 'تصورات',
    'Principles': 'اصول',
    'Applications': 'اطلاق',
    'Techniques': 'تکنیکیں',
    'Methods': 'طریقے',
    'Integration': 'میل',
    'Deployment': 'تنصیب',
    'Bridge': 'پل',
    'Gap': 'فاصلہ',
    'Real-world': 'حقیقی دنیا',
    'Hands-on': 'ہاتھوں ہاتھ',
    'Interactive': 'م انٹرایکٹو',
    'Exercises': 'ورکشاپس',
    'Examples': 'مثالیں',
    'Projects': 'منصوبے',
    'Reinforce': 'مضبوط کریں',
    'Understanding': 'سمجھ',
    'Journey': 'سفر',
    'Progressing': 'پیشرفت',
    'Topics': 'مضامین',
    'High-fidelity': 'زیادہ وفاداری',
    'Proven': 'ثابت',
    'Methodologies': 'طریقہ کار',
    'Cutting-edge': 'جدید ترین',
    'Sensor': 'سینسر',
    'Hardware': 'ہارڈ ویئر',
    'Exercises': 'ورکشاپس',
    'Reinforce': 'مضبوط کریں',
    'Interactive': 'م انٹرایکٹو',
    'Practical': 'عملی',
    'Examples': 'مثالیں',
    'Projects': 'منصوبے',
    'Reinforce': 'مضبوط کریں',
    'Journey': 'سفر',
    'Progressing': 'پیشرفت',
    'Advanced': 'اعلی درجے کی',
    'Topics': 'مضامین',
    'Hands-on': 'ہاتھوں ہاتھ',

    // Basic connectives
    'and': 'اور',
    'in': 'میں',
    'the': 'کا/کی',
    'of': 'کی',
    'to': 'کو',
    'for': 'کے لئے',
    'with': 'کے ساتھ',
    'on': 'پر',
    'is': 'ہے',
    'are': 'ہیں',
    'this': 'یہ',
    'that': 'وہ',
    'from': 'سے',
    'by': 'کی طرف',
    'about': 'کے بارے میں',
  };

  const translateText = (text) => {
    if (!text || typeof text !== 'string') return text;

    let translated = text;

    // Sort keys by length (descending) to match longer phrases first
    const sortedKeys = Object.keys(translationMap).sort((a, b) => b.length - a.length);

    for (const key of sortedKeys) {
      const regex = new RegExp(key.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
      translated = translated.replace(regex, translationMap[key]);
    }

    return translated;
  };

  const toggleLanguage = async () => {
    setIsLoading(true);

    // Simulate translation loading
    await new Promise(resolve => setTimeout(resolve, 500));

    setIsUrdu(!isUrdu);
    setIsLoading(false);
  };

  const getButtonText = () => {
    if (isLoading) return 'ترجمہ ہو رہا ہے...';
    return isUrdu ? 'انگریزی' : 'اردو';
  };

  return (
    <div className={clsx(styles.urduTranslation, className, {
      [styles.urduMode]: isUrdu,
    })}>
      <button
        className={clsx(styles.translateButton, {
          [styles.urduButton]: isUrdu,
          [styles.loading]: isLoading,
        })}
        onClick={toggleLanguage}
        dir="ltr"
      >
        {isLoading ? '🔄' : isUrdu ? '🇺🇦' : '🇵🇰'} {getButtonText()}
      </button>

      <div
        className={clsx(styles.translatedContent, {
          [styles.urduText]: isUrdu,
        })}
        dir={isUrdu ? 'rtl' : 'ltr'}
      >
        {isUrdu ? translateText(children) : children}
      </div>
    </div>
  );
};

export default UrduTranslation;