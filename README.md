# Developer Landing Backend

Backend API для формы обратной связи с AI-анализом пользовательских обращений.

Проект реализован на FastAPI с использованием слоистой архитектуры:
**Routers → Services → Repositories → Database**

Основной функционал:

- REST API для отправки контактных обращений
- сохранение обращений в базе данных
- AI-анализ комментариев
- fallback-анализ при недоступности AI
- отправка email-уведомлений
- rate limiting
- логирование запросов и ошибок
- статистика обращений
- автоматические тесты


# 1. Запуск проекта

## Требования

- Python 3.9+
- PostgreSQL
- Poetry


## Установка зависимостей

Клонировать репозиторий:

```bash
git clone https://github.com/anniebeva/developer_landing_backend.git

cd developer_landing_backend
```


Установить зависимости:

```bash
poetry install
```


Активировать окружение:

```bash
poetry shell
```


## Переменные окружения

Создать файл `.env` в корне проекта:

```env
APP_NAME=Developer Landing Backend

DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/database


# AI provider

AI_API_KEY=
AI_BASE_URL=https://openrouter.ai/api/v1
AI_MODEL=google/gemini-2.0-flash-exp:free


# Email

SMTP_HOST=
SMTP_PORT=
SMTP_USER=
SMTP_PASSWORD=
OWNER_EMAIL=
```


## Запуск приложения

```bash
uvicorn app.main:app --reload
```


После запуска:

Swagger документация:

```
http://localhost:8000/docs
```


## Запуск тестов

```bash
pytest
```


---

# 2. Стек технологий

## Backend

- Python 3.11
- FastAPI
- SQLAlchemy 2.0
- Pydantic
- PostgreSQL
- Alembic
- Poetry


## Дополнительные библиотеки

- aiosmtplib 
- pytest 
- httpx 


## AI

Для AI-интеграции используется OpenRouter API через OpenAI SDK.

Используемая модель:

```
google/gemini-2.0-flash-exp:free
```


AI используется для анализа комментариев:

- Определение тональности
- Определение приоритета
- Генерация краткого summary


---

# 3. Архитектура проекта


```
app/

├── ai/
│   ├── client.py
│   ├── fallback.py
│   └── prompts.py
│
├── core/
│   ├── config.py
│   ├── exceptions.py
│   ├── handlers.py
│   ├── logging.py
│   └── rate_limit.py
│
├── models/
│   ├── contact.py
│   └── contact_analysis.py
│
├── repositories/
│   ├── contact.py
│   └── contact_analysis.py
│
├── routers/
│   ├── contact.py
│   ├── health.py
│   └── metrics.py
│
├── schemas/
│
├── services/
│   ├── contact_service.py
│   ├── ai_service.py
│   └── email_service.py
│
└── main.py
```


## Использованные паттерны

### Service Layer

Бизнес-логика вынесена из роутеров в сервисы.

Например:

```
ContactRouter
        |
        ↓
ContactService
        |
        ↓
Repositories
        |
        ↓
Database
```


### Repository Pattern

Работа с базой данных изолирована в отдельных репозиториях:

- ContactRepository
- ContactAnalysisRepository


### Dependency Injection

FastAPI dependencies используются для управления подключениями и сервисами.


## Почему FastAPI

FastAPI выбран благодаря:

- Автоматической Swagger/OpenAPI документации
- Встроенной валидации через Pydantic
- Удобной работе с async
- Высокой скорости разработки REST API


---

# 4. Реализация API


## POST /api/contact

Создание контактного обращения.


### Request

```json
{
  "name": "Anna",
  "phone": "+79999999999",
  "email": "anna@example.com",
  "comment": "Спасибо, всё отлично"
}
```


### Response

```json
{
  "id": 1,
  "name": "Anna",
  "email": "anna@example.com",
  "created_at": "2026-07-29T10:00:00"
}
```


## GET /health

Проверка состояния сервиса.


Response:

```json
{
  "status": "ok"
}
```


## GET /metrics

Возвращает статистику обращений:

- количество обращений
- распределение по sentiment
- распределение по priority
- источники анализа


Пример:

```json
{
  "total_contacts": 10,
  "sentiment": {
    "positive": 5,
    "neutral": 3,
    "negative": 2
  },
  "analysis_source": {
    "ai": 7,
    "fallback": 3
  }
}
```


---

## Валидация и обработка ошибок


Используется Pydantic validation.

Проверяются:

- Обязательные поля
- Корректность email
- Формат входных данных


Ошибки обрабатываются через:

- Кастомные исключения
- Глобальный FastAPI exception handler
- HTTP статус-коды


Примеры:

```
422 Validation Error
```

Некорректные входные данные.


```
429 Too Many Requests
```

Превышен rate limit.


```
500 Internal Server Error
```

Необработанная ошибка сервера.


---

## Email-интеграция

Для отправки уведомлений о новых контактных обращениях используется SMTP.

После создания заявки система пытается отправить email-уведомление с данными пользователя:

- имя
- email
- телефон
- комментарий

Если отправка письма не удалась, ошибка логируется, но создание заявки не прерывается. Контакт и AI-анализ сохраняются в базе данных.

---

### Настройка SMTP

В `.env` необходимо добавить:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587

SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password

SMTP_FROM=your_email@gmail.com
SMTP_TO=recipient_email@gmail.com
```

---

# 5. AI-интеграция

Для анализа входящих обращений используется AI-сервис через OpenRouter API.

Интеграция выполнена через OpenAI-compatible API, поэтому используемую модель можно менять через переменную окружения `AI_MODEL` без изменения исходного кода приложения.

### Настройка AI

В `.env` необходимо указать:

```env
AI_API_KEY=your_openrouter_token
AI_BASE_URL=https://openrouter.ai/api/v1
AI_MODEL=openai/gpt-4o-mini
```

##Используемая модель

В проекте по умолчанию используется модель:

```text
openai/gpt-4o-mini
```

Модель выбрана по следующим причинам:

- Доступна через OpenRouter API
- Имеет оптимальное соотношение скорости, стоимости и качества
- Подходит для анализа коротких пользовательских сообщений
- Хорошо справляется с задачами классификации текста и определения приоритета обращения

Архитектура позволяет заменить модель без изменения кода приложения. Для этого достаточно изменить значение переменной окружения:

```env
AI_MODEL=<another_model_name>
```

## Используемый инструмент

OpenRouter API + OpenAI SDK.

AI функция: Анализ комментариев пользователя.

На выходе модель возвращает:


```json
{
  "sentiment": "positive",
  "priority": "medium",
  "summary": "Customer is satisfied"
}
```


## Fallback механизм


Если:

- Отсутствует API ключ
- AI сервис недоступен
- Произошла ошибка запроса


Используется локальный анализатор Keyword Analyser

Fallback использует анализ ключевых слов:

- Позитивные слова
- Негативные слова
- Слова срочности


---

## Использованный AI prompt


Системный prompt используется для:

- Определения sentiment
- Определения priority
- Формирования краткого summary

Пример: 

```text
Analyze the user contact request.

Return JSON only:

{
  "sentiment": "positive | neutral | negative",
  "priority": "high | medium | low",
  "summary": "short summary"
}

Rules:
- Determine the emotional tone of the message
- Estimate urgency and importance
- Provide a concise summary
- Do not include additional text outside JSON
```


AI ответ валидируется через Pydantic модель.


---

# 6. Использование AI при разработке


AI-инструменты использовались для:

- Генерации первоначальной структуры проекта
- Проверки архитектурных решений
- Создания шаблонов сервисов и репозиториев
- Помощи при написании тестов
- Анализа ошибок


Примеры запросов:

```
Предложи архитектуру FastAPI проекта для формы обратной связи с AI анализом комментариев.
```


```
Помоги реализовать fallback механизм, если AI API недоступен.
```


```
Напиши integration tests для FastAPI endpoint с mock внешних сервисов.
```

```
Помоги составить README.md документацию на основе требований.
```


Все сгенерированные части были проверены, адаптированы и исправлены вручную.


Основные ручные доработки:

- Настройка SQLAlchemy моделей
- Работа с async session
- Обработка ошибок
- Интеграция сервисов
- Настройка тестового окружения


---

# 7. Хранение данных


## База данных

Используется SQLite.

Основные таблицы:

### contact_requests

Хранит обращения пользователей:

- Имя
- Телефон
- Email
- Комментарий
- Дата создания


### contact_analyses

Хранит результаты AI-анализа:

- Sentiment
- Priority
- Summary
- Source (ai/fallback)
- Используемая модель


---

## Логи


Логирование реализовано через Python logging.


Сохраняются:
- Входящие HTTP запросы
- Ошибки приложения
- Ошибки AI
- Ошибки отправки email


---

## Rate limiting


Реализован простой in-memory rate limiter.


Хранятся:

- IP пользователя
- Время запросов


При превышении лимита возвращается:

```
429 Too Many Requests
```

---

## Статистика


Метрики формируются на основе данных базы:

- Общее количество обращений
- Sentiment распределение
- Priority распределение
- Источник анализа AI/fallback


## Frontend

- Frontend часть не реализована, так как задача сфокусирована на разработке backend API.
- API доступен через Swagger/OpenAPI документацию.