from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Direction, SubDirection, Description
from .forms import SearchForm, AddBasketForm
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
	context = {'menu': menu, 'form':searchform, 'directions': directions}
	return render(request, 'product/homepage.html', context)



def subdirection(request, direction_slug):
	#выводит все поднаправления по заданному направлению
	direction = get_object_or_404(Direction, slug=direction_slug) #находим направление
	subdirections = direction.subdirection_set.order_by() #получаем все записи
	context = {'menu': menu,'form':searchform,'direction': direction, 'subdirections' : subdirections}
	return render(request, 'product/subdirection.html', context)

def products(request, subdirection_slug):
	#выводит все товары по заданному поднаправлению
	addbasketform = AddBasketForm()
	subdirection = get_object_or_404(SubDirection, slug=subdirection_slug) #находим поднаправление
	subproducts = subdirection.description_set.order_by() #получаем все товары по выбранному поднаправлению
	paginator = Paginator(subproducts, 2)  #пагинация по 2 элементам на странице
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	context = {'menu': menu,'form':searchform, 'addbasketform': addbasketform, 'subdirection': subdirection, 'page_obj':page_obj}
	return render(request, 'product/products.html', context)

def product_description(request, description_slug):
	#выводит описание товара
	des_product = get_object_or_404(Description, slug=description_slug) #получаем товар по выбранному поднаправлению
	context = {'menu': menu,'form':searchform, 'des_product': des_product}
	return render(request, 'product/desproduct.html', context)


def search(request):
	#поиск по товарам
	if request.method != 'POST':
		#данные не отправлялись, создается пустая строка
		form = SearchForm()
	else:
		#данные отправлены POST, обработать данные
		form = SearchForm(data=request.POST)
		if form.is_valid(): #проверка
			products = Description.objects.filter(name__icontains = form.cleaned_data['text'])

	context = {'menu': menu, 'form':form, 'products': products}
	return render(request, 'product/search.html', context)
			

			



def basket(request):
	#корзина
	if request.method != 'POST':
		#данные не отправлялись, создается пустая строка
		form = AddBasketForm()
	else:
		#данные отправлены POST, обработать данные
		form = AddBasketForm(data=request.POST)
		if form.is_valid(): #проверка
			print(form.data)

	context = {'menu': menu, 'form':searchform}
	return render(request, 'product/basket.html', context)

def contacts(request):
	#контакты
	context = {'menu': menu, 'form':searchform}
	return render(request, 'product/contacts.html', context)