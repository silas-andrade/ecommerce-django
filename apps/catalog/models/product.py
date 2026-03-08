from django.db import models

from apps.sellers.models import Seller
from apps.catalog.choices import ProductStatus
from core.models import UUIDModel, TimeStampedModel


class Product(UUIDModel, TimeStampedModel):
    seller = models.ForeignKey(
        Seller,
        related_name="products",
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=ProductStatus.choices,
        default=ProductStatus.DRAFT
    )

    price = models.DecimalField(max_digits=10, decimal_places=2)
    compare_at_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    currency = models.CharField(max_length=3, default="BRL")
    stock = models.PositiveIntegerField(default=0)

    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)
