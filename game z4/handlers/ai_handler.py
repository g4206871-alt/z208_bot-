from telegram import Update
from telegram.ext import ContextTypes
from database import db
from utils.ai_service import super_ai
from utils.ai_memory import ai_memory
from utils.ai_personality import ai_personality
from utils.ai_sentiment import sentiment_analyzer
from keyboards.menus import get_back_button
import random


async def ai_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش منوی دستیار هوش مصنوعی"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    # دریافت پیام خوش‌آمد شخصی
    greeting = ai_personality.get_greeting(user_id)
    
    welcome_text = f"""{greeting}

🤖 *من دستیار هوشمند Z208 هستم!*

✨ *کاری که می‌تونم برات انجام بدم:*
• 💬 گپ و گفتگوی خودمونی
• 🎬 پیشنهاد انیمه و فیلم
• 😂 تعریف جوک و داستان خنده‌دار
• 💪 جملات انگیزشی و روحیه‌بخش
• 📅 گفتن ساعت و تاریخ
• 🧠 یادآوری اطلاعاتت
• ❤️ گوش دادن به حرفات

🎯 *فقط کافیه سوالت رو بفرستی!*
هر چی دوست داری بگو، من گوشم به توئه! ✨"""

    await query.edit_message_text(
        welcome_text,
        reply_markup=get_back_button(),
        parse_mode="Markdown"
    )
    
    context.user_data['in_ai_chat'] = True
    context.user_data['message_count'] = 0


async def handle_ai_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پردازش سوال کاربر با AI فوق‌العاده پیشرفته"""
    user = update.effective_user
    user_message = update.message.text.strip()
    user_id = user.id
    first_name = user.first_name or "کاربر"
    
    # شمارنده پیام‌ها
    message_count = context.user_data.get('message_count', 0) + 1
    context.user_data['message_count'] = message_count
    
    # افکت تایپ
    await update.message.chat.send_action(action="typing")
    
    # دریافت پاسخ از AI پیشرفته
    ai_response = super_ai.get_response(
        user_id=user_id,
        user_message=user_message,
        user_name=first_name
    )
    
    # تحلیل احساسات برای لاگ
    sentiment = sentiment_analyzer.analyze(user_message)
    
    # پیام‌های ویژه بر اساس تعداد تعامل
    special_prefix = ""
    special_messages = {
        1: f"🌟 {first_name} جان، خوشحالم که اولین سوالت رو می‌پرسی!",
        5: f"🎯 {first_name} عزیز، این پنجمین سوالتونه! چه کنجکاوی!",
        10: f"🏆 وااای {first_name}! ۱۰ تا سوال! تو واقعاً عالی هستی!",
        25: f"👑 {first_name}، ۲۵ سوال یعنی کلی گپ خوب داشتیم!",
        50: f"🚀 {first_name} افسانه‌ای! ۵۰ سوال! باید یه تندیس بهت بدم! 😄",
        100: f"💎 {first_name}، تو یه اسطوره‌ای! ۱۰۰ سوال یعنی کلی خاطره!"
    }
    
    if message_count in special_messages:
        special_prefix = f"{special_messages[message_count]}\n\n"
    
    # تشویق به ادامه
    encouragements = [
        "\n\n💭 بازم بپرس! من همیشه گوشم به توئه.",
        "\n\n🚀 سوال دیگه‌ای داری؟ کلی حرفای نگفته داریم!",
        "\n\n✨ منتظر سوال بعدیت هستم!",
        "\n\n🎯 هر چی دوست داری بپرس، من اینجام!"
    ]
    
    final_response = f"{special_prefix}{ai_response}{random.choice(encouragements)}"
    
    await update.message.reply_text(
        final_response,
        reply_markup=get_back_button(),
        parse_mode="Markdown"
    )
