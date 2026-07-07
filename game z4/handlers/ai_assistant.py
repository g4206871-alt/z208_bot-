from telegram import Update
from telegram.ext import ContextTypes
from database import db
from utils.ai_service import ai_service
from keyboards.menus import get_back_button


async def ai_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش منوی دستیار هوش مصنوعی"""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "🤖 به دستیار هوش مصنوعی Z208 خوش اومدی!\n\n"
        "من اینجام تا به سوالاتت پاسخ بدم.\n"
        "می‌تونی هر سوالی در مورد خدمات، پروژه‌ها، یا موضوعات عمومی بپرسی.\n\n"
        "💡 مثال:\n"
        "• خدمات استودیو Z208 چیه؟\n"
        "• چطور می‌تونم یه وب‌سایت طراحی کنم؟\n"
        "• بهترین روش بازاریابی دیجیتال چیه؟\n\n"
        "سوالت رو به صورت متن بفرست! 📝",
        reply_markup=get_back_button()
    )


async def handle_ai_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پردازش سوال کاربر و ارسال به هوش مصنوعی"""
    user_message = update.message.text

    # نمایش وضعیت تایپ
    await update.message.chat.send_action(action="typing")

    # دریافت پاسخ از هوش مصنوعی
    context_info = f"کاربر: {update.effective_user.first_name}"
    ai_response = ai_service.get_response(user_message, context_info)

    # ذخیره در دیتابیس
    db.save_message(update.effective_user.id, user_message, ai_response)

    await update.message.reply_text(
        f"🤖 پاسخ Z208 AI:\n\n{ai_response}\n\n"
        "سوال دیگه‌ای داری؟ بپرس! 💭",
        reply_markup=get_back_button()
    )
