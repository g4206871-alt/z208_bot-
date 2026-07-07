import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# OpenAI API Key (برای دستیار هوش مصنوعی)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# ادمین‌ها (آیدی عددی تلگرام)
ADMIN_IDS = [123456789]  # آیدی ادمین رو اینجا بذارید

# تنظیمات دیتابیس
DATABASE_PATH = "z208_bot.db"

# تنظیمات استودیو
STUDIO_NAME = "Z208 Studio"
STUDIO_WEBSITE = "https://z208.studio"
STUDIO_DESCRIPTION = """
🎬 استودیو Z208 - خلاقیت بی‌نهایت

ما در Z208 به خلق محتوای دیجیتال، طراحی گرافیک، 
توسعه وب و اپلیکیشن، و تولید محتوای خلاقانه می‌پردازیم.

✨ خدمات ما:
• طراحی گرافیک و برندینگ
• توسعه وب و اپلیکیشن
• تولید محتوای ویدیویی
• مدیریت شبکه‌های اجتماعی
• مشاوره دیجیتال مارکتینگ
"""