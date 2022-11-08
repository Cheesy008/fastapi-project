# FastAPI example

## Подготовока окружения для разработки
Создать файл `.env`. 

Пример переменных окружения смотреть в `.env.sample`.

## Запуск
#### Запуск контейнеров:
```bash
# Запуск из docker compose
docker-compose up
# Для того, чтобы зайти в fastapi контейнер
docker-compose exec backend bash
```

## Описание
Пример приложения с FastAPI и асинхронной SQLAlchemy.\
Данное приложение демонстрирует пример Чистой Архитектуры и использования фреймворка [Dependency Injector](https://github.com/ets-labs/python-dependency-injector).\
Здесь мы имеем три таблицы - User, OutstandingToken и BlacklistToken.\
В проекте реализована базовая авторизация пользователей через JWT токены, добавление токенов в Blacklist, а также изменение пользователя.
