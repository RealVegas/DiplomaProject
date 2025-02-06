import os
import asyncio
from loguru import logger

from aiogram import Bot, Dispatcher, F, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from aiogram.filters import Command

# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from django.core.management import BaseCommand
from django.core.wsgi import get_wsgi_application

from main.views import get_user  # noqa PyUnresolvedReferences
from main.models import User, Flower, Order  # noqa PyUnresolvedReferences
from posymess.settings import BOT_TOKEN  # noqa PyUnresolvedReferences

from .support import clear_commands
from .keyboards import start_keyboard

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
    await message.answer(text='Я помогу вам с моими функциями\n'
                         '\nВы можете:\n'
                         '1. Создать новый заказ (кнопка «💐 Заказать букет»)\n'
                         '2. Посмотреть свои текущие заказы (кнопка «📦 Мои заказы»)\n'
                         '3. Отменить текущие заказы (кнопка «📦 Мои заказы»)')


# Кнопка мои заказы
@dp.message(F.text == '📦 Мои заказы')
async def show_orders(message: types.Message):
    current_user = get_user()

    if not current_user:
        error_message = 'Вы не авторизованы, войдите в аккаунт на сайте'
        return await message.answer(error_message)

    # Получаем заказы пользователя
    orders = Order.objects.filter(user=current_user)

    if orders.exists():

        for order in orders:
            # Кнопка для отмены заказа
            delete_keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                              InlineKeyboardButton(text=f'❌ Отменить заказ', callback_data=f'delete:{order.id}')]],
                              resize_keyboard=True)

            # Информация о заказе
            await message.answer(text=f'Заказ №{order.id}: «{order.flower.posy_name}»\n'
                                 f'Дата заказа: {order.order_date}\n'

                                 f'Цена: {order.order_price}', reply_markup=delete_keyboard)
    else:
        await message.answer('Заказов нет')


# Отмена заказа
@dp.callback_query(F.data.startswith('delete:'))
async def delete_order(callback: types.CallbackQuery):
    dead_id = callback.data.split(':')[1]
    order = Order.objects.get(order_id=dead_id)
    order.delete()
    # order.save()
    await callback.message.edit_text(text=f'Заказ №{dead_id} отменён')
    await callback.answer(text='')


# Кнопка заказать букет
@dp.message(F.text == '💐 Заказать букет')
async def add_order(message: types.Message, state: FSMContext):
    bouquets = Bouquet.objects.all()
    markup = InlineKeyboardMarkup()

    for bouquet in bouquets:
        markup.add(InlineKeyboardButton(bouquet.name, callback_data=f"select_bouquet:{bouquet.id}"))

    await message.answer("Выберите букет из списка:", reply_markup=markup)


@dp.callback_query(Text(startswith="select_bouquet:"))
async def select_bouquet(callback: types.CallbackQuery, state: FSMContext):
    bouquet_id = int(callback.data.split(":")[1])
    data = await state.get_data()
    email = data.get("email")

    if email:
        user = User.objects.get(email=email)
        bouquet = Bouquet.objects.get(id=bouquet_id)

        # Создание нового заказа
        Order.objects.create(user=user, bouquet=bouquet, status="active")
        await callback.message.edit_text(f"Заказ на {bouquet.name} создан 🌸")
        await callback.answer("Заказ добавлен.")
    else:
        await callback.message.edit_text("Сначала подтвердите email.")
        await callback.answer("Email не найден.")










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