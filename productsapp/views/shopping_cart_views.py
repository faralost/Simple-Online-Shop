from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Sum
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import DeleteView, ListView
from django.views.generic.edit import CreateView

from productsapp.forms import OrderForm
from productsapp.models import Product, Order, OrderProduct


class ShoppingCartAdd(View):

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        cart = self.request.session['cart']
        if str(product.pk) not in cart and product.balance > 0:
            cart[str(product.pk)] = {'qty': 1, 'price': str(product.price)}
            self.request.session['cart'] = cart
            product.balance -= 1
            product.save()
            messages.success(self.request, f'{product.name} в количестве 1шт добавлен в корзину')
        else:
            if product.balance > 0:
                cart[str(product.pk)]['qty'] += 1
                self.request.session['cart'] = cart
                product.balance -= 1
                product.save()
                messages.success(self.request, f"всего {product.name} в корзине теперь {cart[str(product.pk)]['qty']}")
            else:
                messages.error(self.request, f'{product.name} не осталось (:')
        print(cart)
        nexttt = self.request.POST.get('next', '/')
        return redirect(nexttt)


class ShoppingCartDetailView(CreateView):
    form_class = OrderForm
    model = Order
    template_name = 'shopping_cart/detail_view.html'

    def form_valid(self, form):

        self.object = form.save()
        self.get_order()
        return super().form_valid(form)

    def get_order(self):
        for key, value in self.cart.items():
            order_list = OrderProduct.objects.create(order_id=self.object.pk, product_id=int(key),
                                                     quantity=value['qty'])
        return order_list

    def get_success_url(self):
        return reverse('productsapp:shopping_cart_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Корзина'
        context['categories'] = Product.CATEGORY_CHOICES
        context['cart'] = self.get_products()
        context['total'] = self.get_total()
        return context

    def get_products(self):
        self.cart = self.request.session['cart']
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product
        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
        return self.cart

    def get_total(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())


class ShoppingCartDeleteView(View):
    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        cart = self.request.session['cart']
        if cart[str(product.pk)]['qty'] <= 1:
            del cart[str(product.pk)]
            self.request.session['cart'] = cart
            product.balance += 1
            product.save()
        else:
            cart[str(product.pk)]['qty'] -= 1
            self.request.session['cart'] = cart
            product.balance += 1
            product.save()
        return redirect('productsapp:shopping_cart_view')


class UserOrdersView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'shopping_cart/user_orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
