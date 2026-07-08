from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


def get_main_menu():
    """منوی اصلی ربات"""
    keyboard = [
        [InlineKeyboardButton("🎬 انیمه‌های پیشنهادی",
                              callback_data='menu_anime')],
        [InlineKeyboardButton("🤖 دستیار هوش مصنوعی", callback_data='menu_ai')],
        [InlineKeyboardButton("📰 آخرین اخبار Z208",
                              callback_data='menu_news')],
        [InlineKeyboardButton("🎯 پروژه‌های ما",
                              callback_data='menu_projects')],
        [InlineKeyboardButton("💬 ارتباط با پشتیبانی",
                              callback_data='menu_support')],
        [InlineKeyboardButton("⭐ امتیاز دادن به ربات",
                              callback_data='menu_rate')]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_anime_menu():
    """منوی انیمه‌های پیشنهادی"""
    keyboard = [
        [InlineKeyboardButton("🔥 انیمه‌های برتر و محبوب",
                              callback_data='anime_top')],
        [InlineKeyboardButton("🆕 انیمه‌های جدید ۲۰۲۵-۲۰۲۶",
                              callback_data='anime_new')],
        [InlineKeyboardButton("🎭 بر اساس ژانر",
                              callback_data='anime_genre')],
        [InlineKeyboardButton("⭐ انیمه‌های کلاسیک و خاطره‌انگیز",
                              callback_data='anime_classic')],
        [InlineKeyboardButton("🎬 انیمه‌های سینمایی",
                              callback_data='anime_movie')],
        [InlineKeyboardButton("🎲 یه انیمه تصادفی بهم پیشنهاد بده!",
                              callback_data='anime_random')],
        [InlineKeyboardButton("🔙 بازگشت به منوی اصلی",
                              callback_data='main_menu')]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_anime_genre_menu():
    """منوی ژانرهای انیمه"""
    keyboard = [
        [InlineKeyboardButton("⚔️ اکشن و ماجراجویی",
                              callback_data='anime_genre_action'),
         InlineKeyboardButton("😂 کمدی و طنز",
                              callback_data='anime_genre_comedy')],
        [InlineKeyboardButton("💕 عاشقانه و درام",
                              callback_data='anime_genre_romance'),
         InlineKeyboardButton("🔮 فانتزی و ماورایی",
                              callback_data='anime_genre_fantasy')],
        [InlineKeyboardButton("🤖 علمی تخیلی و مکا",
                              callback_data='anime_genre_scifi'),
         InlineKeyboardButton("👻 ترسناک و روانشناختی",
                              callback_data='anime_genre_horror')],
        [InlineKeyboardButton("🏃 ورزشی", callback_data='anime_genre_sports'),
         InlineKeyboardButton("🎵 موزیکال", callback_data='anime_genre_music')],
        [InlineKeyboardButton("🔙 بازگشت", callback_data='menu_anime')]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_back_button():
    """دکمه بازگشت"""
    keyboard = [[InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data='main_menu')]]
    return InlineKeyboardMarkup(keyboard)


def get_admin_menu():
    """منوی پنل ادمین"""
    keyboard = [
        [InlineKeyboardButton("👥 مشاهده کاربران",
                              callback_data='admin_users')],
        [InlineKeyboardButton("📊 آمار ربات", callback_data='admin_stats')],
        [InlineKeyboardButton("📨 ارسال پیام همگانی",
                              callback_data='admin_broadcast')],
        [InlineKeyboardButton("🎬 مدیریت انیمه‌ها",
                              callback_data='admin_anime')],
        [InlineKeyboardButton("📝 مدیریت محتوا",
                              callback_data='admin_content')],
        [InlineKeyboardButton("🚫 مدیریت کاربران مسدود",
                              callback_data='admin_blocks')],
        [InlineKeyboardButton("🔙 خروج از پنل ادمین",
                              callback_data='main_menu')]
    ]
    return InlineKeyboardMarkup(keyboard)
