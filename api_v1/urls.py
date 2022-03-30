from django.urls import path, include
from rest_framework import routers

from api_v1.views import ProductViewSet, OrderViewSet, UserViewSet

app_name = "api_v1"

router = routers.DefaultRouter()
router.register('products', ProductViewSet)
router.register('orders', OrderViewSet)
router.register('users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
