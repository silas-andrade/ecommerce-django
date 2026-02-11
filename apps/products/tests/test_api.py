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

