from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import MedServiceUser
from django import forms

class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(label='Введите имя пользователя',
                               widget=forms.TextInput(
                                   attrs={
                                       'placeholder': 'Допускается 150 символов из набора: a-z / @ / . / + / - / _',
                                       'class': 'form-control',
                                   }
                               ))


    email = forms.EmailField(label='Введите email',
                             widget=forms.EmailInput(
                                 attrs={
                                     'class': 'form-control',
                                 }
                             ))


    password1 = forms.CharField(label='Введите пароль',
                                widget=forms.PasswordInput(attrs={'class': 'form-control', })
                                )


    password2 = forms.CharField(label='Повторите пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', })
                               )


    class Meta:
        model = MedServiceUser
        # 'password1', 'password2' позволяют хэшировать пароль и запрашивать его подтверждение
        fields = ('username', 'email', 'password1', 'password2')


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Введите имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))


    password = forms.CharField(label='Введите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = MedServiceUser
        fields = ('username', 'password1')
