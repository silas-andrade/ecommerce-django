from django.db import models

import uuid

from apps.products.models import Product
from core import settings


class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="cart",
        on_delete=models.CASCADE
        )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CartItem(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    cart = models.ForeignKey(
        Cart,
        related_name="items",
        on_delete=models.CASCADE
        )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT
    )
    quantity = models.PositiveIntegerField(default=1)