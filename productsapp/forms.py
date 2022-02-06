from django import forms
from django.forms import widgets

from productsapp.models import Product, Order


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'description': widgets.Textarea(attrs={'rows': 5, 'cols': 30})
        }


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label='поиск товаров')


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['products']
        widgets = {
            'phone_number': widgets.Input(attrs={'placeholder': '+996XXXXXXXXX'})
        }
