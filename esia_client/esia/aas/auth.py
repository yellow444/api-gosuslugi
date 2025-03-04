# esia/aas/auth.py

import urllib.parse
from esia.aas.config import ESIA_AUTH_URL, CLIENT_ID, REDIRECT_URI, SCOPE_ESIA

"""
📌 Генерация URL для авторизации пользователя через ЕСИА.

🔹 Согласно:
   - "Методические рекомендации по использованию ЕСИА" (Приложение В.2.2)&#8203;:contentReference[oaicite:2]{index=2}
   - "Методические рекомендации по интеграции с REST API Цифрового профиля" (раздел 5.2)&#8203;:contentReference[oaicite:3]{index=3}

📄 ЕСИА требует передачи:
   - `client_id`
   - `redirect_uri`
   - `response_type=code`
   - `scope`
"""

def get_authorization_url():
    """Формирует URL для авторизации пользователя через ЕСИА."""
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPE_ESIA
    }
    return f"{ESIA_AUTH_URL}?{urllib.parse.urlencode(params)}"
