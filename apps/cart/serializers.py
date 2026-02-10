from rest_framework import serializers

from .models import (
    CartItem,
    Cart
    )
from apps.products.serializers import ReadProductSerializer


# CartItem
class CreateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']

    def validate_product(self, product):
        if not product.status == 'draft':
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

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Invalid quantity")
        return value
    


# Cart
class ReadCartSerializer(serializers.ModelSerializer):
    cart_items = ReadCartItemSerializer(
        source='items',
        read_only = True, 
        many=True
        )

    class Meta:
        model = Cart
        fields = ['id', 'cart_items']