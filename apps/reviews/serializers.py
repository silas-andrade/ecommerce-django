import os

from rest_framework import serializers

from .models import (
    Review,
    ReviewMedia,
    ReviewReaction
)
from core import settings

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'product', 'text']


    def create(self, validated_data):
        return Review.objects.create(
            user=self.context["request"].user,
            **validated_data
        )

class ReviewMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewMedia
        fields = ['id', 'review', 'file', 'media_type', 'order']
    
    def validate(self, attrs):
        file = attrs["file"]
        content_type = file.content_type

        if content_type.startswith("image/") and file.size > settings.MAX_REVIEW_IMAGE_SIZE:
            raise serializers.ValidationError("Imagem muito grande (máx 5MB).")

        if content_type.startswith("video/") and file.size > settings.MAX_REVIEW_VIDEO_SIZE:
            raise serializers.ValidationError("Vídeo muito grande (máx 30MB).")

        return attrs


class ReviewReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewReaction
        fields = ['id', 'review', 'is_helpful']
    
    def create(self, validated_data):
        return Review.objects.create(
            user=self.context["request"].user,
            **validated_data
        )