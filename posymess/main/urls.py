from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('flowers/', views.flower_list, name='flower_list')
]