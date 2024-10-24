from django.urls import path
from . import views
from .views import (
    HomepageView,
    SubDirectionView,
    ProductsView,
    ProductDesView,
    SearchView,
    ContactView,
    BasketView,
    GetBasketItemInfoView,
)


app_name = "product"
urlpatterns = [
    # домашняя страница с категориями товаров
    path("", HomepageView.as_view(), name="homepage"),
    # страница с категориями товаров по выбранному направлению
    path(
        "subdirection/<slug:direction_slug>/",
        SubDirectionView.as_view(),
        name="subdirection",
    ),
    # страница с товарами по выбранному поднаправлению
    path("products/<slug:subdirection_slug>/", ProductsView.as_view(), name="products"),
    # страница с описанием товара
    path(
        "product/<slug:description_slug>/",
        ProductDesView.as_view(),
        name="product_description",
    ),
    # корзина
    path("basket/", BasketView.as_view(), name="basket"),
    # удалить из корзины
    path("basket/<int:basketitem_id>/", BasketView.as_view(), name="basketdelete"),
    # изменить количество в корзине
    path("basket/<int:basketitem_id>/", BasketView.as_view(), name="basketchange"),
    # контакты
    path("contacts/", ContactView.as_view(), name="contacts"),
    # поиск
    path("search/", SearchView.as_view(), name="search"),
    # информация о корзине
    path("basketinfo/", GetBasketItemInfoView.as_view(), name="basketinfo"),
]
