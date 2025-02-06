import os
import asyncio

from loguru import logger

from datetime import datetime
from asgiref.sync import sync_to_async
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from django.core.management import BaseCommand
from django.core.wsgi import get_wsgi_application

from main.models import User, Flower, Order  # noqa PyUnresolvedReferences
from posymess.settings import BOT_TOKEN  # noqa PyUnresolvedReferences

from .support import clear_commands
from .keyboards import start_keyboard, main_keyboard

# Настройки Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "posymess.settings")
application = get_wsgi_application()

# Инициализация логирования
logger.add('debug.log', format='{time} {level} {message}', level='DEBUG', rotation='100 MB', compression='zip')


# Определим состояния для FSM
class States(StatesGroup):
    enter_email = State()


# Словарь для хранения активных пользователей
active_users = {}

# Экземпляр бота
mem_storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(bot=bot, storage=mem_storage)


# Приветствие и вызов главного меню
@dp.message(Command('start'))
async def start_command(message: types.Message, state: FSMContext):
    await clear_commands(bot)
    await message.answer(text='Добро пожаловать в Posy message! Я бот для заказа букетов')
    await state.set_state(States.enter_email)
    await message.reply(text='Для продолжения работы с ботом введите адрес вашей электронной почты',
                        reply_markup=start_keyboard)


@dp.message(States.enter_email)
async def enter_email(message: types.Message, state: FSMContext):
    email = message.text

    # Проверка наличия адреса эл. почты в базе данных
    try:
        user = await sync_to_async(User.objects.get)(email=email)
        active_users[message.from_user.id] = user
        await state.update_data(email=email)
        await state.clear()
        await message.answer(text='Вы успешно авторизованы!', reply_markup=main_keyboard)

    except User.DoesNotExist:
        await message.answer('Такая почта еще не зарегистрирована\n'
                             'Пожалуйста, зарегистрируйтесь на сайте, чтобы начать работу с ботом')


# Кнопка запуск
@dp.message(F.text == '🚀 Запуск')
async def start_handler(message: types.Message, state: FSMContext):
    await clear_commands(bot)
    await message.answer(text='Добро пожаловать в Posy message! Я бот для заказа букетов')
    await state.set_state(States.enter_email)
    await message.reply(text='Для продолжения работы с ботом введите адрес вашей электронной почты',
                        reply_markup=start_keyboard)


# Кнопка помощи
@dp.message(F.text == '🤓 Помощь')
async def help_handler(message: types.Message):
    await message.answer(text='Я помогу вам с моими функциями\n'
                              '\nВы можете:\n'
                              '1. Регистрация в боте (кнопка «🚀 Запуск»)\n'
                              '1. Создать новый заказ (кнопка «💐 Заказать букет»)\n'
                              '2. Посмотреть свои текущие заказы (кнопка «📦 Мои заказы»)\n'
                              '3. Отменить текущие заказы (кнопка «📦 Мои заказы»)')


# Создание списка заказов в виде списка словарей
def orders_list(orders) -> list[dict[str, str | float]]:
    new_orders = []

    for one_item in orders:
        temp_dict = {}
        temp_dict = {'id': one_item.id,
                     'posy_name': one_item.flower.posy_name,
                     'order_date': datetime.strftime(one_item.order_date, format='%d.%m.%Y'),
                     'order_price': float(one_item.order_price)}

        new_orders.append(temp_dict)

    return new_orders


# Кнопка мои заказы
@dp.message(F.text == '📦 Мои заказы')
async def show_orders(message: types.Message):
    current_user = active_users[message.from_user.id]

    if not current_user:
        return

    # Получаем заказы пользователя
    orders = await sync_to_async(Order.objects.filter)(user=current_user)

    if await sync_to_async(orders.exists)():

        simple_orders = await sync_to_async(orders_list)(orders)

        for order in simple_orders:
            # Кнопка для отмены заказа
            delete_keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                              InlineKeyboardButton(text=f'❌ Отменить заказ', callback_data=f'delete:{order['id']}')]],
                              resize_keyboard=True)

            # Информация о заказе
            await message.answer(text=f'Заказ №{order['id']} '
                                      f'букет «{order['posy_name']}» '
                                      f'дата заказа: {order['order_date']} '
                                      f'цена {order['order_price']}, ',
                                      reply_markup=delete_keyboard)
    else:
        await message.answer('Заказов нет')


# Отмена заказа
# @dp.callback_query(F.data.startswith('delete:'))
# async def remove_order(callback: types.CallbackQuery):
#     dead_id = callback.data.split(':')[1]
#     order = await sync_to_async(Order.objects.get)(order_id=dead_id)
#     await sync_to_async(order.delete)()
#     # order.save()
#     await callback.message.edit_text(text=f'Заказ №{dead_id} отменён')
#     await callback.answer(text='')


# Кнопка заказать букет
# @dp.message(F.text == '💐 Заказать букет')
# async def new_order(message: types.Message):
#     active_user = current_user(message)
#
#     if not active_user:
#         return
#
#     # Получаем список букетов
#     posies = Flower.objects.all() # noqa PyUnresolvedReferences
#
#     if posies.exists():
#
#         for posy in posies:
#
#             order_keyboard = InlineKeyboardMarkup(inline_keyboard=[[
#                              InlineKeyboardButton(text=posy.posy_name, callback_data=f'pick_one:{posy.id}')]],
#                              resize_keyboard=True)
#
#         await message.answer('Выберите букет из списка:', reply_markup=order_keyboard)
#
#
# @dp.callback_query(Text(startswith="select_bouquet:"))
# async def select_bouquet(callback: types.CallbackQuery, state: FSMContext):
#     bouquet_id = int(callback.data.split(":")[1])
#     data = await state.get_data()
#     email = data.get("email")
#
#     if email:
#         user = User.objects.get(email=email)
#         bouquet = Bouquet.objects.get(id=bouquet_id)
#
#         # Создание нового заказа
#         Order.objects.create(user=user, bouquet=bouquet, status="active")
#         await callback.message.edit_text(f"Заказ на {bouquet.name} создан 🌸")
#         await callback.answer("Заказ добавлен.")
#     else:
#         await callback.message.edit_text("Сначала подтвердите email.")
#         await callback.answer("Email не найден.")


# posy = get_object_or_404(Flower, posy_name=posy_name)
# price = posy.price
# active = request.user
#
# print(type(posy), posy)
# print(type(posy), price)
# print(type(active), active)

# order = Order.objects.create(user=active, flower=posy, order_price = price) # noqa PyUnresolvedReferences
# return redirect('orders')


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