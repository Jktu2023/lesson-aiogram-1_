# Общая цель бота. При команде /start или /random бот:
# Находит случайную главу манги.
# Получает список страниц этой главы.
# Отправляет одну случайную страницу с подписью: название манги и ID главы.
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



# --- Функция получения случайной страницы манги ---
def get_random_manga_page():
    try:
        # Шаг 1: Получаем случайную главу. Этот эндпоинт делает GET-запрос к https://api.mangadex.org/chapter
        chapter_response = requests.get(
            "https://api.mangadex.org/chapter",
            params={
                "limit": 1, # запрашивает одну главу.
                "offset": random.randint(0, 10000), # (чтобы получить случайную, а не первую)
                "contentRating[]": ["safe", "suggestive", "erotica"],  # включает мангу с разными уровнями контента
                "order[createdAt]": "desc" # сортирует по дате (новые сначала).
            }
        )
        chapter_response.raise_for_status() # Проверяем, что GET-запрос выполнен успешено
        chapters = chapter_response.json()["data"] # Получаем список глав "data" из ответа
        if not chapters:
            return None

        chapter = chapters[0] # Берём первую (и единственную) главу
        chapter_id = chapter["id"] # ковыряем ее, сначала берем идентификатор
        manga_title = chapter["attributes"].get("title", "Неизвестная манга") # название манги (если есть).⚠️ title может отсутствовать → используется .get() с дефолтом.

        # Шаг 2: Получаем список страниц главы Этот эндпоинт (at-home/server) возвращает:
        # "baseUrl": "https://s4.mangadex.org",      "chapter":  {"hash": "abc123def",   "data": ["page1.jpg", "page2.jpg", ...]}
        pages_response = requests.get(f"https://api.mangadex.org/at-home/server/{chapter_id}")
        pages_response.raise_for_status() # Проверяем, что запрос успешен
        server_data = pages_response.json() # Получаем данные

        base_url = server_data["baseUrl"] # baseUrl — базовый адрес хоста с изображениями.
        hash_value = server_data["chapter"]["hash"] # hash — папка, где лежат файлы главы
        page_filenames = server_data["chapter"]["data"] # data — список имён файлов (страниц).

        if not page_filenames:
            return None

        # Выбираем случайную страницу
        random_page = random.choice(page_filenames) # Выбираем случайную страницу из списка имён файлов (страниц)
        image_url = f"{base_url}/data/{hash_value}/{random_page}" # Создаем ссылку на изображение. Пример итогового URL:
       # https://s4.mangadex.org/data/abc123def/page1.jpg

        return { # Возвращаем то, что накопали в словарь
            "image_url": image_url,
            "manga_title": manga_title,
            "chapter_id": chapter_id
        }

    except Exception as e: # Если ошибка — ловится в except, печатается в консоль, возвращается None.
        print("Ошибка при получении страницы:", e)
        return None


# --- Обработчик /start ---
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привет! Я — бот MangaDex. 📚\nОтправляю случайные страницы из манги!")

    result = get_random_manga_page() # Вызываем функцию получения случайной страницы манги
    if result: # Если страница успешно получена, потрашим результат
        caption = f"📖 Манга: {result['manga_title']}\n🔗 Глава: {result['chapter_id']}"
        await message.answer_photo(photo=result["image_url"], caption=caption)
    else:
        await message.answer("Не удалось загрузить страницу. Попробуй позже.")


# --- Обработчик /random ---
@dp.message(Command("random"))
async def cmd_random(message: Message):
    await message.answer("Ищу ещё одну случайную страницу...")

    result = get_random_manga_page() # Вызываем функцию получения случайной страницы манги
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