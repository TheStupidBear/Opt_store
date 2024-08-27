from django import forms
from .models import Description, BasketItem, Comment


class SearchForm(forms.Form):
	text = forms.CharField(max_length = 100, label='')
	

		

class AddBasketForm(forms.ModelForm):
	# quantity = forms.IntegerField(min_value = 1)
	class Meta:
		model = BasketItem
		fields = ['quantity']
		labels = {'quantity': 'Кол-во'}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {'text':''}
        widgets = {'text':forms.Textarea(attrs={'cols':80})}
        #указывает, чтобы было 80 столбцов в форме





