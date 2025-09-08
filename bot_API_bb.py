import asyncio
import requests
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from dotenv import load_dotenv
import os

# Загружаем переменные окружения
load_dotenv()

# === Настройки ===
TOKEN_BOT = os.getenv("TOKEN_BOT")
if not TOKEN_BOT:
    raise ValueError("TOKEN_BOT не найден в .env")

# Опционально: ключи Bybit (для приватных данных)
BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
BYBIT_API_SECRET = os.getenv("BYBIT_API_SECRET")

# Базовый URL Bybit (USDT Perpetual)
BYBIT_BASE_URL = "https://api.bybit.com"

# Создаём бота
bot = Bot(token=TOKEN_BOT)
dp = Dispatcher()



# --- Функция: получить цену BTC/USDT ---
def get_btc_price():
    print('щупаем цену')
    try:
        # url = f"{BYBIT_BASE_URL}/v5/execution/list"
        url = f"{BYBIT_BASE_URL}/v5/public/tickers"
        params = {"symbol": "BTCUSDT"}
        response = requests.get(url, params=params)
        data = response.json()
        print(data)

        if data["ret_code"] == 0:
            price = data["result"][0]["last_price"]
            return f"💰 Цена BTC/USDT: ${price}"
        else:
            return "Не удалось получить цену."
    except Exception as e:
        print('не зашли в блок')
        return f"Ошибка: {e}"


# --- Функция: последние сделки ---
def get_recent_trades():
    try:
        url = f"{BYBIT_BASE_URL}/public/realtime"
        params = {"symbol": "BTCUSDT", "resolution": "1", "limit": 5}
        response = requests.get(url, params=params)
        data = response.json()

        if data["ret_code"] == 0:
            trades = data["result"][-5:]  # последние 5 свечей
            lines = ["📉 Последние свечи (1 мин):"]
            for trade in trades:
                lines.append(f"Цена: ${trade['close']}, Объём: {trade['volume']}")
            return "\n".join(lines)
        else:
            return "Не удалось получить сделки."
    except Exception as e:
        return f"Ошибка: {e}"


# --- Функция: баланс (только с API-ключом) ---
def get_wallet_balance():
    if not BYBIT_API_KEY or not BYBIT_API_SECRET:
        return "🔑 API-ключ не настроен. Добавь в .env."

    try:
        # Пример запроса к приватному API (баланс)
        url = f"{BYBIT_BASE_URL}/v2/private/wallet/balance"
        params = {
            "api_key": BYBIT_API_KEY,
            # Здесь нужно добавить подпись (signature) — упрощённо
        }
        # ⚠️ Для реального использования нужна генерация подписи (HMAC)
        return "🔒 Пример: функция требует реализации подписи (см. ниже)."
    except Exception as e:
        return f"Ошибка баланса: {e}"


# --- Обработчик /start ---
@dp.message(Command("start"))
async def cmd_start(message: Message):
    kb = ReplyKeyboardBuilder()
    kb.button(text="Цена BTC")
    kb.button(text="Сделки")
    kb.button(text="Баланс")
    kb.adjust(2)

    await message.answer(
        "Привет! Я — бот для Bybit 📊\nВыбери действие:",
        reply_markup=kb.as_markup(resize_keyboard=True)
    )


# --- Обработчик кнопок ---
@dp.message(F.text == "Цена BTC")
async def send_price(message: Message):
    price = get_btc_price()
    await message.answer(price)

@dp.message(F.text == "Сделки")
async def send_trades(message: Message):
    trades = get_recent_trades()
    await message.answer(trades)

@dp.message(F.text == "Баланс")
async def send_balance(message: Message):
    balance = get_wallet_balance()
    await message.answer(balance)


# --- Запуск бота ---
async def main():
    print("Bybit-бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())