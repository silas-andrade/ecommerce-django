from django.db import models

from core.models import UUIDModel, TimeStampedModel
from apps.catalog.models import Review
from apps.catalog.storage import review_media_path


class ReviewMedia(UUIDModel, TimeStampedModel):
    review = models.ForeignKey(
        Review, 
        related_name="media", 
        on_delete=models.CASCADE
        )
    
    file = models.FileField(
        upload_to=review_media_path
        )
    
    media_type = models.CharField(
        max_length=10,
        choices=[
            ("image", "Image"),
            ("video", "Video"),
            ]
        )
    
    order = models.PositiveIntegerField(default=0)
