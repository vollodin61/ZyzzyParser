## Здравствуйте, кто будет это читать 🤗
Это вариант выполнения тестового задания.
Что хочу сказать предварительно:
1. Так как это тестовое задание, то я не стал совсем уже KISS применять и писать минимальный код. 
2. Решил предоставить нечто удобоваримое, что сразу можно развивать и масштабировать при необходимости.
3. Исходя из пункта №2 не стал разворачивать полный пример работы с базой данных, используя паттерн Unit Of Works. Показалось избыточным, но я в такое умею при необходимости.
4. Добавление Redis и Nginx для такого простого бота, конечно, тоже избыточно. Но в качестве демонстрации возможностей сделал это. Например, боты [FillatovaBot](https://t.me/FillatovaBot) и [FillatovaChatBot](https://t.me/FillatovaChatBot) работают в таком конфиге (на том же сервере, где эти боты висят, ещё и API базы данных крутится, поэтому Nginx). То же самое относится к миддлварям логгирования, антиспам и шедулер; кастомной ошибке, декоратору отлова ошибок, базовому валидированию при приёме таблицы.
5. Задание со "\*" пока не стал делать. Решил, что "готовый продукт" в основной части есть, значит, нужно предоставить. А если потребуется "\*", то и её сделать можно будет сделать.
6. "наверняка что-то забыл 😅"

# ZyzzyParser Bot

Telegram-бот для парсинга данных из Excel-файлов с последующим сохранением в базу данных.
Доступен и работает по ссылке [@ZyzzyParserBot](https://t.me/ZyzzyParserBot)

## 🚀 Технологии
- Python 3.10+
- Aiogram (Telegram Bot API)
- SQLAlchemy (работа с БД)
- Redis (кэширование)
- SQLite (база данных)
- Docker + Docker Compose (контейнеризация и управление)
- Nginx (обратный прокси)
- Pandas (для работы с excel-файлами)
- Tenacity (для контроля переподключения к бд и редис)

## 📦 Зависимости
- Установите [Docker](https://docs.docker.com/get-docker/) и [Docker Compose](https://docs.docker.com/compose/install/)

## 🛠 Установка и запуск

### 1. Клонируйте репозиторий

```shell
git clone -b master https://github.com/ZyzzyParser.git
cd ZyzzyParser
```


### 2. Настройка окружения
Переименуйте файл `.env_template` в корне проекта в `.env` на основе примера:
```shell
mv .env_template .env
```
Отредактируйте `.env` - укажите свои значения:
```ini
DB_URL=url_базы данных, для сохранения записей, например sqlite+aiosqlite:///название файла
TOKEN=Токен бота от BotFather
WEB_SERVER_HOST=0.0.0.0 # потому что у нас nginx проксирует входящие
WEB_SERVER_PORT=8443
BASE_WEBHOOK_URL=https://адрес вашего сервера с глобальной сети интернет))
WEBHOOK_PATH=/путь к контейнеру который указан в конфиге nginx
WEBHOOK_SECRET=some_webhook_secret
ADMINS_IDS=some_id, any_some_id, third_some_id
REDIS_HOST=название контейнера редиски
REDIS_PORT=порт на котором редиска слушает
```
### 2.1 Если у Вас нет сервера и желания настраивать вебхуки и nginx, то:
В файле `main.py` можно на поллинге запустить
для этого закомментируй строки 62-67 и раскомментируй строки 72-86
### 3. Запуск через Docker Compose
```bash
docker-compose up -d --build
```
Готово! Вы восхитительны! Всё работает 😅

## 🌐 Nginx конфигурация
Nginx настроен как reverse proxy с:
- HTTPS поддержкой. [Нужно добавить сертификаты и указать в nginx.conf адрес своего сервера!](https://certbot.eff.org/)
- Базовой защитой
- Статическим контентом (если требуется)

Конфиг находится в `nginx.conf`

## 🗄 Redis конфигурация
Redis настроен с созданием снапшотов каждые 60 секунд
Конфиг находится в `redis_config/redis.conf`

## 🐳 Docker сервисы
- `zyzzybot` - Основное приложение (бот)
- `zyzzy_redis` - Редис кэширование
- `zyzzy_nginx` - Веб-сервер

## 🛑 Остановка
```bash
docker-compose down
```

## 🔧 Дополнительные команды

### Просмотр логов
```bash
docker logs `название контейнера`
```


## 📌 Особенности
- Автоматическое разворачивание всей инфраструктуры
- Готовый к продакшену стек
- Масштабируемая архитектура

## 📄 Лицензия
MIT

