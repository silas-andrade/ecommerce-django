from rest_framework.test import APIClient
from model_bakery import baker
import pytest

from apps.cart.serializers import (
    # CartItem
    CreateCartItemSerializer,
    ReadCartItemSerializer,
    UpdateCartItemSerializer,

    # Cart
    ReadCartSerializer
)
from apps.cart.services import (
    add_item_to_cart,
    calculate_cart_total,
    get_or_create_cart,
    merge_session_cart_into_user_cart
)
from apps.cart.permissions import IsOwnerCart