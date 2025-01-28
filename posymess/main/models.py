from django.db import models

# id: int = db.Column(db.Integer, primary_key=True)
# username: str = db.Column(db.String(20), unique=True, nullable=False)
# email: str = db.Column(db.String(120), unique=True, nullable=False)
# password: str = db.Column(db.String(60), nullable=False)


class User(models.Model):
    username: str = models.CharField('Имя пользователя', max_length=50, unique=True, null=False)
    email: str = models.EmailField('Электронная почта', max_length=120, unique=True, null=False)
    password: str = models.CharField('Пароль', max_length=60, null=False)

    def __str__(self):
        return self.username

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
        return f'Заказ №{self.id} от {self.user.username} букет {self.flower.posy_name}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'