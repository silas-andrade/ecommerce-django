from rest_framework import serializers

from apps.catalog.models import ProductMedia
from apps.catalog.constants import MAX_PRODUCT_IMAGE_SIZE, MAX_PRODUCT_VIDEO_SIZE


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