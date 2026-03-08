from django.db import models

from core.models import UUIDModel, TimeStampedModel
from apps.catalog.models import Product
from .cart import Cart


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