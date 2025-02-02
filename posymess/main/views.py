from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import User
from .forms import RegisterForm, LoginForm
from .forms import add_user, check_auth


# Регистрация
def user_register(request):
    errors = {}

    if request.method == 'POST':
        register_form = RegisterForm(request.POST)

        if register_form.not_valid():
            errors = register_form.errors
            return render(request, 'main/register.html', {'errors': errors})

        fault_list = register_form.verify_data()
        reg_data = register_form.pass_data(fault_list)

        # noinspection PyUnresolvedReferences
        if User.objects.filter(email=reg_data['email']).exists():
            errors['email_exists'] = "Пользователь с таким email уже существует."
            return render(request, 'main/register.html', {'errors': errors})

        answer = add_user(reg_data)

        if answer == 'Ошибка создания пользователя в БД. Попробуйте еще раз':
            errors['create_user'] = answer
            return render(request, 'main/register.html', {'errors': errors})
        else:
            message = 'Вы успешно зарегистрировались в Posy message, воспользуйтесь кнопкой Вход чтобы войти в аккаунт'
            return render(request, 'main/register.html', {'message': message})

    # Если метод не POST — отображаем страницу регистрации (пустая форма)
    return render(request, 'main/register.html')


# Авторизация
def user_login(request):
    errors = {}
    exit_message = ['Неверный пароль', 'Такая почта еще не зарегистрирована']

    if request.method == 'POST':
        login_form = LoginForm(request.POST)

        if login_form.not_valid():
            errors = login_form.errors
            return render(request, 'main/login.html', {'errors': errors})

        fault_list = login_form.verify_data()
        login_data = login_form.pass_data(fault_list)

        username = check_auth(login_data)

        if isinstance(username, User):
            request.user = username
            print(username.is_active)
            test_user = authenticate(request, username=username, password=login_data['password'])
            print(f'authenticated user: {test_user}')
            print(f'request user: {request.user} | authenticated: {request.user.is_authenticated}')
            login(request, username)
            return redirect('layout')

        else:
            errors['login'] = exit_message[username]
            return render(request, 'main/login.html', {'errors': errors})

    # Если метод не POST — отображаем страницу регистрации (пустая форма)
    return render(request, 'main/login.html')


# Главная страница
def layout(request):
    return render(request, 'main/layout.html')


# Выход
def logout(request):
    return render(request, 'main/logout.html')


def flower_list(request):
    flowers = Flower.objects.all()
    return render(request, 'flower_list.html', {'flowers': flowers})