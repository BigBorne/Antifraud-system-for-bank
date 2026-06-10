# Антифрод система для банка

Микросервис на FastAPI для проверки клиентов перед выдачей кредитов.
Система анализирует возраст, номер телефона, кредитную историю и проверяет телефоны по чёрному списку в Redis.

---

## Технологии

- FastAPI — веб-фреймворк
- Redis — база данных для чёрных списков
- Docker / Docker Compose — контейнеризация
- Pydantic — валидация данных
- Uvicorn — ASGI сервер

---

## Структура проекта

```
antifraud-service/
├── main.py                  # Точка входа (запуск сервера)
├── src/
│   ├── config/
│   │   └── local.yaml       # Конфигурация
│   └── app/
│       ├── main.py           # FastAPI приложение
│       ├── config.py         # Загрузка конфига
│       ├── api/
│       │   └── healthz.py    # Health-check
│       └── antifraud/
│           └── check.py      # Логика антифрода
├── Dockerfile
├── pyproject.toml
└── requirements.txt
```

---

## Установка и запуск

### Локально

```bash
git clone https://github.com/BigBorne/antifraud-system.git
cd antifraud-system/antifraud-service
```

Установка uv:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Установка Python и зависимостей:

```bash
uv python install 3.12
uv venv --python 3.12
uv sync
```

Запустить Redis (локально):

```bash
redis-server
```

Запуск сервиса:

```bash
uv run main.py
```

Сервис будет доступен на `http://localhost:8001`.

### Docker Compose

```bash
docker-compose up --build
```

Остановить:

```bash
docker-compose down
```

---

## Конфигурация

Файл `src/config/local.yaml`:

```yaml
app_name: "service-template"
version: "1.0.0"
host: "0.0.0.0"
port: 8001
environment: "local"
debug: true
```

Переменные окружения для Redis (опционально):

| Переменная       | По умолчанию | Описание         |
|------------------|--------------|------------------|
| `REDIS_HOST`     | `localhost`  | Хост Redis       |
| `REDIS_PORT`     | `6379`       | Порт Redis       |
| `REDIS_PASSWORD` | —            | Пароль Redis     |
| `REDIS_DB`       | `0`          | Номер базы Redis |

---

## API

### Проверка клиента

```
POST /antifraud/check
```

```json
{
  "birth_date": "1990-05-15",
  "phone_number": "+79001234567",
  "loans_history": [
    {"amount": 50000, "loan_data": "2024-01-01", "is_closed": true}
  ]
}
```

### Чёрный список

```
POST /antifraud/admin/blacklist/add?phone=+79001234567&reason=fraud
DELETE /antifraud/admin/blacklist/remove/+79001234567
```

### Health-check

```
GET /healthz/live
```
