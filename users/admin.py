from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "number_phone")  # список отображаемых полей
    list_display_links = (
        "id",
        "username",
    )  # список полей в виде ссылки для перехода к конкретной записи
    search_fields = ["username"]  # определяет поля, по которым будет производится поиск


# Register your models here.
admin.site.register(CustomUser, CustomUserAdmin)
