from telegram import Update
from telegram.ext import ContextTypes
from database import db
from keyboards.menus import get_admin_menu, get_back_button
from config import ADMIN_IDS


async def admin_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پنل مدیریت"""
    query = update.callback_query
    if query:
        await query.answer()
        await query.edit_message_text(
            "🔐 پنل مدیریت Z208\n"
            "لطفاً گزینه مورد نظر را انتخاب کنید:",
            reply_markup=get_admin_menu()
        )
    else:
        await update.message.reply_text(
            "🔐 پنل مدیریت Z208\n"
            "لطفاً گزینه مورد نظر را انتخاب کنید:",
            reply_markup=get_admin_menu()
        )


async def show_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش لیست کاربران"""
    query = update.callback_query
    await query.answer()

    users = db.get_all_users()

    if not users:
        await query.edit_message_text(
            "👥 هنوز کاربری ثبت نشده است.",
            reply_markup=get_admin_menu()
        )
        return

    users_text = "👥 لیست کاربران:\n\n"
    for user in users[:20]:  # نمایش ۲۰ کاربر اول
        users_text += f"• {user[2] or 'ناشناس'} (ID: {user[0]})\n"

    if len(users) > 20:
        users_text += f"\n... و {len(users) - 20} کاربر دیگر"

    await query.edit_message_text(
        users_text,
        reply_markup=get_admin_menu()
    )


async def show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش آمار ربات"""
    query = update.callback_query
    await query.answer()

    import sqlite3
    conn = sqlite3.connect('z208_bot.db')
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM users')
    total_users = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM messages')
    total_messages = cursor.fetchone()[0]

    cursor.execute('SELECT SUM(score) FROM users')
    total_scores = cursor.fetchone()[0] or 0

    conn.close()

    stats_text = f"""
📊 آمار ربات Z208:

👥 تعداد کاربران: {total_users}
💬 تعداد پیام‌ها: {total_messages}
⭐ مجموع امتیازات: {total_scores}
📅 تاریخ: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}
    """

    await query.edit_message_text(
        stats_text,
        reply_markup=get_admin_menu()
    )


async def start_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """شروع ارسال پیام همگانی"""
    query = update.callback_query
    await query.answer()

    context.user_data['state'] = 'broadcast_message'

    await query.edit_message_text(
        "📨 پیام خود را برای ارسال به همه کاربران وارد کنید:\n"
        "(برای لغو، /cancel را بفرستید)",
        reply_markup=get_back_button()
    )


async def handle_broadcast_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ارسال پیام همگانی"""
    message = update.message.text

    if message == '/cancel':
        context.user_data['state'] = 'normal'
        await update.message.reply_text("❌ ارسال پیام همگانی لغو شد.", reply_markup=get_admin_menu())
        return

    users = db.get_all_users()
    success_count = 0

    for user in users:
        try:
            await context.bot.send_message(chat_id=user[0], text=f"📢 پیام از طرف Z208:\n\n{message}")
            success_count += 1
        except:
            continue

    context.user_data['state'] = 'normal'

    await update.message.reply_text(
        f"✅ پیام با موفقیت به {success_count} از {len(users)} کاربر ارسال شد.",
        reply_markup=get_admin_menu()
    )
