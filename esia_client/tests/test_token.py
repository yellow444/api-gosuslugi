# tests/test_auth.py

import re
import urllib.parse
import pytest
from esia.aas.auth import get_authorization_url
from esia.aas.config import ESIA_AUTH_URL, CLIENT_ID, REDIRECT_URI, SCOPE_ESIA

"""
📌 Тестирование генерации URL для авторизации.

🔹 Согласно:
   - "Методические рекомендации по использованию ЕСИА" (Приложение В.2.2)&#8203;:contentReference[oaicite:0]{index=0}
"""

def test_get_authorization_url():
    """Проверяет, что сгенерированная ссылка авторизации содержит корректные параметры."""
    
    url = get_authorization_url()
    
    # Проверяем, что ссылка начинается с нужного URL
    assert url.startswith(ESIA_AUTH_URL), "URL должен начинаться с ESIA_AUTH_URL"
    
    # Разбираем параметры запроса
    parsed_url = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    
    # Проверяем наличие всех ключевых параметров
    assert query_params["client_id"][0] == CLIENT_ID, "Неверный client_id"
    assert query_params["redirect_uri"][0] == REDIRECT_URI, "Неверный redirect_uri"
    assert query_params["response_type"][0] == "code", "Неверный response_type"
    assert query_params["scope"][0] == SCOPE_ESIA, "Неверный scope"
    
    # Проверяем, что URL содержит корректный формат
    assert re.match(r"https://esia.gosuslugi.ru/aas/oauth2/ac\?.+", url), "Некорректный формат URL"