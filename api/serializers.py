from rest_framework import serializers

from api.models import Order, OrderItem, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name", "description", "price", "stock")

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price field cannot be negative or zero")
        else:
            return value


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name")
    product_price = serializers.DecimalField(
        source="product.price", max_digits=10, decimal_places=2
    )

    class Meta:
        model = OrderItem
        fields = ("product_name", "product_price", "quantity", "item_subtotal")


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ("order_id", "created_at", "user", "status", "items", "total_price")

    def get_total_price(self, obj):
        order_items = obj.items.all()
        return sum(oi.item_subtotal for oi in order_items)


class ProductInfoSerializer(serializers.Serializer):
    """Get all products, count of proudcts and max price"""

    products = ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()
