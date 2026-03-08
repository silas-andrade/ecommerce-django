from rest_framework.test import APIClient
from model_bakery import baker
import pytest

from apps.users.models import (
    User, 
    Customer
)
from apps.sellers.models import Seller
from apps.catalog.models import Product
from apps.catalog.choices import ProductStatus



@pytest.mark.django_db
def test_user_no_autenticated_add_item_to_cart():
    client = APIClient()

    user = baker.make(User, email="user@test.com", password="123456")
    seller = baker.make(Seller, user=user)
    product = baker.make(Product, seller=seller, status=ProductStatus.PUBLISHED, stock=10)

    payload = {
        'product':product.id,
        'quantity':1
    }

    response = client.post("/api/cart/items/", payload, format="json")
    response = client.get("/api/cart/", format="json")
    assert response.data['cart_items'][0]['product']['id'] == str(product.id)