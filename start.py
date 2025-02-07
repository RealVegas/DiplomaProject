import os
import threading


# Для запуска бота
def run_bot():
    os.system('python manage.py bot')


# Для сайта
def run_server():
    os.system('python manage.py runserver')


# Для тестов
def run_test():
    os.system('python manage.py test')


if __name__ == '__main__':
    if os.path.exists('posymess'):
        os.chdir('posymess')

    start_bot = threading.Thread(target=run_bot)
    start_server = threading.Thread(target=run_server)

    start_bot.start()
    start_server.start()