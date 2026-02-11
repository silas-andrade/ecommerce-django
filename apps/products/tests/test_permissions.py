from django.test import TestCase
from django.contrib.auth import get_user_model

import pytest

from rest_framework.test import APIClient

from apps.products.serializers import (
    CreateProductSerializer,
    UpdateProductSerializer,
    ReadProductSerializer,

    CreateProductMediaSerializer,
    ReadProductMediaSerializer,
    UpdateProductMediaSerializer
)
from ..models import (
    Product,
    ProductMedia
)
from ..permissions import IsProductSellerOrReadOnly, IsSeller

from apps.users.models import User
from apps.sellers.models import Seller

from model_bakery import baker


@pytest.mark.django_db
def test_non_seller_cannot_create_product():
    regular_user = baker.make(User)
    client = APIClient()
    client.force_authenticate(user=regular_user)

    response = client.post("/api/products/", {})

    assert response.status_code == 403
