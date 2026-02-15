import pytest


from ..models import (
    Product,
    ProductMedia
)
from apps.products.exceptions import DomainError
from apps.products.services import (
    publish_product,
    archive_product,
    remove_product_media
)
from apps.products.choices import ProductStatus

from apps.users.models import User
from apps.sellers.models import Seller

from model_bakery import baker


@pytest.mark.django_db
def test_publish_product_requires_media():
    user = baker.make(User)
    seller = baker.make(Seller, user=user)
    product = baker.make(Product, seller=seller) 
    
    product2 = baker.make(Product, seller=seller) 
    productMedia = baker.make(ProductMedia, product=product2) 

    with pytest.raises(DomainError) as exc:
        publish_product(product)
    
    publish_product(product2)

    product.refresh_from_db()
    product2.refresh_from_db()
    assert product.status == ProductStatus.DRAFT
    assert product2.status == ProductStatus.PUBLISHED


@pytest.mark.django_db
def test_archive_product():
    user = baker.make(User)
    seller = baker.make(Seller, user=user)
    product1 = baker.make(Product, seller=seller, status=ProductStatus.DRAFT) 
    product2 = baker.make(Product, seller=seller, status=ProductStatus.ARCHIVED) 
    product3 = baker.make(Product, seller=seller, status=ProductStatus.PUBLISHED) 
    with pytest.raises(DomainError) as exc:
        archive_product(product2)

    archive_product(product3)
    archive_product(product1)
    product1.refresh_from_db()
    product2.refresh_from_db()
    product3.refresh_from_db()
    assert product1.status == ProductStatus.ARCHIVED
    assert product2.status == ProductStatus.ARCHIVED
    assert product3.status == ProductStatus.ARCHIVED


@pytest.mark.django_db
def test_remove_product_media():
    user = baker.make(User)
    seller = baker.make(Seller, user=user)
    product = baker.make(Product, seller=seller) 
    product_media = baker.make(ProductMedia, product=product)
    product_media2 = baker.make(ProductMedia, product=product)

    remove_product_media(product_media)
    with pytest.raises(DomainError) as exc:
        remove_product_media(product_media2)
    
    assert product.media.count() >= 1     