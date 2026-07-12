import re


class SentimentAnalyzer:
    """تحلیل احساسات فارسی"""
    
    # دیکشنری کلمات مثبت
    POSITIVE_WORDS = [
        'خوب', 'عالی', 'فوق‌العاده', 'بی‌نظیر', 'محشر',
        'خوشحال', 'خوش', 'شاد', 'پر انرژی', 'سرحال',
        'دوست', 'دوست دارم', 'عشق', 'زیبا', 'قشنگ',
        'بهترین', 'عالیه', 'دمت گرم', 'ایول', 'بارکلا',
        '😊', '😂', '🤣', '😍', '🥰', '😎', '😁',
        '❤️', '💚', '💙', '💜', '🧡', '💛', '💖',
        '🎉', '🎊', '✨', '🌟', '💫', '🔥', '👑',
        'عالی شد', 'دمت گرم', 'خوشم اومد', 'راضیم',
        'خوبی', 'خوبم', 'خوشحالم', 'ممنون', 'متشکرم'
    ]
    
    # دیکشنری کلمات منفی
    NEGATIVE_WORDS = [
        'بد', 'افتضاح', 'مزخرف', 'ضعیف', 'ناراحت',
        'غمگین', 'افسرده', 'خسته', 'بی‌حوصله', 'عصبی',
        'ناراضی', 'متأسف', 'نگران', 'ترس', 'وحشتناک',
        'درد', 'رنج', 'اشک', 'گریه', 'تنها',
        '😢', '😭', '😡', '🤬', '😤', '😩', '😫',
        '😔', '😟', '😕', '😖', '😣', '😞', '😒',
        '👎', '💔', '😿', '😾',
        'کار نمی‌کنه', 'خرابه', 'مشکل', 'باگ', 'ارور',
        'خسته شدم', 'حوصله ندارم', 'نمی‌خوام', 'بی‌خیال'
    ]
    
    # کلمات تشدیدکننده
    INTENSIFIERS = [
        'خیلی', 'واقعاً', 'فوق‌العاده', 'شدیداً', 'کاملاً',
        'اصلاً', 'مطلقاً', 'به شدت', 'بی‌نهایت', 'وحشتناک'
    ]
    
    # کلمات سوالی (نشانه سردرگمی)
    CONFUSION_WORDS = [
        'نمی‌دونم', 'نمی‌دانم', 'نمیدونم', 'نفهمیدم',
        'متوجه نشدم', 'گیج', 'سردرگم', '؟', '?',
        'چی', 'چطور', 'کجا', 'کی', 'چرا', 'چه'
    ]
    
    def analyze(self, text):
        """تحلیل کامل احساسات متن"""
        text_lower = text.lower().strip()
        
        # شمارش کلمات مثبت و منفی
        positive_score = 0
        negative_score = 0
        confusion_score = 0
        intensity = 1
        
        # بررسی تشدیدکننده‌ها
        for word in self.INTENSIFIERS:
            if word in text_lower:
                intensity = 2
                break
        
        # شمارش کلمات مثبت
        positive_matches = []
        for word in self.POSITIVE_WORDS:
            if word.lower() in text_lower:
                positive_score += 1
                positive_matches.append(word)
        
        # شمارش کلمات منفی
        negative_matches = []
        for word in self.NEGATIVE_WORDS:
            if word.lower() in text_lower:
                negative_score += 1
                negative_matches.append(word)
        
        # بررسی سردرگمی
        for word in self.CONFUSION_WORDS:
            if word in text_lower:
                confusion_score += 1
        
        # اعمال شدت
        positive_score *= intensity
        negative_score *= intensity
        
        # تشخیص احساس نهایی
        if positive_score > negative_score and positive_score >= 2:
            sentiment = 'happy'
            score = positive_score
        elif negative_score > positive_score and negative_score >= 2:
            sentiment = 'sad'
            score = negative_score
        elif confusion_score >= 1:
            sentiment = 'confused'
            score = confusion_score
        else:
            sentiment = 'neutral'
            score = 0
        
        return {
            'sentiment': sentiment,
            'score': score,
            'positive_matches': positive_matches,
            'negative_matches': negative_matches,
            'intensity': intensity,
            'confusion': confusion_score > 0
        }
    
    def get_emotional_response(self, sentiment, user_name=""):
        """دریافت پاسخ احساسی مناسب"""
        name = user_name or "دوست من"
        
        responses = {
            'happy': [
                f"وااای {name}! چقدر انرژی داری! 🌟✨",
                f"حال دلم رو خوب کردی {name} جان! 😊💚",
                f"ایول! تو هم مثل من پر از انرژی هستی! 🚀🔥",
                f"چه روحیه خوبی! 😍 امیدوارم همیشه همینجور باشی!",
            ],
            'sad': [
                f"{name}، ناراحت نباش... 🫂💙",
                f"هی {name}، غصه نخور! من اینجام برات 🌧️☀️",
                f"می‌فهمم حالت رو {name} جان 😔 چطور می‌تونم کمکت کنم؟",
                f"روزای سخت هم می‌گذرن {name}... قول می‌دم! 💪✨",
            ],
            'confused': [
                f"به نظر می‌رسی یه کم گیج شدی {name} 🤔",
                f"سوال خوبی پرسیدی! بیا با هم بررسیش کنیم 🔍",
                f"نگران نباش {name}، من کمکت می‌کنم بفهمی 💡",
            ],
            'neutral': [
                f"چطور می‌تونم کمکت کنم {name}؟ 😊",
                f"من اینجام برات {name}! بگو چی می‌خوای 🎯",
            ]
        }
        
        import random
        return random.choice(responses.get(sentiment, responses['neutral']))


sentiment_analyzer = SentimentAnalyzer()
