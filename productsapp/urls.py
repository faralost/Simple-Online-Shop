from django.urls import path

from productsapp.views import index

urlpatterns = [
    path('', index, name='index'),
    # path('tasks/', tasks_list_view, name='tasks_list_view'),
    # path('task/<int:pk>/', task_view, name='task_view'),
    # path('tasks/add/', task_create, name='task_add'),
    # path('task/<int:pk>/delete/', task_delete, name='task_delete'),
    # path('task/<int:pk>/update/', task_update_view, name='task_update'),
]
