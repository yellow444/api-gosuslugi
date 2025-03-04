# esia/aas/config.py

"""
📌 Конфигурация OAuth2-клиента для ЕСИА, Платформы согласий и API ЕПГУ.

🔹 Согласно документации:
   - "Методические рекомендации по использованию ЕСИА" (раздел 3.2)&#8203;:contentReference[oaicite:0]{index=0}
   - "Методические рекомендации по интеграции с REST API Цифрового профиля" (раздел 4.1)&#8203;:contentReference[oaicite:1]{index=1}

📄 ЕСИА поддерживает:
   - Authorization Code Flow (код авторизации -> токен доступа)
   - Client Credentials Flow (токен доступа для сервисов)
   - Запрос согласий и управление permissions
"""

# ЕСИА: URL-адреса аутентификации и получения токенов
ESIA_AUTH_URL = "https://esia.gosuslugi.ru/aas/oauth2/ac"
ESIA_TOKEN_URL = "https://esia.gosuslugi.ru/aas/oauth2/te"
ESIA_USER_INFO_URL = "https://esia.gosuslugi.ru/rs/prns"

# Платформа согласий (Consent Platform)
CONSENT_REQUEST_URL = "https://esia.gosuslugi.ru/rs/soc/v2/consents"
CONSENT_STATUS_URL = "https://esia.gosuslugi.ru/rs/soc/v2/consents/status"

# API ЕПГУ (Единый портал госуслуг)
EPGU_API_URL = "https://api.gosuslugi.ru"

# Идентификаторы приложения
REDIRECT_URI = "https://yourapp.com/callback"
CLIENT_ID = "your-client-id"
CLIENT_SECRET = "your-client-secret"

# Области доступа
SCOPE_ESIA = "openid profile"
SCOPE_CONSENT = "consent.read consent.write"
SCOPE_EPGU = "epgu.data.read epgu.data.write"

# Логирование запросов
LOG_REQUESTS = True
