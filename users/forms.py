from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class LoginForm(forms.Form):
    # форма для входа
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterUserForm(UserCreationForm):
    # форма для регистрации
    # email = forms.EmailField()
    number_phone = forms.CharField(label="Номер телефона", max_length=20)

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ("username", "number_phone", "password1", "password2")


class ChangeUsernameForm(forms.Form):
    # форма для изменения username
    username = forms.CharField(max_length=20, label="")


class ChangePhoneForm(forms.Form):
    # форма для изменения номера телефона
    number_phone = forms.IntegerField(label="", max_value=100000000, min_value=1)


class ChangePasswordForm(forms.Form):
    # форма для изменения пароля
    old_password = forms.CharField(label="Старый пароль:", max_length=20)
    new_password1 = forms.CharField(label="Новый пароль:", max_length=20)
    new_password2 = forms.CharField(label="Новый пароль повторно:", max_length=20)
