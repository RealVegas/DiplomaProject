import re
from django.contrib.auth.hashers import check_password
from .models import User


class RegisterForm:

    def __init__(self, raw_data: dict[str, str] | None = None) -> None:
        self.raw_data: dict[str, str] = raw_data
        self.clean_data: dict[str, str] = {}
        self.errors: list[str] = []

        self.username: str = self.raw_data.get('username', '')
        self.email: str = self.raw_data.get('email', '')
        self.password: str = self.raw_data.get('password', '')
        self.confirm_password: str = self.raw_data.get('confirm_password', '')

    def clean_raw(self) -> None:
        self.clean_data['username'] = clean_name(self.username)
        self.clean_data['email'] = clean_email(self.email)
        self.clean_data['password'] = clean_password(self.password, self.confirm_password)

    def verify_data(self) -> list[bool]:
        wrong_list: list[bool] = [False, False, False]

        wrong_list[0] = not self.clean_data['username']
        wrong_list[1] = not self.clean_data['email']
        wrong_list[2] = self.clean_data['password'].startswith('Пароль')

        return wrong_list

    def get_errors(self) -> list[str]:
        found_errors = self.verify_data()

        if found_errors[0]:
            self.errors.append('Некорректное имя пользователя, используйте только буквы')
        if found_errors[1]:
            self.errors.append('Некорректный адрес электронной почты')
        if found_errors[2]:
            self.errors.append(self.clean_data['password'])

        return self.errors

    def pass_data(self) -> dict[str, str]:
        return self.clean_data

    def not_valid(self) -> bool:
        self.clean_raw()
        return any(self.verify_data())


class LoginForm:

    def __init__(self, raw_data: dict[str, str] | None = None) -> None:
        self.raw_data: dict[str, str] = raw_data
        self.clean_data: dict[str, str] = {}
        self.errors: list[str] = []
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

    def get_errors(self) -> list[str]:
        found_errors = self.verify_data()

        if found_errors[0]:
            self.errors.append('Некорректный адрес электронной почты')
        if found_errors[1]:
            self.errors.append('Пароль должен содержать не менее 3 символов')

        return self.errors

    def pass_data(self) -> dict[str, str]:
        return self.clean_data

    def not_valid(self) -> bool:
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
        return some_password
    else:
        return 'Пароль не прошел проверку: введенные пароли не совпадают'


# Создание нового пользователя в БД
def add_user(reg_data: dict[str, str]) -> User | str:
    try:
        user = User(
                username=reg_data['username'],
                email=reg_data['email']
        )
        user.set_password(reg_data['password'])

        user.save()
        return user

    except Exception as err:
        return f'Ошибка: {str(err)}'


# Проверка авторизации
def check_auth(log_data) -> int | User:
    pass_list = [False, False]
    current_user = None

    pass_list[0] = User.objects.filter(email=log_data['email']).exists() # noqa PyUnresolvedReferences

    if pass_list[0]:
        current_user = User.objects.get(email=log_data['email']) # noqa PyUnresolvedReferences
        pass_list[1] = check_password(log_data['password'], current_user.password)

    if not pass_list[0]:
        return 1
    elif not pass_list[1]:
        return 0
    else:
        return current_user