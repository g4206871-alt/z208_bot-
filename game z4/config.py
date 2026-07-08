import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# OpenAI API Key (برای دستیار هوش مصنوعی)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# ادمین‌ها (آیدی عددی تلگرام)
ADMIN_IDS = ["@Shirzad2026"]  # آیدی ادمین رو اینجا بذارید

# تنظیمات دیتابیس
DATABASE_PATH = "z208_bot.db"

# تنظیمات استودیو
STUDIO_NAME = "Z208 Studio"
STUDIO_WEBSITE = "https://zippy-semolina-6c6cec.netlify.app/"
STUDIO_DESCRIPTION = """
🎬 استودیو Z208 - خلاقیت بی‌نهایت

ما در Z208 به خلق محتوای دیجیتال، طراحی گرافیک، 
توسعه وب و اپلیکیشن، و تولید محتوای خلاقانه می‌پردازیم.
"""
