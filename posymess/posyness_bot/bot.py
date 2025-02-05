import os
import sys
from pathlib import Path
from django.core.wsgi import get_wsgi_application

BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.append(BASE_DIR.as_posix())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'posymess.posymess.settings')

from posymess.posymess.settings import BOT_TOKEN
from posymess.main.models import User, Flower, Order





import asyncio

from aiogram import Bot, Dispatcher
# from aiogram import Bot, Dispatcher, F, types
# from aiogram.filters import Command
# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.types import Message


# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
# Импорт Django ORM
# from django.core.wsgi import get_wsgi_application




# Логирование
import logging

logging.basicConfig(level=logging.INFO)

#
# django_application = get_wsgi_application()
#
# # Инициализация бота
bot: Bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


#
# # Определим состояния для FSM
# class States(StatesGroup):
#     send_email = State()
#     select_posy = State()
#
# # Создаем Reply кнопки (главное меню)
# main_menu_markup = ReplyKeyboardMarkup(resize_keyboard=True)
# main_menu_markup.add(KeyboardButton("🚀 Help"), KeyboardButton("📦 Мои заказы"))
# main_menu_markup.add(KeyboardButton("💐 Добавить заказ"))
#
# # Start-обработчик: приветствие + вызов главного меню
# @dp.message(Command(commands=["start"]))
# async def start_command(message: types.Message):
#     await message.answer(
#         "Добро пожаловать! Я бот для заказа букетов 🌸\nВыберите действие из меню ниже:",
#         reply_markup=main_menu_markup
#     )


# -----------------------------------------------------------------
async def main():
    # await set_commands(bot)
    print('Бот запущен')
    await dp.start_polling(bot)


async def stop_bot() -> None:
    await bot.session.close()
    print('Бот остановлен')


#

if __name__ == '__main__':

    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        asyncio.run(stop_bot())

    # bot: Bot = Bot(token=BOT_TOKEN)
    # dp = Dispatcher()
    #
    #
    # async def set_commands(robot: Bot) -> None:
    #     commands = [
    #         types.BotCommand(command='/start', description='Запустить бота'),
    #         types.BotCommand(command='/help', description='Помощь'),
    #         types.BotCommand(command='/weather', description='Погода в Екатеринбурге'),
    #     ]
    #     await robot.set_my_commands(commands)