from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from keyboards.menus import get_contact_keyboard, get_back_button, get_main_menu
from config import ADMIN_IDS
import random
from datetime import datetime


async def support_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """منوی پشتیبانی"""
    query = update.callback_query
    await query.answer()

    support_text = """💬 **پشتیبانی Z208**

سلام! 😊 ما همیشه آماده کمک به شما هستیم.

📋 **راه‌های ارتباط با ما:**

• 📱 **چت آنلاین:** همین‌جا پیامتون رو بفرستید
• 📞 **تماس تلفنی:** 0792696278
• 📧 **ایمیل:** edriszenandi@gmail.com
• 👤 **ادمین:** @Shirzad2026

⏰ **ساعت پاسخگویی:**
همه روزه از ۹ صبح تا ۱۰ شب

💡 **چطور می‌تونیم کمکتون کنیم؟**
• سوال درباره خدمات
• مشکل فنی در ربات
• ثبت سفارش جدید
• پیشنهاد و انتقاد

پیامتون رو همین‌جا بنویسید تا در سریع‌ترین زمان ممکن پاسخ بدیم! ✨"""

    await query.edit_message_text(
        support_text,
        reply_markup=get_back_button(),
        parse_mode="Markdown"
    )
    context.user_data['state'] = 'support_chat'


async def handle_support_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ارسال پیام کاربر به ادمین"""
    user_message = update.message.text.strip()
    user = update.effective_user
    user_id = user.id

    # بررسی خالی نبودن پیام
    if not user_message:
        await update.message.reply_text(
            "⚠️ لطفاً پیام خودتون رو بنویسید.",
            reply_markup=get_back_button()
        )
        return

    # زمان ارسال
    sent_time = datetime.now().strftime("%Y/%m/%d - %H:%M")

    # ارسال پیام به ادمین با فرمت زیبا
    admin_message = f"""📨 **پیام جدید از کاربر**

👤 **نام:** {user.first_name or 'ناشناس'}
🆔 **آیدی عددی:** `{user_id}`
📎 **یوزرنیم:** @{user.username if user.username else 'ندارد'}
🕐 **زمان:** {sent_time}

💬 **متن پیام:**
{user_message}

---
🔹 برای پاسخ به کاربر از دستور `/reply {user_id}` استفاده کنید."""

    sent_successfully = False
    for admin_id in ADMIN_IDS:
        try:
            await context.bot.send_message(
                chat_id=admin_id,
                text=admin_message,
                parse_mode="Markdown"
            )
            sent_successfully = True
        except Exception as e:
            print(f"Error sending to admin {admin_id}: {e}")

    # پاسخ به کاربر
    if sent_successfully:
        # پیام‌های متنوع تأیید
        confirmations = [
            "✅ **پیام شما با موفقیت ارسال شد!**\n\nتیم پشتیبانی به زودی با شما تماس می‌گیره.\nصبر و شکیبایی شما رو ارج می‌نهیم 🙏✨",
            "📨 **دریافت شد!**\n\nپیامتون به دست تیم پشتیبانی رسید.\nبه زودی پاسخگو خواهیم بود 😊🌟",
            "🎯 **پیامتون ثبت شد!**\n\nهمکاران ما در اسرع وقت بررسی می‌کنن و پاسخ می‌دن.\nممنون از همراهیتون 💚"
        ]

        await update.message.reply_text(
            random.choice(confirmations),
            reply_markup=get_main_menu(),
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            "❌ متأسفانه مشکلی در ارسال پیام پیش اومد.\n"
            "لطفاً مستقیماً با ادمین در ارتباط باشید:\n"
            "@Shirzad2026",
            reply_markup=get_main_menu()
        )


async def rate_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """امتیازدهی به ربات با افکت‌های جذاب"""
    query = update.callback_query
    await query.answer()

    keyboard = [
        [
            InlineKeyboardButton("😡", callback_data='rate_1'),
            InlineKeyboardButton("😐", callback_data='rate_2'),
            InlineKeyboardButton("🙂", callback_data='rate_3'),
            InlineKeyboardButton("😊", callback_data='rate_4'),
            InlineKeyboardButton("🤩", callback_data='rate_5')
        ],
        [InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data='main_menu')]
    ]

    rate_text = """⭐ **به Z208 امتیاز بده!**

نظر واقعیت رو بگو، ما گوشمون همیشه به شماست! 👂

🔹 نظر شما به ما کمک می‌کنه تا:
• خدماتمون رو بهتر کنیم
• مشکلات رو سریع‌تر برطرف کنیم
• ویژگی‌های جدید اضافه کنیم

روی یکی از ایموجی‌های زیر کلیک کن:"""

    await query.edit_message_text(
        rate_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )


async def handle_rating(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پردازش امتیاز کاربر"""
    query = update.callback_query
    await query.answer()

    # استخراج امتیاز
    rate = int(query.data.split('_')[1])
    user = query.from_user

    # ذخیره امتیاز (می‌تونی به دیتابیس اضافه کنی)
    # db.save_rating(user.id, rate)

    # پیام‌های متنوع بر اساس امتیاز
    if rate <= 2:
        response = "😔 متأسفیم که راضی نبودید.\nلطفاً از بخش پشتیبانی بهمون بگید چطور می‌تونیم بهتر بشیم."
    elif rate == 3:
        response = "🙂 ممنون از نظرتون!\nما همیشه در تلاشیم تا بهترین باشیم."
    elif rate == 4:
        response = "😊 خوشحالمون کردید!\nنظر مثبت شما انرژی ما رو چند برابر می‌کنه."
    else:
        response = "🤩 وااای! شما فوق‌العاده‌اید!\nاین امتیاز عالی باعث افتخار ماست. دوستون داریم! 💚"

    stars = "⭐" * rate

    await query.edit_message_text(
        f"{stars}\n\n{response}\n\n"
        "💡 اگر پیشنهادی برای بهبود ربات داری، حتماً بهمون بگو!",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("💬 ارسال پیشنهاد", callback_data='support')],
            [InlineKeyboardButton("🔙 بازگشت", callback_data='main_menu')]
        ])
    )


async def about_us(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """درباره ما"""
    query = update.callback_query
    await query.answer()

    about_text = f"""🎬 **درباره Z208 Studio**

ما یه تیم کوچیک اما پرانرژی هستیم که عاشق ساخت برنامه‌های کاربردی و خلاقانه‌ایم.

💪 **ماموریت ما:**
ساخت ابزارهای دیجیتالی که زندگی رو برای همه راحت‌تر و جذاب‌تر کنه.

🎯 **ارزش‌های ما:**
• کیفیت رو فدای سرعت نمی‌کنیم
• همیشه در حال یادگیری هستیم
• صداقت و شفافیت با کاربرا برامون اولویته
• هر پروژه رو با عشق می‌سازیم

📞 **راه‌های ارتباطی:**
• 📱 تلفن: 0792696278
• 📧 ایمیل: edriszenandi@gmail.com
• 👤 ادمین: @Shirzad2026
• 🌐 وبسایت: https://zippy-semolina-6c6cec.netlify.app/

---
**با Z208، خلاقیت رو تجربه کن!** ✨🚀"""

    await query.edit_message_text(
        about_text,
        reply_markup=get_back_button(),
        parse_mode="Markdown",
        disable_web_page_preview=True
    )
