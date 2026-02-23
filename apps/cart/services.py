from .models import (
    CartItem, 
    Cart
    )
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


def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart

    if not request.session.session_key:
        request.session.create()

    cart, _ = Cart.objects.get_or_create(
        session_key=request.session.session_key,
        user=None
    )

    return cart


def merge_session_cart_into_user_cart(session_key: str, user):
    with transaction.atomic():
        session_cart = Cart.objects.filter(session_key=session_key).first()
        if not session_cart:
            return 
        
        user_cart, _ = Cart.objects.get_or_create(user=user)

        for item in session_cart.items.select_related("product"):
            user_item, created = CartItem.objects.select_for_update().get_or_create(
                cart=user_cart,
                product = item.product,
                defaults={
                    "quantity":item.quantity
                }
            )
            if not created:
                user_item.quantity += item.quantity
                user_item.save()

        session_cart.delete()