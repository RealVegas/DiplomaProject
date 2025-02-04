import os
from dotenv import load_dotenv, find_dotenv

if find_dotenv():
    load_dotenv(find_dotenv())
else:
    exit('Переменные окружения не загружены: файл .env отсутствует')

BOT_TOKEN: str = os.getenv('BOT_TOKEN')