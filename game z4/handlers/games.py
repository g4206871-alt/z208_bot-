import random
import json
from telegram import Update
from telegram.ext import ContextTypes
from database import db
from keyboards.menus import get_games_menu, get_back_button

# لود کردن دیتابیس جوک‌ها و معماها


def load_json_data(filename):
    try:
        with open(f'data/{filename}', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return get_default_data(filename)


def get_default_data(filename):
    if filename == 'jokes.json':
        return [
            {"joke": "چرا برنامه‌نویس‌ها تاریکی رو دوست ندارن؟ چون باگ توش زیاده! 😂"},
            {"joke": "فرق یه برنامه‌نویس با یه پیتزا چیه؟ پیتزا می‌تونه یه خانواده رو سیر کنه! 🍕"},
            {"joke": "چرا برنامه‌نویس‌ها همیشه سردشونه؟ چون همیشه کنار پنجره‌های باز کار می‌کنن! ❄️"},
        ]
    elif filename == 'riddles.json':
        return [
            {"question": "اون چیه که هر چی ازش برمیداری بزرگتر میشه؟", "answer": "چاله"},
            {"question": "اون چیه که تو آب خیس نمیشه؟", "answer": "سایه"},
            {"question": "چهار نفر زیر یه چتر هستن، چرا هیچکدوم خیس نمیشن؟",
                "answer": "چون بارون نمیاد!"},
        ]
    return []


async def games_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش منوی بازی‌ها"""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "🎮 به بخش بازی‌ها و سرگرمی خوش اومدی!\n"
        "یکی از گزینه‌های زیر رو انتخاب کن:",
        reply_markup=get_games_menu()
    )


async def tell_joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """گفتن جوک تصادفی"""
    query = update.callback_query
    await query.answer()

    jokes = load_json_data('jokes.json')
    joke = random.choice(jokes)['joke']

    # اضافه کردن امتیاز
    db.update_score(query.from_user.id, 5)

    await query.edit_message_text(
        f"😂 جوک امروز:\n\n{joke}\n\n"
        "🎉 5 امتیاز گرفتی!\n"
        "برای جوک دیگه دوباره کلیک کن!",
        reply_markup=get_games_menu()
    )


async def ask_riddle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پرسیدن معما"""
    query = update.callback_query
    await query.answer()

    riddles = load_json_data('riddles.json')
    riddle = random.choice(riddles)

    # ذخیره پاسخ معما در context
    context.user_data['current_answer'] = riddle['answer']

    await query.edit_message_text(
        f"🧩 معما:\n\n{riddle['question']}\n\n"
        "پاسخ خودت رو به صورت متن بفرست! 🤔",
        reply_markup=get_back_button()
    )


async def check_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """بررسی پاسخ معما"""
    user_answer = update.message.text.strip()
    correct_answer = context.user_data.get('current_answer', '')

    if correct_answer and user_answer.lower() == correct_answer.lower():
        db.update_score(update.effective_user.id, 20)
        await update.message.reply_text(
            "🎉 آفرین! پاسخ درست بود!\n"
            "۲۰ امتیاز گرفتی! ⭐\n"
            "برای معماهای بیشتر از منوی بازی‌ها استفاده کن.",
            reply_markup=get_games_menu()
        )
    else:
        await update.message.reply_text(
            f"😅 متأسفانه اشتباه بود! پاسخ درست: {correct_answer}\n"
            "برای امتحان دوباره از منوی بازی‌ها معما رو انتخاب کن.",
            reply_markup=get_games_menu()
        )


async def start_word_guess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """شروع بازی حدس کلمه"""
    query = update.callback_query
    await query.answer()

    words = ["پایتون", "تلگرام", "برنامه‌نویس", "استودیو", "خلاقیت", "ربات"]
    secret_word = random.choice(words)
    context.user_data['secret_word'] = secret_word
    context.user_data['guessed_letters'] = []
    context.user_data['attempts'] = 6

    display = ' '.join(['◼️' if letter not in context.user_data['guessed_letters']
                       else letter for letter in secret_word])

    await query.edit_message_text(
        f"🎯 بازی حدس کلمه\n\n"
        f"کلمه: {display}\n"
        f"تعداد حروف: {len(secret_word)}\n"
        f"فرصت باقیمانده: {context.user_data['attempts']}\n\n"
        "یک حرف یا کلمه کامل رو حدس بزن!",
        reply_markup=get_back_button()
    )


async def show_leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش رتبه‌بندی"""
    query = update.callback_query
    await query.answer()

    top_users = db.get_top_users(10)

    leaderboard_text = "🏆 رتبه‌بندی کاربران:\n\n"

    for i, user in enumerate(top_users, 1):
        name = user[2] or user[1] or "کاربر ناشناس"
        leaderboard_text += f"{i}. {name}: {user[3]} امتیاز\n"

    await query.edit_message_text(
        leaderboard_text,
        reply_markup=get_games_menu()
    )
