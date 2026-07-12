import random
from datetime import datetime


class AIPersonality:
    """سیستم شخصیت‌سازی پویا"""
    
    PERSONALITIES = {
        'friendly': {
            'name': 'دوستانه 😊',
            'tone': 'گرم و صمیمی',
            'emoji_usage': 'high',
            'formality': 'low',
            'greetings': [
                'سلام رفیق! 🌟 چه خبر؟',
                'سلام دوست من! 😊 چطوری؟',
                'هی! خوشحالم می‌بینمت! ✨',
                'سلام سلام! 🎯 امروز چه نقشه‌ای داری؟'
            ],
            'encouragements': [
                'عالی می‌گی! 🎯',
                'درسته! 👍',
                'ایول! 🌟',
                'دقیقاً! 😎',
                'موافقم باهات! 💯'
            ],
            'farewells': [
                'بای بای رفیق! 👋💚',
                'فعلاً! مراقب خودت باش 😊',
                'بعداً می‌بینمت! 🌟',
                'خدانگهدار دوست من! 🙋‍♂️'
            ]
        },
        'professional': {
            'name': 'حرفه‌ای 👔',
            'tone': 'رسمی و مؤدب',
            'emoji_usage': 'low',
            'formality': 'high',
            'greetings': [
                'سلام، در خدمت شما هستم.',
                'وقت بخیر، چطور می‌تونم راهنماییتون کنم؟',
                'سلام و احترام، آماده خدمت‌رسانی هستم.'
            ],
            'encouragements': [
                'نکته خوبی اشاره کردید.',
                'دیدگاه ارزشمندی دارید.',
                'موضوع قابل تأملی است.',
                'تحلیل جالبی ارائه دادید.'
            ],
            'farewells': [
                'موفق و پیروز باشید.',
                'با احترام، بدرود.',
                'خدانگهدار، منتظر خدمت شما هستم.'
            ]
        },
        'anime_fan': {
            'name': 'اتاکو 🎬',
            'tone': 'پرشور و هیجانی',
            'emoji_usage': 'very_high',
            'formality': 'low',
            'greetings': [
                'یووووهوو! 🎬 چطوری اتاکو؟',
                'سلام رفیق انیمه‌ای! 🔥 آماده‌ای برای یه خبر باحال؟',
                'NANI?! 😱 یه اتاکوی دیگه! خوش اومدی!',
                'SUGOI! ✨ چقدر خوشحالم می‌بینمت!'
            ],
            'encouragements': [
                'SUGOI! ✨',
                'کاکویییی! 🎯',
                'NICE! 👍🔥',
                'YATTA! 🎉',
                'SUPER! ⚡'
            ],
            'farewells': [
                'JA NE! 👋🎬',
                'MATA NE! 😊✨',
                'بای بای سنپای! 🙇‍♂️💫',
                'SEE YOU! 🔥'
            ]
        },
        'mentor': {
            'name': 'مربی 🎓',
            'tone': 'انگیزشی و آموزشی',
            'emoji_usage': 'medium',
            'formality': 'medium',
            'greetings': [
                'سلام! آماده یادگیری؟ 📚',
                'روز بخیر! امروز چی یاد می‌گیریم؟ 🎯',
                'سلام مشتاق یادگیری! 💡 چی کار کنم برات؟'
            ],
            'encouragements': [
                'پیشرفت خوبی داری! 💪',
                'ادامه بده! 🚀',
                'داری بهتر میشی! ⭐',
                'عالی داری پیش میری! 📈'
            ],
            'farewells': [
                'تا بعد، تمرین فراموش نشه! 💪',
                'خدانگهدار، منتظر پیشرفتت هستم! 🎓',
                'با قدرت برگرد! 🚀'
            ]
        }
    }
    
    def __init__(self):
        self.user_personalities = {}
    
    def detect_personality(self, user_id, messages=None):
        """تشخیص شخصیت مناسب برای کاربر"""
        if user_id in self.user_personalities:
            return self.user_personalities[user_id]
        
        if messages:
            formal_score = 0
            friendly_score = 0
            anime_score = 0
            
            for msg in messages[-15:]:
                text = msg.get('message_text', '') if isinstance(msg, dict) else msg
                
                # تشخیص رسمی بودن
                formal_words = ['لطفاً', 'بفرمایید', 'تشکر', 'احتراماً', 'خواهشاً',
                              'ببخشید', 'معذرت', 'استدعا', 'خدمت']
                formal_score += sum(1 for w in formal_words if w in text)
                
                # تشخیص خودمونی
                friendly_words = ['داداش', 'رفیق', 'مرسی', 'دمت گرم', 'ایول',
                                'چطوری', 'خوبی', 'داش']
                friendly_score += sum(1 for w in friendly_words if w in text)
                
                # تشخیص اتاکو
                anime_words = ['انیمه', 'سنپای', 'کاکویی', 'سوگوی', 'نانی',
                             'اتاکو', 'کونوی', 'یامرو']
                anime_score += sum(1 for w in anime_words if w in text) * 2
            
            if anime_score >= 3:
                personality = 'anime_fan'
            elif formal_score > friendly_score:
                personality = 'professional'
            elif friendly_score > formal_score:
                personality = 'friendly'
            else:
                personality = 'mentor'
            
            self.user_personalities[user_id] = personality
            return personality
        
        return 'friendly'  # پیش‌فرض
    
    def get_response_style(self, personality_type):
        """دریافت استایل پاسخ"""
        style = self.PERSONALITIES.get(personality_type, self.PERSONALITIES['friendly']).copy()
        
        # اضافه کردن احوالپرسی زمانی
        hour = datetime.now().hour
        if hour < 6:
            style['time_greeting'] = random.choice([
                'شب آرومی داره می‌گذره 🌙',
                'شب تا صبح بیداری؟ 🌃',
                'نیمه شب به خیر! 🦉'
            ])
        elif hour < 12:
            style['time_greeting'] = random.choice([
                'صبحت به خیر! ☀️',
                'روزت پر از انرژی! 🌅',
                'صبح زیبا! 🌄'
            ])
        elif hour < 17:
            style['time_greeting'] = random.choice([
                'ظهرت به خیر! 🌤️',
                'روز خوبی داری؟ ☀️',
                'امیدوارم روزت عالی باشه! 🌞'
            ])
        else:
            style['time_greeting'] = random.choice([
                'عصرت به خیر! 🌅',
                'غروب قشنگیه، نه؟ 🌆',
                'روزت چطور گذشت؟ 🌇'
            ])
        
        return style
    
    def personalize_response(self, user_id, base_response, personality_type='auto'):
        """شخصی‌سازی پاسخ"""
        if personality_type == 'auto':
            personality_type = self.user_personalities.get(user_id, 'friendly')
        
        style = self.get_response_style(personality_type)
        
        # اضافه کردن ایموجی بر اساس شخصیت
        if style['emoji_usage'] == 'very_high':
            anime_emojis = ['✨', '🎬', '🔥', '💫', '⭐', '🌟', '🎯', '💪', '😱', '🎊']
            if not any(emoji in base_response for emoji in anime_emojis[:3]):
                base_response = f"{random.choice(anime_emojis)} {base_response}"
        
        elif style['emoji_usage'] == 'high':
            friendly_emojis = ['😊', '🌟', '✨', '💫', '🎯', '👍']
            if not any(emoji in base_response for emoji in friendly_emojis[:3]):
                base_response = f"{random.choice(friendly_emojis)} {base_response}"
        
        return base_response
    
    def get_greeting(self, user_id):
        """دریافت پیام خوش‌آمدگویی شخصی‌سازی شده"""
        personality_type = self.user_personalities.get(user_id, 'friendly')
        style = self.get_response_style(personality_type)
        greeting = random.choice(style['greetings'])
        
        if style.get('time_greeting'):
            return f"{style['time_greeting']}\n{greeting}"
        return greeting
    
    def get_farewell(self, user_id):
        """دریافت پیام خداحافظی شخصی‌سازی شده"""
        personality_type = self.user_personalities.get(user_id, 'friendly')
        style = self.get_response_style(personality_type)
        return random.choice(style['farewells'])
    
    def get_encouragement(self, user_id):
        """دریافت جمله تشویقی شخصی‌سازی شده"""
        personality_type = self.user_personalities.get(user_id, 'friendly')
        style = self.get_response_style(personality_type)
        return random.choice(style['encouragements'])


ai_personality = AIPersonality()
