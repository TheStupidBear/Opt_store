from django import forms
from .models import Description, BasketItem, Comment


class SearchForm(forms.Form):
    text = forms.CharField(max_length=100, label="")


class AddBasketForm(forms.ModelForm):
    class Meta:
        model = BasketItem
        fields = ["quantity"]
        labels = {"quantity": ""}


class DeleteBasketForm(forms.ModelForm):
    class Meta:
        model = BasketItem
        fields = []
        labels = {"quantity": ""}


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class ChangeQuantityBasketForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        labels = {"text": ""}
        widgets = {"text": forms.Textarea(attrs={"cols": 80})}
        # указывает, чтобы было 80 столбцов в форме
