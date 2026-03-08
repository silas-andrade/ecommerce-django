from rest_framework.test import APIClient
from rest_framework.exceptions import ErrorDetail

from apps.catalog.models import (
    Product,
    ProductMedia
)
from apps.catalog.services.product import publish_product

from apps.sellers.models import Seller
from apps.users.models import User

from model_bakery import baker

import pytest


@pytest.mark.django_db
def test_non_seller_create_product():
    user = baker.make(User, email="user@test.com", password="123456")
    client = APIClient()
    client.force_authenticate(user=user)
    payload = {
        "name": "Produto Teste",
        "description": "Descrição do produto teste",
        "price": "49.90",
        "slug":'teste'
    }
    response = client.post("/api/products/", payload, format="json")
    
    assert response.data['detail'] == ErrorDetail(string='You do not have permission to perform this action.', code='permission_denied')


@pytest.mark.django_db
def test_another_seller_put_product():
    owner_user = baker.make(User, email="user@test.com", password="123456")
    owner_seller = baker.make(Seller, user=owner_user)

    other_user = baker.make(User, email="user123@test.com", password="123456")
    other_seller = baker.make(Seller, user=other_user)

    product = baker.make(Product, seller=owner_seller)
    productMedia = baker.make(ProductMedia, product=product) 

    publish_product(product)

    client = APIClient()
    client.force_authenticate(user=other_user)

    payload = {
        "name": "Novo Nome",
        "description": "Nova descrição",
        "price": 99.90
    }

    response = client.put(
        f"/api/products/{product.id}/",
        payload,
        format="json"
    )

    assert response.status_code == 403