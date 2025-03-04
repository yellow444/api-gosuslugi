# esia/aas/token.py

import requests
from esia.aas.config import ESIA_TOKEN_URL, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from esia.aas.errors import handle_http_errors, handle_network_errors, parse_error

"""
📌 Получение access_token через Authorization Code Flow и Client Credentials Flow.

🔹 Согласно:
   - "Методические рекомендации по использованию ЕСИА" (раздел 4.3)&#8203;:contentReference[oaicite:4]{index=4}
   - "Методические рекомендации по интеграции с REST API Цифрового профиля" (раздел 5.1.5)&#8203;:contentReference[oaicite:5]{index=5}

📄 ЕСИА поддерживает два способа получения токенов:
1. **Authorization Code Flow** (по коду авторизации)
2. **Client Credentials Flow** (для системного доступа)
"""

@handle_network_errors
def exchange_code_for_token(auth_code: str):
    """Обменивает authorization_code на access_token."""
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI
    }
    response = requests.post(ESIA_TOKEN_URL, data=data)

    handle_http_errors(response)

    response_json = response.json()
    if "error" in response_json:
        raise parse_error(response.text)

    return response_json


@handle_network_errors
def get_service_token():
    """Получает access_token для API ЕПГУ (Client Credentials Flow)."""
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    response = requests.post(ESIA_TOKEN_URL, data=data)

    handle_http_errors(response)

    response_json = response.json()
    if "error" in response_json:
        raise parse_error(response.text)

    return response_json
