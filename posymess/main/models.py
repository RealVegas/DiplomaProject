from django.db import models


class User(models.Model):
    user_name: str = models.CharField('Имя пользователя', max_length=50, unique=False, null=False)
    email: str = models.EmailField('Электронная почта', max_length=120, unique=True, null=False)
    password: str = models.CharField('Пароль', max_length=200, null=False)
    last_login = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.user_name

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Flower(models.Model):
    posy_name: str = models.CharField('Название букета', max_length=50, unique=True, null=False)
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