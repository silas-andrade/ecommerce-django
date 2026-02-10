from .models import CartItem
from django.db import transaction 
from .exceptions import DomainError


def calculate_cart_total(cart):
    return sum(
        item.product.price * item.quantity for item in cart.items.select_related("product")
    )


def add_item_to_cart(product, cart, quantity):
    if quantity <= 0:
        raise DomainError("Quantity must be greater than zero.")
    if product.stock >= quantity:
        with transaction.atomic():
            cart_item, created = CartItem.objects.select_for_update().get_or_create(
                cart=cart,
                product=product,
                defaults={"quantity": quantity}
            )
            if not created:
                new_quantity = cart_item.quantity + quantity

                if product.stock < new_quantity:
                    raise DomainError("Insufficient stock.")

                cart_item.quantity = new_quantity
                cart_item.save()

    return cart_item