from django.db.models import F, Sum
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView

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


class ShoppingCartDetailView(ListView):
    model = ShoppingCart
    template_name = 'shopping_cart/detail_view.html'
    context_object_name = 'shopping_cart'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ShoppingCartDetailView, self).get_context_data(**kwargs)
        context['title'] = 'Корзина'
        context['categories'] = Product.CATEGORY_CHOICES
        context['total'] = self.get_total()
        return context

    def get_total(self):
        total = ShoppingCart.objects.annotate(mult=F('quantity')*F('product__price')).aggregate(sum=Sum('mult'))
        return total
