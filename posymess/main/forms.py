import re
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password
from .models import User


class RegisterForm:

    def __init__(self, raw_data: dict[str, str] | None = None) -> None:
        self.raw_data: dict[str, str] = raw_data
        self.clean_data: dict[str, str] = {}
        self.errors: dict[str, str] = {}

        self.user_name: str = self.raw_data.get('user_name', '')
        self.email: str = self.raw_data.get('email', '')
        self.password: str = self.raw_data.get('password', '')
        self.confirm_password: str = self.raw_data.get('confirm_password', '')

    def clean_raw(self) -> None:
        self.clean_data['user_name'] = clean_name(self.user_name)
        self.clean_data['email'] = clean_email(self.email)
        self.clean_data['password'] = clean_password(self.password, self.confirm_password)

    def verify_data(self) -> list[bool]:
        wrong_list: list[bool] = [False, False, False]

        wrong_list[0] = not self.clean_data['user_name']
        wrong_list[1] = not self.clean_data['email']
        wrong_list[2] = self.clean_data['password'].startswith('Пароль')

        return wrong_list

    def pass_data(self, error_list: list[bool]) -> dict[str, str]:

        if error_list[0]:
            self.errors['user_name'] = 'Некорректное имя пользователя, используйте только буквы'
        if error_list[1]:
            self.errors['email'] = 'Некорректный адрес электронной почты'
        if error_list[2]:
            self.errors['password'] = self.clean_data['password']

        if self.errors:
            return self.errors
        else:
            return self.clean_data

    def not_valid(self):
        self.clean_raw()
        return any(self.verify_data())


class LoginForm:

    def __init__(self, raw_data: dict[str, str] | None = None) -> None:
        self.raw_data: dict[str, str] = raw_data
        self.clean_data: dict[str, str] = {}
        self.errors: dict[str, str] = {}
        self.email: str = self.raw_data.get('email', '')
        self.password: str = self.raw_data.get('password', '')

    def clean_raw(self) -> None:
        self.clean_data['email'] = clean_email(self.email)
        self.clean_data['password'] = self.password

    def verify_data(self) -> list[bool]:
        wrong_list: list[bool] = [False, False]

        wrong_list[0] = not self.clean_data['email']
        wrong_list[1] = len(self.password) < 3

        return wrong_list

    def pass_data(self, error_list: list[bool]) -> None | dict[str, str] | bool:

        if error_list[0]:
            self.errors['email'] = 'Некорректный адрес электронной почты'
        if error_list[1]:
            self.errors['password'] = 'Пароль должен содержать не менее 3 символов'

        if self.errors:
            return self.errors
        else:
            return self.clean_data

    def not_valid(self):
        self.clean_raw()
        return any(self.verify_data())





































# Проверка имени пользователя
def clean_name(some_name: str) -> str | None:
    if not some_name:
        return None

    new_name: str = re.sub(r'[^а-яёА-ЯЁa-zA-Z ]', '', some_name)
    new_name: str = re.sub(r'\s+', ' ', new_name).strip()

    return new_name or None


# Проверка электронной почты
def clean_email(some_email: str) -> str | None:
    if not some_email:
        return None

    check_email = re.match(r'^[a-zA-Z][a-zA-Z0-9_.+-]*[a-zA-Z0-9]@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$', some_email)

    return some_email if check_email else None


# Проверка пароля
def clean_password(some_password: str, some_confirm: str) -> str:
    if len(some_password) < 3:
        return 'Пароль должен содержать не менее 3 символов'

    if some_password == some_confirm:
        return make_password(some_password)
    else:
        return 'Пароль не прошел проверку: введенные пароли не совпадают'


# Создание нового пользователя в БД
def add_user(reg_data: dict[str, str]) -> User | str:
    try:
        # noinspection PyUnresolvedReferences
        user = User.objects.create(
                user_name=reg_data['user_name'],
                email=reg_data['email'],
                password=reg_data['password'],
        )
        return user

    except IntegrityError:
        return 'Ошибка создания пользователя. Попробуйте еще раз'











# user_name = forms.CharField(max_length=50, required=True, label='Имя пользователя')
# email = forms.EmailField(max_length=120, required=True, label='Электронная почта')
# password = forms.CharField(widget=forms.PasswordInput, required=True, label='Пароль', min_length=3)
# confirm_password = forms.CharField(widget=forms.PasswordInput, required=True, label='Подтвердите пароль')
#
# def clean(self) -> dict[str, str]:
#     cleaned_data = super().clean()
#
#     user_name = cleaned_data.get('user_name')
#     email = cleaned_data.get('email')
#     password = cleaned_data.get('password')
#     confirm_password = cleaned_data.get('confirm_password')
#
#     if password != confirm_password:
#         raise forms.ValidationError('Пароли не совпадают.')
#     else:
#         cleaned_data['password'] = make_password(password)
#
#     return cleaned_data

# def __init__(self, raw_data: dict | None = None) -> None:
#     self.raw_data = raw_data or {}
#     self.errors = {}
#     self.cleaned_data = {}
#
# def validation(self):
#     username = self.raw_data.get('username', '')
#     email = self.raw_data.get('email', '')
#     password = self.raw_data.get('password', '')
#     password_confirm = self.raw_data.get('password_confirm', '')
#
#     if not username:
#         self.errors['username'] = 'Имя пользователя обязательно.'
#     elif len(username) < 3:
#         self.errors['username'] = 'Имя пользователя должно содержать минимум 3 символа.'
#
#     if not email:
#         self.errors['email'] = 'Электронная почта обязательна.'
#     elif forms.EmailAddressField().clean(email).errors():
#         self.errors['email'] = 'Электронная почта должна содержать минимум 3 символа.'
#
#     if not password:
#         self.errors['password'] = 'Пароль обязателен.'
#     elif len(password) < 3:
#         self.errors['password'] = 'Пароль должен содержать не менее 3 символов.'
#
#     if password != password_confirm:
#         self.errors['password_confirm'] = 'Пароли не совпадают.'
#
#     # Если нет ошибок, сохранить данные в cleaned_data
#     if not self.errors:
#         self.cleaned_data['username'] = username
#         self.cleaned_data['password'] = make_password(password)
#         return True
#
#     return False