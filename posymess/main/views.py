from django.shortcuts import render
from .models import User, Flower, Order


# Create your views here.
def index(request):
    return render(request, 'main/index.html')


# Регистрация
def register(request):
    error = ''
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            error = 'Неверные данные'
    return render(request, 'main/register.html', {'form': form, 'error': error})


def flower_list(request):
    flowers = Flower.objects.all()
    return render(request, 'flower_list.html', {'flowers': flowers})