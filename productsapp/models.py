from django.db import models
from django.urls import reverse


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
        return f"{self.pk}. {self.name}: {self.price}"

    def get_absolute_url(self):
        return reverse('product_view', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super(Product, self).save(*args, **kwargs)

    class Meta:
        db_table = 'products'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class ShoppingCart(models.Model):
    product = models.ForeignKey('productsapp.Product', on_delete=models.CASCADE, related_name='products',
                                verbose_name='Товар в корзине')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество товара в корзине')

    @property
    def amount(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.product.name}: {self.quantity}"

    class Meta:
        db_table = 'shopping_cart'
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
