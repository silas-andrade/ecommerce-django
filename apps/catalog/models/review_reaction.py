from django.db import models

from core.models import UUIDModel, TimeStampedModel
from apps.catalog.models import Review
from core import settings

class ReviewReaction(UUIDModel, TimeStampedModel):
    review = models.ForeignKey(
        Review,
        related_name="reactions",
        on_delete=models.CASCADE
        )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="review_reactions",
        on_delete=models.CASCADE
        )
    
    is_helpful = models.BooleanField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["review", "user"],
                name="unique_review_reaction"
            )
        ]