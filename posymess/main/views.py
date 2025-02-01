from django.contrib.auth import login
from django.shortcuts import render, redirect
from .models import User  # , Flower
from .forms import RegisterForm, LoginForm, add_user
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password


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

        if answer == 'Ошибка создания пользователя. Попробуйте еще раз':
            errors['create_user'] = answer
            return render(request, 'main/register.html', {'errors': errors})

        return redirect('login')

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

        user_name = check_auth(login_data)

        if isinstance(user_name, User):
            login(request, user_name)
            return redirect('layout')

        else:
            errors['login'] = exit_message[user_name]
            return render(request, 'main/login.html', {'errors': errors})

    # Если метод не POST — отображаем страницу регистрации (пустая форма)
    return render(request, 'main/login.html')


# Проверка авторизации
def check_auth(login_data) -> int | str:
    pass_list = [False, False]
    name = None

    pass_list[0] = User.objects.filter(email=login_data['email']).exists() # noqa PyUnresolvedReferences

    if pass_list[0]:
        name = User.objects.get(email=login_data['email']) # noqa PyUnresolvedReferences
        pass_list[1] = check_password(login_data['password'], name.password)

    if not pass_list[0]:
        return 1
    elif not pass_list[1]:
        return 0
    else:
        return name


# Главная страница
def layout(request):
    return render(request, 'main/layout.html')


# Выход
def logout(request):
    return render(request, 'main/logout.html')


# def flower_list(request):
#     flowers = Flower.objects.all()
#     return render(request, 'flower_list.html', {'flowers': flowers})