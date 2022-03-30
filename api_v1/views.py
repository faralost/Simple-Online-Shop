from rest_framework import viewsets

from api_v1.serializers import ProductSerializer
from productsapp.models import Product


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
