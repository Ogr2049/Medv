from django import forms

from .models import *

class UserSigninForm(forms.Form):
    username = forms.CharField(label='Имя пользователя',)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(),)

class UserSignupForm(forms.Form):
    username = forms.CharField(label='Имя пользователя',)
    name = forms.CharField(label='Имя',)
    surname = forms.CharField(label='Фамилия',)
    email = forms.EmailField(label='Почта')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(),)
    password_confirm = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(),)

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'image')