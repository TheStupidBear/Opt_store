from django.urls import path
from . import views

app_name = 'product'
urlpatterns = [
	#домашняя страница с категориями товаров
	path('', views.homepage, name='homepage'),
	#страница с категориями товаров по выбранному направлению
	path('subdirection/<slug:direction_slug>/', views.subdirection, name='subdirection'),
	#страница с товарами по выбранному поднаправлению
	path('products/<slug:subdirection_slug>/', views.products, name='products'),
	#страница с описанием товара
	path('product/<slug:description_slug>/', views.product_description, name='product_description'),
	#корзина
	path('basket/', views.basket, name='basket'),
	#контакты
	path('contacts/', views.contacts, name='contacts'),
	#поиск
	path('search/', views.search, name='search'),
	
]