from telegram import Update
from telegram.ext import ContextTypes
from database import db
from keyboards.menus import get_main_menu
from config import STUDIO_NAME, STUDIO_DESCRIPTION


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """هندلر دستور /start"""
    user = update.effective_user

    # ذخیره اطلاعات کاربر در دیتابیس
    db.add_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name
    )

    welcome_message = f"""
🌟 به {STUDIO_NAME} خوش اومدی {user.first_name} عزیز!

{STUDIO_DESCRIPTION}

🎯 من دستیار هوشمند Z208 هستم و می‌تونم در موارد زیر کمکت کنم:

• 🎮 بازی‌های سرگرم‌کننده و چالش‌برانگیز
• 🤖 پاسخ به سوالات با هوش مصنوعی
• 📰 اطلاع از آخرین اخبار استودیو
• 🎬 مشاهده نمونه کارها و پروژه‌ها
• 💬 ارتباط با تیم پشتیبانی

از منوی زیر گزینه مورد نظرت رو انتخاب کن! 👇
    """

    await update.message.reply_text(
        welcome_message,
        reply_markup=get_main_menu(),
        parse_mode='HTML'
    )


async def main_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """بازگشت به منوی اصلی"""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        f"🎯 منوی اصلی {STUDIO_NAME}\n"
        "لطفاً گزینه مورد نظر خود را انتخاب کنید:",
        reply_markup=get_main_menu()
    )
