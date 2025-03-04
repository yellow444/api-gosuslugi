# esia/aas/errors.py

import json
from requests.exceptions import RequestException, Timeout, ConnectionError

"""
📌 Обработчик ошибок ЕСИА и API ЕПГУ.

🔹 Согласно:
   - "Методические рекомендации по использованию ЕСИА" (раздел 5.2)&#8203;:contentReference[oaicite:7]{index=7}
   - "Методические рекомендации по интеграции с REST API Цифрового профиля" (таблица ошибок)&#8203;:contentReference[oaicite:8]{index=8}
"""

class EsiaError(Exception):
    """Ошибка ЕСИА"""
    pass

class DigitalProfileError(Exception):
    """Ошибка платформы согласий"""
    pass

class EPGUApiError(Exception):
    """Ошибка API ЕПГУ"""
    pass
