from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
	#создаем копию модели User
	number_phone = models.CharField(max_length=20) #обязательное поле

