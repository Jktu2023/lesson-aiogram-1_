# Этот бот будет: Приветствовать пользователя.
# Показывать Reply-кнопки и обрабатывать их.
# Показывать Inline-кнопки (каталог, новости, профиль).
# Обрабатывать нажатия на Inline-кнопки.
# Менять сообщение и клавиатуру при нажатии.
# Показывать всплывающее уведомление (callback.answer).

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

import asyncio
from keyboards import main_kb, inline_keyboard_test, test_keyboard

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

# === Обработчик команды /start ===
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        f"Приветики, {message.from_user.first_name}!",
        reply_markup=inline_keyboard_test  # Показываем Inline-клавиатуру
        # reply_markup=main_kb  # Показываем Reply-клавиатуру
    )

# === Обработка Reply-кнопок ===
@dp.message(F.text == "Тестовая кнопка 1")
async def test_button_1(message: Message):
    await message.answer('Обработка нажатия на reply кнопку "Тестовая кнопка 1"')
@dp.message(F.text == "Тестовая кнопка 2")
async def test_button_2(message: Message):
    await message.answer('Обработка нажатия на reply кнопку "Тестовая кнопка 2"')


# === Обработка Inline-кнопки "Новости" ===
@dp.callback_query(F.data == "news")
async def news(callback: CallbackQuery): # callback: CallbackQuery — параметр, содержащий всю информацию о нажатии кнопки:
                                        # Кто нажал,
                                        # Какое сообщение,
                                        # Какие данные переданы (callback_data),
                                        # Информация о пользователе и т.д.
    # Показываем всплывающее окно (с уведомлением  и кнопкой), потом меняем текст и клавиатуру
    await callback.answer("Новости подгружаются", show_alert=True) # Показываем всплывающее окно как предупреждение с кнопкой
    # Меняем текст и клавиатуру
    await callback.message.edit_text(
        "Вот свежие новости!", # Вот свежие новости!" — это новый текст сообщения, а test_keyboard() — новая клавиатура под ним.
        reply_markup=await test_keyboard() # Сделай это на месте старого сообщения, чтобы не засорять чат.
    )

# === Обработка Inline-кнопки "Каталог" ===
@dp.callback_query(F.data == "catalog")# будет вызвана, когда пользователь нажмёт на inline-кнопку с callback_data='catalog'
async def catalog(callback: CallbackQuery): # callback: CallbackQuery — параметр, представляющий само событие нажатия кнопки.
    await callback.answer("Открываем каталог...") # Это ответ на callback-запрос. Убирает "крутящийся индикатор" под кнопкой. Показывает всплывающее уведомление
    builder = InlineKeyboardBuilder() # InlineKeyboardBuilder — удобный инструмент (построитель) из aiogram, чтобы динамически создавать кнопки (особенно если их много или они генерируются из списка).
    builder.add(InlineKeyboardButton(text="Товар 1", callback_data="item_1")) # Добавляет кнопки в построитель.
    builder.add(InlineKeyboardButton(text="Товар 2", callback_data="item_2")) #text="Товар 1" — что написано на кнопке.
                                                    # callback_data="item_2" — данные, которые придут боту при нажатии.
    # builder.add() добавляет кнопки в одну строку, если не указано иное. Чтобы распределить по строкам, используют .adjust().
    await callback.message.edit_text("Выберите товар:", reply_markup=builder.as_markup())

# === Обработка Inline-кнопки "Профиль" ===
@dp.callback_query(F.data == "person") # «Запусти эту функцию, когда пользователь нажмёт на inline-кнопку с callback_data='person'»
                                    # F.data == "person" — фильтр: сработает только если данные кнопки — "person".
async def profile(callback: CallbackQuery):
    user = callback.from_user # Получаем объект пользователя, который нажал кнопку. callback.from_user — это объект типа User, содержащий:
                            # имя,
                            # ID,
                            # username,
                            # язык и др. Теперь можем использовать user.first_name, user.id, user.username и т.п.
    await callback.answer("Ваш профиль") # Отправляет ответ на callback-запрос. Убирает "крутящийся кружок" под кнопкой.
    # Показывает всплывающее уведомление (toast) у пользователя: 📱 "Ваш профиль"
    text = f"👤 Имя: {user.first_name}\n"
    text += f"🆔 ID: {user.id}\n"
    text += f"📎 Username: @{user.username}" if user.username else ""
    await callback.message.edit_text(text) # Меняем текст. Редактирует исходное сообщение (то, под которым была кнопка).
                                            # Заменяет его текст на сформированную информацию о профиле.

# === обработки нажатий на товары в каталоге, где каждый товар имеет callback_data вида item_1, item_2 и т.д. ===
@dp.callback_query(F.data.startswith("item_"))  #Запусти эту функцию, если данные кнопки (callback_data) начинаются с item_
async def item(callback: CallbackQuery):
    item_id = callback.data.split("_")[1]   # Если callback.data == "item_1" → item_id = "1"
                                            # Если callback.data == "item_42" → item_id = "42"
    await callback.answer(f"Вы выбрали товар {item_id}")
    await callback.message.edit_text(f"Вы выбрали **Товар {item_id}**. Спасибо за выбор!")

# === Запуск бота ===
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())