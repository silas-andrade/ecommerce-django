from django.db import models

from core.models import UUIDModel, TimeStampedModel
from apps.catalog.models import Product
from apps.orders.models import Order


class OrderItem(UUIDModel, TimeStampedModel):
    order = models.ForeignKey(
        Order,
        related_name="items",
        on_delete=models.CASCADE
        )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT
        )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    quantity = models.PositiveIntegerField(default=1)