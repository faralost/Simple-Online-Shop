from django.contrib import admin

from productsapp.models import Product, ShoppingCart


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'price', 'balance']
    list_filter = ['category']
    search_fields = ['name']
    fields = ['name', 'description', 'category', 'balance', 'price']


admin.site.register(Product, ProductAdmin)
admin.site.register(ShoppingCart)
