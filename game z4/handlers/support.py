from telegram import Update
from telegram.ext import ContextTypes
from keyboards.menus import get_contact_keyboard, get_back_button, get_main_menu
from config import ADMIN_IDS


async def support_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """منوی پشتیبانی"""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "💬 بخش پشتیبانی Z208\n\n"
        "برای ارتباط با تیم پشتیبانی، می‌تونید:\n"
        "• پیام خودتون رو اینجا بفرستید\n"
        "• با شماره زیر تماس بگیرید\n\n"
        "📞 تلفن-0792696278\n"
        "📧 ایمیل: support@z208.studio\n\n"
        "پیام شما در اسرع وقت بررسی خواهد شد.",
        reply_markup=get_back_button()
    )
    context.user_data['state'] = 'support_chat'


async def handle_support_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ارسال پیام کاربر به ادمین"""
    user_message = update.message.text
    user = update.effective_user

    # ارسال پیام به ادمین
    for admin_id in ADMIN_IDS:
        try:
            await context.bot.send_message(
                chat_id=admin_id,
                text=f"📨 پیام جدید از کاربر:\n"
                f"👤 کاربر: {user.first_name} (@{user.username})\n"
                f"🆔 آیدی: {user.id}\n"
                f"💬 پیام: {user_message}"
            )
        except:
            pass

    await update.message.reply_text(
        "✅ پیام شما با موفقیت ارسال شد.\n"
        "تیم پشتیبانی به زودی با شما تماس خواهد گرفت.",
        reply_markup=get_main_menu()
    )


async def rate_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """امتیازدهی به ربات"""
    query = update.callback_query
    await query.answer()

    from telegram import InlineKeyboardButton, InlineKeyboardMarkup

    keyboard = [
        [InlineKeyboardButton("⭐", callback_data='rate_1'),
         InlineKeyboardButton("⭐⭐", callback_data='rate_2'),
         InlineKeyboardButton("⭐⭐⭐", callback_data='rate_3'),
         InlineKeyboardButton("⭐⭐⭐⭐", callback_data='rate_4'),
         InlineKeyboardButton("⭐⭐⭐⭐⭐", callback_data='rate_5')],
        [InlineKeyboardButton("🔙 بازگشت", callback_data='main_menu')]
    ]

    await query.edit_message_text(
        "⭐ به ربات Z208 امتیاز دهید:\n"
        "نظر شما به ما کمک می‌کنه تا بهتر بشیم! 🌟",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
