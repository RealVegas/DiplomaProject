import os
import asyncio
from loguru import logger

from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from django.core.management import BaseCommand
from django.core.wsgi import get_wsgi_application

from main.models import User, Flower, Order  # noqa PyUnresolvedReferences
from posymess.settings import BOT_TOKEN  # noqa PyUnresolvedReferences

# Настройки Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "posymess.settings")
application = get_wsgi_application()

# Инициализация логирования
logger.add('debug.log', format='{time} {level} {message}', level='DEBUG', rotation='100 MB', compression='zip')


# Состояния для FSM
class States(StatesGroup):
    enter_email = State()
    select_flower = State()


# Экземпляр бота
mem_storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(bot=bot, storage=mem_storage)



































class Command(BaseCommand):
    """
    Класс создает команду для запуска бота

    """
    @classmethod
    async def run_bot(cls) -> None:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

    @classmethod
    async def escape_bot(cls) -> None:
        await bot.session.close()

    def handle(self, *args, **kwargs) -> None:
        try:
            logger.info('Бот запущен')
            asyncio.run(self.run_bot())

        except KeyboardInterrupt:
            logger.info('Бот остановлен')

        finally:
            asyncio.run(self.escape_bot())