from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class User(AbstractUser):
    email = models.EmailField('Электронная почта', max_length=100, unique=True, null=False)
    username = models.CharField('Имя пользователя', max_length=100, unique=False, null=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email


class Flower(models.Model):
    posyname: str = models.CharField('Название букета', max_length=50, unique=True, null=False)
    price: float = models.DecimalField('Цена', max_digits=10, decimal_places=2)

    def __str__(self):
        return self.posyname

    class Meta:
        verbose_name = 'Букет'
        verbose_name_plural = 'Букеты'


class Order(models.Model):
    user: str = models.ForeignKey(User, on_delete=models.CASCADE)
    flower: str = models.ForeignKey(Flower, on_delete=models.CASCADE)
    order_date: str = models.DateTimeField('Дата заказа', auto_now_add=True)

    def __str__(self):
        return f'Заказ №{self.id} от {self.user.email} букет {self.flower.posyname}' # noqa UnresolvedReference

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'