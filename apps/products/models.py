import uuid

from django.db import models


from apps.sellers.models import Seller
from .storage import product_media_path
from .choices import ProductStatus


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProductMedia(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
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
    created_at = models.DateTimeField(auto_now_add=True)
