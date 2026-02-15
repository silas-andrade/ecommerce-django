from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework.test import APIClient
from rest_framework import status

from ..models import (
    Product,
    ProductMedia
)
from ..permissions import IsProductSellerOrReadOnly, IsSeller
from ..services import publish_product
from ..exceptions import DomainError
from ..choices import ProductStatus

from apps.sellers.models import Seller
from apps.users.models import User

from model_bakery import baker

import pytest



@pytest.mark.django_db
def test_create_product_api():
    """
    Testa a criação de um produto via API.
    """

    user = baker.make(User, email="user@test.com", password="123456")
    seller = baker.make(Seller, user=user)

    client = APIClient()
    client.force_authenticate(user=user)

    payload = {
        "name": "Produto Teste",
        "description": "Descrição do produto teste",
        "price": "49.90",
        "slug":'teste'
    }


    response = client.post("/api/products/", payload, format="json")
    print(response)
    product = Product.objects.get(id=response.data["id"])
    product.refresh_from_db()

    with pytest.raises(DomainError):
        publish_product(product)

    assert product.status == ProductStatus.DRAFT
    assert product.description == payload["description"]
    assert product.name == payload["name"]
    assert str(product.price) == payload["price"]
    assert product.seller.id == seller.id


@pytest.mark.django_db
def test_create_product_with_media_api():
    """
    Testa a criação de um produto via API.
    """


    user = baker.make(User, email="user@test.com", password="123456")
    seller = baker.make(Seller, user=user)

    client = APIClient()
    client.force_authenticate(user=user)

    payload = {
        "name": "Produto Teste",
        "description": "Descrição do produto teste",
        "price": "49.90",
        "slug":'teste'
    }

    response = client.post("/api/products/", payload, format="json")

    product = Product.objects.get(id=response.data["id"])

    payload_media = {
        "file": SimpleUploadedFile(
                name="test.jpg",
                content=b"file_content",
                content_type="image/jpeg"
                ),
        "media_type":"image",
        "order":1
    }
    response_media = client.post(
        f"/api/products/{product.id}/media/", 
        data=payload_media,
        format="multipart"
        )

    publish_product(product=product)

    assert product.status == ProductStatus.PUBLISHED
    assert product.description == payload["description"]
    assert product.name == payload["name"]
    assert str(product.price) == payload["price"]
    assert product.seller.id == seller.id

