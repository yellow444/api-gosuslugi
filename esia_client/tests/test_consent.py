# tests/test_token.py

import requests
import requests_mock
import pytest
from esia.aas.token import exchange_code_for_token, get_service_token
from esia.aas.config import ESIA_TOKEN_URL, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

"""
📌 Тестирование получения токенов.

🔹 Согласно:
   - "Методические рекомендации по использованию ЕСИА" (раздел 4.3)&#8203;:contentReference[oaicite:1]{index=1}
   - "Методические рекомендации по интеграции с REST API Цифрового профиля" (раздел 5.1.5)&#8203;:contentReference[oaicite:2]{index=2}
"""


@pytest.fixture
def requests_mocks():
    with requests_mock.Mocker() as mock:
        yield mock


def test_exchange_code_for_token(requests_mocks):
    """Тест успешного обмена кода авторизации на токен."""
    requests_mocks.post(ESIA_TOKEN_URL, json={
                       "access_token": "test_token", "expires_in": 3600})
    response = exchange_code_for_token("valid_auth_code")
    assert response["access_token"] == "test_token"


def test_get_service_token(requests_mocks):
    """Тест успешного получения сервисного токена."""
    requests_mocks.post(ESIA_TOKEN_URL, json={
                       "access_token": "service_token", "expires_in": 3600})
    response = get_service_token()
    assert response["access_token"] == "service_token"


def test_exchange_code_for_token_invalid(requests_mocks):
    """Тест обработки ошибки ЕСИА."""
    requests_mocks.post(ESIA_TOKEN_URL, json={
                       "error": "invalid_grant"}, status_code=400)
    with pytest.raises(Exception, match="invalid_grant"):
        exchange_code_for_token("invalid_auth_code")
