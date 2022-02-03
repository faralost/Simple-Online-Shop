from django.urls import path

from productsapp.views import product_view, product_add, product_update, product_delete, products_category, \
    ProductsIndexView

urlpatterns = [
    path('', ProductsIndexView.as_view(), name='index'),
    path('product/<int:pk>/', product_view, name='product_view'),
    path('product/add/', product_add, name='product_add'),
    path('product/<int:pk>/delete/', product_delete, name='product_delete'),
    path('product/<int:pk>/update/', product_update, name='product_update'),
    path('products/<str:category>/', products_category, name='products_category')
]
