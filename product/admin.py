from django.contrib import admin
from .models import Direction, SubDirection, Description, Basket, BasketItem

class DirectionAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'image') #список отображаемых полей
	list_display_links = ('id', 'name') #список полей в виде ссылки для перехода к конкретной записи
	search_fields = ['name'] #определяет поля, по которым будет производится поиск
	prepopulated_fields = {'slug': ('name',)} #автоматический slug по названию модели

class SubDirectionAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'image') #список отображаемых полей
	list_display_links = ('id', 'name') #список полей в виде ссылки для перехода к конкретной записи
	search_fields = ['name'] #определяет поля, по которым будет производится поиск
	prepopulated_fields = {'slug': ('name',)} #автоматический slug по названию модели

class DescriptionAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'image') #список отображаемых полей
	list_display_links = ('id', 'name') #список полей в виде ссылки для перехода к конкретной записи
	search_fields = ['name'] #определяет поля, по которым будет производится поиск
	prepopulated_fields = {'slug': ('name',)} #автоматический slug по названию модели

# Register your models here.
admin.site.register(Direction, DirectionAdmin)
admin.site.register(SubDirection, SubDirectionAdmin)
admin.site.register(Description, DescriptionAdmin)
admin.site.register(Basket)
admin.site.register(BasketItem)

