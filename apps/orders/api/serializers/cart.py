from rest_framework import serializers

from .cart_item import ReadCartItemSerializer
from apps.orders.models import Cart
from apps.orders.services import calculate_cart_total

class ReadCartSerializer(serializers.ModelSerializer):
    cart_items = ReadCartItemSerializer(
        source='items',
        read_only = True, 
        many=True
        )
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'cart_items', 'total_price']


    def get_total_price(self, obj):
        return calculate_cart_total(obj)