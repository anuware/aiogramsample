# Telegram Bot - aiogramsample

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![aiogram](https://img.shields.io/badge/aiogram-3.7.0-blue)
![SQLAlchemy](https://img.shields.io/badge/sqlalchemy-2.0.30-blue)

## Описание

Этот проект представляет собой Telegram-бота, разработанного с использованием библиотеки [aiogram](https://docs.aiogram.dev/en/latest/) и ORM [SQLAlchemy](https://www.sqlalchemy.org/).

## Функционал


 - Бот имеет самый основной функционал:
 - Основа базы данных
 - Архитектура
 - Безопасность токентов и другой информации

## Установка

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/yourusername/aiogramsample.git
   cd aiogramsample
   ```

2. Создайте виртуальное окружение и активируйте его:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Для Linux/Mac
   venv\Scripts\activate  # Для Windows
   ```

3. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

4. Создайте файл `.env` в корне проекта и добавьте свои переменные окружения:

   ```env
   BOT_TOKEN=your_bot_token_here
   DATABASE_URL=sqlite+aiosqlite:///db.sqlite3
   ```

## Запуск

Для запуска бота выполните:

```bash
python main.py
```



## Получение прав владельца
 - Пропишите /init_owner

