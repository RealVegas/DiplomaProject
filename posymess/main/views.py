from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.http import HttpResponse


# Регистрация
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # return redirect('login')
            return HttpResponse("Регистрация прошла успешно! Вы можете войти.")
        else:
            return render(request, 'main/register.html', {'form': form})
    else:
        form = RegisterForm()
        return render(request, 'main/register.html', {'form': form})


# Главная страница
def layout(request):
    return render(request, 'main/layout.html')


# Выход
def logout(request):
    return render(request, 'main/layout.html')


# Вход
def login(request):
    return render(request, 'main/login.html')


def flower_list(request):
    flowers = Flower.objects.all()
    return render(request, 'flower_list.html', {'flowers': flowers})