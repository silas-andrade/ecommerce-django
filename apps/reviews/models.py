from django.db import models

import uuid

from .storage import review_media_path
from core import settings
from apps.products.models import Product


class Review(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        related_name="reviews",
        on_delete=models.SET_NULL,
        null=True
        )
    product = models.ForeignKey(
        Product,
        related_name="reviews",
        on_delete=models.CASCADE
        )
    text = models.TextField(max_length=2000)

    created_at = models.DateTimeField(auto_now_add=True)


class ReviewMedia(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
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
    created_at = models.DateTimeField(auto_now_add=True)


class ReviewReaction(models.Model):
    review = models.ForeignKey(
        Review,
        related_name="reactions",
        on_delete=models.PROTECT
        )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="review_reactions",
        on_delete=models.CASCADE
        )
    
    is_helpful = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)