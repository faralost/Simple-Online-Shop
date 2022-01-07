from django.urls import path

from productsapp.views import index, product_view

urlpatterns = [
    path('', index, name='index'),
    path('product/<int:pk>/', product_view, name='product_view'),
    # path('tasks/add/', task_create, name='task_add'),
    # path('task/<int:pk>/delete/', task_delete, name='task_delete'),
    # path('task/<int:pk>/update/', task_update_view, name='task_update'),
]
