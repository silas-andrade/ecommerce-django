from django.db import transaction
from decimal import Decimal

from apps.orders.models import Order, OrderItem
from apps.orders.services.cart import calculate_cart_total
from apps.catalog.choices import ProductStatus

@transaction.atomic
def create_order_from_cart(user):
    cart = user.cart.get()
    order = Order.objects.create(
        user=user,
        total_amount=calculate_cart_total(cart)
    )
    for cart_item in cart.items.select_related("product"):
        if (cart_item.product.status == ProductStatus.PUBLISHED) and (cart_item.quantity >= 1):
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                price=cart_item.product.price,
                quantity=cart_item.quantity
            )
    
    cart.items.all().delete()
    return order