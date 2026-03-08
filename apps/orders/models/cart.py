from django.db import models

from core.models import UUIDModel, TimeStampedModel
from core import settings


class Cart(UUIDModel, TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="cart",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    session_key = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        db_index=True
    )