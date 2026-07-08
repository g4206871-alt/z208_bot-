import random
import json
import os
import time
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ContextTypes
from database import db
from keyboards.menus import get_games_menu, get_back_button
from collections import defaultdict

# ============ سیستم پیشرفته لود داده ============

def load_json_data(filename):
    """لود کردن دیتابیس با قابلیت بروزرسانی خودکار"""
    try:
        filepath = f'data/{filename}'
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if data:
                    return data
    except Exception as e:
        print(f"Error loading {filename}: {e}")

    return get_default_data(filename)


def save_json_data(filename, data):
    """ذخیره دیتابیس برای بروزرسانی"""
    try:
        os.makedirs('data', exist_ok=True)
        with open(f'data/{filename}', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error saving {filename}: {e}")
        return False


def get_default_data(filename):
    """دیتابیس پیش‌فرض فوق‌العاده غنی"""
    if filename == 'jokes.json':
        return [
            # جوک‌های تکنولوژی
            {"joke": "چرا برنامه‌نویس‌ها تاریکی رو دوست ندارن؟ چون باگ توش زیاده! 😂", "category": "tech"},
            {"joke": "فرق یه برنامه‌نویس با یه پیتزا چیه؟ پیتزا می‌تونه یه خانواده رو سیر کنه! 🍕", "category": "tech"},
            {"joke": "چرا برنامه‌نویس‌ها همیشه سردشونه؟ چون همیشه کنار پنجره‌های باز کار می‌کنن! ❄️", "category": "tech"},
            {"joke": "چرا CSS از JavaScript ناراحته؟ چون JS همیشه می‌گه 'من همه کاره‌ام!' 😤", "category": "tech"},
            {"joke": "یه هکر میره خواستگاری، به پدر عروس می‌گه: من بچه‌هاتون رو دوست دارم، پسورد WiFi رو می‌دید؟ 📶", "category": "tech"},

            # جوک‌های طراحی
            {"joke": "طراح گرافیک به مشتری: این لوگو رو با عشق طراحی کردم. مشتری: میشه با فتوشاپ طراحی کنی؟ 😑", "category": "design"},
            {"joke": "چرا طراح‌ها همیشه قهوه می‌خورن؟ چون بدون کافئین، CMYK رو با CMYK اشتباه می‌گیرن! ☕", "category": "design"},
            {"joke": "مشتری: می‌خوام لوگو هم ساده باشه هم شلوغ، هم مدرن هم کلاسیک! طراح: 🫠", "category": "design"},

            # جوک‌های عمومی
            {"joke": "چرا اسکلت‌ها دعوا نمی‌کنن؟ چون دل و جگر ندارن! 💀", "category": "general"},
            {"joke": "به یارو می‌گن چرا اینقدر خوشحالی؟ می‌گه دیشب خواب دیدم برق رایگان شده، صبح که بیدار شدم دیدم شارژر گوشیم هنوز به برقه! 🔌", "category": "general"},
            {"joke": "چرا ریاضی‌دان‌ها همیشه غمگینن؟ چون پر از مسئله‌ن! 📐", "category": "general"},
            {"joke": "فرق گربه با کاما چیه؟ گربه ۹ جون داره، کاما ۹ تا کاربرد! 🐱", "category": "general"},
            {"joke": "یه مورچه به فیل می‌گه: بیا کشتی بگیریم! فیل می‌گه: باشه، فقط قول بده نخندی! 🐘🐜", "category": "general"},

            # جوک‌های Z208
            {"joke": "چرا Z208 اینقدر خلاقه؟ چون حتی Ctrl+Z هم نمی‌تونه جلوش رو بگیره! 🎨", "category": "z208"},
            {"joke": "تو Z208 یه پروژه رو سریع‌تر از چیزی که بگی 'خاموش نشو!' تحویل می‌دیم! ⚡", "category": "z208"},
        ]

    elif filename == 'riddles.json':
        return [
            # معماهای آسون (امتیاز ۱۰)
            {"question": "اون چیه که هر چی ازش برمیداری بزرگتر میشه؟", "answer": "چاله", "difficulty": "easy", "points": 10},
            {"question": "اون چیه که تو آب خیس نمیشه؟", "answer": "سایه", "difficulty": "easy", "points": 10},
            {"question": "چهار نفر زیر یه چتر هستن، چرا هیچکدوم خیس نمیشن؟", "answer": "چون بارون نمیاد", "difficulty": "easy", "points": 10},
            {"question": "اون چیه که هر چی بیشتر باشه، کمتر می‌بینی؟", "answer": "تاریکی", "difficulty": "easy", "points": 10},

            # معماهای متوسط (امتیاز ۲۰)
            {"question": "من هر روز می‌روم اما هرگز راه نمی‌روم، من کیستم؟", "answer": "ساعت", "difficulty": "medium", "points": 20},
            {"question": "کدوم ماه ۲۸ روز داره؟", "answer": "همه ماه‌ها", "difficulty": "medium", "points": 20},
            {"question": "وقتی منو می‌خوری، سازنده‌م گریه می‌کنه. وقتی منو می‌کشی، همه غمگین میشن. من چی هستم؟", "answer": "پیاز", "difficulty": "medium", "points": 20},
            {"question": "من شهرها رو می‌بینم اما شهرها منو نمی‌بینن، من چی هستم؟", "answer": "ماهواره", "difficulty": "medium", "points": 20},

            # معماهای سخت (امتیاز ۳۰)
            {"question": "دیروز قبل از فردا بود، امروز بعد از پریروز است، امروز چه روزیست؟", "answer": "شنبه", "difficulty": "hard", "points": 30},
            {"question": "من نه دست دارم نه پا، اما درها رو باز می‌کنم. من چی هستم؟", "answer": "کلید", "difficulty": "hard", "points": 30},
            {"question": "هر شب می‌آیم بدون اینکه صدا کنم، هر روز می‌روم بدون اینکه خداحافظی کنم. من چی هستم؟", "answer": "خواب", "difficulty": "hard", "points": 30},

            # معماهای تکنولوژی (امتیاز ۲۵)
            {"question": "من بدون بدن زنده‌ام، بدون دهان حرف می‌زنم، بدون گوش می‌شنوم. من کیستم؟", "answer": "هوش مصنوعی", "difficulty": "tech", "points": 25},
            {"question": "من همه جا هستم ولی دیده نمیشم، همه رو وصل می‌کنم اما خودم تنهام. من چی هستم؟", "answer": "اینترنت", "difficulty": "tech", "points": 25},
        ]

    elif filename == 'facts.json':
        return [
            {"fact": "آیا می‌دونستی اولین باگ کامپیوتری واقعاً یه پروانه بود که داخل کامپیوتر گیر کرده بود؟ 🦋💻", "category": "tech"},
            {"fact": "طراحی لوگو توییتر فقط ۱۵ دلار هزینه داشت! 🐦", "category": "design"},
            {"fact": "مغز انسان می‌تونه تصاویر رو ۶۰,۰۰۰ برابر سریع‌تر از متن پردازش کنه! 🧠", "category": "science"},
            {"fact": "اولین وبسایت جهان هنوز هم فعاله: info.cern.ch 🌐", "category": "tech"},
            {"fact": "گوگل روزانه حدود ۳.۵ میلیارد جستجو پردازش می‌کنه! 🔍", "category": "tech"},
            {"fact": "رنگ آبی باعث افزایش خلاقیت میشه! 🎨", "category": "design"},
            {"fact": "Z208 یعنی خلاقیت ضربدر بی‌نهایت! 🚀", "category": "z208"},
        ]

    elif filename == 'quiz.json':
        return [
            {
                "question": "پایتون چه نوع زبان برنامه‌نویسیه؟",
                "options": ["کامپایلری", "مفسری", "هیبریدی", "ماشینی"],
                "correct": 1,
                "category": "tech",
                "points": 15
            },
            {
                "question": "کدوم ابزار برای طراحی وکتور استفاده میشه؟",
                "options": ["فتوشاپ", "ایلوستریتور", "لایت‌روم", "پریمیر"],
                "correct": 1,
                "category": "design",
                "points": 15
            },
            {
                "question": "Z208 مخفف چیه؟",
                "options": ["Zero to 208", "Zone 208", "Zed 208 Studio", "Zetta 208"],
                "correct": 2,
                "category": "z208",
                "points": 20
            },
            {
                "question": "کدوم شبکه اجتماعی اول ساخته شد؟",
                "options": ["فیسبوک", "مای‌اسپیس", "فرندستر", "لینکدین"],
                "correct": 2,
                "category": "tech",
                "points": 15
            },
            {
                "question": "RGB مخفف چیه؟",
                "options": ["Red Green Blue", "Real Graphic Base", "Raster Gradient Bit", "Random Grey Black"],
                "correct": 0,
                "category": "design",
                "points": 10
            },
        ]

    return []


# ============ سیستم دستاوردها ============

ACHIEVEMENTS = {
    "first_joke": {"name": "😂 جوک‌خوان", "desc": "اولین جوکت رو خوندی!", "icon": "😂"},
    "joke_master": {"name": "🎭 استندآپ کمدین", "desc": "۱۰ تا جوک خوندی!", "icon": "🎭", "target": 10},
    "riddle_beginner": {"name": "🧩 معما باز", "desc": "اولین معما رو جواب دادی!", "icon": "🧩"},
    "riddle_master": {"name": "🧠 انیشتین", "desc": "۵ تا معما حل کردی!", "icon": "🧠", "target": 5},
    "high_score": {"name": "⭐ ستاره", "desc": "به ۱۰۰ امتیاز رسیدی!", "icon": "⭐", "target": 100},
    "super_star": {"name": "🌟 سوپراستار", "desc": "به ۵۰۰ امتیاز رسیدی!", "icon": "🌟", "target": 500},
    "legend": {"name": "👑 افسانه", "desc": "به ۱۰۰۰ امتیاز رسیدی!", "icon": "👑", "target": 1000},
    "night_owl": {"name": "🦉 شب‌زنده‌دار", "desc": "بعد از نیمه‌شب بازی کردی!", "icon": "🦉"},
    "early_bird": {"name": "🐦 سحرخیز", "desc": "قبل از ۶ صبح بازی کردی!", "icon": "🐦"},
    "quiz_king": {"name": "👨‍🎓 پروفسور", "desc": "۳ تا کوییز کامل دادی!", "icon": "👨‍🎓", "target": 3},
}


# ============ Handler های اصلی ============

async def games_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش منوی پیشرفته بازی‌ها با انیمیشن و آمار"""
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    user_score = db.get_user_score(user_id) or 0
    achievements = db.get_user_achievements(user_id) or []

    # محاسبه رتبه
    rank = get_user_rank(user_score)

    welcome_messages = [
        f"""🎮 *به مرکز سرگرمی Z208 خوش اومدی!*

{rank} *رتبه شما:* {rank.split(' ')[0]}
⭐ *امتیاز:* {user_score}
🏆 *دستاوردها:* {len(achievements)} عدد

🎯 *بازی‌های موجود:*
• 😂 جوک‌های باحال
• 🧩 معماهای چالشی
• 🎯 حدس کلمه
• 🧠 کوییز هوش
• 📚 حقایق جالب
• 🏆 رتبه‌بندی

یکی رو انتخاب کن و بزن بریم! 🚀""",

        f"""🌟 *سلام قهرمان!* 🌟

{rank}
امتیاز فعلی: *{user_score}* ⭐
دستاوردهای کسب شده: *{len(achievements)}* 🏆

آماده‌ای برای یه چالش جدید؟ 🎯
از منوی زیر انتخاب کن!"""
    ]

    await query.edit_message_text(
        random.choice(welcome_messages),
        reply_markup=get_games_menu(),
        parse_mode="Markdown"
    )


def get_user_rank(score):
    """تعیین رتبه کاربر بر اساس امتیاز"""
    if score >= 1000:
        return "👑 افسانه‌ای"
    elif score >= 500:
        return "🌟 سوپراستار"
    elif score >= 250:
        return "⭐ حرفه‌ای"
    elif score >= 100:
        return "🎯 بااستعداد"
    elif score >= 50:
        return "💪 در حال پیشرفت"
    elif score >= 10:
        return "🌱 تازه‌کار"
    else:
        return "🆕 مبتدی"


# ============ جوک‌های پیشرفته ============

async def tell_joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """گفتن جوک تصادفی با دسته‌بندی و افکت‌های ویژه"""
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    # افکت تایپ خنده‌دار
    await query.message.chat.send_action(action="typing")

    jokes = load_json_data('jokes.json')

    # انتخاب جوک بر اساس ساعت روز
    current_hour = datetime.now().hour
    if current_hour < 6:
        category = "general"
        vibe = "نیمه‌شبی"
    elif current_hour < 12:
        category = random.choice(["tech", "design", "general", "z208"])
        vibe = "صبحگاهی"
    elif current_hour < 18:
        category = random.choice(["tech", "design", "z208"])
        vibe = "کاری"
    else:
        category = random.choice(["general", "z208"])
        vibe = "شبانه"

    # فیلتر جوک‌ها بر اساس دسته
    category_jokes = [j for j in jokes if j.get('category') == category] if random.random() > 0.3 else jokes
    if not category_jokes:
        category_jokes = jokes

    joke_data = random.choice(category_jokes)
    joke_text = joke_data['joke']
    joke_category = joke_data.get('category', 'general')

    # ایموجی دسته‌بندی
    category_emoji = {
        "tech": "💻",
        "design": "🎨",
        "general": "😄",
        "z208": "🎬"
    }

    # محاسبه امتیاز
    points_earned = random.choice([5, 10, 15]) if random.random() > 0.7 else 5

    # اضافه کردن امتیاز
    db.update_score(user_id, points_earned)

    # ثبت آمار جوک
    joke_stats = context.user_data.get('joke_stats', {"count": 0, "categories": defaultdict(int)})
    joke_stats["count"] += 1
    joke_stats["categories"][joke_category] += 1
    context.user_data['joke_stats'] = joke_stats

    # بررسی دستاورد
    new_achievement = None
    if joke_stats["count"] == 1:
        new_achievement = "first_joke"
    elif joke_stats["count"] == 10:
        new_achievement = "joke_master"

    if new_achievement:
        db.add_achievement(user_id, new_achievement)
        achievement_data = ACHIEVEMENTS[new_achievement]

    # افکت نمایش پیام
    await asyncio_sleep_simulate(0.8)  # تأخیر جذاب

    # ساخت پیام پاسخ
    response = f"{category_emoji.get(joke_category, '😄')} *جوک {vibe}*\n\n"
    response += f"{joke_text}\n\n"
    response += f"🎁 *{points_earned} امتیاز* گرفتی!\n"

    if joke_stats["count"] > 1:
        response += f"📊 این جوک شماره *{joke_stats['count']}* امروزته!\n"

    if new_achievement:
        response += f"\n🏆 *دستاورد جدید:* {achievement_data['icon']} {achievement_data['name']}\n"
        response += f"_{achievement_data['desc']}_\n"

    response += "\n🔄 برای جوک دیگه دوباره کلیک کن!"

    await query.edit_message_text(
        response,
        reply_markup=get_games_menu(),
        parse_mode="Markdown"
    )


# ============ معماهای پیشرفته ============

async def ask_riddle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پرسیدن معما با سطح دشواری و راهنمایی"""
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    # انتخاب سطح بر اساس سابقه کاربر
    user_score = db.get_user_score(user_id) or 0
    riddles = load_json_data('riddles.json')

    if user_score < 50:
        # بیشتر معماهای آسون
        weights = {"easy": 0.5, "medium": 0.3, "hard": 0.15, "tech": 0.05}
    elif user_score < 200:
        weights = {"easy": 0.2, "medium": 0.4, "hard": 0.3, "tech": 0.1}
    else:
        weights = {"easy": 0.1, "medium": 0.3, "hard": 0.4, "tech": 0.2}

    # انتخاب معما با وزن‌دهی
    riddle = weighted_choice(riddles, weights)

    # ذخیره در context
    context.user_data['current_riddle'] = {
        'question': riddle['question'],
        'answer': riddle['answer'],
        'points': riddle.get('points', 10),
        'difficulty': riddle.get('difficulty', 'easy'),
        'hints_used': 0,
        'start_time': time.time()
    }

    # نمایش معما
    difficulty_emoji = {"easy": "🟢", "medium": "🟡", "hard": "🔴", "tech": "💻"}
    difficulty_text = {"easy": "آسون", "medium": "متوسط", "hard": "سخت", "tech": "تکنولوژی"}

    response = f"🧩 *معما - سطح {difficulty_text.get(riddle.get('difficulty', 'easy'), 'متوسط')}*\n\n"
    response += f"📝 *{riddle['question']}*\n\n"
    response += f"💰 امتیاز این معما: *{riddle.get('points', 10)}*\n"
    response += f"💡 با دستور `/راهنمایی` می‌تونی راهنمایی بگیری (امتیاز کمتر)\n\n"
    response += "🤔 *جوابت رو به صورت متن بفرست!*"

    await query.edit_message_text(
        response,
        reply_markup=get_back_button(),
        parse_mode="Markdown"
    )


async def give_hint(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دادن راهنمایی برای معما"""
    riddle_data = context.user_data.get('current_riddle')

    if not riddle_data:
        await update.message.reply_text(
            "❌ معمای فعالی وجود نداره! اول یه معما انتخاب کن.",
            reply_markup=get_games_menu()
        )
        return

    hints_used = riddle_data.get('hints_used', 0)
    answer = riddle_data['answer']

    if hints_used == 0:
        # راهنمایی اول: تعداد حروف
        hint = f"🔤 راهنمایی ۱: پاسخ *{len(answer)}* حرف داره.\n(امتیاز به {riddle_data['points'] // 2} کاهش یافت)"
        riddle_data['points'] = riddle_data['points'] // 2
    elif hints_used == 1:
        # راهنمایی دوم: حرف اول
        hint = f"🔤 راهنمایی ۲: پاسخ با *{answer[0]}* شروع میشه.\n(امتیاز به {riddle_data['points'] // 2} کاهش یافت)"
        riddle_data['points'] = riddle_data['points'] // 2
    else:
        # راهنمایی آخر
        hint = f"😅 دیگه راهنمایی نداریم! آخرین شانس: پاسخ با *{answer[:3]}...* شروع میشه."

    riddle_data['hints_used'] = hints_used + 1
    context.user_data['current_riddle'] = riddle_data

    await update.message.reply_text(
        hint,
        parse_mode="Markdown",
        reply_markup=get_back_button()
    )


async def check_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """بررسی پیشرفته پاسخ معما"""
    user_answer = update.message.text.strip()
    riddle_data = context.user_data.get('current_riddle', {})

    if not riddle_data:
        await update.message.reply_text(
            "🤔 معما فعال نیست! از منوی بازی‌ها یه معما انتخاب کن.",
            reply_markup=get_games_menu()
        )
        return

    correct_answer = riddle_data.get('answer', '')
    user_id = update.effective_user.id

    # بررسی پاسخ با دقت ۸۰٪
    is_correct = check_answer_similarity(user_answer, correct_answer)

    if is_correct:
        # محاسبه زمان پاسخگویی
        elapsed = time.time() - riddle_data.get('start_time', time.time())
        points = riddle_data.get('points', 10)

        # امتیاز اضافه برای پاسخ سریع
        if elapsed < 10:
            points += 5
            speed_bonus = "⚡ *پاسخ سریع!* ۵ امتیاز اضافه!"
        elif elapsed < 30:
            points += 2
            speed_bonus = "👏 *خوب بود!* ۲ امتیاز اضافه!"
        else:
            speed_bonus = ""

        db.update_score(user_id, points)

        # ثبت آمار معما
        riddle_stats = context.user_data.get('riddle_stats', {"solved": 0, "total_points": 0})
        riddle_stats["solved"] += 1
        riddle_stats["total_points"] += points
        context.user_data['riddle_stats'] = riddle_stats

        # بررسی دستاورد
        new_achievement = None
        if riddle_stats["solved"] == 1:
            new_achievement = "riddle_beginner"
        elif riddle_stats["solved"] == 5:
            new_achievement = "riddle_master"

        if new_achievement:
            db.add_achievement(user_id, new_achievement)
            achievement_data = ACHIEVEMENTS[new_achievement]

        # پیام موفقیت
        success_messages = [
            f"🎉 *آفرین! کاملاً درست گفتی!*\n\n✅ پاسخ: *{correct_answer}*\n⏱️ زمان: {elapsed:.1f} ثانیه\n🎁 *{points}* امتیاز گرفتی!",
            f"🌟 *ایول! مغزت عالی کار می‌کنه!*\n\n✅ پاسخ: *{correct_answer}*\n⏱️ زمان: {elapsed:.1f} ثانیه\n🎁 *{points}* امتیاز بهت اضافه شد!",
            f"🧠 *چه باهوش! درست حدس زدی!*\n\n✅ پاسخ: *{correct_answer}*\n🎁 *{points}* امتیاز برنده شدی!"
        ]

        response = random.choice(success_messages)
        if speed_bonus:
            response += f"\n{speed_bonus}"
        if new_achievement:
            response += f"\n\n🏆 *دستاورد جدید:* {achievement_data['icon']} {achievement_data['name']}"
        response += f"\n\n📊 معماهای حل شده: *{riddle_stats['solved']}*"

    else:
        # پیام شکست
        fail_messages = [
            f"😅 *متأسفانه اشتباه بود!*\n\n✅ پاسخ درست: *{correct_answer}*\n💡 دفعه بعد حتماً درست جواب بده!",
            f"🤔 *نزدیک بودی ولی نه!*\n\n✅ پاسخ درست: *{correct_answer}*\n🔁 از منوی بازی‌ها دوباره امتحان کن!",
            f"😬 *ای دفعه نشد!*\n\n✅ پاسخ: *{correct_answer}*\n🎯 معماهای بیشتری منتظرتن!"
        ]
        response = random.choice(fail_messages)

    # پاک کردن معما از context
    context.user_data.pop('current_riddle', None)

    await update.message.reply_text(
        response,
        reply_markup=get_games_menu(),
        parse_mode="Markdown"
    )


def check_answer_similarity(user_answer, correct_answer):
    """بررسی شباهت پاسخ با تحمل خطا"""
    user_clean = user_answer.lower().strip().replace(' ', '')
    correct_clean = correct_answer.lower().strip().replace(' ', '')

    # بررسی دقیق
    if user_clean == correct_clean:
        return True

    # بررسی ۸۰٪ شباهت
    if len(user_clean) > 3 and len(correct_clean) > 3:
        common = set(user_clean) & set(correct_clean)
        if len(common) / len(set(correct_clean)) > 0.8:
            return True

    return False


# ============ بازی حدس کلمه پیشرفته ============

async def start_word_guess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """شروع بازی حدس کلمه با دسته‌بندی و افکت"""
    query = update.callback_query
    await query.answer()

    # دیتابیس کلمات با دسته‌بندی
    word_categories = {
        "tech": ["پایتون", "تلگرام", "برنامه‌نویس", "الگوریتم", "دیتابیس", "سرور", "کلاینت", "کامپایلر",
                 "جاوااسکریپت", "ریکت", "جنگو", "گیت‌هاب", "داکر", "لینوکس", "هوش مصنوعی"],
        "design": ["فتوشاپ", "ایلوستریتور", "وکتور", "پیکسل", "تایپوگرافی", "برندینگ", "پالت رنگ",
                   "مینیمال", "کمپوزیشن", "کنتراست"],
        "z208": ["خلاقیت", "استودیو", "دیجیتال", "مارکتینگ", "محتوانویس", "ایده‌پردازی"],
        "general": ["کتابخانه", "چتربازی", "ستاره", "کهکشان", "آتشفشان", "دایناسور", "آکواریوم"]
    }

    # انتخاب تصادفی دسته و کلمه
    category = random.choice(list(word_categories.keys()))
    category_words = word_categories[category]
    secret_word = random.choice(category_words)

    category_emoji = {"tech": "💻", "design": "🎨", "z208": "🎬", "general": "🌟"}

    # ذخیره وضعیت بازی
    context.user_data['word_game'] = {
        'secret_word': secret_word,
        'guessed_letters': [],
        'attempts': 6,
        'category': category,
        'start_time': time.time(),
        'wrong_guesses': 0
    }

    display = get_word_display(secret_word, [])

    response = f"🎯 *بازی حدس کلمه*\n\n"
    response += f"{category_emoji.get(category, '🎯')} دسته: *{category}*\n"
    response += f"📝 کلمه: `{display}`\n"
    response += f"🔤 تعداد حروف: *{len(secret_word)}*\n"
    response += f"❤️ فرصت باقیمانده: *{6}*\n\n"
    response += "✍️ یه حرف یا کلمه کامل بفرست!"

    await query.edit_message_text(
        response,
        reply_markup=get_back_button(),
        parse_mode="Markdown"
    )


async def guess_letter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """بررسی حدس در بازی کلمه"""
    guess = update.message.text.strip()
    word_game = context.user_data.get('word_game')

    if not word_game:
        await update.message.reply_text(
            "🎮 بازی فعالی نیست! از منوی بازی‌ها شروع کن.",
            reply_markup=get_games_menu()
        )
        return

    secret_word = word_game['secret_word']
    guessed_letters = word_game['guessed_letters']
    attempts = word_game['attempts']
    user_id = update.effective_user.id

    # بررسی حدس کامل کلمه
    if len(guess) > 1:
        if guess.lower() == secret_word.lower():
            # برنده شدن!
            elapsed = time.time() - word_game['start_time']
            points = 50
            if elapsed < 20:
                points += 20

            db.update_score(user_id, points)
            context.user_data.pop('word_game', None)

            await update.message.reply_text(
                f"🎉 *شگفت‌انگیز! کلمه رو درست حدس زدی!*\n\n"
                f"✅ کلمه: *{secret_word}*\n"
                f"⏱️ زمان: {elapsed:.1f} ثانیه\n"
                f"🎁 *{points}* امتیاز برنده شدی!\n\n"
                f"🔄 برای بازی دوباره از منو انتخاب کن.",
                reply_markup=get_games_menu(),
                parse_mode="Markdown"
            )
            return
        else:
            attempts -= 1
            word_game['attempts'] = attempts
            word_game['wrong_guesses'] += 1

            if attempts <= 0:
                context.user_data.pop('word_game', None)
                await update.message.reply_text(
                    f"💀 *باختی!*\n\n✅ کلمه: *{secret_word}*\n"
                    f"😢 شانس دیگه‌ای نمونده!\n🔄 بازی جدید از منو.",
                    reply_markup=get_games_menu(),
                    parse_mode="Markdown"
                )
                return

    # بررسی حدس تک حرف
    elif len(guess) == 1:
        if guess in guessed_letters:
            await update.message.reply_text(
                f"⚠️ حرف *{guess}* رو قبلاً گفتی! یه حرف دیگه بگو.",
                parse_mode="Markdown",
                reply_markup=get_back_button()
            )
            return

        guessed_letters.append(guess)

        if guess not in secret_word:
            attempts -= 1
            word_game['attempts'] = attempts
            word_game['wrong_guesses'] += 1

    # بروزرسانی بازی
    context.user_data['word_game'] = word_game
    display = get_word_display(secret_word, guessed_letters)

    # بررسی برنده شدن
    if '◼️' not in display:
        points = 30
        db.update_score(user_id, points)
        elapsed = time.time() - word_game['start_time']
        context.user_data.pop('word_game', None)

        await update.message.reply_text(
            f"🌟 *برنده شدی!*\n\n✅ کلمه: *{secret_word}*\n"
            f"⏱️ زمان: {elapsed:.1f} ثانیه\n🎁 *{points}* امتیاز!\n\n"
            f"🔄 بازی جدید؟",
            reply_markup=get_games_menu(),
            parse_mode="Markdown"
        )
        return

    # نمایش وضعیت فعلی
    if attempts <= 0:
        context.user_data.pop('word_game', None)
        await update.message.reply_text(
            f"💀 *تموم شد!*\n\n✅ کلمه: *{secret_word}*\n🔄 دوباره تلاش کن!",
            reply_markup=get_games_menu(),
            parse_mode="Markdown"
        )
        return

    # ایموجی وضعیت
    hangman_stages = ["😊", "😐", "😟", "😰", "😱", "💀"]
    stage_emoji = hangman_stages[word_game['wrong_guesses']]

    await update.message.reply_text(
        f"🎯 *حدس کلمه*\n\n{stage_emoji}\n"
        f"📝 `{display}`\n"
        f"🔤 حروف حدس زده: {', '.join(guessed_letters) if guessed_letters else 'هیچی!'}\n"
        f"❤️ فرصت: *{attempts}*\n\n✍️ حدس بعدی:",
        reply_markup=get_back_button(),
        parse_mode="Markdown"
    )


def get_word_display(secret_word, guessed_letters):
    """نمایش کلمه با حروف حدس زده شده"""
    return ' '.join([letter if letter in guessed_letters else '◼️' for letter in secret_word])


# ============ کوییز ============

async def start_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """شروع کوییز چند سوالی"""
    query = update.callback_query
    await query.answer()

    quiz_data = load_json_data('quiz.json')
    if not quiz_data:
        await query.edit_message_text(
            "❌ متأسفانه سوالی موجود نیست!",
            reply_markup=get_games_menu()
        )
        return

    # انتخاب ۳ سوال تصادفی
    selected_questions = random.sample(quiz_data, min(3, len(quiz_data)))

    context.user_data['quiz'] = {
        'questions': selected_questions,
        'current': 0,
        'score': 0,
        'total_points': 0
    }

    await show_quiz_question(query, context)


async def show_quiz_question(query_or_update, context):
    """نمایش سوال فعلی کوییز"""
    quiz = context.user_data.get('quiz')
    if not quiz:
        return

    current = quiz['current']
    questions = quiz['questions']

    if current >= len(questions):
        await finish_quiz(query_or_update, context)
        return

    question = questions[current]

    # ساخت کیبورد گزینه‌ها
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    keyboard = []
    for i, option in enumerate(question['options']):
        keyboard.append([InlineKeyboardButton(
            f"{'🅰️' if i==0 else '🅱️' if i==1 else '©️' if i==2 else '🅳️'} {option}",
            callback_data=f"quiz_answer_{i}"
        )])

    # دکمه خروج
    keyboard.append([InlineKeyboardButton("🚪 خروج از کوییز", callback_data="exit_quiz")])

    text = f"🧠 *کوییز هوش*\n\n"
    text += f"📝 سوال {current + 1} از {len(questions)}:\n"
    text += f"*{question['question']}*\n\n"
    text += f"💰 امتیاز این سوال: {question.get('points', 15)}"

    if isinstance(query_or_update, Update):
        await query_or_update.message.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
    else:
        await query_or_update.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )


async def handle_quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """بررسی پاسخ کوییز"""
    query = update.callback_query
    await query.answer()

    quiz = context.user_data.get('quiz')
    if not quiz:
        await query.edit_message_text("کوییز تموم شده!", reply_markup=get_games_menu())
        return

    answer = int(query.data.split('_')[-1])
    question = quiz['questions'][quiz['current']]
    user_id = query.from_user.id

    if answer == question['correct']:
        points = question.get('points', 15)
        quiz['score'] += points
        quiz['total_points'] += points

        responses = ["✅ درست!", "🎯 عالی!", "🌟 آفرین!", "👏 ایول!"]
        await query.edit_message_text(
            f"{random.choice(responses)}\n🎁 {points} امتیاز!",
            reply_markup=None
        )
    else:
        correct_option = question['options'][question['correct']]
        await query.edit_message_text(
            f"❌ اشتباه!\n✅ پاسخ درست: {correct_option}",
            reply_markup=None
        )

    # رفتن به سوال بعدی
    quiz['current'] += 1
    context.user_data['quiz'] = quiz

    # تاخیر کوتاه
    import asyncio
    await asyncio.sleep(1)

    await show_quiz_question(query, context)


async def finish_quiz(update_or_query, context):
    """پایان کوییز و نمایش نتیجه"""
    quiz = context.user_data.get('quiz', {})
    total = quiz.get('score', 0)
    questions_count = len(quiz.get('questions', []))

    if total > 0:
        db.update_score(update_or_query.from_user.id, total)

    max_points = questions_count * 20
    percentage = (total / max_points * 100) if max_points > 0 else 0

    if percentage >= 80:
        emoji = "🏆"
        message = "عالی بود!"
    elif percentage >= 50:
        emoji = "👍"
        message = "بد نبود!"
    else:
        emoji = "📚"
        message = "بیشتر تمرین کن!"

    text = f"🧠 *کوییز تموم شد!*\n\n{emoji} {message}\n"
    text += f"✅ امتیاز: *{total}* از {max_points}\n"
    text += f"📊 درصد: *{percentage:.0f}%*\n\n"
    text += "🎯 برای بازی دوباره از منو انتخاب کن."

    # پاک کردن کوییز
    context.user_data.pop('quiz', None)

    if isinstance(update_or_query, Update):
        await update_or_query.message.reply_text(
            text,
            reply_markup=get_games_menu(),
            parse_mode="Markdown"
        )
    else:
        await update_or_query.edit_message_text(
            text,
            reply_markup=get_games_menu(),
            parse_mode="Markdown"
        )


# ============ حقایق جالب ============

async def show_fact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش حقایق جالب و خواندنی"""
    query = update.callback_query
    await query.answer()

    facts = load_json_data('facts.json')
    fact = random.choice(facts)

    category_emoji = {
        "tech": "💻",
        "design": "🎨",
        "science": "🔬",
        "z208": "🎬"
    }

    emoji = category_emoji.get(fact.get('category', 'general'), "📚")

    db.update_score(query.from_user.id, 3)

    await query.edit_message_text(
        f"{emoji} *آیا می‌دونستی؟*\n\n{fact['fact']}\n\n"
        "🎁 ۳ امتیاز گرفتی!\n🔄 برای یه حقیقت دیگه کلیک کن.",
        reply_markup=get_games_menu(),
        parse_mode="Markdown"
    )


# ============ رتبه‌بندی پیشرفته ============

async def show_leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش رتبه‌بندی با آمار پیشرفته"""
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    top_users = db.get_top_users(10)

    # آمار کلی
    all_users_count = db.get_users_count() or 0
    total_points_all = db.get_total_points() or 0

    leaderboard_text = f"🏆 *رتبه‌بندی Z208*\n"
    leaderboard_text += f"👥 کاربران: {all_users_count} | ⭐ کل امتیازات: {total_points_all}\n\n"

    # مدال‌ها
    medals = {0: "🥇", 1: "🥈", 2: "🥉"}

    for i, user in enumerate(top_users):
        name = (user[2] or user[1] or "کاربر")[:20]
        score = user[3]

        medal = medals.get(i, f"{i+1}.")
        bar = "█" * min(int(score / 100), 10) if score > 0 else ""

        # هایلایت کاربر فعلی
        if str(user[0]) == str(user_id):
            leaderboard_text += f"*{medal} {name}: {score} ⭐ {bar}* 👈 شما\n"
        else:
            leaderboard_text += f"{medal} {name}: {score} ⭐\n"

    # رتبه کاربر
    user_rank = db.get_user_rank(user_id)
    if user_rank and user_rank > 10:
        user_score = db.get_user_score(user_id) or 0
        leaderboard_text += f"\n...\n🔹 *رتبه شما:* {user_rank} با {user_score} ⭐"

    leaderboard_text += "\n\n💪 *برای افزایش امتیاز، بازی کن!*"

    await query.edit_message_text(
        leaderboard_text,
        reply_markup=get_games_menu(),
        parse_mode="Markdown"
    )


# ============ توابع کمکی ============

def weighted_choice(items, weights):
    """انتخاب تصادفی با وزن‌دهی"""
    weighted_items = []
    for item in items:
        difficulty = item.get('difficulty', 'medium')
        weight = weights.get(difficulty, 0.25)
        weighted_items.extend([item] * int(weight * 100))

    return random.choice(weighted_items) if weighted_items else random.choice(items)


async def asyncio_sleep_simulate(seconds):
    """تاخیر Async برای افکت‌های نمایشی"""
    import asyncio
    await asyncio.sleep(seconds)


def get_user_stats(user_id):
    """دریافت آمار کامل بازی‌های کاربر"""
    score = db.get_user_score(user_id) or 0
    achievements = db.get_user_achievements(user_id) or []
    rank = get_user_rank(score)

    return {
        "score": score,
        "rank": rank,
        "achievements_count": len(achievements),
        "achievements": achievements
    }
