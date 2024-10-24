from django.contrib import admin
from .models import Direction, SubDirection, Description, Basket, BasketItem, DesImage

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
	list_display = ('id', 'name') #список отображаемых полей
	list_display_links = ('id', 'name') #список полей в виде ссылки для перехода к конкретной записи
	search_fields = ['name'] #определяет поля, по которым будет производится поиск
	prepopulated_fields = {'slug': ('name',)} #автоматический slug по названию модели

class DesImageAdmin(admin.ModelAdmin):
	list_display = ('id', 'product', 'image') #список отображаемых полей
	search_fields = ['product'] #определяет поля, по которым будет производится поиск

class BasketAdmin(admin.ModelAdmin):
	list_display = ('id', 'user') #список отображаемых полей
	search_fields = ['user'] #определяет поля, по которым будет производится поиск
	

class BasketItemAdmin(admin.ModelAdmin):
	list_display = ('id', 'basket', 'product', 'quantity') #список отображаемых полей
	search_fields = ['basket'] #определяет поля, по которым будет производится поиск

# Register your models here.
admin.site.register(Direction, DirectionAdmin)
admin.site.register(SubDirection, SubDirectionAdmin)
admin.site.register(Description, DescriptionAdmin)
admin.site.register(Basket, BasketAdmin)
admin.site.register(BasketItem, BasketItemAdmin)
admin.site.register(DesImage, DesImageAdmin)

