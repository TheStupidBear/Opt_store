from django.urls import path, include
from . import views

app_name = 'users'
urlpatterns = [
	#страница входа пользователя
	path('login/', views.user_login, name='login'),
	path('logout/', views.user_logout, name='logout'),
	path('register/', views.register, name='register'),
]