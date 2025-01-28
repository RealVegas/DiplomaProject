from .models import User
from django.forms import ModelForm, TextInput, EmailInput, PasswordInput


class RegisterForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя пользователя', 'value': ''}),
            'email': EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите электронную почту', 'value': ''}),
            'password': PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль', 'value': ''})
        }