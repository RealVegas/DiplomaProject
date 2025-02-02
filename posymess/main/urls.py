from django.urls import path
from . import views

urlpatterns = [
    path('', views.layout, name='layout'),
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]


#http://127.0.0.1:8000/register/
#http://127.0.0.1:8000/login/


    # path('flowers/', views.flower_list, name='flower_list')