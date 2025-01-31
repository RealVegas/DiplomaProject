from django.urls import path
from . import views

urlpatterns = [
    path('', views.layout, name='layout'),

    path('logout/', views.logout, name='logout'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),


    # path('flowers/', views.flower_list, name='flower_list')
]