from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class LoginForm(forms.Form):
	#форма для входа
	username = forms.CharField(max_length = 20)
	password = forms.CharField(widget = forms.PasswordInput)

class RegisterUserForm(UserCreationForm):
	#форма для регистрации
	#email = forms.EmailField()
	number_phone = forms.CharField(label='Номер телефона', max_length=20)
	class Meta(UserCreationForm):
		model = CustomUser
		fields = ('username', 'number_phone', 'password1', 'password2')

# class ChangeUserForm(UserChangeForm):
# 	#форма для изменения логина или пароля
#     class Meta:
#         model = CustomUser
#         fields = ('username', 'email')
	
