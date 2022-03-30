from django.urls import path, include
from rest_framework import routers

from api_v1.views import ProductViewSet

app_name = "api_v1"

router = routers.DefaultRouter()
router.register('products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls))
]
