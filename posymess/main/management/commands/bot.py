import os
import asyncio
from loguru import logger

from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from django.core.management import BaseCommand
from django.core.wsgi import get_wsgi_application


from .support import clear_commands
from .keyboards import start_keyboard
from main.views import get_user # noqa PyUnresolvedReferences
from main.models import User, Flower, Order  # noqa PyUnresolvedReferences
from posymess.settings import BOT_TOKEN  # noqa PyUnresolvedReferences

# Настройки Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "posymess.settings")
application = get_wsgi_application()

# Инициализация логирования
logger.add('debug.log', format='{time} {level} {message}', level='DEBUG', rotation='100 MB', compression='zip')

# Экземпляр бота
mem_storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(bot=bot, storage=mem_storage)


# Приветствие и вызов главного меню
@dp.message(Command('start'))
async def start_command(message: types.Message):
    await clear_commands(bot)
    await message.answer(text='Добро пожаловать в Posy message!\nЯ бот для заказа букетов', reply_markup=start_keyboard)


# Кнопка помощь
@dp.message(F.text == '🤓 Помощь')
async def help_handler(message: types.Message):
    await message.answer('Я помогу вам с моими функциями\n'
                         '\nВы можете:\n'
                         '1. Создать новый заказ (кнопка «💐 Заказать букет»)\n'
                         '2. Посмотреть свои текущие заказы (кнопка «📦 Мои заказы»)\n'
                         '3. Отменить текущие заказы (кнопка «📦 Мои заказы»)')


# Кнопка мои заказы
@dp.message(F.text == "📦 Мои заказы")
async def show_orders(message: types.Message):
    current_user = get_user()

    if not current_user:
        error_message = 'Вы не авторизованы, войдите в аккаунт на сайте'
        return await message.answer(error_message)

    # Получаем пользователя и его заказы
    orders = Order.objects.filter(user=current_user)

    if orders.exists():
        for order in orders:
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(f"❌ Отменить заказ {order.id}", callback_data=f"cancel_order:{order.id}"))
            await message.answer(f"Заказ #{order.id}: {order.bouquet.name} 🌹\n"
                                 f"Статус: {order.status}", reply_markup=markup)
    else:
        await message.answer("У вас нет активных заказов.")анный email не найден. Попробуйте еще раз.")



















class Command(BaseCommand):
    """
    Класс создает команду для запуска бота

    """

    @classmethod
    async def run_bot(cls) -> None:
        await clear_commands(bot)
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