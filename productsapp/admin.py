from django.contrib import admin

from productsapp.models import Product, Order


class MembershipInline(admin.TabularInline):
    model = Order.products.through


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'price', 'balance']
    list_filter = ['category']
    search_fields = ['name']
    fields = ['name', 'description', 'category', 'balance', 'price']
    inlines = [
        MembershipInline,
    ]


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'phone_number', 'created_at']
    fields = ['customer_name', 'phone_number', 'address', 'created_at']
    readonly_fields = ['created_at']
    inlines = [
        MembershipInline,
    ]
    exclude = ('products',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
