from django.db import models

import uuid

from apps.products.models import Product
from core import settings

from core.models import UUIDModel, TimeStampedModel


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


class CartItem(UUIDModel, TimeStampedModel):
    cart = models.ForeignKey(
        Cart,
        related_name="items",
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT
    )
    quantity = models.PositiveIntegerField(
        default=1
    )