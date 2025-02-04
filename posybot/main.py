import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from config_data.bot_config import BOT_TOKEN
from weather import CityWeather

bot: Bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def set_commands(robot: Bot) -> None:
    commands = [
        types.BotCommand(command='/start', description='Запустить бота'),
        types.BotCommand(command='/help', description='Помощь'),
        types.BotCommand(command='/weather', description='Погода в Екатеринбурге'),
    ]
    await robot.set_my_commands(commands)


@dp.message(Command('weather'))
async def weather(message: Message):
    climate = CityWeather('Yekaterinburg,RU').get_weather()

    if climate['desc'] != 'Данные о погоде не найдены':
        await message.answer(f'Сегодня: {climate["date"]}\n'
                             f'В городе: {climate["name"]}\n'
                             f'Погодные условия: {climate["desc"]}\n'
                             f'Температура воздуха: {climate["temp"]} °С\n'
                             f'Ощущается как: {climate["feel"]} °С\n'
                             f'Скорость ветра: {climate["wind"]} м/с\n'
                             f'Относительная влажность: {climate["humid"]} %\n'
                             f'Давление: {climate["press"]} мм. ртутного столба\n'
                             f'Видимость: {climate["visi"]} км')
    else:
        await message.answer(f'Сегодня: {climate["date"]}\n'
                             f'{climate['desc']}')


@dp.message(Command('help'))
async def bot_help(message: Message):
    await message.answer('Этот бот умеет выполнять команды:\n/start - приветствие\n/help - помощь\n/weather - погода в Екатеринбурге')


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('Привет! Я бот!')


async def main():
    await set_commands(bot)
    print('Бот запущен')
    await dp.start_polling(bot)


async def stop_bot() -> None:
    await bot.session.close()
    print('Бот остановлен')


if __name__ == '__main__':
    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        asyncio.run(stop_bot())