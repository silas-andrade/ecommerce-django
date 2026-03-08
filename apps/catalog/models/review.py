from django.db import models


from core.models import UUIDModel, TimeStampedModel
from apps.catalog.models import Product
from core import settings


class Review(UUIDModel, TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        related_name="reviews",
        on_delete=models.CASCADE
        )
    product = models.ForeignKey(
        Product,
        related_name="reviews",
        on_delete=models.CASCADE
        )
    text = models.TextField()