from rest_framework.test import APIClient
from model_bakery import baker
import pytest

from apps.orders.api.serializers import (
    # CartItem
    CreateCartItemSerializer,
    ReadCartItemSerializer,
    UpdateCartItemSerializer,
)