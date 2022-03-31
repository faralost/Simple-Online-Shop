from rest_framework import serializers

from productsapp.models import Product, Order, OrderProduct, User


class UserSerializer(serializers.ModelSerializer):
    orders = serializers.PrimaryKeyRelatedField(many=True, queryset=Order.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'orders']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'category', 'balance', 'price']


class OrderProductSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_total_price(obj):
        return obj.quantity * obj.product.price

    class Meta:
        model = OrderProduct
        fields = ['product', 'quantity', 'total_price']


class OrderSerializer(serializers.ModelSerializer):
    order_products = OrderProductSerializer(many=True)
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'phone_number', 'address', 'user', 'order_products']

    def create(self, validated_data):
        order_products_data = validated_data.pop('order_products')
        order = Order.objects.create(**validated_data)
        for order_product_data in order_products_data:
            OrderProduct.objects.create(order=order, **order_product_data)
        return order
