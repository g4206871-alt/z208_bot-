from telegram import Update
from telegram.ext import ContextTypes
from keyboards.menus import get_anime_menu, get_anime_genre_menu, get_back_button, get_main_menu
import random


# ============ دیتابیس انیمه‌ها ============

ANIME_DB = {
    "top": [
        {"name": "حمله به تایتان", "japanese": "Shingeki no Kyojin", "episodes": "۸۷ + ۲ قسمت ویژه",
         "year": "۲۰۲۳-۲۰۱۳", "score": "۹.۱", "desc": "انسان‌ها در برابر غول‌های غول‌پیکر می‌جنگن. داستانی عمیق با پیچش‌های باورنکردنی."},
        {"name": "دث نوت", "japanese": "Death Note", "episodes": "۳۷", "year": "۲۰۰۶",
         "score": "۸.۶", "desc": "دانش‌آموزی یه دفترچه پیدا می‌کنه که هر کی اسمش توش نوشته بشه می‌میره. نبرد ذهنی نفس‌گیر!"},
        {"name": "فول متال آلکمیست: برادرهود", "japanese": "Fullmetal Alchemist: Brotherhood", "episodes": "۶۴",
         "year": "۲۰۰۹", "score": "۹.۱", "desc": "دو برادر برای برگردوندن بدنشون دنبال سنگ جادو می‌گردن. شاهکار بی‌نظیر!"},
        {"name": "مبارز باکسر", "japanese": "Hajime no Ippo", "episodes": "۱۲۷ +", "year": "۲۰۱۴-۲۰۰۰",
         "score": "۸.۸", "desc": "داستان پسری خجالتی که قهرمان بوکس میشه. انگیزشی و پر از صحنه‌های حماسی."},
        {"name": "کد گیاس", "japanese": "Code Geass", "episodes": "۵۰", "year": "۲۰۰۸",
         "score": "۸.۷", "desc": "شاهزاده‌ای تبعیدی قدرت کنترل ذهن بدست میاره. استراتژی، خیانت و پایانی فراموش‌نشدنی."},
        {"name": "استینز گیت", "japanese": "Steins;Gate", "episodes": "۲۴", "year": "۲۰۱۱",
         "score": "۹.۱", "desc": "دانشمند دیوانه‌ای ماشین زمان می‌سازه. داستان سفر در زمان با احساسات عمیق."},
        {"name": "هانتر x هانتر", "japanese": "Hunter x Hunter", "episodes": "۱۴۸", "year": "۲۰۱۴-۲۰۱۱",
         "score": "۹.۰", "desc": "پسربچه‌ای برای پیدا کردن پدرش شکارچی میشه. سیستم قدرتی پیچیده و داستانی عمیق."},
        {"name": "وان پیس", "japanese": "One Piece", "episodes": "۱۰۰۰+", "year": "۱۹۹۹-ادامه دارد",
         "score": "۸.۹", "desc": "لوفی و خدمش دنبال گنج افسانه‌ای وان پیس می‌گردن. ماجراجویی بی‌پایان!"},
        {"name": "جوموتسو کایسن", "japanese": "Jujutsu Kaisen", "episodes": "۴۸ + فیلم", "year": "۲۰۲۳-۲۰۲۰",
         "score": "۸.۷", "desc": "دانش‌آموزی با خوردن انگشت یه نفرین قدرتمند، وارد دنیای جادوگران میشه. اکشن نفس‌گیر!"},
        {"name": "ارن یا شکارچی", "japanese": "Solo Leveling", "episodes": "۲۵+", "year": "۲۰۲۵-۲۰۲۴",
         "score": "۸.۶", "desc": "ضعیف‌ترین شکارچی دنیا قدرت عجیبی بدست میاره. انیمه‌ای با انیمیشن فوق‌العاده!"},
    ],
    "new": [
        {"name": "سولو لولینگ فصل ۲", "japanese": "Solo Leveling S2", "episodes": "۱۳", "year": "۲۰۲۵",
         "score": "۸.۸", "desc": "ادامه ماجرای سونگ جین‌وو که حالا قدرتمندتر از همیشه‌ست."},
        {"name": "کایجو شماره ۸", "japanese": "Kaiju No. 8", "episodes": "۱۲", "year": "۲۰۲۴",
         "score": "۸.۳", "desc": "مردی که تبدیل به هیولا میشه تا با هیولاها بجنگه. اکشن و کمدی عالی!"},
        {"name": "فایریرن", "japanese": "Frieren: Beyond Journey's End", "episodes": "۲۸", "year": "۲۰۲۴-۲۰۲۳",
         "score": "۹.۲", "desc": "جادوگری الف که بعد از مرگ قهرمان، معنای زندگی رو درک می‌کنه. شاهکار احساسی."},
        {"name": "مشل", "japanese": "Mashle: Magic and Muscles", "episodes": "۲۴+", "year": "۲۰۲۴-۲۰۲۳",
         "score": "۷.۸", "desc": "تو دنیایی که همه جادو دارن، یه نفر فقط عضله داره! کمدی محض."},
        {"name": "شاهزاده خانم و حیوان", "japanese": "The Apothecary Diaries", "episodes": "۲۴+", "year": "۲۰۲۴-۲۰۲۳",
         "score": "۸.۷", "desc": "دختر داروسازی که در حرمسرای امپراتور معماها رو حل می‌کنه."},
        {"name": "دندان‌های شیری", "japanese": "Dandadan", "episodes": "۱۲", "year": "۲۰۲۴",
         "score": "۸.۴", "desc": "دختری که به ارواح اعتقاد داره و پسری که به فضایی‌ها. انیمه‌ای دیوانه‌وار و باحال!"},
    ],
    "classic": [
        {"name": "دراگون بال زد", "japanese": "Dragon Ball Z", "episodes": "۲۹۱", "year": "۱۹۹۶-۱۹۸۹",
         "score": "۸.۸", "desc": "گوکو و دوستانش از زمین در برابر تهدیدات فضایی دفاع می‌کنن. افسانه‌ای!"},
        {"name": "ناروتو", "japanese": "Naruto", "episodes": "۲۲۰ + ۵۰۰ شیپودن", "year": "۲۰۱۷-۲۰۰۲",
         "score": "۸.۴", "desc": "نینجای یتیمی که می‌خواد رهبر دهکده بشه. داستان بلوغ و دوستی."},
        {"name": "بلیچ", "japanese": "Bleach", "episodes": "۳۶۶ + دنباله", "year": "۲۰۲۴-۲۰۰۴",
         "score": "۸.۲", "desc": "پسری که شینیگامی میشه تا از ارواح شیطانی محافظت کنه."},
        {"name": "کابوی بی‌باپ", "japanese": "Cowboy Bebop", "episodes": "۲۶", "year": "۱۹۹۸",
         "score": "۸.۹", "desc": "شکارچیان جایزه‌بگیر در فضا. موسیقی جاز و فضای نوآر فوق‌العاده."},
        {"name": "نئون جنسیس اونگلیون", "japanese": "Neon Genesis Evangelion", "episodes": "۲۶ + فیلم",
         "year": "۱۹۹۷-۱۹۹۵", "score": "۸.۵", "desc": "نوجوانانی که با ربات‌های غول‌پیکر موجودات مرموز رو شکست می‌دن. عمیق و فلسفی."},
    ],
    "movie": [
        {"name": "شهر اشباح", "japanese": "Spirited Away", "year": "۲۰۰۱", "score": "۸.۸",
         "desc": "دختری در دنیای ارواح گیر می‌افته. شاهکار هایائو میازاکی و برنده اسکار."},
        {"name": "نام تو", "japanese": "Your Name", "year": "۲۰۱۶", "score": "۸.۹",
         "desc": "پسر و دختری که بدن‌هاشون جابجا میشه. عاشقانه‌ای اشک‌آور و زیبا."},
        {"name": "آکیرا", "japanese": "Akira", "year": "۱۹۸۸", "score": "۸.۶",
         "desc": "توکیوی پساآخرالزمانی و پسری با قدرت روانی. انقلابی در انیمه!"},
        {"name": "پرنسس مونونوکه", "japanese": "Princess Mononoke", "year": "۱۹۹۷", "score": "۸.۸",
         "desc": "جنگ بین انسان و طبیعت. حماسی، عمیق و فراموش‌نشدنی."},
        {"name": "قلعه متحرک هاول", "japanese": "Howl's Moving Castle", "year": "۲۰۰۴", "score": "۸.۷",
         "desc": "دختری که تبدیل به پیرزن میشه و عاشق جادوگری مرموز. فانتزی عاشقانه."},
        {"name": "قاتل شیطان: قطار بی‌نهایت", "japanese": "Demon Slayer: Mugen Train", "year": "۲۰۲۰",
         "score": "۸.۶", "desc": "پرفروش‌ترین انیمه تاریخ ژاپن! تانجیرو در قطاری مرموز با شیطانی قدرتمند می‌جنگه."},
    ],
}

ANIME_BY_GENRE = {
    "action": ["حمله به تایتان", "جوموتسو کایسن", "ارن یا شکارچی", "ناروتو", "بلیچ", "وان پیس", "مبارز باکسر"],
    "comedy": ["وان پانچ من", "گینتاما", "مشل", "سایکی کوسو", "دندان‌های شیری"],
    "romance": ["نام تو", "قلعه متحرک هاول", "فروتس بسکت", "عشق جنگ است", "کمدی رمانتیک من"],
    "fantasy": ["فول متال آلکمیست", "فایریرن", "مشل", "شاهزاده خانم و حیوان", "هانتر x هانتر"],
    "scifi": ["استینز گیت", "کد گیاس", "آکیرا", "کابوی بی‌باپ", "نئون جنسیس اونگلیون"],
    "horror": ["دث نوت", "توکیو غول", "ارواح", "هیولا", "آنیه دیگر"],
    "sports": ["مبارز باکسر", "هایکیو", "کوروکو نو باسکت", "بلو لاک", "اسلم دانک"],
    "music": ["دروغ آوریل تو", "بکی", "کا-اون", "نودامه کانتابیله"],
}

# ژانرها به فارسی
GENRE_NAMES = {
    "action": "اکشن و ماجراجویی ⚔️",
    "comedy": "کمدی و طنز 😂",
    "romance": "عاشقانه و درام 💕",
    "fantasy": "فانتزی و ماورایی 🔮",
    "scifi": "علمی تخیلی و مکا 🤖",
    "horror": "ترسناک و روانشناختی 👻",
    "sports": "ورزشی 🏃",
    "music": "موزیکال 🎵",
}


# ============ Handler ها ============

async def anime_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """منوی اصلی انیمه"""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "🎬 *به دنیای انیمه خوش اومدی!*\n\n"
        "اینجا می‌تونی بهترین انیمه‌ها رو بر اساس سلیقه‌ات پیدا کنی.\n"
        "از منوی زیر انتخاب کن:\n\n"
        "🔥 برترین‌ها\n"
        "🆕 جدیدترین‌ها\n"
        "🎭 بر اساس ژانر\n"
        "⭐ کلاسیک‌ها\n"
        "🎬 سینمایی‌ها\n"
        "🎲 یه پیشنهاد تصادفی!\n\n"
        "انیمه بازها جمع بشن! 😎🍿",
        reply_markup=get_anime_menu(),
        parse_mode="Markdown"
    )


async def show_top_anime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش انیمه‌های برتر"""
    query = update.callback_query
    await query.answer()

    anime_list = ANIME_DB["top"]
    text = "🔥 *برترین انیمه‌های تاریخ*\n\n"

    for i, anime in enumerate(anime_list[:5], 1):
        text += f"{i}. *{anime['name']}*\n"
        text += f"   📺 {anime['episodes']} | ⭐ {anime['score']}\n"
        text += f"   📝 {anime['desc'][:80]}...\n\n"

    text += "🔍 برای دیدن بقیه یا جزئیات بیشتر، به ربات بگو:\n"
    text += "مثلاً: «حمله به تایتان»"

    await query.edit_message_text(
        text,
        reply_markup=get_anime_menu(),
        parse_mode="Markdown"
    )


async def show_new_anime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش انیمه‌های جدید"""
    query = update.callback_query
    await query.answer()

    anime_list = ANIME_DB["new"]
    text = "🆕 *انیمه‌های جدید و داغ ۲۰۲۵-۲۰۲۶*\n\n"

    for anime in anime_list:
        text += f"🎬 *{anime['name']}*\n"
        text += f"   📅 {anime['year']} | ⭐ {anime['score']}\n"
        text += f"   📝 {anime['desc']}\n\n"

    await query.edit_message_text(
        text,
        reply_markup=get_anime_menu(),
        parse_mode="Markdown"
    )


async def show_anime_genre_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش منوی ژانرها"""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "🎭 *انیمه بر اساس ژانر*\n\n"
        "چه حسی داری امروز؟\n"
        "ژانر مورد علاقه‌ات رو انتخاب کن تا بهترین‌ها رو بهت پیشنهاد بدم! 🎯",
        reply_markup=get_anime_genre_menu(),
        parse_mode="Markdown"
    )


async def show_anime_by_genre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش انیمه‌های یک ژانر خاص"""
    query = update.callback_query
    await query.answer()

    genre = query.data.replace("anime_genre_", "")
    genre_name = GENRE_NAMES.get(genre, genre)

    anime_names = ANIME_BY_GENRE.get(genre, [])
    text = f"{genre_name}\n\n"

    if anime_names:
        text += "🎬 *انیمه‌های پیشنهادی:*\n"
        for name in anime_names:
            text += f"• {name}\n"
    else:
        text += "😅 این ژانر در حال بروزرسانیه!"

    text += f"\n💡 برای اطلاعات بیشتر اسم انیمه رو توی ربات جستجو کن!"

    await query.edit_message_text(
        text,
        reply_markup=get_anime_genre_menu(),
        parse_mode="Markdown"
    )


async def show_classic_anime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش انیمه‌های کلاسیک"""
    query = update.callback_query
    await query.answer()

    anime_list = ANIME_DB["classic"]
    text = "⭐ *انیمه‌های کلاسیک و خاطره‌انگیز*\n\n"

    for anime in anime_list:
        text += f"🎬 *{anime['name']}*\n"
        text += f"   📅 {anime['year']} | 📺 {anime['episodes']} | ⭐ {anime['score']}\n"
        text += f"   📝 {anime['desc']}\n\n"

    text += "✨ *نوستالژی رو با این شاهکارها زنده کن!*"

    await query.edit_message_text(
        text,
        reply_markup=get_anime_menu(),
        parse_mode="Markdown"
    )


async def show_movie_anime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش انیمه‌های سینمایی"""
    query = update.callback_query
    await query.answer()

    anime_list = ANIME_DB["movie"]
    text = "🎬 *انیمه‌های سینمایی برتر*\n\n"

    for anime in anime_list:
        text += f"🎥 *{anime['name']}*\n"
        text += f"   📅 {anime['year']} | ⭐ {anime['score']}\n"
        text += f"   📝 {anime['desc']}\n\n"

    text += "🍿 *پاپ‌کورن آماده کن و لذت ببر!*"

    await query.edit_message_text(
        text,
        reply_markup=get_anime_menu(),
        parse_mode="Markdown"
    )


async def random_anime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پیشنهاد یه انیمه تصادفی"""
    query = update.callback_query
    await query.answer()

    # افکت تایپ برای هیجان
    await query.message.chat.send_action(action="typing")

    # انتخاب تصادفی از همه انیمه‌ها
    all_anime = []
    for category in ANIME_DB.values():
        all_anime.extend(category)

    anime = random.choice(all_anime)

    # ایموجی‌های تصادفی برای هیجان
    emojis = ["🎲", "🎯", "🎪", "🎰", "🎮", "💫", "✨", "🌟"]
    emoji = random.choice(emojis)

    text = f"{emoji} *پیشنهاد تصادفی امروز:*\n\n"
    text += f"🎬 *{anime['name']}*\n"
    text += f"🇯🇵 {anime.get('japanese', '')}\n" if anime.get('japanese') else ""
    text += f"📺 {anime.get('episodes', '')} | " if anime.get('episodes') else ""
    text += f"📅 {anime.get('year', '')} | " if anime.get('year') else ""
    text += f"⭐ {anime.get('score', '')}\n\n" if anime.get('score') else "\n"
    text += f"📝 {anime.get('desc', '')}\n\n"

    encouragements = [
        "🎯 اینو ببین، ضرر نمی‌کنی!",
        "🍿 امشب با این انیمه حال کن!",
        "💯 یکی از بهترین‌هاست!",
        "🔥 فوق‌العاده‌ست، شک نکن!",
        "👌 انتخاب امروز من اینه!"
    ]
    text += random.choice(encouragements)

    await query.edit_message_text(
        text,
        reply_markup=get_anime_menu(),
        parse_mode="Markdown"
    )


async def search_anime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """جستجوی انیمه با اسم"""
    user_message = update.message.text.strip()

    # جستجو در همه انیمه‌ها
    found = None
    for category in ANIME_DB.values():
        for anime in category:
            if user_message.lower() in anime['name'].lower():
                found = anime
                break
        if found:
            break

    if found:
        text = f"🔍 *نتیجه جستجو:*\n\n"
        text += f"🎬 *{found['name']}*\n"
        text += f"🇯🇵 {found.get('japanese', '')}\n" if found.get('japanese') else ""
        text += f"📺 {found.get('episodes', '')} | " if found.get('episodes') else ""
        text += f"📅 {found.get('year', '')}\n" if found.get('year') else "\n"
        text += f"⭐ امتیاز: {found.get('score', 'نامشخص')}/۱۰\n\n"
        text += f"📝 {found.get('desc', '')}\n\n"
        text += "🍿 *آماده‌ای برای تماشا؟*"
    else:
        text = "🤔 *پیدا نشد!*\n\n"
        text += "اما نگران نباش!\n"
        text += "می‌تونی از منوی انیمه‌ها، کلی پیشنهاد عالی ببینی 🎬\n"
        text += "یا اسم یه انیمه دیگه رو امتحان کن!"

    await update.message.reply_text(
        text,
        reply_markup=get_back_button(),
        parse_mode="Markdown"
    )
