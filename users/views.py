from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from .forms import (
    LoginForm,
    RegisterUserForm,
    ChangeUsernameForm,
    ChangePhoneForm,
    ChangePasswordForm,
)
from product.forms import SearchForm
from product.models import Basket
from .models import CustomUser

from django.http import HttpResponse


searchform = SearchForm()

menu = [
    {"title": "Главная страница", "url_name": "product:homepage"},
    {"title": "Корзина", "url_name": "product:basket"},
    {"title": "Контакты", "url_name": "product:contacts"},
]


# Create your views here.


class User_login(View):
    # авторизация пользователя
    template_name = "registration/login.html"
    message = ""  # сообщение о входе пользователя (удачно, удаленный аккаунт, неправильные данные)

    def get(self, request):
        loginform = LoginForm()
        context = {
            "menu": menu,
            "loginform": loginform,
            "searchform": searchform,
            "message": self.message,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            cd = loginform.cleaned_data  # данные в виде словаря
            user = authenticate(username=cd["username"], password=cd["password"])
            if user is not None:  # правильный
                if user.is_active:  # активный user
                    login(request, user)
                    self.message = "Успешный вход"
                    return redirect("product:homepage")
                else:
                    self.message = "удаленный аккаунт"
            else:
                self.message = "Неправильные данные"
        context = {
            "menu": menu,
            "loginform": loginform,
            "searchform": searchform,
            "message": self.message,
        }
        return render(request, self.template_name, context)


def user_logout(request):  # выход из авторизации
    logout(request)
    return redirect("product:homepage")


class Register(View):
    # регистрация пользователя
    template_name = "registration/register.html"

    def get(self, request):
        # выводим пустую форму регистрации
        registerform = RegisterUserForm()
        context = {"menu": menu, "registerform": registerform, "searchform": searchform}
        return render(request, self.template_name, context)

    def post(self, request):
        # обработка заполненной формы
        registerform = RegisterUserForm(data=request.POST)
        if registerform.is_valid():
            new_user = registerform.save()
            # выполнение входа и перенаправление на домашнюю страницу
            login(request, new_user)
            # создаем корзину для каждого нового пользователя
            basket = Basket.objects.create(user=new_user)
            return redirect("product:homepage")
        context = {"menu": menu, "registerform": registerform, "searchform": searchform}
        return render(request, self.template_name, context)


class Profile(View):
    template_name = "registration/profile.html"
    form_class1 = ChangeUsernameForm  # форма для изменения username
    form_class2 = ChangePhoneForm  # форма для изменения номера телефона
    form_class3 = ChangePasswordForm  # форма для изменения пароля
    message = ""  # сообщение для ошибки

    def get(self, request):
        user = request.user
        print(user.number_phone)
        changeusernameform = self.form_class1()
        change_phone_form = self.form_class2()
        change_password_form = self.form_class3()
        context = {
            "menu": menu,
            "searchform": searchform,
            "changeusernameform": changeusernameform,
            "change_phone_form": change_phone_form,
            "change_password_form": change_password_form,
            "message": self.message,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user = request.user
        changeusernameform = self.form_class1(request.POST)
        change_phone_form = self.form_class2(request.POST)
        change_password_form = self.form_class3(request.POST)
        if changeusernameform.is_valid():
            # если есть такой логин
            if len(CustomUser.objects.filter(username=request.POST["username"])) > 0:
                self.message = "Уже есть такой логин"
            else:
                customuser = CustomUser.objects.get(id=user.id)
                customuser.username = request.POST["username"]
                customuser.save(update_fields=["username"])
                return redirect(request.path)

        if change_phone_form.is_valid():
            customuser = CustomUser.objects.get(id=user.id)
            customuser.number_phone = request.POST["number_phone"]
            customuser.save(update_fields=["number_phone"])
            return redirect(request.path)

        if change_password_form.is_valid():
            pass

        context = {
            "menu": menu,
            "searchform": searchform,
            "changeusernameform": changeusernameform,
            "change_phone_form": change_phone_form,
            "change_password_form": change_password_form,
            "message": self.message,
        }
        return render(request, self.template_name, context)
