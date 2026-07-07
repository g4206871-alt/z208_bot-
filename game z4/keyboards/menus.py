from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


def get_main_menu():
    """منوی اصلی ربات"""
    keyboard = [
        [InlineKeyboardButton("🎮 بازی‌ها و سرگرمی",
                              callback_data='menu_games')],
        [InlineKeyboardButton("🤖 دستیار هوش مصنوعی", callback_data='menu_ai')],
        [InlineKeyboardButton("📰 آخرین اخبار Z208",
                              callback_data='menu_news')],
        [InlineKeyboardButton("🎬 معرفی پروژه‌ها",
                              callback_data='menu_projects')],
        [InlineKeyboardButton("💬 ارتباط با پشتیبانی",
                              callback_data='menu_support')],
        [InlineKeyboardButton("⭐ امتیاز دادن به ربات",
                              callback_data='menu_rate')]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_games_menu():
    """منوی بازی‌ها"""
    keyboard = [
        [InlineKeyboardButton("😂 جوک و داستان کوتاه",
                              callback_data='game_joke')],
        [InlineKeyboardButton("🧩 معما و چالش ذهنی",
                              callback_data='game_riddle')],
        [InlineKeyboardButton(
            "🎯 بازی حدس کلمه", callback_data='game_word_guess')],
        [InlineKeyboardButton("🏆 رتبه‌بندی کاربران",
                              callback_data='game_leaderboard')],
        [InlineKeyboardButton("🔙 بازگشت به منوی اصلی",
                              callback_data='main_menu')]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_back_button():
    """دکمه بازگشت"""
    keyboard = [[InlineKeyboardButton("🔙 بازگشت", callback_data='main_menu')]]
    return InlineKeyboardMarkup(keyboard)


def get_admin_menu():
    """منوی پنل ادمین"""
    keyboard = [
        [InlineKeyboardButton("👥 مشاهده کاربران",
                              callback_data='admin_users')],
        [InlineKeyboardButton("📊 آمار ربات", callback_data='admin_stats')],
        [InlineKeyboardButton("📨 ارسال پیام همگانی",
                              callback_data='admin_broadcast')],
        [InlineKeyboardButton(
            "📝 مدیریت محتوا", callback_data='admin_content')],
        [InlineKeyboardButton("🚫 مدیریت کاربران مسدود",
                              callback_data='admin_blocks')],
        [InlineKeyboardButton("🔙 خروج از پنل ادمین",
                              callback_data='main_menu')]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_contact_keyboard():
    """کیبورد اشتراک‌گذاری تماس"""
    keyboard = [
        [KeyboardButton("📱 اشتراک‌گذاری شماره تماس", request_contact=True)]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
