from django.db.models import F, Sum
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import DeleteView
from django.views.generic.edit import CreateView

from productsapp.forms import OrderForm
from productsapp.models import ShoppingCart, Product, Order, OrderProduct


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


class ShoppingCartDetailView(CreateView):
    form_class = OrderForm
    model = Order
    template_name = 'shopping_cart/detail_view.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ShoppingCartDetailView, self).get_context_data(**kwargs)
        context['shopping_cart'] = ShoppingCart.objects.all()
        context['title'] = 'Корзина'
        context['categories'] = Product.CATEGORY_CHOICES
        context['total'] = self.get_total()
        return context

    def form_valid(self, form):
        self.object = form.save()
        self.get_order()
        self.delete_shopping_cart()
        return super().form_valid(form)

    def delete_shopping_cart(self):
        ShoppingCart.objects.all().delete()

    def get_order(self):
        for item in ShoppingCart.objects.all():
            order_list = OrderProduct.objects.create(order_id=self.object.pk, product_id=item.product_id,
                                                     quantity=item.quantity)
            Product.objects.filter(id=item.product_id).update(balance=F('balance')-item.quantity)
        return order_list

    def get_total(self):
        total = ShoppingCart.objects.annotate(mult=F('quantity') * F('product__price')).aggregate(sum=Sum('mult'))
        return total

    def get_success_url(self):
        return reverse('productsapp:shopping_cart_view')


class ShoppingCartDeleteView(DeleteView):
    model = ShoppingCart

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('productsapp:shopping_cart_view')

    def delete(self, *args, **kwargs):
        quantity = ShoppingCart.objects.filter(pk=self.kwargs['pk']).update(quantity=F('quantity') - 1)
        self.object = self.get_object()
        if self.object.quantity >= quantity:
            return redirect('productsapp:shopping_cart_view')
        return super(ShoppingCartDeleteView, self).delete(*args, **kwargs)
