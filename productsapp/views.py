from django.shortcuts import render, get_object_or_404, redirect

from productsapp.forms import ProductForm
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


def product_add(request):
    if request.method == 'GET':
        form = ProductForm()
        return render(request, 'product_add.html', {'form': form})
    else:
        form = ProductForm(data=request.POST)
        if form.is_valid():
            new_product = form.save()
            # task = form.cleaned_data.get('task')
            # status = form.cleaned_data.get('status')
            # deadline = form.cleaned_data.get('deadline')
            # task_description = form.cleaned_data.get('task_description')
            # new_task = Task.objects.create(task=task, status=status, deadline=deadline or None,
            #                                task_description=task_description or None)
            return redirect('product_view', pk=new_product.pk)
        return render(request, 'product_add.html', {'form': form})
