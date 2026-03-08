from rest_framework import serializers

from apps.catalog.models import (
    Review,
    ReviewReaction
)
from apps.users.serializers import ReadUserSerializer

from apps.catalog.api.serializers.review_media import ReadReviewMediaSerializer


class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['text']

    #TODO Validar se o produto está publicado ou não para publicação

class ReadReviewSerializer(serializers.ModelSerializer):
    user = ReadUserSerializer(read_only=True)
    media = ReadReviewMediaSerializer(read_only=True, many=True)
    class Meta:
        model = Review
        fields = [
            'id',
            'user',
            'product', 
            'text',
            'media',
            'created_at'
            ]


class UpdateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['text']



class CreateReviewReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewReaction
        fields = ['id', 'review', 'is_helpful']