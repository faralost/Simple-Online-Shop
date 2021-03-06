from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView

from productsapp.base import SearchListView
from productsapp.forms import ProductForm
from productsapp.models import Product


class ProductsIndexView(SearchListView):
    model = Product
    template_name = 'product/index.html'
    context_object_name = 'products'
    paginate_by = 6
    ordering = ['category', 'name']
    search_fields = ['name__icontains']
    extra_context = {'title': 'Главная'}

    def get(self, request, *args, **kwargs):
        cart = request.session.get('cart', {})
        if not cart:
            request.session['cart'] = {}
        response = super().get(request, *args, **kwargs)
        return response

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(balance__gt=0)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Product.CATEGORY_CHOICES
        return context


class ProductView(DetailView):
    model = Product
    template_name = 'product/product_view.html'

    def get_context_data(self, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)
        context['title'] = self.object.name
        return context


class ProductAddView(PermissionRequiredMixin, CreateView):
    form_class = ProductForm
    template_name = 'product/product_add.html'
    model = Product
    extra_context = {'title': 'Добавление товара'}
    permission_required = 'productsapp.add_product'


class ProductUpdate(PermissionRequiredMixin, UpdateView):
    form_class = ProductForm
    template_name = 'product/product_update.html'
    model = Product
    extra_context = {'title': 'Редактирование товара'}
    permission_required = 'productsapp.change_product'


class ProductDelete(PermissionRequiredMixin, DeleteView):
    template_name = 'product/product_delete.html'
    model = Product
    success_url = reverse_lazy('productsapp:index')
    extra_context = {'title': 'Удаление товара'}
    permission_required = 'productsapp.delete_product'


class ProductsByCategory(ListView):
    model = Product
    template_name = 'product/index.html'
    context_object_name = 'products'
    paginate_by = 6

    def get_queryset(self):
        return Product.objects.filter(category=self.kwargs['category'], balance__gt=0).order_by('name')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsByCategory, self).get_context_data(**kwargs)
        category = self.kwargs.get('category')
        context['title'] = dict(Product.CATEGORY_CHOICES).get(category)
        context['categories'] = Product.CATEGORY_CHOICES
        return context
