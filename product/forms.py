from django import forms
from .models import Description, BasketItem


class SearchForm(forms.Form):
	text = forms.CharField(max_length = 100)

class AddBasketForm(forms.ModelForm):
	# quantity = forms.IntegerField(min_value = 1)
	class Meta:
		model = BasketItem
		fields = ['product', 'quantity']
	
