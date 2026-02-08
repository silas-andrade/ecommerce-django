from django.db import models


from apps.users.models import User
from .storage import (
    seller_cover_image_path, 
    seller_profile_image_path
    )


class Seller(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='seller'
    )
    profile_image  = models.ImageField(upload_to=seller_profile_image_path, null=True, blank=True)
    cover_image = models.ImageField(
        upload_to=seller_cover_image_path,
        null=True,
        blank=True
    )
    store_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"Seller: {self.store_name}"