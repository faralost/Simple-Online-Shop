from django.urls import path

from productsapp.views import index, product_view, product_add, product_update

urlpatterns = [
    path('', index, name='index'),
    path('product/<int:pk>/', product_view, name='product_view'),
    path('product/add/', product_add, name='product_add'),
    # path('task/<int:pk>/delete/', task_delete, name='task_delete'),
    path('product/<int:pk>/update/', product_update, name='product_update'),
]
