## Описание проекта

Данный проект представляет собой систему взаимодействия с API Госуслуг (ЕПГУ) для автоматизации подачи заявлений и обработки результатов. Включает в себя фронтенд и бэкенд, предназначенные для работы в тестовой версии ЕПГУ.

## Использование

1. **Авторизация:**
   - Организация-потребитель проходит авторизацию через API-ключ, выданный вендором.
   - Доступ осуществляется через механизм JWT-токенов.

2. **Создание заявления:**
   - Генерация XML-запроса в соответствии со спецификацией ЕПГУ.
   - Подпись заявления с помощью КриптоПро.
   - Отправка заявления через API.

3. **Обработка ответов:**
   - Получение статуса поданных заявлений.
   - Загрузка ответных документов.

4. **Работа с сертификатами:**
   - Управление сертификатами для подписания данных.
   - Проверка валидности сертификатов.

5. **Администрирование:**
   - Управление пользователями и API-ключами.
   - Мониторинг активности системы.

## Требования
- Node.js / React для фронтенда
- FastAPI / Python для бэкенда
- СУБД PostgreSQL
- Интеграция с КриптоПро для подписания документов

