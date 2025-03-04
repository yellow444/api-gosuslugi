import json
import re
from requests.exceptions import RequestException, Timeout, ConnectionError

"""
📌 Обработчик ошибок ЕСИА, платформы согласий и цифрового профиля.

🔹 Согласно документации:
   - "Методические рекомендации по использованию ЕСИА" (раздел 5.2.20, 5.2.25)&#8203;:contentReference[oaicite:0]{index=0}
   - "Методические рекомендации по интеграции с REST API Цифрового профиля" (таблица 23, 42, 44)&#8203;:contentReference[oaicite:1]{index=1}

📄 ЕСИА возвращает ошибки в параметре `"error"`, `"error_description"`.  
📄 Цифровой профиль возвращает ошибки в параметре `"errorCode"`.  
📄 Платформа согласий использует `permissions` для контроля доступа.
"""

# === 1. Ошибки первого уровня (глобальные) ===
class EsiaError(Exception):
    """Базовый класс для ошибок ЕСИА."""
    def __init__(self, error_code, message):
        self.error_code = error_code
        self.message = message
        super().__init__(f"[{error_code}] {message}")

class EsiaAuthError(EsiaError):
    """Ошибка аутентификации в ЕСИА"""

class EsiaTokenError(EsiaError):
    """Ошибка получения токена ЕСИА"""

class EsiaAPIError(EsiaError):
    """Ошибка взаимодействия с API ЕСИА"""

class EsiaNetworkError(EsiaError):
    """Ошибка сети при обращении к ЕСИА"""

class DigitalProfileError(Exception):
    """Ошибка цифрового профиля"""

class NetworkError(Exception):
    """Ошибка сетевого взаимодействия"""

# === 2. Ошибки второго уровня (детализированные ошибки ЕСИА) ===
ESIA_ERRORS = {
    # Ошибки OAuth2
    "ESIA-007002": "Несоответствие сертификата и мнемоники",
    "ESIA-007003": "Отсутствует обязательный параметр",
    "ESIA-007004": "Запрос отклонен владельцем ресурса",
    "ESIA-007005": "Система-клиент не имеет прав на получение токена",
    "ESIA-007006": "Некорректный scope",
    "ESIA-007007": "Внутренняя ошибка ЕСИА",
    "ESIA-007008": "Сервис временно недоступен",
    "ESIA-007009": "Неподдерживаемый метод получения токена",
    "ESIA-007011": "Авторизационный код недействителен",
    "ESIA-007012": "Неподдерживаемый тип grant",
    "ESIA-007013": "Не указан scope",
    "ESIA-007014": "Отсутствует обязательный параметр",
    "ESIA-007015": "Некорректное время запроса",
    "ESIA-007019": "Отсутствует разрешение на доступ",
    "ESIA-007046": "Требуется двухфакторная аутентификация",
    "ESIA-007053": "Некорректный client_secret",
    "ESIA-007055": "Вход с неподтвержденной учетной записью",
    "ESIA-008010": "Ошибка аутентификации системы-клиента",
}

# === 3. Ошибки платформы согласий (permissions) ===
PERMISSIONS_ERRORS = {
    "ESIA-036700": "Не указана мнемоника типа согласия",
    "ESIA-036701": "Не найден тип согласия",
    "ESIA-036702": "Не указан обязательный scope",
    "ESIA-036703": "Скоупы выходят за рамки разрешенных",
    "ESIA-036704": "Запрещено указывать скоупы",
    "ESIA-036705": "Необходимо указать хотя бы одно действие",
    "ESIA-036706": "Указанное действие не существует",
    "ESIA-036707": "Необходимо указать хотя бы одну цель",
    "ESIA-036716": "Некорректное время истечения срока согласия",
}

# === 4. Функции обработки ошибок ===
def parse_error(response_text: str):
    """
    Извлекает код ошибки из ответа сервера ЕСИА или платформы согласий.

    📄 Согласно "Методическим рекомендациям по использованию ЕСИА" (раздел 5.2.20)&#8203;:contentReference[oaicite:0]{index=0}

    :param response_text: JSON-ответ сервера
    :return: соответствующее исключение с кодом ошибки
    """
    try:
        response = json.loads(response_text)

        if "error" in response:
            error_code = response["error"]
            return EsiaAPIError(error_code, ESIA_ERRORS.get(error_code, f"Неизвестная ошибка ЕСИА: {error_code}"))

        if "errorCode" in response and response["errorCode"] in PERMISSIONS_ERRORS:
            return DigitalProfileError(PERMISSIONS_ERRORS[response["errorCode"]])

    except json.JSONDecodeError:
        raise EsiaAPIError("JSONDecodeError", "Ошибка парсинга JSON.")


# === 5. Хендлер парсинга ошибок из query-параметров ===
def parse_callback_error(query: dict):
    """
    Парсинг ошибок ЕСИА из callback-запросов.

    📄 Согласно "Методическим рекомендациям по использованию ЕСИА" (раздел 5.2.25)&#8203;:contentReference[oaicite:3]{index=3}

    :param query: Словарь с query-параметрами
    :return: Исключение с расшифровкой ошибки
    """
    error_desc = query.get("error_description", "")
    match = re.search(r"ESIA-\d{6}", error_desc)
    error_code = match.group(0) if match else "UNKNOWN"
    return EsiaAPIError(error_code, ESIA_ERRORS.get(error_code, f"Неизвестная ошибка ЕСИА: {error_code}"))

# === 6. Обработчик HTTP-ошибок ===
def handle_http_errors(response):
    """Обрабатывает ошибки HTTP-запросов к ЕСИА."""
    if response.status_code == 400:
        raise EsiaAPIError("400", f"Некорректный запрос - {response.text}")
    elif response.status_code == 401:
        raise EsiaAuthError("401", f"Ошибка аутентификации - {response.text}")
    elif response.status_code == 403:
        raise EsiaAuthError("403", f"Доступ запрещён - {response.text}")
    elif response.status_code == 500:
        raise EsiaAPIError("500", f"Внутренняя ошибка сервера ЕСИА - {response.text}")
    else:
        response.raise_for_status()

# === 7. Обработчик сетевых ошибок ===
def handle_network_errors(func):
    """
    Декоратор для обработки сетевых ошибок.

    📄 Согласно "Методическим рекомендациям по использованию ЕСИА" (раздел 5.2.20)&#8203;:contentReference[oaicite:4]{index=4}

    :param func: Функция, выполняющая сетевой запрос
    :return: Результат выполнения функции или исключение NetworkError
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Timeout:
            raise NetworkError("Ошибка: превышено время ожидания запроса")
        except ConnectionError:
            raise NetworkError("Ошибка: сервер ЕСИА недоступен")
        except RequestException as e:
            raise NetworkError(f"Ошибка сети: {str(e)}")
    return wrapper
