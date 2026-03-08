from django.db import models

from core.models import UUIDModel, TimeStampedModel
from apps.orders.choices import OrderStatus
from core import settings


class Order(UUIDModel, TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="orders",
        on_delete=models.PROTECT
    )

    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    shipping_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    
    def __str__(self):
        return f"Order {self.id}"