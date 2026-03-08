from rest_framework import serializers


from apps.catalog.constants import MAX_REVIEW_IMAGE_SIZE, MAX_REVIEW_VIDEO_SIZE
from apps.catalog.models import ReviewMedia

class CreateReviewMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewMedia
        fields = ['file', 'media_type', 'order']
    
    def validate(self, attrs):
        file = attrs["file"]
        content_type = file.content_type

        if content_type.startswith("image/") and file.size > MAX_REVIEW_IMAGE_SIZE:
            raise serializers.ValidationError("Very large image (max 5MB).")

        if content_type.startswith("video/") and file.size > MAX_REVIEW_VIDEO_SIZE:
            raise serializers.ValidationError("Very large video (max 30MB).")

        return attrs


class ReadReviewMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewMedia
        fields = [
            'id',
            'review',
            'file',
            'media_type',
            'order',
        ]
