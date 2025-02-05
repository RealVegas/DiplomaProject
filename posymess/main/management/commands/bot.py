import os
from loguru import logger
from django.core.management.base import BaseCommand
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from main.models import User, Flower, Order # noqa PyUnresolvedReferences

# Здесь нужно обязательно определить настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'posymess.settings')

# noinspection PyUnresolvedReferences
from posymess.settings import BOT_TOKEN

# Инициализация логирования
logger.add('debug.log', format='{time} {level} {message}', level='DEBUG', rotation='100 MB', compression='zip')

# Создаем экземпляр бота
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

# Создаем экземпляр диспетчера и передаем ему бота
dp = Dispatcher(bot=bot, storage=MemoryStorage())


# Хэндлер команды /start
@dp.message(Command('start'))
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я ваш бот, работающий вместе с Django!")


# Хэндлер для всех остальных текстовых сообщений
@dp.message()
async def echo(message: types.Message):
    await message.answer(message.text)


class Command(BaseCommand):
    @classmethod
    async def start_bot(cls):
        logger.info('Бот запущен')
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

    @classmethod
    async def stop_bot(cls) -> None:
        await bot.session.close()
        logger.info('Бот остановлен')

    def handle(self, *args, **kwargs):
        try:
            asyncio.run(self.start_bot())
        except KeyboardInterrupt:
            asyncio.run(self.stop_bot())