# Telegram Bot for Review Management

### 📋 Description

This Telegram bot was created to store product review information in a PostgreSQL database, while saving photo and video files in the `uploads/order_id` folder. It performs the following functions:
- Provides a list of item codes for orders associated with the user's `telegram_id`
- Records review details, including review text, photos, videos, and the scheduled posting time.

> *(Due to unusual client preferences, handlers were written directly in `bot.py` instead of the `handlers` folder 😶)*

### 🛠️ Technologies

- **Python** with **Aiogram 3** for the Telegram bot framework
- **PostgreSQL** for the database

---

# Telegram бот для управления отзывами

### 📋 Описание

Этот Telegram бот был создан для сохранения информации об отзыве на товар в базе данных PostgreSQL, а также для хранения фото и видеофайлов в папке `uploads/order_id`. Он выполняет следующие функции:
- Предоставляет список артикулов на заказы, которые привязаны к `telegram_id` пользователя
- Сохраняет данные отзыва, включая текст, фото, видео, и время, через которое выложить данный отзыв

> *(По странным предпочтениям заказчика, handlers были прописаны прямо в `bot.py`, а не в папке `handlers` 😶)*

### 🛠️ Технологии

- **Python** с фреймворком **Aiogram 3** для Telegram-бота
- **PostgreSQL** для базы данных
