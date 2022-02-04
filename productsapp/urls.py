from django.urls import path

from productsapp.views import ProductsIndexView, ProductView, ProductAddView, ProductUpdate, \
    ProductDelete, ProductsByCategory

urlpatterns = [
    path('', ProductsIndexView.as_view(), name='index'),
    path('product/<int:pk>/', ProductView.as_view(), name='product_view'),
    path('product/add/', ProductAddView.as_view(), name='product_add'),
    path('product/<int:pk>/delete/', ProductDelete.as_view(), name='product_delete'),
    path('product/<int:pk>/update/', ProductUpdate.as_view(), name='product_update'),
    path('products/<str:category>/', ProductsByCategory.as_view(), name='products_category')
]
