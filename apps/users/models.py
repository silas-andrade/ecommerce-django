from django.contrib.auth.models import AbstractUser
from django.db import models

import uuid

from .storage import (
    customer_profile_image_path,
)
from core import settings


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Customer(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='customer'
    )
    profile_image  = models.ImageField(upload_to=customer_profile_image_path, null=True, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return f"Customer: {self.user.username}"
    
"""
if hasattr(user, 'seller'):
    # é seller

if hasattr(user, 'customer'):
    # é customer
"""