from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Главная клавиатура бота
start_keyboard = ReplyKeyboardMarkup(keyboard=[[
                 KeyboardButton(text='🤓 Помощь'),
                 KeyboardButton(text='💐 Заказать букет'),
                 KeyboardButton(text='📦 Мои заказы'), ]],
                 resize_keyboard=True)