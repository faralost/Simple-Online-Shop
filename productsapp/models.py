from django.db import models


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

    class Meta:
        db_table = 'products'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
