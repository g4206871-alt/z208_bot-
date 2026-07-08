from telegram import Update
from telegram.ext import ContextTypes
from database import db
from utils.ai_service import ai_service
from keyboards.menus import get_back_button
import random


async def ai_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش منوی دستیار هوش مصنوعی"""
    query = update.callback_query
    await query.answer()

    # پیام خوش‌آمدگویی با ایموجی‌های جذاب
    welcome_messages = [
        f"""🤖 *به دستیار هوشمند Z208 خوش اومدی!* 🌟

من اینجام تا هر سوالی داری رو برات جواب بدم. از خدمات استودیو گرفته تا مشاوره خلاقانه، هر چی دوست داری بپرس!

💡 *چندتا مثال باحال:*
• 🎨 طراحی لوگو چقدر طول میکشه؟
• 💻 یه سایت فروشگاهی می‌خوام، از کجا شروع کنم؟
• 📱 چطور تو اینستاگرام رشد کنم؟
• 🎬 ساخت تیزر تبلیغاتی چقدر هزینه داره؟
• 🚀 بهترین استراتژی دیجیتال مارکتینگ چیه؟

🧠 *یا حتی سوالات عمومی:*
• ساعت چنده؟
• یه جوک بگو
• یه جمله انگیزشی می‌خوام

✨ فقط کافیه سوالت رو به صورت متن بفرستی!
🎯 برای برگشت به منوی اصلی، دکمه زیر رو بزن.""",

        f"""🌟 *سلام به دنیای هوش مصنوعی Z208!* 🤖

کنجکاویهات رو با من به اشتراک بذار! هر سوالی تو حوزه‌های زیر داشته باشی، جواب می‌دم:

🎨 طراحی و خلاقیت
💻 تکنولوژی و توسعه
📱 شبکه‌های اجتماعی
📈 بازاریابی و رشد
💡 ایده‌پردازی

*فقط کافیه بنویسی...* 📝"""
    ]

    await query.edit_message_text(
        random.choice(welcome_messages),
        reply_markup=get_back_button(),
        parse_mode="Markdown"
    )

    # ذخیره وضعیت کاربر در context
    context.user_data['in_ai_chat'] = True
    context.user_data['message_count'] = 0


async def handle_ai_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پردازش هوشمند سوال کاربر با امکانات پیشرفته"""
    user = update.effective_user
    user_message = update.message.text.strip()
    user_id = user.id
    first_name = user.first_name or "کاربر عزیز"

    # بررسی وضعیت چت
    if not context.user_data.get('in_ai_chat', False):
        # اگه کاربر تازه وارد چت AI شده
        context.user_data['in_ai_chat'] = True
        context.user_data['message_count'] = 0

    # افزایش شمارنده پیام‌ها
    context.user_data['message_count'] = context.user_data.get('message_count', 0) + 1
    message_count = context.user_data['message_count']

    # ============ پیام‌های ویژه بر اساس تعداد تعامل ============
    special_messages = {
        1: f"🌟 {first_name} جان، خوشحالم که اولین سوالت رو می‌پررسی!",
        5: f"🎯 {first_name} عزیز، چه کنجکاوی! این پنجمین سوالتونه.",
        10: f"🏆 وااای {first_name}! ۱۰ تا سوال پرسیدی! تو واقعاً اهل یادگیری هستی!",
        20: f"👑 {first_name}، تو بهترین کاربر من هستی! ۲۰ سوال یعنی کلی گپ خوب داشتیم!",
        50: f"🚀 {first_name} افسانه‌ای! ۵۰ سوال! باید یه تندیس بهت بدم! 😄",
        100: f"💎 {first_name}، تو دیگه یه افسانه‌ای! ۱۰۰ سوال یعنی کلی یاد گرفتیم و خندیدیم!"
    }

    # نمایش وضعیت تایپ با افکت‌های مختلف
    typing_actions = ["typing", "upload_photo", "record_video", "upload_video"]
    await update.message.chat.send_action(action=random.choice(typing_actions))

    # ============ ساخت context اطلاعاتی غنی برای AI ============
    context_info = f"""
    نام کاربر: {first_name}
    آیدی کاربر: {user_id}
    تعداد سوالات این جلسه: {message_count}
    زمان: الان
    """

    # ============ دریافت پاسخ از هوش مصنوعی ============
    ai_response = ai_service.get_response(user_message, context_info)

    # ============ ذخیره در دیتابیس با اطلاعات کامل ============
    try:
        db.save_message(user_id, user_message, ai_response)
    except Exception as e:
        print(f"Database save error: {e}")

    # ============ ساخت پاسخ نهایی با استایل ============
    # اضافه کردن پیام ویژه بر اساس تعداد
    special_prefix = ""
    if message_count in special_messages:
        special_prefix = f"{special_messages[message_count]}\n\n"

    # انتخاب ایموجی پاسخ بر اساس محتوای پاسخ
    response_emoji = get_response_emoji(ai_response)

    # استایل‌دهی پاسخ
    styled_response = f"{special_prefix}{response_emoji} *پاسخ Z208 AI:*\n\n{ai_response}"

    # ============ پیشنهادات هوشمند برای ادامه گفتگو ============
    suggestions = get_smart_suggestions(user_message, ai_response)

    if suggestions and message_count % 3 == 0:  # هر ۳ پیام یکبار پیشنهاد بده
        styled_response += f"\n\n💡 *شاید این سوالات هم برات جالب باشه:*\n{suggestions}"

    # اضافه کردن دعوت به ادامه گفتگو
    encouragements = [
        "\n\n✨ سوال دیگه‌ای داری؟ من همیشه آماده‌ام!",
        "\n\n🚀 بازم بپرس! کلی چیزای جذاب دیگه هست که می‌تونیم درباره‌ش حرف بزنیم.",
        "\n\n💭 هر سوال دیگه‌ای تو ذهنت هست، بگو!",
        "\n\n🎯 کنجکاوی رو ادامه بده! سوال بعدی چیه؟",
        "\n\n🌟 منتظر سوال بعدیت هستم!",
        "\n\n💫 اگه سوال دیگه‌ای داری، دریغ نکن!"
    ]
    styled_response += random.choice(encouragements)

    # ============ ارسال پاسخ ============
    await update.message.reply_text(
        styled_response,
        reply_markup=get_back_button(),
        parse_mode="Markdown"
    )

    # ============ لاگ کردن برای تحلیل ============
    print(f"[AI Chat] User: {first_name} (ID: {user_id}) | "
          f"Msg #{message_count} | Query: {user_message[:50]}...")


def get_response_emoji(response_text: str) -> str:
    """تشخیص ایموجی مناسب بر اساس محتوای پاسخ"""
    response_lower = response_text.lower()

    if any(w in response_lower for w in ["سلام", "خوش", "درود", "خوش‌آمد"]):
        return "👋"
    elif any(w in response_lower for w in ["ممنون", "خواهش", "تشکر"]):
        return "🙏"
    elif any(w in response_lower for w in ["طراحی", "گرافیک", "لوگو", "رنگ"]):
        return "🎨"
    elif any(w in response_lower for w in ["وب", "سایت", "برنامه", "کد"]):
        return "💻"
    elif any(w in response_lower for w in ["مارکتینگ", "بازاریابی", "فروش"]):
        return "📈"
    elif any(w in response_lower for w in ["شبکه", "اجتماعی", "اینستاگرام", "تلگرام"]):
        return "📱"
    elif any(w in response_lower for w in ["ویدیو", "فیلم", "تیزر", "تدوین"]):
        return "🎬"
    elif any(w in response_lower for w in ["قیمت", "هزینه", "سفارش"]):
        return "💰"
    elif any(w in response_lower for w in ["جوک", "خنده", "بامزه"]):
        return "😄"
    elif any(w in response_lower for w in ["انگیزه", "موفقیت", "تلاش"]):
        return "💪"
    elif any(w in response_lower for w in ["ساعت", "زمان", "تاریخ"]):
        return "⏰"
    elif any(w in response_lower for w in ["ربات", "هوش", "مصنوعی"]):
        return "🤖"
    else:
        return random.choice(["✨", "🌟", "💡", "🎯", "🚀", "💫", "🔥"])


def get_smart_suggestions(user_message: str, ai_response: str) -> str:
    """پیشنهاد سوالات مرتبط بر اساس گفتگو"""
    msg_lower = user_message.lower()
    suggestions = []

    if any(w in msg_lower for w in ["طراحی", "گرافیک", "لوگو"]):
        suggestions = [
            "🎨 طراحی بنر تبلیغاتی چقدر طول میکشه؟",
            "🖌️ تفاوت طراحی وکتور و رستر چیه؟",
            "🌈 بهترین ترکیب رنگ برای برند من چیه؟"
        ]
    elif any(w in msg_lower for w in ["وب", "سایت", "اپلیکیشن"]):
        suggestions = [
            "💻 هزینه طراحی سایت فروشگاهی چقدره؟",
            "📱 سایت بهتره یا اپلیکیشن موبایل؟",
            "🔒 امنیت سایت چطور تأمین میشه؟"
        ]
    elif any(w in msg_lower for w in ["بازاریابی", "مارکتینگ", "فروش"]):
        suggestions = [
            "📈 بهترین روش تبلیغات برای کسب‌وکار کوچیک چیه؟",
            "🎯 چطور مشتری هدف رو پیدا کنم؟",
            "💡 استراتژی محتوا رو چطور بچینم؟"
        ]
    elif any(w in msg_lower for w in ["قیمت", "هزینه", "سفارش"]):
        suggestions = [
            "💰 شرایط پرداخت چطوریه؟",
            "📋 مراحل ثبت سفارش چه شکلیه؟",
            "⏱️ زمان تحویل پروژه چقدره؟"
        ]

    if suggestions:
        return "\n".join([f"• {s}" for s in random.sample(suggestions, min(2, len(suggestions)))])

    return ""


def get_ai_stats(user_id: int) -> dict:
    """دریافت آمار استفاده از AI برای یک کاربر"""
    try:
        messages = db.get_user_messages(user_id, limit=100)
        total = len(messages)
        return {
            "total_messages": total,
            "status": "فعال" if total > 0 else "غیرفعال",
            "level": "مبتدی" if total < 10 else "متوسط" if total < 50 else "پیشرفته" if total < 100 else "افسانه‌ای"
        }
    except:
        return {"total_messages": 0, "status": "نامشخص", "level": "تازه‌کار"}
