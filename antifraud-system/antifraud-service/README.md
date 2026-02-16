# Антифрод система для банка

Микросервис на FastAPI для проверки клиентов перед выдачей кредитов.
Система анализирует возраст, номер телефона, кредитную историю и проверяет телефоны по чёрному списку в Redis.

---

## Технологии

- FastAPI — веб-фреймворк
- Redis — база данных для чёрных списков и кэширования
- Docker / Docker Compose — контейнеризация
- Pydantic — валидация данных
- Uvicorn — ASGI сервер

---

## Функционал

### Основная проверка (`/antifraud/check`)
- Расчёт возраста по дате рождения
- Проверка формата телефона (+7 или 8)
- Анализ кредитной истории
- Проверка телефона по чёрному списку в Redis
- Кэширование успешных проверок (на 1 час)

### Админка (`/antifraud/admin`)
- Добавление телефонов в чёрный список
- Удаление из чёрного списка
- Просмотр всего чёрного списка

---
## Установка и запуск

### Локально
```bash
git clone https://github.com/твой-логин/antifraud-system.git
cd antifraud-system
```

```bash
Установка uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Установка версии Python
```bash
uv python install 3.12
```

Инициализация проекта
```bash
uv init --python 3.12
```


```bash
uv venv --python 3.12
```

Добавление библиотек
```bash
uv add 'uvicorn>=0.40.0'
uv add 'fastapi>=0.122.0'
uv add 'pydantic>=2.12.5'
uv add pydantic-settings
uv add pyyaml
uv add --dev 'pytest>=9.0.1'
```

Запустить Redis (локально)
```bash
redis-server
```

Запуск
```bash
uv run src/run.py
```

### Запуск в Docker-compose
Запустить
```bash
docker-compose up --build
```

Закрыть все контейнеры
```bash
docker-compose down
```




