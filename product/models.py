from django.db import models
from django.urls import reverse
from django.conf import settings

# Create your models here.


class Direction(models.Model):
    # направление товара
    # класс для admin панели
    class Meta:
        verbose_name = "Направление товаров"  # изменяет название модели в admin панели
        verbose_name_plural = "Направления товаров"

    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="images/direction")  # фото направления
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        # возвращает строковое представление модели
        return self.name

    def get_absolute_url(self):
        return reverse("product:subdirection", kwargs={"direction_slug": self.slug})


class SubDirection(models.Model):
    # поднаправление товара
    # класс для admin панели
    class Meta:
        verbose_name = (
            "Поднаправление товаров"  # изменяет название модели в admin панели
        )
        verbose_name_plural = "Поднаправления товаров"

    direction = models.ForeignKey(
        Direction, on_delete=models.CASCADE
    )  # связывается с конкретной темой
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="images/subdirection")  # фото поднаправления
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        # возвращает строковое представление модели
        return self.name

    def get_absolute_url(self):
        return reverse("product:products", kwargs={"subdirection_slug": self.slug})


class Description(models.Model):
    # описание товара
    # класс для admin панели
    class Meta:
        verbose_name = "Описание товара"  # изменяет название модели в admin панели
        verbose_name_plural = "Описания товара"

    subdirection = models.ForeignKey(
        SubDirection, on_delete=models.CASCADE
    )  # связывается с конкретной темой
    name = models.CharField(max_length=200)  # название продукта
    text = models.TextField()  # описание продукта
    main_image = models.ImageField(upload_to="images/products")  # главное фото
    date_added = models.DateTimeField(
        auto_now_add=True
    )  # записывает время в момент публикации
    price = models.PositiveIntegerField()  # цена продукта
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            "product:product_description", kwargs={"description_slug": self.slug}
        )


class DesImage(models.Model):
    product = models.ForeignKey(Description, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/products")  # фотки продукта


class Basket(models.Model):
    # модель корзины, связанная с пользователем, и имеющая дату её создания
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # отношение один к одному. У одного пользователя одна корзина
    created_at = models.DateTimeField(auto_now_add=True)
    # дата создания автоматически выставляется в момент создания


class BasketItem(models.Model):
    # модель товара для корзины, имеющяя какое-то количество товаров (по умолчанию = 1)
    basket = models.ForeignKey(
        Basket, on_delete=models.CASCADE, related_name="basketitem"
    )
    product = models.ForeignKey(Description, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return "%s: %s" % (self.product, self.quantity)


class Comment(models.Model):
    # комментарии к товарам
    product = models.ForeignKey(Description, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        if len(self.text) > 50:
            return f"{self.text[:50]}..."
        else:
            return f"{self.text[:50]}"
