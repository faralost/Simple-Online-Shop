from django.urls import path

from productsapp.views.product_views import ProductsIndexView, ProductView, ProductAddView, ProductUpdate, \
    ProductDelete, ProductsByCategory
from productsapp.views.shopping_cart_views import ShoppingCartAdd, ShoppingCartDetailView, ShoppingCartDeleteView

app_name = 'productsapp'

urlpatterns = [
    path('', ProductsIndexView.as_view(), name='index'),
    path('product/<int:pk>/', ProductView.as_view(), name='product_view'),
    path('product/add/', ProductAddView.as_view(), name='product_add'),
    path('product/<int:pk>/delete/', ProductDelete.as_view(), name='product_delete'),
    path('product/<int:pk>/update/', ProductUpdate.as_view(), name='product_update'),
    path('products/<str:category>/', ProductsByCategory.as_view(), name='products_category'),
    path('products/<int:pk>/to_shopping_cart', ShoppingCartAdd.as_view(), name='adding_to_shopping_cart'),
    path('shopping_cart/', ShoppingCartDetailView.as_view(), name='shopping_cart_view'),
    path('shopping_cart/<int:pk>/delete/', ShoppingCartDeleteView.as_view(), name='shopping_cart_delete_view'),
]
