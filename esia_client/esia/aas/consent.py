# esia/aas/consent.py

import requests
from esia.aas.config import CONSENT_REQUEST_URL, CONSENT_STATUS_URL
from esia.aas.errors import handle_http_errors, handle_network_errors, parse_error

"""
📌 Работа с платформой согласий ЕСИА.

🔹 Согласно:
   - "Методические рекомендации по интеграции с REST API Цифрового профиля" (раздел 6.1)&#8203;:contentReference[oaicite:6]{index=6}

📄 ЕСИА требует передачи `sysname` для запроса согласия.
"""

@handle_network_errors
def request_consent(user_id: str, sysname: str):
    """Отправляет запрос на согласие пользователя."""
    data = {
        "sysname": sysname,
        "userId": user_id
    }
    response = requests.post(CONSENT_REQUEST_URL, json=data)

    handle_http_errors(response)

    response_json = response.json()
    if "error" in response_json:
        raise parse_error(response.text)

    return response_json
