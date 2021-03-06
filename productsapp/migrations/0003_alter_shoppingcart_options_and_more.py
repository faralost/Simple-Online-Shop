# Generated by Django 4.0.1 on 2022-02-04 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productsapp', '0002_shoppingcart'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shoppingcart',
            options={'verbose_name': 'Корзина', 'verbose_name_plural': 'Корзина'},
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='quantity',
            field=models.PositiveIntegerField(default=1, verbose_name='Количество товара в корзине'),
        ),
    ]
