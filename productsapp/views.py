from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from productsapp.base import SearchListView
from productsapp.forms import ProductForm
from productsapp.models import Product


class ProductsIndexView(SearchListView):
    model = Product
    template_name = 'index.html'
    context_object_name = 'products'
    paginate_by = 10
    ordering = ['category', 'name']
    search_fields = ['name__icontains']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(balance__gt=0)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Product.CATEGORY_CHOICES
        return context


class ProductView(DetailView):
    model = Product
    template_name = 'product_view.html'


class ProductAddView(CreateView):
    form_class = ProductForm
    template_name = 'product_add.html'
    model = Product


class ProductUpdate(UpdateView):
    form_class = ProductForm
    template_name = 'product_update.html'
    model = Product


class ProductDelete(DeleteView):
    template_name = 'product_delete.html'
    model = Product
    success_url = reverse_lazy('index')


def products_category(request, category):
    query = request.GET.get('query')
    products = Product.objects.filter(category=category).order_by('name')
    if query:
        products = Product.objects.filter(category=category, name__icontains=query).order_by('name')
        return render(request, 'products_categories.html',
                      {'categories': Product.CATEGORY_CHOICES, 'products': products})
    return render(request, 'products_categories.html',
                  {'categories': Product.CATEGORY_CHOICES, 'products': products, 'category': category})
