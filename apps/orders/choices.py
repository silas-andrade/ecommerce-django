from django.db import models

class OrderStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    PAID = "paid", "Paid"
    CANCELED = "canceled", "Canceled"
    SHIPPED = "shipped", "Shipped"
    DELIVERED = "delivered", "Delivered"