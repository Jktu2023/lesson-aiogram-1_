
import asyncio
import requests
import random
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from dotenv import load_dotenv # load_dotenv — загружает переменные из .env файла.
import os

load_dotenv()
# токены из файла .env
TOKEN_BOT = os.getenv('TOKEN_BOT')
if not TOKEN_BOT:
    raise ValueError("TOKEN_BOT не найден в .env")

# Создаём бота и диспетчер
bot = Bot(token=TOKEN_BOT)
dp = Dispatcher()



# URL для получения случайного изображения кошки
RANDOM_CAT_URL = "https://api.thecatapi.com/v1/images/search"

# Список забавных подписей (опционально)
CAPTIONS = [
    "Вот тебе милая кошечка! 😻",
    "Держи котика на поднятие настроения! 🐾",
    "Кто-то просил кошачью агрессию? Нет? А вот тебе всё равно! 😼",
    "Смотри, кто тут у нас! Очаровашка! 🐱",
    "Ты не можешь грустить, когда видишь это! 🥰"
]

# === Обработчик команды /start ===
@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Привет! Я — бот с кошками. Напиши /random_cat, чтобы получить милого котёнка!")


@dp.message(Command("random_cat"))
async def random_cat_handler(message: Message):
    # Делаем запрос к TheCatAPI
    try:
        response = requests.get(RANDOM_CAT_URL)
        data = response.json()

        if response.status_code == 200 and data: # Если запрос прошел успешно
            # Получаем ссылку на изображение
            image_url = data[0]["url"]

            # Выбираем случайную подпись
            caption = random.choice(CAPTIONS)

            # Отправляем фото
            await message.answer_photo(photo=image_url, caption=caption) # message, отвечает на входящее сообщение пользователя.
                                                                         # используется .answer_photo (ответить на сообщение стрелочкой).
                                                                        # photo=image_url Указывает, что именно отправить. В данном случае — ссылка на изображение например, https://example.com/cat.jpg
        else:
            await message.answer("Не удалось получить фото. Попробуй ещё раз позже.")

    except Exception as e:
        await message.answer("Ошибка при получении фото: " + str(e))








# === Запуск бота ===
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())