from rest_framework import serializers

from .models import Product, ProductMedia
from apps.sellers.serializers import ReadSellerSerializer

from .constants import MAX_PRODUCT_IMAGE_SIZE, MAX_PRODUCT_VIDEO_SIZE

# ProductMedia
class CreateProductMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMedia
        fields = ['file', 'media_type', 'order']

    def validate(self, attrs):
        file = attrs["file"]
        content_type = file.content_type

        if content_type.startswith("image/") and file.size > MAX_PRODUCT_IMAGE_SIZE:
            raise serializers.ValidationError("Very large image (max 5MB).")

        if content_type.startswith("video/") and file.size > MAX_PRODUCT_VIDEO_SIZE:
            raise serializers.ValidationError("Very large video (max 30MB).")

        return attrs


class ReadProductMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMedia
        fields = ['id', 'file', 'media_type', 'order']


class UpdateProductMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMedia
        fields = ['file', 'media_type', 'order']

    def validate(self, attrs):
        file = attrs["file"]
        content_type = file.content_type

        if content_type.startswith("image/") and file.size > MAX_PRODUCT_IMAGE_SIZE:
            raise serializers.ValidationError("Very large image (max 5MB).")

        if content_type.startswith("video/") and file.size > MAX_PRODUCT_VIDEO_SIZE:
            raise serializers.ValidationError("Very large video (max 30MB).")

        return attrs

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