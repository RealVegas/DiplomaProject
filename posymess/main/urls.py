from django.urls import path
from . import views

urlpatterns = [
    path('', views.layout, name='layout'),
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout, name='logout'),

    # path('flowers/', views.flower_list, name='flower_list')
]