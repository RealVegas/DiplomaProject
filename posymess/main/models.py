from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class User(AbstractUser, models.Model):
    username: str = models.CharField('Имя пользователя', max_length=50, unique=True, null=False)
    email: str = models.EmailField('Электронная почта', max_length=120, unique=True, null=False)
    password: str = models.CharField('Пароль', max_length=200, null=False)
    is_active: bool = models.BooleanField('Активен', default=True)
    is_staff: bool = models.BooleanField('Доступ к админ панели', default=False)
    last_login = models.DateTimeField('Последний вход', auto_now_add=True, null=True, blank=True)

    objects = UserManager()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Flower(models.Model):
    posyname: str = models.CharField('Название букета', max_length=50, unique=True, null=False)
    price: float = models.DecimalField('Цена', max_digits=10, decimal_places=2)

    def __str__(self):
        return self.posy_name

    class Meta:
        verbose_name = 'Букет'
        verbose_name_plural = 'Букеты'


class Order(models.Model):
    user: str = models.ForeignKey(User, on_delete=models.CASCADE)
    flower: str = models.ForeignKey(Flower, on_delete=models.CASCADE)
    order_date: str = models.DateTimeField('Дата заказа', auto_now_add=True)

    def __str__(self):
        return f'Заказ №{self.id} от {self.user.user_name} букет {self.flower.posy_name}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'