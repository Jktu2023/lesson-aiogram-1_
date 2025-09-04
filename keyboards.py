# keyboards.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton #  ReplyKeyboardMarkup — клавиатура, KeyboardButton — кнопка. Я хочу использовать кнопки, которые появляются внизу экрана (как клавиатура), и чтобы пользователь мог нажимать на них, отправляя текст или данные
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton # InlineKeyboardMarkup — клавиатура, InlineKeyboardButton — кнопка
from aiogram.utils.keyboard import InlineKeyboardBuilder # InlineKeyboardBuilder — строитель клавиатуры

# === Reply-клавиатура ===
main_kb = ReplyKeyboardMarkup( #ReplyKeyboardMarkup — вся клавиатура. Это обёртка, которая объединяет несколько кнопок в реальную клавиатуру,
    # которая появляется внизу чата
    keyboard=[
        [KeyboardButton(text="Тестовая кнопка 1")], # KeyboardButton — это класс из библиотеки aiogram, который создаёт одну кнопку
        [KeyboardButton(text="Тестовая кнопка 2")]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

# === Inline-клавиатура 1: главное меню ===
inline_keyboard_test = InlineKeyboardMarkup(inline_keyboard=[ # InlineKeyboardMarkup — клавиатура, которая появляется внутри сообщения
    [InlineKeyboardButton(text="Каталог", callback_data='catalog')], # InlineKeyboardButton — кнопка, которая появляется внутри клавиатуры
    [InlineKeyboardButton(text="Новости", callback_data='news')],
    [InlineKeyboardButton(text="Профиль", callback_data='person')]
])

# === Inline-клавиатура 2: после нажатия (например, YouTube) ===
async def test_keyboard():
    # Список с названиями и разными ссылками
    videos = [
        {"text": "Видео 1", "url": "https://www.youtube.com/watch?v=abc123"},
        {"text": "Видео 2", "url": "https://www.youtube.com/watch?v=def456"},
        {"text": "Видео 3", "url": "https://www.youtube.com/watch?v=ghi789"}
    ]

    # Создаём построитель клавиатуры
    keyboard = InlineKeyboardBuilder()

    # Добавляем кнопки
    for video in videos: # перебираем список из словарей
        keyboard.add( # Добавляем кнопку
            InlineKeyboardButton(# InlineKeyboardButton — кнопка, которая появляется внутри клавиатуры
                text=video["text"], # Текст кнопки
                url=video["url"]  # Уникальная ссылка для каждой кнопки
            )
        )

    # Располагаем по 2 кнопки в ряду keyboard.adjust(2):
#       [Кнопка 1] [Кнопка 2]
#       [Кнопка 3] [Кнопка 4]
#       [Кнопка 5]
    return keyboard.adjust(2).as_markup() # Это ключевая часть при создании inline-клавиатуры в aiogram 3.x.
    # Она отвечает за форматирование и возврат готовой клавиатуры, которую можно показать пользователю
    # .as_markup() — превращаем в "готовую" клавиатуру