from django.shortcuts import render
from .models import User, Flower, Order


# Create your views here.
def index(request):
    return render(request, 'main/index.html')


def register(request):
    return render(request, 'main/register.html')


def flower_list(request):
    flowers = Flower.objects.all()
    return render(request, 'flower_list.html', {'flowers': flowers})