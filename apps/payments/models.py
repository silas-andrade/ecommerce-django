from django.db import models

import uuid

from .choices import PaymentStatus
from apps.orders import Order


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    order = models.OneToOneField(
        Order,
        related_name="payment",
        on_delete=models.PROTECT
    )

    provider = models.CharField(max_length=50)  # stripe, mercadopago, pix
    provider_payment_id = models.CharField(max_length=255, blank=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
