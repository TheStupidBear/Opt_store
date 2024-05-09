from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm, RegisterUserForm
from django.http import HttpResponse




menu = [{'title': 'Главная страница', 'url_name': 'product:homepage' },
		{'title': 'Корзина', 'url_name': 'product:basket' },
		{'title': 'Контакты', 'url_name': 'product:contacts' }
]


# Create your views here.
def user_login(request): #авторизация пользователя
	message = ''  #сообщение о входе пользователя (удачно, удаленный аккаунт, неправильные данные)
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data #данные в виде словаря
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
		form = LoginForm()
	context = {'menu': menu, 'form':form, 'message': message}
	return render(request, 'registration/login.html', context)


def user_logout(request):  #выход из авторизации
	logout(request)
	return redirect('product:homepage')

def register(request):
	#регистрируем нового пользователя
	if request.method == 'POST':
		#обработка заполненной формы
		form = RegisterUserForm(data = request.POST)
		if form.is_valid():
			new_user = form.save()
			#выполнение входа и перенаправление на домашнюю страницу
			login(request, new_user)
			return redirect('product:homepage')
	else:
		#выводим пустую форму регистрации
		form = RegisterUserForm()
	context = {'menu': menu, 'form':form}
	return render(request, 'registration/register.html', context)
