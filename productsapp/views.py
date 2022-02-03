from django.shortcuts import render, get_object_or_404, redirect

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


def product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_view.html', {'product': product})


def product_add(request):
    if request.method == 'GET':
        form = ProductForm()
        return render(request, 'product_add.html', {'form': form})
    else:
        form = ProductForm(data=request.POST)
        if form.is_valid():
            new_product = form.save()
            return redirect('product_view', pk=new_product.pk)
        return render(request, 'product_add.html', {'form': form})


def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'GET':
        form = ProductForm(initial={
            'name': product.name,
            'description': product.description,
            'category': product.category,
            'balance': product.balance,
            'price': product.price
        })
        return render(request, 'product_update.html', {'product': product, 'form': form})
    elif request.method == 'POST':
        form = ProductForm(data=request.POST)
        if form.is_valid():
            product.name = form.cleaned_data.get('name')
            product.description = form.cleaned_data.get('description')
            product.category = form.cleaned_data.get('category')
            product.balance = form.cleaned_data.get('balance')
            product.price = form.cleaned_data.get('price')
            product.save()
            return redirect('product_view', pk=product.pk)
        return render(request, 'product_update.html', {'product': product, 'form': form})


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'GET':
        return render(request, 'product_delete.html', {'product': product})
    elif request.method == 'POST':
        product.delete()
        return redirect('index')


def products_category(request, category):
    query = request.GET.get('query')
    products = Product.objects.filter(category=category).order_by('name')
    if query:
        products = Product.objects.filter(category=category, name__icontains=query).order_by('name')
        return render(request, 'products_categories.html',
                      {'categories': Product.CATEGORY_CHOICES, 'products': products})
    return render(request, 'products_categories.html',
                  {'categories': Product.CATEGORY_CHOICES, 'products': products, 'category': category})
