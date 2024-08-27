from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm, RegisterUserForm
from product.forms import SearchForm
from product.models import Basket

from django.http import HttpResponse


searchform = SearchForm()

menu = [{'title': 'Главная страница', 'url_name': 'product:homepage' },
		{'title': 'Корзина', 'url_name': 'product:basket' },
		{'title': 'Контакты', 'url_name': 'product:contacts' }
]


# Create your views here.
def user_login(request): #авторизация пользователя
	message = ''  #сообщение о входе пользователя (удачно, удаленный аккаунт, неправильные данные)
	if request.method == 'POST':
		loginform = LoginForm(request.POST)
		if loginform.is_valid():
			cd = loginform.cleaned_data #данные в виде словаря
			user = authenticate(username = cd['username'], password = cd['password'])
			if user is not None: #правильный
				if user.is_active: #активный user
					login(request, user)
					message = 'Успешный вход'
					return redirect('product:homepage')
				else:
					message = 'удаленный аккаунт'
			else:
				message = 'Неправильные данные'
	else:
		loginform = LoginForm()
	context = {'menu': menu, 'loginform':loginform, 'searchform':searchform, 'message': message}
	return render(request, 'registration/login.html', context)


def user_logout(request):  #выход из авторизации
	logout(request)
	return redirect('product:homepage')

def register(request):
	#регистрируем нового пользователя
	if request.method == 'POST':
		#обработка заполненной формы
		registerform = RegisterUserForm(data = request.POST)
		if registerform.is_valid():
			new_user = registerform.save()
			#выполнение входа и перенаправление на домашнюю страницу
			login(request, new_user)
			#создаем корзину для каждого нового пользователя
			basket = Basket.objects.create(user = new_user)
			return redirect('product:homepage')
	else:
		#выводим пустую форму регистрации
		registerform = RegisterUserForm()
	context = {'menu': menu, 'registerform':registerform, 'searchform':searchform}
	return render(request, 'registration/register.html', context)
