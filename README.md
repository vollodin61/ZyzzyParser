

# ZyzzyParser Bot

Telegram-бот для парсинга данных из Excel-файлов с последующим сохранением в базу данных.

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
git clone https://github.com/ZyzzyParser.git
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
### 2.1 Создание базы данных

### 3. Запуск через Docker Compose
```bash
docker-compose up -d --build
```
Готово! Вы восхитительны! Всё работает 😅
## 🌐 Nginx конфигурация
Nginx настроен как reverse proxy с:
- HTTPS поддержкой ([нужно добавить сертификаты](https://certbot.eff.org/))
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

