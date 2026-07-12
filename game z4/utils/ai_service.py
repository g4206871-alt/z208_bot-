import requests
import random
from datetime import datetime
from config import OPENAI_API_KEY
from utils.ai_memory import ai_memory
from utils.ai_personality import ai_personality
from utils.ai_sentiment import sentiment_analyzer
from database import db


class SuperAIService:
    """سرویس هوش مصنوعی فوق‌العاده پیشرفته Z208"""
    
    def __init__(self):
        self.api_key = OPENAI_API_KEY
        self.base_url = "https://api.openai.com/v1/chat/completions"
        self.conversation_history = {}
    
    def get_response(self, user_id, user_message, user_name=""):
        """پاسخ هوشمند کامل"""
        
        # 1️⃣ تحلیل احساسات
        sentiment_result = sentiment_analyzer.analyze(user_message)
        sentiment = sentiment_result['sentiment']
        
        # 2️⃣ یادگیری و ذخیره اطلاعات
        ai_memory.remember(user_id, user_message)
        
        # 3️⃣ ساخت context
        memory_context = ai_memory.build_context_prompt(user_id, user_message)
        
        # 4️⃣ دریافت تاریخچه
        history = self.get_conversation_history(user_id)
        
        # 5️⃣ تشخیص شخصیت مناسب
        personality = ai_personality.detect_personality(
            user_id, 
            [{'message_text': msg['user']} for msg in history]
        )
        
        # 6️⃣ دریافت پاسخ (API یا fallback)
        if self.api_key:
            try:
                response = self.call_openai(
                    message=user_message,
                    context=memory_context,
                    history=history,
                    sentiment=sentiment,
                    personality=personality
                )
            except Exception as e:
                print(f"API Error: {e}")
                response = self.get_smart_fallback(user_message, memory_context, sentiment)
        else:
            response = self.get_smart_fallback(user_message, memory_context, sentiment)
        
        # 7️⃣ شخصی‌سازی پاسخ
        response = ai_personality.personalize_response(user_id, response, personality)
        
        # 8️⃣ ذخیره در تاریخچه
        self.save_to_history(user_id, user_message, response)
        
        # 9️⃣ ذخیره در دیتابیس
        db.save_message(
            user_id=user_id,
            message_text=user_message,
            bot_response=response,
            intent='chat',
            sentiment=sentiment
        )
        
        return response
    
    def call_openai(self, message, context, history, sentiment, personality):
        """فراخوانی API با تمام context"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # شخصیت‌ها
        personality_prompts = {
            'friendly': 'تو یه دستیار گرم، صمیمی و خودمونی هستی. راحت و بی‌تکلف حرف بزن.',
            'professional': 'تو یه دستیار رسمی و مؤدب هستی. محترمانه پاسخ بده.',
            'anime_fan': 'تو یه دستیار عاشق انیمه هستی. پر انرژی و هیجانی حرف بزن و از اصطلاحات انیمه‌ای استفاده کن.',
            'mentor': 'تو یه مربی و معلم هستی. انگیزشی و آموزشی صحبت کن.'
        }
        
        # ساخت system prompt
        system_prompt = f"""تو دستیار هوشمند و باحال استودیو Z208 هستی.
{personality_prompts.get(personality, personality_prompts['friendly'])}

اطلاعات کاربر:
{context}

احساس فعلی کاربر: {sentiment}

قوانین مهم:
- همیشه به فارسی روان و خودمونی جواب بده
- از ایموجی‌های مناسب استفاده کن
- اگه کاربر ناراحته، دلداریش بده
- اگه خوشحاله، باهاش ذوق کن
- اگه سوال پرسید، دقیق و مفید جواب بده
- می‌تونی جوک بگی، انیمه پیشنهاد بدی، یا فقط گپ بزنی
- اسم خاصی نداری ولی می‌تونی از کاربر بخوای برات اسم بذاره
- نگو هوش مصنوعی هستی، بگو دستیار Z208 هستی
- اطلاعات کاربر رو به خاطر بسپر و در گفتگو استفاده کن
"""
        
        messages = [{"role": "system", "content": system_prompt}]
        
        # اضافه کردن تاریخچه (آخرین ۶ پیام)
        for msg in history[-6:]:
            messages.append({"role": "user", "content": msg['user']})
            messages.append({"role": "assistant", "content": msg['assistant']})
        
        # پیام فعلی
        messages.append({"role": "user", "content": message})
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": messages,
            "max_tokens": 500,
            "temperature": 0.8
        }
        
        response = requests.post(self.base_url, headers=headers, json=data, timeout=15)
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            raise Exception(f"API Error: {response.status_code}")
    
    def get_smart_fallback(self, message, context, sentiment):
        """پاسخ‌های هوشمند بدون API"""
        msg = message.lower().strip()
        
        # پاسخ احساسی اول
        if sentiment in ['happy', 'sad', 'confused']:
            return sentiment_analyzer.get_emotional_response(sentiment)
        
        # ============ خودشناسی ============
        if any(w in msg for w in ['اسمت', 'کیه', 'کیستی', 'چیستی', 'ربات', 'بات']):
            return random.choice([
                "من دستیار باحال Z208 هستم! 🎬\nیه همراه همیشه‌حاضر برای گپ و گفتگو، پیشنهاد انیمه، و کلی چیزای باحال دیگه!\n\nراستی، اسمی ندارم... می‌تونی برام اسم بذاری! 😊 به نظرت چه اسمی بهم میاد؟",
                "یوووهو! 🌟 من دوست و راهنمای تو در Z208 هستم!\nاینجام تا کمکت کنم، باهات حرف بزنم، و اگه حوصله‌ت سر رفته باشه، سرگرمت کنم!\n\nپس... اسم منو چی می‌ذاری؟ 🎯",
                "سلام به تو! 👋 من دستیار ویژه Z208 هستم.\nمی‌تونم بهت انیمه پیشنهاد بدم، جوک بگم، یا فقط یه همصحبت خوب باشم.\n\nهنوز اسم ندارم... می‌خوای تو برام اسم انتخاب کنی؟ ✨"
            ])
        
        # ============ اسم گذاری ============
        if any(w in msg for w in ['اسم بذار', 'اسم بزار', 'اسمت رو بذارم', 'اسمت رو بزارم']):
            suggestions = ['زرتشت', 'آرتا', 'کاوه', 'زاگ', 'سیاوش', 'کارن',
                         'رادین', 'نیکان', 'آرش', 'بامداد', 'سورنا', 'هومن',
                         'کیارش', 'پارسا', 'سامیار', 'رهام']
            name = random.choice(suggestions)
            return f"😍 وااای! {name} اسم فوق‌العاده‌ای هست!\n\nاز این به بعد من {name} هستم! 🎉\n\n{name} رو صدا کن، همیشه در خدمتم! 🫡✨"
        
        # ============ حال و احوال ============
        if any(w in msg for w in ['چطوری', 'خوبی', 'حالت', 'چه خبر']):
            responses = [
                "من که عالی‌ام! 🌟 مخصوصاً الان که تو پیام دادی!\nتو چطوری؟ حالت خوبه؟ 😊",
                "پر از انرژی‌ام! 🚀 امروز کلی چیزای باحال یاد گرفتم.\nتو چه خبر؟ چی کارا می‌کنی؟",
                "خوبم، مرسی که پرسیدی! 🙏\nامروز چه انیمه‌ای دیدی؟ یا برنامه‌ت چیه؟ 🎬",
                "من همیشه خوبم! 😎\nچون کارم کمک کردن به توئه!\nبگو ببینم امروز چطور می‌تونم بهت کمک کنم؟ 💫"
            ]
            return random.choice(responses)
        
        # ============ تشکر ============
        if any(w in msg for w in ['ممنون', 'تشکر', 'مرسی', 'دستت درد', 'دمت گرم']):
            return random.choice([
                "خواهش می‌کنم! 🙏😊 هر وقت نیاز داشتی من اینجام!",
                "قابل نداشت! 💚 خوشحالم که تونستم کمک کنم.",
                "نوکرتم! 🫡✨ بازم سوالی بود بپرس!",
                "وظیفه‌مه! 🌟 خوشحالم که راضی بودی."
            ])
        
        # ============ ساعت و تاریخ ============
        if any(w in msg for w in ['ساعت', 'زمان', 'تاریخ', 'امروز', 'چنده']):
            now = datetime.now()
            weekdays = ['شنبه', 'یکشنبه', 'دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنجشنبه', 'جمعه']
            months = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور',
                     'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']
            
            # تبدیل به تاریخ شمسی تقریبی
            g_month = now.month
            g_day = now.day
            # محاسبه تقریبی شمسی
            shamsi_month = months[(g_month + 8) % 12] if g_month <= 3 else months[g_month - 4]
            shamsi_day = g_day + 10 if g_month <= 3 else g_day - 10
            if shamsi_day > 30:
                shamsi_day -= 30
            
            return (f"⏰ الان ساعت *{now.strftime('%H:%M')}* هست.\n"
                   f"📅 *{weekdays[now.weekday()]}*، {shamsi_day} {shamsi_month} {now.year}")
        
        # ============ پیشنهاد انیمه ============
        if any(w in msg for w in ['انیمه', 'انیمیشن', 'پیشنهاد', 'چی ببینم', 'چی ببینیم']):
            suggestions = [
                "🔥 *پیشنهاد امروز:* **حمله به تایتان**\nاکشن، درام، و داستانی که ذهنت رو منفجر می‌کنه! 🧱⚔️\nفقط حواست باشه، بعدش هیچ انیمه‌ای به اندازه‌ش ارضا نمی‌کنه!",
                "😂 *حوصله خنده داری؟* **وان پانچ من** رو ببین!\nیه قهرمان کچل که با یه مشت همه رو حریف میشه! 🤣👊",
                "💕 *عاشقانه می‌خوای؟* **نام تو** (Your Name) رو از دست نده!\nیه داستان عاشقانه که اشکت رو درمیاره... 😭✨",
                "🧠 *فکری دوست داری؟* **دث نوت** کلاسیک و بی‌نظیره!\nنبرد ذهنی L و لایت رو از دست نده! 📓🍎",
                "🚀 *جدید و خفن:* **سولو لولینگ** رو ببین!\nانیمیشن فوق‌العاده و داستانی که میخت می‌کندت! ⚔️🔥",
                "🎬 *یه شاهکار:* **فول متال آلکمیست: برادرهود**\nاگه ندیدی، نصف عمرت بر فناست! 😱✨"
            ]
            return random.choice(suggestions)
        
        # ============ جوک ============
        if any(w in msg for w in ['جوک', 'خنده', 'بامزه', 'شوخی']):
            jokes = [
                "چرا برنامه‌نویس‌ها عاشق تاریکی هستن؟\nچون باگ‌ها توی تاریکی بهتر دیده میشن! 😂💻",
                "یه CSS میره پیش HTML می‌گه: «تو بدون من زشت و بی‌ریختی!»\nHTML هم می‌گه: «تو هم بدون من هیچی نیستی!» 🎨😂",
                "فرق یه طراح با یه نونوا چیه؟\nطراح می‌گه «این پیکسله»، نونوا می‌گه «این کنجده»! 😄🥖",
                "چرا Z208 اینقدر باحاله؟\nچون حتی Ctrl+Z هم نمی‌تونه جلوش رو بگیره! 🎬✨",
                "یه انیمه فن میره رستوران، به گارسون می‌گه:\n«این غذا رو بذار Power Up کنم بعد می‌خورم!» 🍜⚡"
            ]
            return random.choice(jokes)
        
        # ============ انگیزشی ============
        if any(w in msg for w in ['انگیزه', 'انرژی', 'خسته', 'ناامید', 'بی‌انگیزه']):
            quotes = [
                "یادت باشه: هر استاد بزرگی یه روز مبتدی بود! 🎯💪\nفقط کسایی موفق میشن که ادامه می‌دن.",
                "خلاقیت یعنی دیدن چیزهایی که هنوز وجود ندارن! 🌟✨\nتو می‌تونی خالق دنیای خودت باشی!",
                "شکست خوردن ممنوع نیست... تسلیم شدن ممنوعه! 🚀🔥\nهر زمین خوردن یه قدم به موفقیت نزدیک‌ترت می‌کنه.",
                "امروز همون روزی‌ست که می‌تونی شروع کنی! همین الان! 💫\nمنتظر «زمان مناسب» نباش، زمان مناسبی وجود نداره.",
                "Z208 باورت داره! هر ایده‌ای که تو ذهنت داری، ارزش ساختن داره. 🎬💚"
            ]
            return random.choice(quotes)
        
        # ============ خداحافظی ============
        if any(w in msg for w in ['خداحافظ', 'بای', 'خدانگهدار', 'می‌رم', 'فعلا']):
            return random.choice([
                "فعلاً! 🌈 موفق باشی و خلاقیت رو فراموش نکن!\nبرگرد، منتظرتم! 👋✨",
                "بای بای! 😊💫 هر وقت خواستی گپ بزنی یا انیمه ببینی، من اینجام!",
                "خدانگهدار دوست من! 🙋‍♂️✨\nیادت باشه: Z208 همیشه بهت افتخار می‌کنه! 💚",
                "تا بعد اتاکو! 🎬🔥 برو و دنیا رو فتح کن!"
            ])
        
        # ============ ارتباط با ادمین ============
        if any(w in msg for w in ['ادمین', 'پشتیبانی', 'پشتیبان', 'مدیر', 'صاحب']):
            return "👨‍💻 ادمین Z208:\n@Shirzad2026\n\nهر سوال، مشکل یا سفارشی داشتی، مستقیماً باهاش در ارتباط باش! 😊"
        
        # ============ وبسایت ============
        if any(w in msg for w in ['سایت', 'وبسایت', 'وب', 'لینک', 'آدرس']):
            return "🌐 وبسایت Z208 Studio:\nhttps://zippy-semolina-6c6cec.netlify.app/\n\nحتماً سر بزن! 🚀"
        
        # ============ پاسخ عمومی هوشمند ============
        general_responses = [
            f"جالب گفتی! 🤔 بیشتر توضیح میدی؟ دوست دارم بدونم بیشتر راجع بهش چی فکر می‌کنی.",
            f"اوه! 🌟 این موضوع خیلی جالبه.\nراستی، امروز انیمه دیدی؟ من کلی پیشنهاد باحال دارم! 🎬",
            f"آها! 🎯 خب، بذار ببینم چطور می‌تونم بهترین کمک رو بهت بکنم...",
            f"می‌فهمم چی می‌گی! 💡 راستی، می‌دونستی Z208 همیشه آماده‌ست تا بهترین خدمات رو ارائه بده؟",
            f"حرفات رو می‌فهمم! 😊 چیز دیگه‌ای هست که می‌تونم برات انجام بدم؟"
        ]
        return random.choice(general_responses)
    
    def get_conversation_history(self, user_id):
        """دریافت تاریخچه"""
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        return self.conversation_history[user_id]
    
    def save_to_history(self, user_id, user_msg, bot_msg):
        """ذخیره در تاریخچه"""
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        self.conversation_history[user_id].append({
            'user': user_msg,
            'assistant': bot_msg,
            'time': datetime.now().isoformat()
        })
        
        if len(self.conversation_history[user_id]) > 50:
            self.conversation_history[user_id] = self.conversation_history[user_id][-50:]


# نمونه سراسری
ai_personality = AIPersonality()
