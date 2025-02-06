from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Главная клавиатура бота
start_buttons = [[
    KeyboardButton(text='🤓 Помощь'),
KeyboardButton(text='💐 Заказать букет'),
    KeyboardButton(text='📦 Мои заказы'),
]]

start_keyboard = ReplyKeyboardMarkup(keyboard=start_buttons, resize_keyboard=True)