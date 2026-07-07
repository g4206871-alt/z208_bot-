from telegram import Update
from telegram.ext import ContextTypes
from keyboards.menus import get_back_button


async def show_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش اخبار استودیو"""
    query = update.callback_query
    await query.answer()

    news_text = """
📰 آخرین اخبار Z208:

🎉 پروژه جدید: رونمایی از وب‌سایت فروشگاهی مدرن
📅 تاریخ: ۱۵ تیر ۱۴۰۳
ما اخیراً یک وب‌سایت فروشگاهی پیشرفته برای یکی از مشتریانمون راه‌اندازی کردیم.

🏆 افتخار آفرینی: کسب مقام اول در مسابقات طراحی
📅 تاریخ: ۱۰ تیر ۱۴۰۳
تیم طراحی Z208 در مسابقات کشوری طراحی گرافیک مقام اول رو کسب کرد.

🚀 خدمات جدید: اضافه شدن سئو و بهینه‌سازی
📅 تاریخ: ۱ تیر ۱۴۰۳
از این ماه خدمات سئو و بهینه‌سازی سایت رو به خدماتمون اضافه کردیم.

برای اطلاعات بیشتر به وب‌سایت ما سر بزنید! 🌐
    """

    await query.edit_message_text(
        news_text,
        reply_markup=get_back_button(),
        disable_web_page_preview=True
    )


async def show_projects(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش پروژه‌ها"""
    query = update.callback_query
    await query.answer()

    projects_text = """
🎬 نمونه کارهای Z208:

1️⃣ **وب‌سایت فروشگاهی "دیجی‌مارکت"**
• طراحی کامل UI/UX
• توسعه با React و Node.js
• افزایش فروش ۲۰۰٪

2️⃣ **برندینگ "کافه‌نو"**
• طراحی لوگو و هویت بصری
• بسته‌بندی و منو
• ۵۰۰۰+ مشتری جدید

3️⃣ **اپلیکیشن "فیت‌لایف"**
• اپلیکیشن اندروید و iOS
• ۱۰۰۰۰+ دانلود
• امتیاز ۴.۸ در گوگل پلی

4️⃣ **کمپین تبلیغاتی "استارتاپ‌هاب"**
• مدیریت شبکه‌های اجتماعی
• افزایش ۳۰۰٪ تعامل
• جذب سرمایه ۱ میلیارد تومانی

برای دیدن جزئیات بیشتر و درخواست پروژه، با ما تماس بگیرید! 💼
    """

    await query.edit_message_text(
        projects_text,
        reply_markup=get_back_button()
    )
