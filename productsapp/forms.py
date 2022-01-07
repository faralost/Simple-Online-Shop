from django import forms
from django.forms import widgets

from productsapp.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'description': widgets.Textarea(attrs={'rows': 5, 'cols': 30})
        }
