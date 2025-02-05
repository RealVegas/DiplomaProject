from django.test import TestCase
from .models import User, Flower, Order
from django.urls import reverse  # Для генерации URL по имени маршрута
from decimal import Decimal


# Тесты для регистрации пользователя
class RegistrationTestCase(TestCase):
    def test_registration_success(self):
        """
        Успешная регистрация нового пользователя.
        """
        print('Тесты регистрации:')
        print('1. Успешная регистрация нового пользователя')
        print('2. Провал регистрации в случае несовпадения паролей')
        print('3. Провал регистрации из-за слишком короткого пароля\n')
        print('Тесты авторизации:')
        print('1. Успешный вход в аккаунт')
        print('2. Провал авторизации в случае неверных данных\n')
        print('Тесты создания заказа:')
        print('1. Создание заказа авторизованным пользователем\n')
        print('Тестировать провал создания заказа неавторизованным пользователем не требуется\n'
              'потому, что неавторизованный пользователь не имеет возможности создавать заказы')

        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'confirm_password': 'testpassword'
        })

        # Проверяем HTTP-ответ: после успешной регистрации не перенаправляет (200 Found)
        self.assertEqual(response.status_code, 200)

        # Проверяем, что пользователь был создан
        email_exists = User.objects.filter(email='testuser@example.com').exists()
        self.assertTrue(email_exists)

        # Проверяем, что сообщение об успешной регистрации присутствует в контексте
        test_message = 'Вы успешно зарегистрировались в Posy message, воспользуйтесь кнопкой Вход чтобы войти в аккаунт'
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], test_message)

    def test_registration_failure_due_to_password_mismatch(self):
        """
        Провал регистрации, если пароли не совпадают.
        """
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword123',
            'confirm_password': 'wrongpassword'
        })

        # Ожидается, что регистрация не пройдет (HTTP 200, т.к. форма возвращает ошибки)
        self.assertEqual(response.status_code, 200)

        # Пользователь НЕ должен быть создан
        email_exists = User.objects.filter(email='testuser@example.com').exists()
        self.assertFalse(email_exists)

    def test_registration_failure_due_to_short_password(self):
        """
        Провал регистрации из-за слишком короткого пароля.
        """
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': '12',
            'confirm_password': '12'
        })

        # Ожидается, что форма выдаст ошибки (HTTP 200, возвращается страница с формой)
        self.assertEqual(response.status_code, 200)

        # Пользователь не должен быть создан
        email_exists = User.objects.filter(email='testuser@example.com').exists()
        self.assertFalse(email_exists)


# Тесты для авторизации пользователя
class LoginTestCase(TestCase):
    def setUp(self):
        """
        Создаем пользователя для тестов. Вызовется перед каждым тестом.
        """
        self.user = User.objects.create_user(
                username='testuser',
                email='testuser@example.com',
                password='testpassword123'
        )

    def test_login_success(self):
        """
        Успешный вход с корректными данными.
        """
        response = self.client.post(reverse('login'), {
            'email': 'testuser@example.com',
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
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        })

        # Проверяем, что остается на той же странице (HTTP 200)
        self.assertEqual(response.status_code, 200)

        # Пользователь НЕ должен быть аутентифицирован
        self.assertFalse(response.wsgi_request.user.is_authenticated)


# # Тесты для создания заказа
class OrderCreationTestCase(TestCase):
    def setUp(self):
        """
        Создаем пользователя и цветок для тестов
        Авторизуем пользователя

        """
        self.user = User.objects.create_user(
                username='vasya',
                email='vasya@mail.ru',
                password='password123'
        )

        self.flower = Flower.objects.create( # noqa PyUnresolvedReferences
                posy_name='Желтые розы',
                price=1700.00,
                posy_path='main/img/posies/small_04.png'
        )

    def test_order_creation_success(self):
        """
        Успешное создание заказа авторизованным пользователем.
        """
        self.client.login(email='testuser@example.com', password='testpassword123')

        test_user = User.objects.get(email='vasya@mail.ru')
        test_posy = self.flower
        test_price = Decimal(test_posy.price)

        test_order = Order.objects.create(user=test_user, flower=test_posy, order_price=test_price) # noqa PyUnresolvedReferences
        # Проверяем, что объект заказа создан корректно
        self.assertIsInstance(test_order, Order)  # Убеждаемся, что объект — это Order
        self.assertEqual(test_order.user, test_user)  # Проверяем пользователя
        self.assertEqual(test_order.flower, test_posy)  # Проверяем объект букета
        self.assertEqual(test_order.order_price, test_price)  # Проверяем цену заказа