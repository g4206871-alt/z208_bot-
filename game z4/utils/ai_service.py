import requests
from config import OPENAI_API_KEY


class AIService:
    def __init__(self):
        self.api_key = OPENAI_API_KEY
        self.base_url = "https://api.openai.com/v1/chat/completions"

    def get_response(self, user_message, context=""):
        """دریافت پاسخ از هوش مصنوعی"""
        try:
            if not self.api_key:
                return self.get_fallback_response(user_message)

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            data = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "system",
                        "content": f"""شما دستیار هوشمند استودیو Z208 هستید.
                        یک استودیو خلاقیت دیجیتال که در زمینه طراحی گرافیک، توسعه وب، 
                        تولید محتوا و دیجیتال مارکتینگ فعالیت می‌کند.
                        پاسخ‌ها باید دوستانه، حرفه‌ای و مفید باشند.
                        {context}"""
                    },
                    {"role": "user", "content": user_message}
                ],
                "max_tokens": 500,
                "temperature": 0.7
            }

            response = requests.post(
                self.base_url, headers=headers, json=data, timeout=10)
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                return self.get_fallback_response(user_message)

        except Exception as e:
            print(f"AI Service Error: {e}")
            return self.get_fallback_response(user_message)

    def get_fallback_response(self, message):
        """پاسخ‌های پیش‌فرض در صورت عدم دسترسی به API"""
        responses = {
            "سلام": "سلام! 🌟 چطور می‌تونم به شما کمک کنم؟",
            "چطوری": "من همیشه آماده کمک به شما هستم! 😊",
            "خدمات": "ما در Z208 خدمات طراحی گرافیک، توسعه وب، تولید محتوا و مشاوره دیجیتال مارکتینگ ارائه می‌دهیم.",
            "پروژه": "برای مشاهده پروژه‌های ما می‌تونید از منوی اصلی گزینه 'معرفی پروژه‌ها' رو انتخاب کنید.",
        }

        for key in responses:
            if key in message.lower():
                return responses[key]

        return "متأسفانه در حال حاضر نمی‌تونم پاسخ دقیقی بدم. لطفاً با پشتیبانی تماس بگیرید یا سوال خودتون رو دوباره مطرح کنید. 🙏"


ai_service = AIService()
