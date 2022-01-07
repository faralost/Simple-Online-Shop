from django.shortcuts import render, get_object_or_404, redirect

from productsapp.forms import ProductForm
from productsapp.models import Product


def index(request):
    if request.method == 'GET':
        products = Product.objects.filter(balance__gt=0).order_by('category', 'name')
        return render(request, 'index.html', {'products': products})
    else:
        pass


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
