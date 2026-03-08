from core.models import UUIDModel, TimeStampedModel
from django.db import models

from apps.catalog.storage import product_media_path
from apps.catalog.models import Product


class ProductMedia(UUIDModel, TimeStampedModel):
    product = models.ForeignKey(
        Product,
        related_name="media", 
        on_delete=models.CASCADE
        )
    
    file = models.FileField(
        upload_to=product_media_path,
        blank=True,
        null=True
        )

    media_type = models.CharField(
        max_length=10,
        choices=[
            ("image", "Image"),
            ("video", "Video"),
            ]
        )
    order = models.PositiveIntegerField(default=0)