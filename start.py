import os

if __name__ == '__main__':
    if os.path.exists('posymess'):
        os.chdir('posymess')

    #os.system('python manage.py test')
    os.system('python manage.py runserver')