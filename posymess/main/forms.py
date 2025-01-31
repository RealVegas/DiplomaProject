from django import forms
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from .models import User


class RegisterForm(forms.ModelForm):
    # user_name: str = models.CharField(label='Имя пользователя', max_length=50)
    # email: str = models.EmailField(label='Электронная почта', max_length=120)
    # password: str = models.CharField(label='Пароль', widget=forms.PasswordInput)
    #confirm_password: str = models.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['user_name', 'email', 'password']

        widgets = {
            'user_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя пользователя'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите e-mail'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}),
            'confirm_password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтвердите пароль'})
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise ValidationError('Пароли не совпадают')

        if password:
            cleaned_data['password'] = make_password(password)
        else:
            raise ValueError('Пароль не может быть пустым')

        return cleaned_data