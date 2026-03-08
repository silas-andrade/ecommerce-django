from rest_framework import serializers

from apps.sellers.serializers import ReadSellerSerializer
from .product_media import ReadProductMediaSerializer
from apps.catalog.models import Product



# Product
class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'currency', 'stock', 'slug']


class ReadProductSerializer(serializers.ModelSerializer):
    media = ReadProductMediaSerializer(read_only=True, many=True)
    seller = ReadSellerSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'seller', 'name', 'description', 'media', 'price', 'currency', 'stock', 'slug',]


class UpdateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'currency', 'stock']
        read_only_fields = ['slug']