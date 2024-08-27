from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Direction, SubDirection, Description, BasketItem, Basket
from .forms import SearchForm, AddBasketForm, CommentForm
from django.core.paginator import Paginator


menu = [{'title': 'Главная страница', 'url_name': 'product:homepage' },
		{'title': 'Корзина', 'url_name': 'product:basket' },
		{'title': 'Контакты', 'url_name': 'product:contacts' }
]
searchform = SearchForm()

# Create your views here.
def homepage(request):
	#домашняя страница с категориями товаров
	directions = Direction.objects.all()
	#получение числа визитов (сессии)
	num_visits = request.session.get('num_visits', 0)
	request.session['num_visits'] = num_visits + 1
	context = {'menu': menu, 'searchform':searchform, 'directions': directions, 'num_visits':num_visits}
	return render(request, 'product/homepage.html', context)

def subdirection(request, direction_slug):
	#выводит все поднаправления по заданному направлению
	direction = get_object_or_404(Direction, slug=direction_slug) #находим направление
	subdirections = direction.subdirection_set.order_by() #получаем все записи
	context = {'menu': menu,'searchform':searchform,'direction': direction, 'subdirections' : subdirections}
	return render(request, 'product/subdirection.html', context)

def products(request, subdirection_slug):
	#выводит все товары по заданному поднаправлению
	subdirection = get_object_or_404(SubDirection, slug=subdirection_slug) #находим поднаправление
	subproducts = subdirection.description_set.order_by() #получаем все товары по выбранному поднаправлению
	paginator = Paginator(subproducts, 2)  #пагинация по 2 элементам на странице
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	context = {'menu': menu,'searchform':searchform, 'subdirection': subdirection, 'page_obj':page_obj}
	return render(request, 'product/products.html', context)

def product_description(request, description_slug):
	#выводит описание товара
	#получаем товар по выбранному поднаправлению
	des_product = get_object_or_404(Description, slug=description_slug) 
	

	#форма добавления в корзину
	if request.method != 'POST':
		#данные не отправлялись, создается пустая строка
		addbasketform = AddBasketForm()
	else:
		#данные отправлены POST, обработать данные
		#проверка на авторизованного пользователя
		if request.user.is_authenticated:
			addbasketform = AddBasketForm(data=request.POST)
			if addbasketform.is_valid(): #проверка
				new_basket_item = addbasketform.save(commit=False)
				print(new_basket_item)
				new_basket_item.basket = Basket.objects.get(user=request.user)
				new_basket_item.product = des_product
				new_basket_item.save()
				return redirect ('.')
		else:
				#перенаправление, если анонимный пользователь
				return redirect('users:login')
	context = {'menu': menu,'searchform':searchform, 'des_product': des_product, 'addbasketform':addbasketform}
	return render(request, 'product/desproduct.html', context)


def search(request):
	#поиск по товарам
	if request.method != 'POST':
		#данные не отправлялись, создается пустая строка
		searchform = SearchForm()
	else:
		#данные отправлены POST, обработать данные
		searchform = SearchForm(data=request.POST)
		if searchform.is_valid(): #проверка
			products = Description.objects.filter(name__icontains = searchform.cleaned_data['text'])

	context = {'menu': menu, 'searchform':searchform, 'products': products}
	return render(request, 'product/search.html', context)
			

			
def basket(request):
	#корзина
	#если пользователь зарегистрирован
	if request.user.is_authenticated:
		basket = Basket.objects.get(user=request.user)
		basketitems = basket.basketitem_set.all()
		final_price = 0
		for basketitem in basketitems:
			final_price = final_price + basketitem.product.price * basketitem.quantity
		
	else:
		#перенаправление, если анонимный пользователь
		return redirect('users:login')

				
	context = {'menu': menu, 'searchform':searchform, 'basketitems':basketitems, 'final_price':final_price}
	return render(request, 'product/basket.html', context)


def contacts(request):
	#контакты
	context = {'menu': menu, 'searchform':searchform}
	return render(request, 'product/contacts.html', context)


