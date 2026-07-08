import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from config import BOT_TOKEN, ADMIN_IDS
from database import db

# ایمپورت هندلرها
from handlers.start import start, main_menu_callback
from handlers.anime_handler import (anime_menu, show_top_anime, show_new_anime,
                                     show_anime_genre_menu, show_anime_by_genre,
                                     show_classic_anime, show_movie_anime,
                                     random_anime, search_anime)
from handlers.ai_assistant import ai_menu, handle_ai_query
from handlers.support import support_menu, handle_support_message, rate_bot
from handlers.news import show_news, show_projects
from handlers.admin import (admin_menu, show_users, show_stats,
                            start_broadcast, handle_broadcast_message)

# تنظیمات لاگینگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class Z208Bot:
    def __init__(self):
        self.app = Application.builder().token(BOT_TOKEN).build()
        self.setup_handlers()

    def setup_handlers(self):
        """تنظیم تمام هندلرهای ربات"""

        # دستورات اصلی
        self.app.add_handler(CommandHandler("start", start))
        self.app.add_handler(CommandHandler("admin", self.admin_command))

        # ============ منوی اصلی ============
        self.app.add_handler(CallbackQueryHandler(
            main_menu_callback, pattern='^main_menu$'))

        # انیمه‌ها
        self.app.add_handler(CallbackQueryHandler(
            anime_menu, pattern='^menu_anime$'))
        self.app.add_handler(CallbackQueryHandler(
            show_top_anime, pattern='^anime_top$'))
        self.app.add_handler(CallbackQueryHandler(
            show_new_anime, pattern='^anime_new$'))
        self.app.add_handler(CallbackQueryHandler(
            show_anime_genre_menu, pattern='^anime_genre$'))
        self.app.add_handler(CallbackQueryHandler(
            show_anime_by_genre, pattern='^anime_genre_'))
        self.app.add_handler(CallbackQueryHandler(
            show_classic_anime, pattern='^anime_classic$'))
        self.app.add_handler(CallbackQueryHandler(
            show_movie_anime, pattern='^anime_movie$'))
        self.app.add_handler(CallbackQueryHandler(
            random_anime, pattern='^anime_random$'))

        # هوش مصنوعی
        self.app.add_handler(CallbackQueryHandler(
            ai_menu, pattern='^menu_ai$'))

        # اخبار و پروژه‌ها
        self.app.add_handler(CallbackQueryHandler(
            show_news, pattern='^menu_news$'))
        self.app.add_handler(CallbackQueryHandler(
            show_projects, pattern='^menu_projects$'))

        # پشتیبانی و امتیازدهی
        self.app.add_handler(CallbackQueryHandler(
            support_menu, pattern='^menu_support$'))
        self.app.add_handler(CallbackQueryHandler(
            rate_bot, pattern='^menu_rate$'))

        # ============ پنل ادمین ============
        self.app.add_handler(CallbackQueryHandler(
            admin_menu, pattern='^admin_menu$'))
        self.app.add_handler(CallbackQueryHandler(
            show_users, pattern='^admin_users$'))
        self.app.add_handler(CallbackQueryHandler(
            show_stats, pattern='^admin_stats$'))
        self.app.add_handler(CallbackQueryHandler(
            start_broadcast, pattern='^admin_broadcast$'))

        # ============ پیام‌های متنی ============
        self.app.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND, self.handle_text_messages))

        # خطاها
        self.app.add_error_handler(self.error_handler)

    async def admin_command(self, update: Update, context):
        """دسترسی به پنل ادمین"""
        if update.effective_user.id in ADMIN_IDS:
            await admin_menu(update, context)
        else:
            await update.message.reply_text("⛔ شما دسترسی به پنل ادمین ندارید!")

    async def handle_text_messages(self, update: Update, context):
        """پردازش پیام‌های متنی بر اساس context فعلی"""
        user_state = context.user_data.get('state', 'normal')

        if user_state == 'ai_chat':
            await handle_ai_query(update, context)
        elif user_state == 'support_chat':
            await handle_support_message(update, context)
        elif user_state == 'broadcast_message':
            await handle_broadcast_message(update, context)
        else:
            # حالت پیش‌فرض: ارسال به هوش مصنوعی
            await handle_ai_query(update, context)

    async def error_handler(self, update: Update, context):
        """مدیریت خطاها"""
        logger.error(f"Update {update} caused error {context.error}")

        try:
            if update and update.effective_message:
                await update.effective_message.reply_text(
                    "😔 متأسفانه خطایی رخ داد. لطفاً دوباره تلاش کنید یا با پشتیبانی تماس بگیرید."
                )
        except:
            pass

    def run(self):
        """اجرای ربات"""
        logger.info("🤖 Z208 Bot is starting...")
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    bot = Z208Bot()
    bot.run()
