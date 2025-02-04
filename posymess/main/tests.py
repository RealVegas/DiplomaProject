from django.test import TestCase
from .models import User, Order
from django.urls import reverse  # Для генерации URL по имени маршрута

# Тесты для регистрации пользователя
class RegistrationTestCase(TestCase):
    def test_registration_success(self):
        """
        Успешная регистрация нового пользователя.
        """
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        })
        # Проверяем HTTP-ответ: после успешной регистрации перенаправляет (302 Found)
        self.assertEqual(response.status_code, 302)
        # Проверяем, что пользователь был создан
        user_exists = User.objects.filter(username='testuser').exists()
        self.assertTrue(user_exists)

    def test_registration_failure_due_to_password_mismatch(self):
        """
        Провал регистрации, если пароли не совпадают.
        """
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'wrongpassword'
        })
        # Ожидается, что регистрация не пройдет (HTTP 200, т.к. форма возвращает ошибки)
        self.assertEqual(response.status_code, 200)
        # Пользователь НЕ должен быть создан
        user_exists = User.objects.filter(username='testuser').exists()
        self.assertFalse(user_exists)

    def test_registration_failure_due_to_short_password(self):
        """
        Провал регистрации из-за слишком короткого пароля.
        """
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': '123',
            'password2': '123'
        })
        # Ожидается, что форма выдаст ошибки (HTTP 200, возвращается страница с формой)
        self.assertEqual(response.status_code, 200)
        # Пользователь не должен быть создан
        user_exists = User.objects.filter(username='testuser').exists()
        self.assertFalse(user_exists)


# Тесты для авторизации пользователя
class LoginTestCase(TestCase):
    def setUp(self):
        """
        Создаем пользователя для тестов. Вызовется перед каждым тестом.
        """
        self.user = User.objects.create_user(username='testuser', password='testpassword123')

    def test_login_success(self):
        """
        Успешный вход с корректными данными.
        """
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword123'
        })
        # Ожидаем перенаправление после успешного входа
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_failure(self):
        """
        Неудачная попытка входа с неверными данными.
        """
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        # Проверяем, что остается на той же странице (HTTP 200)
        self.assertEqual(response.status_code, 200)
        # Пользователь НЕ должен быть аутентифицирован
        self.assertFalse(response.wsgi_request.user.is_authenticated)


# Тесты для создания заказа
class OrderCreationTestCase(TestCase):
    def setUp(self):
        """
        Создаем пользователя для тестов и логиним его.
        """
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.client.login(username='testuser', password='testpassword123')

    def test_order_creation_success(self):
        """
        Успешное создание заказа авторизованным пользователем.
        """
        response = self.client.post(reverse('order', args=['Roses Bouquet']))
        # Проверяем, что был редирект или успех (302)
        self.assertEqual(response.status_code, 302)
        # Проверяем, что заказ создан в базе
        order_exists = Order.objects.filter(user=self.user, posy_name='Roses Bouquet').exists()
        self.assertTrue(order_exists)

    def test_order_creation_failure_without_login(self):
        """
        Провал при попытке создания заказа неавторизованным пользователем.
        """
        self.client.logout()  # Выходим из аккаунта
        response = self.client.post(reverse('order', args=['Roses Bouquet']))
        # Нельзя создать заказ: возможно, будет редирект на страницу логина (302)
        self.assertEqual(response.status_code, 302)
        # Заказ не должен быть создан
        order_exists = Order.objects.filter(posy_name='Roses Bouquet').exists()
        self.assertFalse(order_exists)