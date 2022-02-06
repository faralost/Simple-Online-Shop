from django.db.models import F, Sum
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DeleteView
from django.views.generic.edit import FormMixin, FormView

from productsapp.forms import OrderForm
from productsapp.models import ShoppingCart, Product, Order


class ShoppingCartAdd(View):

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs['pk'])
        shopping_cart = ShoppingCart.objects.all()
        if not shopping_cart.filter(product_id=product.pk) and product.balance > 0:
            shopping_cart.create(product_id=product.pk)
        elif shopping_cart.filter(product_id=product.pk) and shopping_cart.get(
                product_id=product.pk).quantity < product.balance:
            shopping_cart.filter(product_id=product.pk).update(quantity=F('quantity') + 1)
        nexttt = request.POST.get('next', '/')
        return redirect(nexttt)


class ShoppingCartDetailView(ListView):
    model = ShoppingCart
    template_name = 'shopping_cart/detail_view.html'
    context_object_name = 'shopping_cart'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ShoppingCartDetailView, self).get_context_data(**kwargs)
        context['title'] = 'Корзина'
        context['categories'] = Product.CATEGORY_CHOICES
        context['total'] = self.get_total()
        context['form'] = OrderForm()
        return context

    def get_total(self):
        total = ShoppingCart.objects.annotate(mult=F('quantity') * F('product__price')).aggregate(sum=Sum('mult'))
        return total


class OrderAdd(FormView):
    template_name = 'shopping_cart/detail_view.html'
    form_class = OrderForm
    model = Order

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('shopping_cart_view')


class ShoppingCartDeleteView(DeleteView):
    model = ShoppingCart

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('shopping_cart_view')
