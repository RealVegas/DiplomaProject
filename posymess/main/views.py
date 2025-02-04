from typing import Union

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Flower, Order
from .forms import RegisterForm, LoginForm
from .forms import add_user, check_auth


# Главная страница
def layout(request):
    # Данные букетов
    flowers_data = [
        {'posy_name': 'Ландыши', 'price': 2000, 'posy_path': 'main/img/posies/small_01.png'},
        {'posy_name': 'Красные и белые розы', 'price': 3500, 'posy_path': 'main/img/posies/small_02.png'},
        {'posy_name': 'Фиолетовый букет из роз и хризантем', 'price': 4000, 'posy_path': 'main/img/posies/small_03.png'},
        {'posy_name': 'Желтые розы', 'price': 1700.00, 'posy_path': 'main/img/posies/small_04.png'},
        {'posy_name': 'Розовые розы, нарциссы и сирень', 'price': 2500.00, 'posy_path': 'main/img/posies/small_05.png'},
        {'posy_name': 'Желтые тюльпаны', 'price': 3000.00, 'posy_path': 'main/img/posies/small_06.png'},
        {'posy_name': 'Герберы и розы', 'price': 2700.00, 'posy_path': 'main/img/posies/small_07.png'},
        {'posy_name': 'Желтые розы и хризантемы Бакарди', 'price': 3400.00, 'posy_path': 'main/img/posies/small_08.png'},
    ]

    # Добавление данных в таблицу
    for num, flower in enumerate(flowers_data):
        Flower.objects.get_or_create( # noqa PyUnresolvedReferences
                posy_name=flower["posy_name"],
                defaults={"price": flower["price"], "posy_path": flower["posy_path"]}
        )

    return render(request, 'layout.html')


# Заказ букетов
def flowers(request):
    initial: dict = {'pri_active': 'active'}
    posies: list = Flower.objects.all() # noqa PyUnresolvedReferences

    settings: dict = {**initial, 'posies': posies}
    return render(request, 'flowers.html', context=settings)


# Кнопка заказать
@login_required
def make_order(request, posy_name):
    posy = get_object_or_404(Flower, posy_name=posy_name)
    price = posy.price
    active = request.user

    order = Order.objects.create(user=active, flower=posy, order_price = price) # noqa PyUnresolvedReferences
    return redirect('orders')


# Удаление заказа
@login_required
def delete_order(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        order.delete()
    return redirect('orders')


# Список заказов
@login_required
def view_orders(request):
    user_orders = Order.objects.filter(user=request.user)
    amount_price = sum(order.order_price for order in user_orders)
    return render(request, 'orders.html', {'orders': user_orders, 'amount': amount_price})


# Контакты
def bond(request):
    settings = {'sec_active': 'active'}
    return render(request, 'bond.html', context=settings)


# Регистрация
def user_register(request) -> render:
    errors = []

    if request.method == 'POST':
        register_form = RegisterForm(request.POST)

        if register_form.not_valid():
            errors = register_form.get_errors()
            print(errors)
            return render(request, 'register.html', {'errors': errors})

        reg_data = register_form.pass_data()

        if User.objects.filter(email=reg_data['email']).exists(): # noqa PyUnresolvedReferences
            errors.append('Пользователь с таким email уже существует')
            return render(request, 'register.html', {'errors': errors})

        answer = add_user(reg_data)

        if isinstance(answer, str):
            errors.append(answer)
            return render(request, 'register.html', {'errors': errors})
        else:
            message = 'Вы успешно зарегистрировались в Posy message, воспользуйтесь кнопкой Вход чтобы войти в аккаунт'
            return render(request, 'register.html', {'message': message})

    # Если метод не POST — отображаем страницу регистрации (пустая форма)
    return render(request, 'register.html')


# Авторизация
def user_login(request) -> Union[render, redirect]:
    errors: list[str] = []
    exit_message = ['Неверный пароль', 'Такая почта еще не зарегистрирована']

    if request.method == 'POST':
        login_form = LoginForm(request.POST)

        if login_form.not_valid():
            errors = login_form.get_errors()
            return render(request, 'login.html', {'errors': errors})

        login_data = login_form.pass_data()

        mail = check_auth(login_data)

        if isinstance(mail, User):
            user_mail = authenticate(request, username=mail, password=login_data['password'])
            login(request, user_mail)
            return redirect('flowers')

        else:
            errors.append(exit_message[mail])
            return render(request, 'login.html', {'errors': errors})

    # Если метод не POST — отображаем страницу регистрации (пустая форма)
    return render(request, 'login.html')


# Выход
@login_required
def user_logout(request) -> redirect:
    logout(request)
    return redirect('login')