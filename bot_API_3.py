# Этот бот возвращает фото кошек
import asyncio
import requests
import random

import sqlite3
import aiohttp
import logging # Модуль для логирования событий. Помогает отслеживать ошибки и ход выполнения программы.
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

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

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    handlers=[
        logging.StreamHandler()
            ])

button_registr = KeyboardButton(text='Регистрация в телеграм боте')
button_exchange_rates = KeyboardButton(text='Курс валют')
button_tips = KeyboardButton(text='Совты по экономии')
button_finances = KeyboardButton(text='Личные финансы')

keyboards = ReplyKeyboardMarkup(
    keyboard=[
        [button_registr, button_exchange_rates],
        [button_tips, button_finances]
            ], resize_keyboard=True)

conn = sqlite3.connect('user.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER unique,
        name TEXT,
        category1 TEXT,
        category2 TEXT, 
        category3 TEXT,
        expenciences1 REAL,
        expenciences2 REAL,
        expenciences3 REAL)
                ''')
conn.commit()
conn.close()

# Вызов инициализации
init_db()

class FinanceForm(StatesGroup):
    category1 = State()
    expenciences1 = State()
    category2 = State()
    expenciences2 = State() # expenciences2
    category3 = State()
    expenciences3 = State()

@dp.message(Command('start')) # Обработчик команды /start
async def send_start(message: Message): # Объявление асинхронной функции
    await message.answer('Привет! Я ваш финансовый помошник. Выбирете нужную кнопку в меню.', reply_markup=keyboards)

@dp.message(F.text == 'Регистрация в телеграм боте') #
async def registration(message: Message): # Объявление асинхронной функции
    telegram_id = message.from_user.id
    name = message.from_user.full_name
    cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
    user = cursor.fetchone()
    if user:
        await message.answer(f"Вы уже зарегистрированы в базе данных. Ваше имя: {user[2]}")
    else:
        cursor.execute("INSERT INTO users (telegram_id, name) VALUES (?, ?)", (telegram_id, name))
        conn.commit()
        await message.answer(f"Вы успешно зарегистрированы в базе данных. Ваше имя: {name}")

@dp.message(F.text == 'Курс валют')  #
async def exchange_rates(message: Message): # Объявление асинхронной функции
    # url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    # url = 'https://api.exchangerate.host/latest'
    url = "https://v6.exchangerate-api.com/v6/09edf8b2bb246e1f801cbfba/latest/USD"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code != 200:
            await message.answer("Не удалось получить курс валют.")
            return
        usd_to_rub = data["conversion_rates"]["RUB"]
        eur_to_usd = data["conversion_rates"]["EUR"]
        eur_to_rub = eur_to_usd * usd_to_rub

        await message.answer(f"Курс USD/RUB: {usd_to_rub:2f}\nКурс EUR/USD: {eur_to_usd:2f}\nКурс EUR/RUB: {eur_to_rub:2f}")

    except:
        await message.answer("Не удалось получить курс валют.")

@dp.message(F.text == 'Совты по экономии') #
async def tips(message: Message): # Объявление асинхронной функции
    tips = [
        "Уменьшите расходы на коммунальные услуги.",
        "Придерживайтесь бюджета на еду.",
        "Придерживайтесь бюджета на развлечения.",
        "Придерживайтесь бюджета на образование.",
        "Ведите бюджет и следите за своими расходами.",
        "Откладывайте часть доходов на сбережения.",
        "Покупайте товары по скидкам и распродажам."
    ]
    tip = random.choice(tips)
    await message.answer(tip)

@dp.message(F.text == 'Личные финансы') #
async def finances(message: Message, state: FSMContext): # Объявление асинхронной функции
    await state.set_state(FinanceForm.category1)
    await message.reply('Выберите первую категорию расходов:')

@dp.message(FinanceForm.category1  ) #
async def category1(message: Message, state: FSMContext): # Объявление асинхронной функции
    await state.update_data(category1=message.text)
    await state.set_state(FinanceForm.expenciences1)
    await message.reply('Введите сумму расходов в первой категории:')

@dp.message(FinanceForm.expenciences1) #
async def expenciences1(message: Message, state: FSMContext): # Объявление асинхронной функции
    await state.update_data(expenciences1=float(message.text))
    await state.set_state(FinanceForm.category2)
    await message.reply('Выберите вторую категорию расходов:')

@dp.message(FinanceForm.category2) #
async def category2(message: Message, state: FSMContext): # Объявление асинхронной функции
    await state.update_data(category2=message.text)
    await state.set_state(FinanceForm.expenciences2)
    await message.reply('Введите сумму расходов во второй категории:')

@dp.message(FinanceForm.expenciences2) #
async def expenciences2(message: Message, state: FSMContext): # Объявление асинхронной функции
    await state.update_data(expenciences2=float(message.text))
    await state.set_state(FinanceForm.category3)
    await message.reply('Выберите третью категорию расходов:')

@dp.message(FinanceForm.category3) #
async def category3(message: Message, state: FSMContext): # Объявление асинхронной функции
    await state.update_data(category3=message.text)
    await state.set_state(FinanceForm.expenciences3)
    await message.reply('Введите сумму расходов в третьей категории:')

@dp.message(FinanceForm.expenciences3) #
async def expenciences3(message: Message, state: FSMContext): # Объявление асинхронной функции
    await state.update_data(expenciences3=float(message.text))
    data = await state.get_data()

    telegram_id = message.from_user.id
    with sqlite3.connect('user.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO finances (user_id, category1, expenciences1, category2, expenciences2, category3, expenciences3)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (telegram_id, data['category1'], data['expenciences1'], data['category2'], data['expenciences2'], data['category3'], data['expenciences3']))
        conn.commit()

    await message.reply('Данные сохранены.')

    total_expenciences = data['expenciences1'] + data['expenciences2'] + data['expenciences3']
    total_expenciences = round(total_expenciences, 2)
    await message.reply(f'Всего расходов: {total_expenciences}')

    await state.clear()


# === Запуск бота ===
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())