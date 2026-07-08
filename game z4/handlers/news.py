from telegram import Update
from telegram.ext import ContextTypes
from keyboards.menus import get_back_button
import random


async def show_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش اخبار استودیو"""
    query = update.callback_query
    await query.answer()

    news_text = """📰 **آخرین اخبار Z208**

🚀 **ما تازه شروع کردیم!**

تیم Z208 در حال کوشش و تلاشه تا برنامه‌های کاربردی و مفید بسازه. 
الآن در مرحله‌ی توسعه و یادگیری هستیم و سخت مشغول کاریم.

💡 **هدف ما چیه؟**
می‌خوایم ابزارهایی بسازیم که واقعاً به درد بخوره و زندگی دیجیتالی رو براتون راحت‌تر کنه.

📌 **فعلاً همه‌چیز در دست ساخت و توسعه‌ست.**
به محض اینکه پروژه‌ی جدیدی آماده بشه، همین‌جا خبرش رو بهتون می‌دیم!

پس حواست به ربات باشه 😉🔔

---
🌟 **ارتباط با ما:**
👤 ادمین: @Shirzad2026
🌐 وبسایت: https://zippy-semolina-6c6cec.netlify.app/
"""

    await query.edit_message_text(
        news_text,
        reply_markup=get_back_button(),
        parse_mode="Markdown",
        disable_web_page_preview=True
    )


async def show_projects(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش پروژه‌ها"""
    query = update.callback_query
    await query.answer()

    projects_text = """🎬 **پروژه‌های Z208**

👋 سلام! ما توی Z208 در حال ساختن و کوششیم.

🎯 **الآن در چه وضعیتی هستیم؟**
ما فعلاً در مرحله‌ی توسعه هستیم و هنوز پروژه‌ای رو به طور کامل آماده نکردیم که به نمایش بذاریم. 
اما داریم با دقت و حوصله کار می‌کنیم تا چیزایی بسازیم که واقعاً ارزشمند باشه.

💪 **چه کار می‌کنیم؟**
• یادگیری مداوم و ارتقاء مهارت‌ها
• کار روی ایده‌های جدید
• ساخت و تست برنامه‌های کاربردی

🔜 **به زودی...**
وقتی اولین پروژه‌مون آماده بشه، همین‌جا با افتخار معرفیش می‌کنیم!

✨ **چرا عجله نمی‌کنیم؟**
چون باور داریم کیفیت مهم‌تر از کمیت هست. می‌خوایم چیزی بسازیم که واقعاً بهش افتخار کنیم.

---
📩 **برای همکاری یا پیشنهاد:**
👤 @Shirzad2026
🌐 https://zippy-semolina-6c6cec.netlify.app/

**با هم می‌سازیم، قدم به قدم!** 🤝✨
"""

    await query.edit_message_text(
        projects_text,
        reply_markup=get_back_button(),
        parse_mode="Markdown",
        disable_web_page_preview=True
    )
