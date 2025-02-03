from django.urls import path
from . import views

urlpatterns = [
    path('', views.layout, name='layout'),
    path('flowers/', views.flowers, name='flowers'),
    path('bond/', views.bond, name='bond'),
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('orders/', views.view_orders, name='orders'),
    path('make_order/<str:posy_name>', views.make_order, name='make_order'),
    path('delete_order/<int:order_id>/', views.delete_order, name='delete_order')
]