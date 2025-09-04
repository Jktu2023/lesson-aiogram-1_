import asyncio # Запускает асинхронную функцию main()
from aiogram import Bot, Dispatcher, F # Основные классы aiogram: бот и диспетчер (обработчик событий) и Специальный объект
# для фильтрации сообщений (например, по тексту или типу)
from aiogram.types import Message, FSInputFile # Тип Message для аннотации — чтобы IDE подсказывала методы
from aiogram.filters import CommandStart, Command # Фильтры для команд /start, /help и т.д.
import random
import httpx # httpx - библиотека для асинхронного HTTP-клиента
from gtts import gTTS
from translate import Translator

from dotenv import load_dotenv
import os

load_dotenv()
# токены из файла .env
TOKEN_BOT = os.getenv('TOKEN_BOT')
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')


bot = Bot(token=TOKEN_BOT) # экземпляр бота, который будет общаться с Telegram API.
dp = Dispatcher() # диспетчер, отвечает за прослушивание входящих обновлений от Telegram (сообщений, команд, фото и т.д.).
                        # Он решает, какую функцию выбрать и вызвать в ответ на то или иное сообщение.


@dp.message(Command('doc'))
async def doc(message: Message):
    doc = FSInputFile("tmp/prices.csv")
    await bot.send_document(message.chat.id, doc)
@dp.message(Command('training'))
async def training(message: Message):
    training_list = [
       "Тренировка 1:\n1. Скручивания: 3 подхода по 15 повторений\n2. Велосипед: 3 подхода по 20 повторений (каждая сторона)\n3. Планка: 3 подхода по 30 секунд",
       "Тренировка 2:\n1. Подъемы ног: 3 подхода по 15 повторений\n2. Русский твист: 3 подхода по 20 повторений (каждая сторона)\n3. Планка с поднятой ногой: 3 подхода по 20 секунд (каждая нога)",
       "Тренировка 3:\n1. Скручивания с поднятыми ногами: 3 подхода по 15 повторений\n2. Горизонтальные ножницы: 3 подхода по 20 повторений\n3. Боковая планка: 3 подхода по 20 секунд (каждая сторона)",
   ]
    rand_tr = random.choice(training_list)
    await message.answer(f"Это ваша мини-тренировка на сегодня {rand_tr}")

@dp.message(Command('training_vioce'))
async def training(message: Message):
    training_list = [
       "Тренировка 1:\n1. Скручивания: 3 подхода по 15 повторений\n2. Велосипед: 3 подхода по 20 повторений (каждая сторона)\n3. Планка: 3 подхода по 30 секунд",
       "Тренировка 2:\n1. Подъемы ног: 3 подхода по 15 повторений\n2. Русский твист: 3 подхода по 20 повторений (каждая сторона)\n3. Планка с поднятой ногой: 3 подхода по 20 секунд (каждая нога)",
       "Тренировка 3:\n1. Скручивания с поднятыми ногами: 3 подхода по 15 повторений\n2. Горизонтальные ножницы: 3 подхода по 20 повторений\n3. Боковая планка: 3 подхода по 20 секунд (каждая сторона)",
   ]
    rand_tr = random.choice(training_list)
    await message.answer(f"Это ваша мини-тренировка на сегодня {rand_tr}")
    tts = gTTS(text=rand_tr, lang='ru')
    tts.save("training.ogg")
    audio = FSInputFile("training.ogg")
    await bot.send_chat_action(message.chat.id, 'upload_audio')
    await bot.send_voice(chat_id=message.chat.id, voice=audio)
    os.remove("training.ogg")

@dp.message(Command('video'))
async def video(message: Message):
    video = FSInputFile('tmp/video.mp4')
    await bot.send_chat_action(message.chat.id, 'upload_video')
    await bot.send_video(message.chat.id, video)

@dp.message(Command('audio'))
async def audio(message: Message):
    audio = FSInputFile('tmp/sound2.mp3')
    await bot.send_chat_action(message.chat.id, 'upload_audio')
    await bot.send_audio(message.chat.id, audio)

@dp.message(Command('photo')) # это декоратор в библиотеке aiogram (3.x), который указывает диспетчеру (Dispatcher):
                              # «Эту функцию нужно вызывать, когда приходит сообщение, подходящее под указаные условия.»
async def photo(message: Message): # Обработчик команды /photo
    list = ['https://epoi.ru/wa-data/public/shop/products/32/01/132/images/870/870.970.jpg',
            'https://epoi.ru/wa-data/public/shop/products/32/01/132/images/24/24.970.jpg',
            'https://epoi.ru/wa-data/public/shop/products/32/01/132/images/434/434.970.jpg',
            'https://epoi.ru/wa-data/public/shop/products/32/01/132/images/434/434.970.jpg',
            'https://epoi.ru/wa-data/public/shop/products/32/01/132/images/424/424.970.jpg',
            'https://epoi.ru/wa-data/public/shop/products/32/01/132/images/716/716.970.jpg',
            'https://epoi.ru/wa-data/public/shop/products/32/01/132/images/900/900.740x484.jpg',
            'https://epoi.ru/wa-data/public/shop/products/32/01/132/images/715/715.970.jpg',
            ]
    rand_photo = random.choice(list)
    await message.answer_photo(photo=rand_photo, caption='Это супер крутая картинка') #  «await - Подожди, пока это действие (например, отправка фото в Telegram)
    # завершится, прежде чем переходить к следующей строке». async и await — основа асинхронного кода. Где можно использовать await? Только внутри async def функций!

@dp.message(F.photo) # Фильтр для фотографий F.photo — значит "если сообщение содержит фото". @bot.message_handler(commands('photos', prefix='&')) сработает команда в боте &photo
async def react_photo(message: Message):
    list = ['Ого, какая фотка!', 'Класс!', 'Не отправляй мне такое больше', 'Много интересного у тебя!', 'Прикольная фотка!', 'Супер!', 'Круто!']
    rand_answ = random.choice(list)
    await message.answer(rand_answ)
    await bot.download(message.photo[-1],destination=f'tmp/{message.photo[-1].file_id}.jpg')

@dp.message(F.text == "что такое ИИ?") # Фильтр для текста F.text — значит "если сообщение содержит текст".  F.text == "..." — строгое сравнение текста.
async def aitext(message: Message): # Обработчик текста
    await message.answer('Искусственный интеллект — это свойство искусственных интеллектуальных систем...')

@dp.message(CommandStart()) # Обработчик команды /start
async def start(message: Message):
    await message.answer(f"Приветики,  {message.from_user.first_name}") # имя, {message.from_user.full_name} - полное имя.



@dp.message(Command('help')) #
async def help(message: Message): # Обработчик команды /help
    await message.answer("Этот бот умеет принимать твои фотографии с коментариями и еще выполнять команды:\n/start\n/help\n/photo\n/weather")

@dp.message(Command('weather'))
async def weather_tomsk(message: Message): # Объявление асинхронной функции (обязательно для aiogram).
                                            # message: Message — параметр с информацией о сообщении от пользователя.
    city = "Tomsk"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric&lang=ru"

    async with httpx.AsyncClient() as client: # httpx - библиотека для асинхронного HTTP-клиента
        try:
            response = await client.get(url)
            data = response.json()
            print(response.status_code)
            print(data)

            if response.status_code == 200: # Если запрос прошел успешно
                temp = data['main']['temp']
                sea_level = data['main']['sea_level']
                feels_like = data['main']['feels_like']
                description = data['weather'][0]['description'].capitalize()
                humidity = data['main']['humidity']
                wind_speed = data['wind']['speed']

                weather_text = (
                    f"🌤 Город {city} погода сегодня:\n"
                    f"🌡 Температура: {temp}°C\n"
                    f"🤔 Ощущается как: {feels_like}°C\n"
                    f"📝 {description}\n"
                    f"💧 Влажность: {humidity}%\n"
                    f"💨 Ветер: {wind_speed} м/с\n"
                    f"🌊 Высота над уровнем моря: {sea_level} м"

                )
            else:
                weather_text = "❌ Не удалось получить погоду. Проверь название города."

        except Exception as e:
            weather_text = f"⚠️ Ошибка: не удалось получить данные о погоде."

        await message.answer(weather_text)

@dp.message(F.text)  # Ловим любое текстовое сообщение для перевода
async def translate_text(message: Message): # Объявление асинхронной функции
    # Список команд, которые НЕ нужно переводить
    commands = {'/start', '/help', '/photo', '/weather', '/training', '/doc', '/video', '/audio', '/training_voice', 'что такое ии?'}
    user_text = message.text.strip().lower()

    # Если это команда — не переводим
    if user_text in [cmd.lower() for cmd in commands] or user_text.startswith('/'):
        return  # Пропускаем, пусть другие обработчики работают

    try:
        # Создаём переводчик с русского на английский
        translator = Translator(from_lang="ru", to_lang="en")
        translation = translator.translate(message.text)

        # Отправляем перевод
        await message.reply(f"🇬🇧 {translation}")

    except Exception as e:
        await message.reply("❌ Не удалось выполнить перевод. Попробуйте снова.")

@dp.message() # ответ на все
async def echo(message: Message):
    if message.text.lower() == 'test':
        await message.answer('Тестируем')
    await message.send_copy(chat_id=message.chat.id) # эхо




async def main():
    await dp.start_polling(bot) # Запускаем бота

if __name__ == "__main__":
    asyncio.run(main())


# Как это работает?  !
# Когда пользователь что-то пишет боту:
# Telegram отправляет обновление (update).
# Dispatcher (dp) проверяет все зарегистрированные обработчики.
# Находит подходящий по фильтру (например, CommandStart()).
# Вызывает соответствующую функцию.

# Ответ сервера погоды:{'coord': {'lon': 82.5, 'lat': 58.5},
# 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'пасмурно', 'icon': '04n'}],
# 'base': 'stations',
# 'main': {'temp': 16.8, 'feels_like': 16.52, 'temp_min': 16.8, 'temp_max': 16.8, 'pressure': 1014, 'humidity': 76, 'sea_level': 1014, 'grnd_level': 1008},
# 'visibility': 10000,
# 'wind': {'speed': 3.45, 'deg': 144, 'gust': 7.22}, 'clouds': {'all': 99}, 'dt': 1756389329,
# 'sys': {'country': 'RU', 'sunrise': 1756336786, 'sunset': 1756388595}, 'timezone': 25200, 'id': 1489421, 'name': 'Томская область', 'cod': 200}
