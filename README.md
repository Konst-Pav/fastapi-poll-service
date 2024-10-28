# HTTP-сервис для проведения опросов

[![CI](https://github.com/Konst-Pav/fastapi-poll-service/actions/workflows/ci.yaml/badge.svg)](https://github.com/Konst-Pav/fastapi-poll-service/actions/workflows/ci.yaml)

Этот проект представляет собой HTTP-сервис для голосования, разработанный с использованием FastAPI. Сервис позволяет создавать опросы с вариантами ответов, отправлять свои голоса и просматривать результаты.

## Оглавление

- [Описание](#описание)
- [Установка](#установка)
- [Использование](#использование)
  - [Создание опроса](#создание-опроса)
  - [Голосование](#голосование)
  - [Просмотр результатов](#просмотр-результатов)
- [API](#api)
- [Тестирование](#тестирование)
- [Лицензия](#лицензия)

## Описание

Сервис предоставляет API для работы с опросами. Пользователи могут создавать новые опросы, добавлять варианты ответов, голосовать за варианты и просматривать результаты опросов.

## Установка

Для запуска сервиса вам потребуется Python 3.11 или выше. Рекомендуется создать виртуальное окружение.

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/Konst-Pav/fastapi-poll-service
   cd ваш-репозиторий
   ```

2. Установите poetry (https://python-poetry.org/docs/#installation)
   ```bash
   pipx install poetry
   ```

3. Установите зависимости:
   ```bash
   poetry install
   ```

4. Чтобы настроить среду для проекта, необходимо определить переменные окружения в файле .env
   ```bash
   DB_URL='postgresql+asyncpg://user:password@localhost:5432/poll_db'
   DBTEST_URL='postgresql+asyncpg://user:password@localhost:5433/poll_db_test'
   POSTGRES_USER=user
   POSTGRES_PASSWORD=password
   POSTGRES_DB=poll_db
   POSTGRES_DB_TEST=poll_db_test
   ```

5. Запустите базы данных, например с помощью docker-compose:
   ```bash
   docker compose up -d pg pg_test 
   ```

6. Запустите сервер:
   ```bash
   uvicorn poll-service-app.main:main_app
   ```
   Сервис будет доступен по адресу http://127.0.0.1:8000.


## Использование
### Создание опроса
Для создания нового опроса отправьте POST-запрос на api/create-poll/ с телом запроса в формате JSON:
   ```bash
   {
     "title": "string",
     "description": "string",
     "options": [
     {
       "point": "string"
       }
     ]
   }
   ```


## Голосование
Для голосования за вариант ответа отправьте POST-запрос на /api/poll/ с телом запроса:
   ```bash
   {
     "poll_id": 0,
     "choice_id": 0
   }
   ```

## Просмотр результатов
Чтобы получить результаты опроса, отправьте GET-запрос на /api/get-result/{poll_id}


## Тестирование
   ```bash
   pytest ./poll-service-app/api/test_views.py
   ```
