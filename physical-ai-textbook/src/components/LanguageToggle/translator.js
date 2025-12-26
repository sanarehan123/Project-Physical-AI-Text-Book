// Urdu translation mappings for common terms
const urduTranslations = {
  // Technical terms
  'Physical AI': 'جسمانی مصنوعی ذہانت',
  'Humanoid Robotics': 'ہیومنوائڈ روبوٹکس',
  'AI Systems': 'مصنوعی ذہانت کے نظام',
  'Embodied Intelligence': 'لیسانی مصنوعی ذہانت',
  'ROS 2': 'ROS 2',
  'Simulation': 'تقلید',
  'Vision-Language-Action': 'بینائش-زبان-عمل',
  'Capstone': 'کیپسٹون',
  'Digital Twins': 'ڈیجیٹل جڑواں',
  'AI-Robot Brains': 'مصنوعی ذہانت-روبوٹ دماغ',
  'VLA': 'VLA',

  // Common educational terms
  'Module': 'ماڈیول',
  'Chapter': 'باب',
  'Foundations': 'ادار',
  'Landscape': 'منظر نامہ',
  'Perception': 'ادراک',
  'Reality Gaps': ' حقیقت کے فاصلے',
  'Architecture': 'تعمیر',
  'Python Agents': 'پائی تھون ایجنٹس',
  'Robot Description': 'روبوٹ کی تفصیل',
  'Systems Engineering': 'نظام ہائے انجینئرنگ',
  'Physics Simulation': 'طبیعیات تقلید',
  'Human Robot Interaction': 'انسان روبوٹ مداخلت',
  'Vision': 'بینائش',
  'Language Control': 'زبان کنٹرول',
  'Autonomous': 'خود مختار',

  // Navigation and UI terms
  'Textbook': 'دستور',
  'Resources': 'وسائل',
  'More': 'مزید',
  'GitHub': 'گیٹ ہب',
  'Docusaurus': 'ڈوکوسورس',
  'ROS': 'ROS',
  'Gazebo': 'گزیبو',
  'NVIDIA': 'این وی ڈی ائی اے',
  'Isaac': 'آئزیک',
  'Welcome': 'خوش آمدید',
  'Getting Started': 'شروع کریں',
  'Introduction': 'تعارف',
  'Sensors': 'سینسرز',
  'Constraints': 'پابندیاں',
  'Agents': 'ایجنٹس',
  'URDF': 'URDF',
  'Navigation': 'ہدایت',
  'Unity': 'یونٹی',

  // General terms
  'and': 'اور',
  'in': 'میں',
  'the': 'کا',
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
  'explore': 'دریافت کریں',
  'learn': 'سیکھیں',
  'understand': 'سمجھیں',
  'implement': 'نافذ کریں',
  'design': 'ڈیزائن',
  'develop': 'ترقی دیں',
  'build': 'تعمیر کریں',
  'create': 'تخلیق کریں',
  'master': 'مہارت',
  'advanced': 'اعلی درجے کی',
  'practical': 'عملی',
  'comprehensive': 'جامع',
  'essential': 'ضروری',
  'concepts': 'تصورات',
  'principles': 'اصول',
  'applications': 'اطلاق',
  'techniques': 'تکنیکیں',
  'methods': 'طریقے',
  'systems': 'نظام',
  'integration': 'میل',
  'deployment': 'تنصیب',
  'bridge': 'پل',
  'gap': 'فاصلہ',
  'real-world': 'حقیقی دنیا',
  'hands-on': 'ہاتھوں ہاتھ',
  'interactive': 'م Interactive',
  'exercises': 'ورکشاپس',
  'examples': 'مثالیں',
  'projects': 'منصوبے',
  'reinforce': 'مضبوط کریں',
  'understanding': 'سمجھ',
  'journey': 'سفر',
  'progressing': 'پیشرفت',
  'advanced': 'اعلی درجے کی',
  'topics': ' مضامین',
  'integration': 'میل',
  'reality': ' حقیقت',
  'simulation': ' تقلید',
  'high-fidelity': 'زیادہ وفاداری',
  'proven': 'ثابت',
  'methodologies': 'طریقہ کار',
  'cutting-edge': 'جدید ترین',
  'techniques': 'تکنیکیں',
  'sensor': 'سینسر',
  'integration': 'میل',
  'real': ' حقیقی',
  'hardware': 'ہارڈ ویئر',
  'deployment': 'تنصیب',
  'exercises': 'ورکشاپس',
  'reinforce': ' مضبوط کریں',
  'understanding': 'سمجھ',
  'interactive': 'م انٹرایکٹو',
  'practical': ' عملی',
  'examples': 'مثالیں',
  'projects': 'منصوبے',
  'reinforce': ' مضبوط کریں',
  'journey': ' سفر',
  'progressing': ' پیشرفت',
  'advanced': ' اعلی درجے کی',
  'topics': ' مضامین',
  'hands-on': ' ہاتھوں ہاتھ',
};

export const translateToUrdu = (text) => {
  if (!text || typeof text !== 'string') return text;

  // For longer texts, we'll use a more sophisticated approach
  // This is a simplified version that handles common words
  let translated = text;

  // First, try to match longer phrases
  const sortedKeys = Object.keys(urduTranslations).sort((a, b) => b.length - a.length);

  for (const key of sortedKeys) {
    const regex = new RegExp(key, 'gi');
    translated = translated.replace(regex, urduTranslations[key]);
  }

  // Handle some special cases for better readability
  translated = translated.replace(/\b([A-Z][A-Z0-9]*)\b/g, (match) => {
    // Keep acronyms as they are but in context
    return urduTranslations[match] || match;
  });

  // Clean up any double spaces or awkward formatting
  translated = translated.replace(/\s+/g, ' ').trim();

  return translated;
};