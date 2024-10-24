from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Direction, SubDirection, Description, BasketItem, Basket, DesImage
from .forms import (
    SearchForm,
    AddBasketForm,
    CommentForm,
    DeleteBasketForm,
    ChangeQuantityBasketForm,
)
from users.models import CustomUser
from django.core.paginator import Paginator
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import BasketSerializer, BasketItemSerializer

menu = [
    {"title": "Главная страница", "url_name": "product:homepage"},
    {"title": "Корзина", "url_name": "product:basket"},
    {"title": "Контакты", "url_name": "product:contacts"},
]

searchform = SearchForm()

# Create your views here.


class HomepageView(View):
    template_name = "product/homepage.html"

    def get(self, request):
        # домашняя страница с категориями товаров
        directions = Direction.objects.all()
        # получение числа визитов (сессии)
        num_visits = request.session.get("num_visits", 0)
        request.session["num_visits"] = num_visits + 1
        context = {
            "menu": menu,
            "searchform": searchform,
            "directions": directions,
            "num_visits": num_visits,
        }
        return render(request, self.template_name, context)


class SubDirectionView(View):
    template_name = "product/subdirection.html"

    def get(self, request, direction_slug):
        # выводит все поднаправления по заданному направлению
        direction = get_object_or_404(
            Direction, slug=direction_slug
        )  # находим направление
        subdirections = direction.subdirection_set.order_by()  # получаем все записи
        context = {
            "menu": menu,
            "searchform": searchform,
            "direction": direction,
            "subdirections": subdirections,
        }
        return render(request, self.template_name, context)


class ProductsView(View):
    template_name = "product/products.html"

    def get(self, request, subdirection_slug):
        # выводит все товары по заданному поднаправлению
        subdirection = get_object_or_404(
            SubDirection, slug=subdirection_slug
        )  # находим поднаправление
        # получаем все товары по выбранному поднаправлению
        subproducts = subdirection.description_set.order_by()
        # пагинация по 2 элементам на странице
        paginator = Paginator(subproducts, 2)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {
            "menu": menu,
            "searchform": searchform,
            "subdirection": subdirection,
            "page_obj": page_obj,
        }
        return render(request, self.template_name, context)


class ProductDesView(View):
    template_name = "product/desproduct.html"
    form_class1 = AddBasketForm  # форма для корзины
    form_class2 = CommentForm  # форма для комментариев

    def get(self, request, description_slug):
        # получаем товар по выбранному поднаправлению
        des_product = get_object_or_404(Description, slug=description_slug)
        des_images = DesImage.objects.filter(product=des_product)
        # выводит все комментарии к записи (знак - это сортировка в обратном порядке по времени)
        comments = des_product.comment_set.order_by("-date_added")

        # данные не отправлялись, создается пустая строка
        addbasketform = self.form_class1(prefix="basket")
        commentform = self.form_class2(prefix="comment")
        context = {
            "menu": menu,
            "searchform": searchform,
            "des_product": des_product,
            "des_images": des_images,
            "addbasketform": addbasketform,
            "commentform": commentform,
            "comments": comments,
        }
        return render(request, self.template_name, context)

    def post(self, request, description_slug):
        # получаем товар по выбранному поднаправлению
        des_product = get_object_or_404(Description, slug=description_slug)
        des_images = DesImage.objects.filter(product=des_product)
        # выводит все комментарии к записи (знак - это сортировка в обратном порядке по времени)
        comments = des_product.comment_set.order_by("-date_added")

        addbasketform = self.form_class1(request.POST, prefix="basket")
        commentform = self.form_class2(request.POST, prefix="comment")

        print(request.POST)
        if addbasketform.is_valid():
            new_basket_item = addbasketform.save(commit=False)
            if request.user.is_authenticated:
                print(request.user)
                new_basket_item.basket = Basket.objects.get(user=request.user)
                # фильтрация на добавление одного и того же товара в корзину
                if (
                    len(
                        BasketItem.objects.filter(
                            product=des_product,
                            basket=Basket.objects.get(user=request.user),
                        )
                    )
                    > 0
                ):
                    return redirect(
                        request.path
                    )  # обновляем страницу, чтобы форма очистилась
                else:
                    new_basket_item.product = des_product
                    new_basket_item.save()
                    return redirect(
                        request.path
                    )  # обновляем страницу, чтобы форма очистилась

            else:
                # перенаправление, если анонимный пользователь
                return redirect("users:login")

        if commentform.is_valid():
            new_comment = commentform.save(commit=False)
            if request.user.is_authenticated:
                new_comment.owner = request.user
            else:
                new_comment.owner = CustomUser.objects.get(username="anonymous")
            new_comment.product = des_product
            new_comment.save()  # сохраняем в базу данных
            return redirect(request.path)  # обновляем страницу, чтобы форма очистилась

        context = {
            "menu": menu,
            "searchform": searchform,
            "des_product": des_product,
            "des_images": des_images,
            "addbasketform": addbasketform,
            "commentform": commentform,
            "comments": comments,
        }
        return render(request, self.template_name, context)


class SearchView(View):
    template_name = "product/search.html"
    form_class = SearchForm

    def get(self, request):
        searchform = self.form_class
        context = {"menu": menu, "searchform": searchform, "products": products}
        return render(request, self.template_name, context)

    def post(self, request):
        searchform = self.form_class(data=request.POST)
        if searchform.is_valid():  # проверка
            products = Description.objects.filter(
                name__icontains=searchform.cleaned_data["text"]
            )
        context = {"menu": menu, "searchform": searchform, "products": products}
        return render(request, self.template_name, context)


class ContactView(View):
    template_name = "product/contacts.html"

    def get(self, request):
        context = {"menu": menu, "searchform": searchform}
        return render(request, self.template_name, context)


class BasketView(View):
    template_name = "product/basket.html"
    form_class1 = DeleteBasketForm  # форма для удаления
    form_class2 = AddBasketForm  # форма для изменения количества
    # корзина для удаления товара из корзины

    def get(self, request):
        # если пользователь зарегистрирован
        if request.user.is_authenticated:
            basket = Basket.objects.get(user=request.user)
            basketitems = basket.basketitem.all()
            final_price = 0
            for basketitem in basketitems:
                final_price = (
                    final_price + basketitem.product.price * basketitem.quantity
                )
        else:
            # перенаправление, если анонимный пользователь
            return redirect("users:login")
        deletebasketform = self.form_class1(prefix="deletebasket")
        changequantitybasketform = self.form_class2(prefix="changebasket")

        context = {
            "menu": menu,
            "searchform": searchform,
            "basketitems": basketitems,
            "final_price": final_price,
            "deletebasketform": deletebasketform,
            "changequantitybasketform": changequantitybasketform,
        }
        return render(request, self.template_name, context)

    def post(self, request, basketitem_id):
        basket_item = BasketItem.objects.get(id=basketitem_id)
        deletebasketform = self.form_class1(request.POST, prefix="deletebasket")
        changequantitybasketform = self.form_class2(
            request.POST, instance=basket_item, prefix="changebasket"
        )
        if request.user.is_authenticated:
            basket = Basket.objects.get(user=request.user)
            basketitems = basket.basketitem.all()
            final_price = 0
            for basketitem in basketitems:
                final_price = (
                    final_price + basketitem.product.price * basketitem.quantity
                )

        else:
            # перенаправление, если анонимный пользователь
            return redirect("users:login")

        if changequantitybasketform.is_valid():  # удалить продукт из корзины
            print("hello")
            changequantitybasketform.save()
            return redirect(
                "product:basket"
            )  # обновляем страницу, чтобы форма очистилась

        if deletebasketform.is_valid():  # удалить продукт из корзины
            BasketItem.objects.filter(id=basketitem_id).delete()
            return redirect(
                "product:basket"
            )  # обновляем страницу, чтобы форма очистилась

        context = {
            "menu": menu,
            "searchform": searchform,
            "basketitems": basketitems,
            "final_price": final_price,
            "deletebasketform": deletebasketform,
            "changequantitybasketform": changequantitybasketform,
        }
        return render(request, self.template_name, context)


class GetBasketItemInfoView(APIView):
    def get(self, request):
        queryset = Basket.objects.all()
        print(queryset)
        # сериализуем полученные данные
        serializer_for_queryset = BasketSerializer(instance=queryset, many=True)
        print(serializer_for_queryset.data)
        return Response(serializer_for_queryset.data)
