from django.urls import path
from . import views

urlpatterns = [
    path('', views.layout, name='layout'),
    path('flowers/', views.flowers, name='flowers'),
    path('bond/', views.bond, name='bond'),
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('order/<str:posy_name>', views.new_order, name='order'),
    path('orders/', views.orders_list, name='orders')
]