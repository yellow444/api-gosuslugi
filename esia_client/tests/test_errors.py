# tests/test_errors.py

import pytest
import json
import re
from requests import Response
from requests.exceptions import Timeout, ConnectionError, RequestException
from esia.aas.errors import (
    EsiaAPIError, EsiaAuthError, DigitalProfileError, NetworkError,
    parse_error, parse_callback_error, handle_http_errors, handle_network_errors
)


"""
📌 Тестирование обработки ошибок.

🔹 Согласно:
   - "Методические рекомендации по интеграции с REST API Цифрового профиля" (таблица ошибок)&#8203;:contentReference[oaicite:4]{index=4}
   - "Методические рекомендации по использованию ЕСИА" (раздел 5.2)&#8203;:contentReference[oaicite:5]{index=5}
"""


# === 1. Тесты для классов ошибок ===


def test_esia_api_error():
    """Тест создания исключения EsiaAPIError."""
    error = EsiaAPIError("ESIA-007002", "Несоответствие сертификата")
    assert str(error) == "[ESIA-007002] Несоответствие сертификата"


def test_digital_profile_error():
    """Тест создания исключения DigitalProfileError."""
    error = DigitalProfileError("Ошибка цифрового профиля")
    assert str(error) == "Ошибка цифрового профиля"


def test_network_error():
    """Тест создания исключения NetworkError."""
    error = NetworkError("Ошибка сети")
    assert str(error) == "Ошибка сети"

# === 2. Тесты для parse_error() ===


def test_parse_esia_error():
    """Тест обработки ошибки ЕСИА."""
    error_json = json.dumps({"error": "ESIA-007002"})
    with pytest.raises(EsiaAPIError) as exc_info:
        raise parse_error(error_json)
    assert exc_info.value.error_code == "ESIA-007002"
    assert "Несоответствие сертификата" in str(exc_info.value)


def test_parse_unknown_esia_error():
    """Тест обработки неизвестной ошибки ЕСИА."""
    error_json = json.dumps({"error": "unknown_error"})
    with pytest.raises(EsiaAPIError) as exc_info:
        raise parse_error(error_json)
    assert "Неизвестная ошибка ЕСИА" in str(exc_info.value)


def test_parse_digital_profile_error():
    """Тест обработки ошибки цифрового профиля."""
    error_json = json.dumps({"errorCode": "ESIA-036701"})
    with pytest.raises(DigitalProfileError) as exc_info:
        raise parse_error(error_json)
    assert "Не найден тип согласия" in str(exc_info.value)


def test_parse_json_decode_error():
    """Тест обработки некорректного JSON-ответа."""
    invalid_json = "invalid json"
    with pytest.raises(Exception, match="Ошибка парсинга JSON"):
        raise parse_error(invalid_json)

# === 3. Тесты для parse_callback_error() ===


def test_parse_callback_error():
    """Тест обработки callback-ошибки ЕСИА."""
    query_params = {
        "error": "invalid_request",
        "error_description": "ESIA-007003: Отсутствует параметр",
        "state": "12345"
    }
    with pytest.raises(EsiaAPIError) as exc_info:
        raise parse_callback_error(query_params)
    assert "ESIA-007003" in str(exc_info.value)


def test_parse_callback_unknown_error():
    """Тест обработки неизвестной callback-ошибки."""
    query_params = {
        "error": "unknown_error",
        "error_description": "Неизвестная ошибка",
        "state": "67890"
    }
    with pytest.raises(EsiaAPIError) as exc_info:
        raise parse_callback_error(query_params)
    assert "Неизвестная ошибка ЕСИА" in str(exc_info.value)

# === 4. Тесты для handle_http_errors() ===


@pytest.fixture
def mock_response():
    """Создает объект Response для тестирования."""
    response = Response()
    response._content = b'{"error": "ESIA-007014"}'
    response.encoding = 'utf-8'
    return response


def test_handle_http_errors_400(mock_response):
    """Тест обработки ошибки 400 (Некорректный запрос)."""
    mock_response.status_code = 400
    with pytest.raises(EsiaAPIError) as exc_info:
        handle_http_errors(mock_response)
    assert "400" in str(exc_info.value)
    assert exc_info.value.error_code == "400"


def test_handle_http_errors_401(mock_response):
    """Тест обработки ошибки 401 (Ошибка аутентификации)."""
    mock_response.status_code = 401
    with pytest.raises(EsiaAuthError) as exc_info:
        handle_http_errors(mock_response)
    assert "401" in str(exc_info.value)
    assert exc_info.value.error_code == "401"


def test_handle_http_errors_403(mock_response):
    """Тест обработки ошибки 403 (Доступ запрещён)."""
    mock_response.status_code = 403
    with pytest.raises(EsiaAuthError) as exc_info:
        handle_http_errors(mock_response)
    assert "403" in str(exc_info.value)
    assert exc_info.value.error_code == "403"


def test_handle_http_errors_500(mock_response):
    """Тест обработки ошибки 500 (Внутренняя ошибка сервера ЕСИА)."""
    mock_response.status_code = 500
    with pytest.raises(EsiaAPIError) as exc_info:
        handle_http_errors(mock_response)
    assert "500" in str(exc_info.value)
    assert exc_info.value.error_code == "500"
