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
