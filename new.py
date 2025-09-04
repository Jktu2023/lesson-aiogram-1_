# Создайте Телеграм-бота, который запрашивает у пользователя имя, возраст и группу (grade), в котором он учится.
# Сделайте так чтоб бот сохранял введенные данные в таблицу students базы данных school_data.db с указанием даты и времени регистрации.
# и возвращал сохраненную информацию об этом пользователе.
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile # FSInputFile — позволяет отправлять файлы с диска (например, фото, документы).
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext # Контекст машины состояний (FSM). Позволяет хранить временные данные пользователя (например, имя, возраст) между сообщениями.
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from logging.handlers import RotatingFileHandler # Модуль для логирования с ротацией. RotatingFileHandler — это как умный секретарь,
# который говорит:"Когда дневник достигнет 10 страниц — закрой его, подпиши 'Архив 1', начни новый. А если архивов станет слишком много — удали самый старый."

import sqlite3 #Встроенный модуль Python для работы с SQLite — лёгкой встраиваемой СУБД. Используется для сохранения данных пользователей
import aiohttp
import logging # Модуль для логирования событий. Помогает отслеживать ошибки и ход выполнения программы.

from dotenv import load_dotenv # load_dotenv — загружает переменные из .env файла.
import os

load_dotenv()
# токены из файла .env
TOKEN_BOT = os.getenv('TOKEN_BOT')
if not TOKEN_BOT:
    raise ValueError("TOKEN_BOT не найден в .env")

bot = Bot(token=TOKEN_BOT) # Создаёт объект бота с указанным токеном. Через него отправляются сообщения.
dp = Dispatcher()

# Логирование с ротацией: максимум 5 файлов по 10 МБ
handler = RotatingFileHandler("tmp/bot.log", maxBytes=10*1024*1024, backupCount=5, encoding="utf-8")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    handlers=[
        handler,
        logging.StreamHandler()
    ]
)

class Form(StatesGroup): # Группа состояний FSM
    name = State() # Состояние name
    age = State()
    grade = State()



def init_db():
    with sqlite3.connect('school_data.db') as conn: # контекстный менеджер with для автоматического закрытия соединения. Это защитит от утечек соединений, если возникнет ошибка.
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                age INTEGER,
                grade TEXT,
                registration_date TEXT
            )
        ''')
        # conn.commit()

init_db() # Вызывает функцию при запуске — таблица создаётся один раз.

@dp.message(CommandStart()) # Обработчик команды /start
async def start(message: Message, state: FSMContext): # state: FSMContext — это "память" бота для одного пользователя во время диалога.
    await state.clear()  # на случай, если он уже заполнял форму
    await message.answer('Привет! Давайте заполним форму. Как тебя зовут?')
    await state.set_state(Form.name)  # ← боту сказали: жди имя

@dp.message(Form.name) # ← этот обработчик сработает ТОЛЬКО если state == Form.name, то есть имя, которое бот ждал
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text) # сохрани имя, которое ты ждал
    await message.answer('Сколько тебе лет?')
    await state.set_state(Form.age) # ← боту сказали: жди возраст

@dp.message(Form.age) # ← этот обработчик сработает ТОЛЬКО если state == Form.age - возраст
async def process_age(message: Message, state: FSMContext):
    if not message.text.isdigit(): # Проверяем, является ли возраст числом
        await message.answer("Пожалуйста, введите возраст числом.")
        return
    await state.update_data(age=int(message.text)) # сохрани возраст
    await message.answer('В какой группе (классе) ты учишься?')
    await state.set_state(Form.grade) # ← боту сказали: жди группу

@dp.message(Form.grade) # ← этот обработчик сработает ТОЛЬКО если state == Form.grade - группа
async def process_grade(message: Message, state: FSMContext):
    await state.update_data(grade=message.text) # сохрани группу
    data = await state.get_data() # "Достань все временные данные, которые ты сохранял в этом состоянии для пользователя."  и сохрани их в переменную

    try:
        with sqlite3.connect('school_data.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO students (name, age, grade, registration_date)
                VALUES (?, ?, ?, datetime('now'))
            ''', (data['name'], data['age'], data['grade']))
            # conn.commit()

        await message.answer(
            f"Спасибо, {data['name']}! Тебе {data['age']} лет, ты в группе {data['grade']}. Данные сохранены."
        )
    except Exception as e:
        logging.error(f"Ошибка при сохранении в БД: {e}")
        await message.answer("Произошла ошибка при сохранении данных. Попробуйте позже.")
    finally:
        await state.clear()
    logging.info(f"Сохранены данные: {data['name']}, возраст {data['age']}, группа {data['grade']}")
@dp.message(Command('cancel')) # Обработчик команды /cancel
async def cancel(message: Message, state: FSMContext): # Объявление асинхронной функции
    await state.clear() # Очищаем состояние
    await message.answer('Форма была отменена.')

async def main():
    await dp.start_polling(bot) # Запускаем бота

if __name__ == "__main__":
    asyncio.run(main())