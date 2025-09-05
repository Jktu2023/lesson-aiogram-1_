
import asyncio
import requests
import random
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from io import BytesIO
from aiogram.types import FSInputFile

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



# --- Функция получения случайной страницы манги ---
def get_random_manga_page():
    try:
        # Шаг 1: Получаем случайную главу
        chapter_response = requests.get(
            "https://api.mangadex.org/chapter",
            params={
                "limit": 1,
                "offset": random.randint(0, 10000),
                "contentRating[]": ["safe", "suggestive", "erotica"],  # Все категории
                "order[createdAt]": "desc"
            }
        )
        chapter_response.raise_for_status()
        chapters = chapter_response.json()["data"]
        if not chapters:
            return None

        chapter = chapters[0]
        chapter_id = chapter["id"]
        manga_title = chapter["attributes"].get("title", "Неизвестная манга")

        # Шаг 2: Получаем список страниц главы
        pages_response = requests.get(f"https://api.mangadex.org/at-home/server/{chapter_id}")
        pages_response.raise_for_status()
        server_data = pages_response.json()

        base_url = server_data["baseUrl"]
        hash_value = server_data["chapter"]["hash"]
        page_filenames = server_data["chapter"]["data"]

        if not page_filenames:
            return None

        # Выбираем случайную страницу
        random_page = random.choice(page_filenames)
        image_url = f"{base_url}/data/{hash_value}/{random_page}"

        return {
            "image_url": image_url,
            "manga_title": manga_title,
            "chapter_id": chapter_id
        }

    except Exception as e:
        print("Ошибка при получении страницы:", e)
        return None


# --- Обработчик /start ---
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привет! Я — бот MangaDex. 📚\nОтправляю случайные страницы из манги!")

    result = get_random_manga_page()
    if result:
        caption = f"📖 Манга: {result['manga_title']}\n🔗 Глава: {result['chapter_id']}"
        await message.answer_photo(photo=result["image_url"], caption=caption)
    else:
        await message.answer("Не удалось загрузить страницу. Попробуй позже.")


# --- Обработчик /random ---
@dp.message(Command("random"))
async def cmd_random(message: Message):
    await message.answer("Ищу ещё одну случайную страницу...")

    result = get_random_manga_page()
    if result:
        caption = f"📖 Манга: {result['manga_title']}\n🔗 Глава: {result['chapter_id']}"
        await message.answer_photo(photo=result["image_url"], caption=caption)
    else:
        await message.answer("Не удалось загрузить страницу. Попробуй ещё раз.")





# === Запуск бота ===
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())