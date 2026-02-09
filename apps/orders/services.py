from decimal import Decimal
from django.db import transaction

from apps.orders.models import Order, OrderItem
from apps.cart.services import calculate_cart_total


@transaction.atomic
def create_order_from_cart(user, cart):
    order = Order.objects.create(
        user=user,
        total_amount=calculate_cart_total(cart)
    )
    for cart_item in cart.items.select_related("product"):
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            price=cart_item.product.price,
            quantity=cart_item.quantity
        )
    
    cart.items.all().delete()
    return order