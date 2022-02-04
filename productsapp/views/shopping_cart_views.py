from django.db.models import F
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import CreateView

from productsapp.models import ShoppingCart, Product


class ShoppingCartAdd(View):

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs['pk'])
        shopping_cart = ShoppingCart.objects.all()
        if not shopping_cart.filter(product_id=product.pk) and product.balance > 0:
            shopping_cart.create(product_id=product.pk)
        elif shopping_cart.filter(product_id=product.pk) and shopping_cart.get(
                product_id=product.pk).quantity < product.balance:
            shopping_cart.filter(product_id=product.pk).update(quantity=F('quantity') + 1)
        return redirect('index')
