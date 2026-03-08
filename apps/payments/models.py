from django.core.exceptions import ValidationError
from django.db import models


from core.models import UUIDModel, TimeStampedModel
from apps.orders.models import Order
from .choices import (
    PaymentStatus, 
    CardBrand, 
    CardType, 
    PaymentMethod
)


class Payment(UUIDModel, TimeStampedModel):

    order = models.OneToOneField(
        Order,
        related_name="payment",
        on_delete=models.PROTECT
    )

    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )

    method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    transaction_id = models.CharField(max_length=255, blank=True, null=True)

    provider = models.CharField(max_length=50, blank=True, null=True)

    # CARD ATTRIBUTES
    card_type = models.CharField(
        max_length=30,
        choices=CardType.choices,
        null=True,
        blank=True
    )
    
    card_brand = models.CharField(
        max_length=30,
        choices=CardBrand.choices,
        null=True,
        blank=True
    )


    def clean(self):
        if self.method == PaymentMethod.CARD:
            if not self.card_type or not self.card_brand:
                raise ValidationError("Card payments require card_type and card_brand.")
        else:
            if self.card_type or self.card_brand:
                raise ValidationError("card_type and card_brand should only be set for card payments.")
            
            
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)