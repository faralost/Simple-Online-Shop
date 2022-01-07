from django.urls import path

from productsapp.views import index, product_view, product_add, product_update, product_delete

urlpatterns = [
    path('', index, name='index'),
    path('product/<int:pk>/', product_view, name='product_view'),
    path('product/add/', product_add, name='product_add'),
    path('product/<int:pk>/delete/', product_delete, name='product_delete'),
    path('product/<int:pk>/update/', product_update, name='product_update'),
]
