import json
import re
from datetime import datetime
from database import db


class AIMemory:
    """سیستم حافظه پیشرفته برای AI"""
    
    def __init__(self):
        self.memory_cache = {}
        self.learning_log = []
    
    def remember(self, user_id, message, response=""):
        """ذخیره و یادگیری از گفتگو"""
        # استخراج اطلاعات شخصی
        extracted_info = self.extract_info(message)
        
        if extracted_info:
            for key, value in extracted_info.items():
                db.remember_user_info(user_id, key, value)
                self.learning_log.append({
                    'user_id': user_id,
                    'type': 'info_learned',
                    'key': key,
                    'value': value,
                    'time': datetime.now().isoformat()
                })
                print(f"🧠 یاد گرفتم: کاربر {user_id} - {key} = {value}")
        
        # تشخیص و ذخیره موضوعات
        topics = self.detect_topics(message)
        if topics:
            memory = db.get_user_memory(user_id) or {}
            last_topics = memory.get('last_topics', [])
            if isinstance(last_topics, str):
                try:
                    last_topics = json.loads(last_topics)
                except:
                    last_topics = []
            
            last_topics.extend(topics)
            last_topics = list(dict.fromkeys(last_topics))[-10:]  # حذف تکراری و محدود به ۱۰
            
            db.update_user_memory_field(user_id, 'last_topics', last_topics)
        
        # تشخیص و ذخیره علایق جدید
        new_interests = self.detect_interests(message)
        if new_interests:
            memory = db.get_user_memory(user_id) or {}
            interests = memory.get('interests', [])
            if isinstance(interests, str):
                try:
                    interests = json.loads(interests)
                except:
                    interests = []
            
            for interest in new_interests:
                if interest not in interests:
                    interests.append(interest)
            
            db.update_user_memory_field(user_id, 'interests', interests)
    
    def recall(self, user_id):
        """به یاد آوردن تمام اطلاعات کاربر"""
        memory = db.get_user_memory(user_id)
        if not memory:
            return self._empty_memory()
        
        # تبدیل فیلدهای JSON
        result = {
            'facts': self._safe_json(memory.get('remembered_facts', '{}')),
            'interests': self._safe_json(memory.get('interests', '[]')),
            'preferences': self._safe_json(memory.get('preferences', '{}')),
            'last_topics': self._safe_json(memory.get('last_topics', '[]')),
            'personality': self._safe_json(memory.get('personality_traits', '{}')),
            'learning_style': memory.get('learning_style', 'visual'),
        }
        
        return result
    
    def _safe_json(self, data):
        """تبدیل امن به JSON"""
        if isinstance(data, (dict, list)):
            return data
        if isinstance(data, str):
            try:
                return json.loads(data)
            except:
                return {} if data.startswith('{') else []
        return {} if isinstance(data, dict) else []
    
    def _empty_memory(self):
        """حافظه خالی پیش‌فرض"""
        return {
            'facts': {},
            'interests': [],
            'preferences': {},
            'last_topics': [],
            'personality': {},
            'learning_style': 'visual'
        }
    
    def extract_info(self, text):
        """استخراج اطلاعات شخصی از متن"""
        info = {}
        
        # الگوهای تشخیص اسم
        name_patterns = [
            (r'اسمم (\S+) (?:هست|است|ه|می‌باشد)', 1),
            (r'اسم من (\S+) (?:هست|است|ه)', 1),
            (r'من (\S+) (?:هستم|ام|می‌باشم)', 1),
            (r'اسمم (\S+)', 1),
            (r'صدام کن (\S+)', 1),
            (r'منو (\S+) صدا کن', 1),
            (r'(\S+) صدایم کن', 1),
            (r'من (\S+) هستم', 1),
            (r'اسم من (\S+)', 1),
        ]
        
        for pattern, group in name_patterns:
            match = re.search(pattern, text)
            if match:
                name = match.group(group)
                # فیلتر کلمات غیر اسم
                if name not in ['هستم', 'هست', 'است', 'نیست', 'هستیم', 'خوبم', 'خوب']:
                    info['user_name'] = name
                    break
        
        # تشخیص سن
        age_patterns = [
            (r'(\d{1,2})\s*سال(?:ه|م|مه|م هست|م می‌باشد)', 1),
            (r'(\d{1,2})\s*سالم(?:ه|هست)?', 1),
            (r'سنم\s*(\d{1,2})', 1),
            (r'(\d{1,2})\s*سالشه', 1),
        ]
        
        for pattern, group in age_patterns:
            match = re.search(pattern, text)
            if match:
                age = int(match.group(group))
                if 5 <= age <= 100:  # سن منطقی
                    info['age'] = str(age)
                    break
        
        # تشخیص شغل
        jobs = [
            'برنامه‌نویس', 'برنامه نویس', 'توسعه‌دهنده', 'توسعه دهنده',
            'طراح', 'گرافیست', 'دانشجو', 'دانش آموز', 'محصل',
            'معلم', 'استاد', 'مدرس', 'دکتر', 'پزشک',
            'مهندس', 'مدیر', 'کارمند', 'فروشنده', 'نویسنده',
            'عکاس', 'فیلمبردار', 'ادیتور', 'تدوینگر',
            'بازاریاب', 'مارکتر', 'سئوکار', 'مدیر محتوا',
            'فریلنسر', 'آزادکار', 'کسب‌وکار', 'کارآفرین'
        ]
        
        for job in jobs:
            if job in text:
                info['job'] = job
                break
        
        # تشخیص موقعیت مکانی
        cities = [
            'تهران', 'مشهد', 'اصفهان', 'شیراز', 'تبریز',
            'کابل', 'هرات', 'مزار', 'مزار شریف', 'قندهار',
            'کرج', 'اهواز', 'قم', 'کرمانشاه', 'رشت',
            'ارومیه', 'زاهدان', 'همدان', 'کرمان', 'یزد',
            'بامیان', 'ننگرهار', 'بلخ', 'کندز', 'غزنی'
        ]
        
        for city in cities:
            if city in text:
                info['location'] = city
                break
        
        # تشخیص انیمه/فیلم مورد علاقه
        anime_triggers = ['انیمه', 'انیمیشن', 'سریال', 'فیلم', 'انیمه‌ای']
        if any(trigger in text for trigger in anime_triggers):
            if any(word in text for word in ['مورد علاقه', 'دوست دارم', 'عاشق', 'بهترین', 'عالی']):
                anime_list = [
                    'حمله به تایتان', 'دث نوت', 'ناروتو', 'وان پیس',
                    'جوجوتسو کایسن', 'ارن یا شکارچی', 'سولو لولینگ',
                    'فول متال', 'کد گیاس', 'استینز گیت', 'هانتر',
                    'بلیچ', 'دراگون بال', 'مبارز باکسر', 'هایکیو',
                    'توکیو غول', 'کابوی بی‌باپ', 'مشل', 'فایریرن'
                ]
                for anime in anime_list:
                    if anime.lower() in text.lower():
                        info['favorite_anime'] = anime
                        break
        
        return info
    
    def detect_topics(self, text):
        """تشخیص موضوعات گفتگو"""
        topics = []
        
        topic_keywords = {
            'anime': ['انیمه', 'انیمیشن', 'مانگا', 'اتک', 'ناروتو', 'دث نوت',
                     'انیمه‌ای', 'شخصیت انیمه', 'دوبله', 'زیرنویس'],
            'tech': ['برنامه', 'کد', 'پایتون', 'هوش', 'ربات', 'اپلیکیشن',
                    'وبسایت', 'سرور', 'گیت', 'گیت‌هاب', 'جاوا', 'ریکت'],
            'design': ['طراحی', 'گرافیک', 'لوگو', 'رنگ', 'فتوشاپ', 'ایلوستریتور',
                      'وکتور', 'پیکسل', 'تایپوگرافی', 'برند', 'هویت بصری'],
            'marketing': ['بازاریابی', 'فروش', 'اینستاگرام', 'تبلیغات', 'سئو',
                         'کانال', 'محتوا', 'فالوور', 'کمپین'],
            'support': ['مشکل', 'کمک', 'سوال', 'راهنما', 'پشتیبانی', 'ارور',
                       'باگ', 'کار نمی‌کنه', 'خراب'],
            'personal': ['من', 'خودم', 'زندگی', 'کار', 'خونه', 'خانواده',
                        'دوست', 'عشق', 'احساس', 'دلم'],
            'entertainment': ['جوک', 'خنده', 'بازی', 'سرگرمی', 'موسیقی', 'آهنگ',
                            'فیلم', 'سینما', 'کنسرت'],
        }
        
        text_lower = text.lower()
        for topic, keywords in topic_keywords.items():
            if any(kw in text_lower for kw in keywords):
                topics.append(topic)
        
        return topics
    
    def detect_interests(self, text):
        """تشخیص علایق کاربر"""
        interests = []
        
        interest_patterns = {
            'anime': ['انیمه', 'انیمیشن', 'مانگا'],
            'programming': ['برنامه‌نویسی', 'کدنویسی', 'پایتون', 'جاوا', 'توسعه'],
            'design': ['طراحی', 'گرافیک', 'هنر', 'نقاشی'],
            'gaming': ['بازی', 'گیم', 'پلی‌استیشن', 'ایکس باکس', 'کامپیوتر'],
            'reading': ['کتاب', 'مطالعه', 'رمان', 'شعر'],
            'music': ['موسیقی', 'آهنگ', 'ساز', 'گیتار', 'پیانو', 'خواننده'],
            'sports': ['ورزش', 'فوتبال', 'والیبال', 'شنا', 'بدنسازی'],
            'movies': ['فیلم', 'سینما', 'سریال', 'نقد فیلم'],
            'cooking': ['آشپزی', 'غذا', 'کیک', 'شیرینی'],
            'travel': ['سفر', 'مسافرت', 'گردش', 'طبیعت'],
        }
        
        text_lower = text.lower()
        for interest, keywords in interest_patterns.items():
            if any(kw in text_lower for kw in keywords):
                interests.append(interest)
        
        return interests
    
    def build_context_prompt(self, user_id, user_message=""):
        """ساخت پرامپت با تمام اطلاعات کاربر"""
        memory = self.recall(user_id)
        facts = memory.get('facts', {})
        interests = memory.get('interests', [])
        last_topics = memory.get('last_topics', [])
        
        context_parts = []
        
        # اطلاعات شخصی
        if facts.get('user_name'):
            context_parts.append(f"اسم کاربر: {facts['user_name']}")
        if facts.get('age'):
            context_parts.append(f"سن: {facts['age']} سال")
        if facts.get('job'):
            context_parts.append(f"شغل: {facts['job']}")
        if facts.get('location'):
            context_parts.append(f"موقعیت: {facts['location']}")
        if facts.get('favorite_anime'):
            context_parts.append(f"انیمه مورد علاقه: {facts['favorite_anime']}")
        
        # علایق
        if interests:
            interest_names = {
                'anime': 'انیمه', 'programming': 'برنامه‌نویسی',
                'design': 'طراحی', 'gaming': 'بازی', 'reading': 'مطالعه',
                'music': 'موسیقی', 'sports': 'ورزش', 'movies': 'فیلم',
                'cooking': 'آشپزی', 'travel': 'سفر'
            }
            named = [interest_names.get(i, i) for i in interests]
            context_parts.append(f"علایق: {', '.join(named)}")
        
        # موضوعات اخیر
        if last_topics:
            context_parts.append(f"گفتگوهای اخیر: {', '.join(last_topics[-3:])}")
        
        return "\n".join(context_parts) if context_parts else ""
    
    def get_conversation_context(self, user_id, limit=10):
        """دریافت زمینه کامل گفتگو"""
        messages = db.get_last_conversation(user_id, limit)
        memory = self.recall(user_id)
        
        return {
            'recent_messages': messages,
            'user_memory': memory,
            'conversation_length': len(messages)
        }


ai_memory = AIMemory()
