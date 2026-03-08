from rest_framework import serializers

from apps.orders.models import CartItem
from apps.catalog.api.serializers import ReadProductSerializer


class CreateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']

    def validate_product(self, product):
        if not product.status == 'published':
            raise serializers.ValidationError("Product unavailable.")
        return product
    
    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Invalid quantity")
        return value


class ReadCartItemSerializer(serializers.ModelSerializer):
    product = ReadProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']

    def validate_product(self, product):
        if not product.status == 'published':
            raise serializers.ValidationError("Product unavailable.")
        return product


    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Invalid quantity")
        return value
    

