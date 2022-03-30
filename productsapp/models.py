from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


class Product(models.Model):
    CATEGORY_CHOICES = [('other', 'Разное'), ('drinks', 'Напитки'), ('food', 'Еда'),
                        ('books', 'Книги'), ('clothes', 'Одежда')]

    name = models.CharField(max_length=100, verbose_name='Название товара')
    description = models.TextField(max_length=2000, null=True, blank=True, default=None,
                                   verbose_name='Описание товара')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other',
                                verbose_name='Категория товара')
    balance = models.PositiveIntegerField(default=0, verbose_name='Остаток товара')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Цена товара')

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse('productsapp:product_view', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super(Product, self).save(*args, **kwargs)

    class Meta:
        db_table = 'products'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Order(models.Model):
    customer_name = models.CharField(max_length=40, verbose_name='Имя покупателя')
    phone_number = models.CharField(max_length=15, verbose_name='Номер телефона')
    address = models.CharField(max_length=100, verbose_name='Адрес')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    products = models.ManyToManyField("productsapp.Product", related_name="orders", through="productsapp.OrderProduct",
                                      through_fields=("order", "product"), blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='Пользователь',
                             null=True, blank=True)

    def __str__(self):
        return f"{self.customer_name}"

    class Meta:
        db_table = 'order'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderProduct(models.Model):
    product = models.ForeignKey('productsapp.Product', on_delete=models.CASCADE, related_name='product_orders',
                                verbose_name='Товар')
    order = models.ForeignKey('productsapp.Order', on_delete=models.CASCADE, related_name='order_products',
                              verbose_name='Заказ')
    quantity = models.PositiveIntegerField(verbose_name='Количество заказа')

    def __str__(self):
        return f"{self.product} в количестве: {self.quantity}"
