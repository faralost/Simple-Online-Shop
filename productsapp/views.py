from django.shortcuts import render, get_object_or_404

from productsapp.models import Product


def index(request):
    if request.method == 'GET':
        products = Product.objects.all()
        return render(request, 'index.html', {'products': products})
    else:
        pass


def product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_view.html', {'product': product})

